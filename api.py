"""FastAPI HTTP wrapper for the ad-generator pipeline."""
from __future__ import annotations

import asyncio
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="ad-generator API", version="1.0.0")

# CORS — em produção quem consome é o proxy Vercel (server-side, sem CORS).
# Lista cobre dev local (brand-system, telegram bot) + ALLOWED_ORIGINS via env var.
_extra_origins = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        *_extra_origins,
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Bearer auth — opcional. Se AD_GENERATOR_TOKEN não estiver setado, endpoints ficam abertos
# (modo dev). Em produção, sempre definir o token via secret/env var.
_EXPECTED_TOKEN = os.getenv("AD_GENERATOR_TOKEN", "").strip()


def require_token(authorization: Optional[str] = Header(default=None)) -> None:
    if not _EXPECTED_TOKEN:
        return  # sem token configurado → modo aberto (dev local, telegram bot interno)
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Authorization: Bearer <token>")
    if authorization.removeprefix("Bearer ").strip() != _EXPECTED_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid token")


class GenerateRequest(BaseModel):
    briefing: str
    mock: bool = False


class GenerateResponse(BaseModel):
    run_id: str
    ok: bool
    png_path: Optional[str] = None
    error: Optional[str] = None


def _run_pipeline(briefing_text: str, mock: bool = False) -> dict:
    """Run the ad-generator pipeline synchronously."""
    from skills_runner import SkillRunner
    from adapters.llm import LLMAdapter, MockLLMAdapter
    from adapters.image_gen import ImageGenAdapter
    from adapters.assembler import AssemblerAdapter
    from pipeline import MOCK_FIXTURES, write_artifact

    artifacts_dir = Path(os.getenv("ARTIFACTS_DIR", "./artifacts"))
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]

    llm = MockLLMAdapter(fixtures=MOCK_FIXTURES) if mock else LLMAdapter()
    runner = SkillRunner(llm=llm)

    # Skill 01 — briefing parser
    result = runner.run("01-briefing-parser", briefing_text)
    if not result.ok:
        return {"ok": False, "error": f"briefing-parser: {result.error}", "run_id": run_id}
    briefing = result.output
    if briefing.get("clarifying_questions"):
        questions = "; ".join(briefing["clarifying_questions"])
        return {"ok": False, "error": f"Preciso de mais detalhes: {questions}", "run_id": run_id}
    write_artifact(run_id, "01-briefing", briefing, artifacts_dir)

    # Skill 02 — style selector (with optional vector search)
    vector_context = ""
    if not mock:
        try:
            from vector_search import search_styles, candidates_to_context
            query = briefing.get("tese_central", "") + " | " + briefing.get("intent", "")
            candidates, _ = search_styles(query, top_k=5)
            if candidates:
                vector_context = candidates_to_context(candidates)
        except Exception:
            pass

    result = runner.run("02-style-selector", briefing, extra_context=vector_context)
    if not result.ok:
        return {"ok": False, "error": f"style-selector: {result.error}", "run_id": run_id}
    style_rec = result.output
    write_artifact(run_id, "02-style-recommendation", style_rec, artifacts_dir)
    chosen_model_id = style_rec["recommended"][0]["model_id"]

    # Skill 03 — layout composer
    layout_input = {
        "briefing": briefing,
        "model_id": chosen_model_id,
        "copy": {"_note": "MVP — generate copy inside layout composer"},
    }
    result = runner.run(
        "03-layout-composer",
        layout_input,
        extra_context="Generate copy yourself. Use model slot constraints.",
    )
    if not result.ok:
        return {"ok": False, "error": f"layout-composer: {result.error}", "run_id": run_id}
    layout_spec = result.output

    try:
        from layout_enforcer import enforce
        layout_spec, _ = enforce(layout_spec, briefing)
    except Exception:
        pass
    write_artifact(run_id, "03-layout-spec", layout_spec, artifacts_dir)

    # Skill 04 — image prompt engineer + image generation
    image_slots = [el for el in layout_spec.get("elements", []) if el.get("type") == "image_slot"]
    image_urls: dict[str, str] = {}
    if image_slots:
        prompt_input = {"layout_spec": layout_spec, "briefing": briefing, "image_slots": image_slots}
        result = runner.run("04-image-prompt-engineer", prompt_input)
        if not result.ok:
            return {"ok": False, "error": f"image-prompt-engineer: {result.error}", "run_id": run_id}
        image_spec = result.output
        write_artifact(run_id, "04-image-prompt", image_spec, artifacts_dir)

        if not image_spec.get("skip"):
            image_gen = ImageGenAdapter()
            for p in image_spec.get("prompts", []):
                try:
                    ig_result = image_gen.generate(
                        prompt=p["prompt"],
                        negative_prompt=p.get("negative_prompt", ""),
                        aspect_ratio=p.get("aspect_ratio", "9:16"),
                        reference_images=p.get("reference_images", []),
                    )
                    image_urls[p["slot_name"]] = ig_result.url
                except Exception:
                    pass

    # Skill 05 — assembler (PNG)
    assembler = AssemblerAdapter()
    asm_result = assembler.assemble(layout_spec, image_urls)
    write_artifact(
        run_id,
        "05-ad-output",
        {"png_path": asm_result.png_path, "destination": "png", "warnings": asm_result.warnings or []},
        artifacts_dir,
    )

    if not asm_result.png_path:
        return {"ok": False, "error": "assembler did not produce a PNG", "run_id": run_id}

    return {"ok": True, "run_id": run_id, "png_path": asm_result.png_path}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest, _auth: None = Depends(require_token)):
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, _run_pipeline, req.briefing, req.mock)
    if not result["ok"]:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@app.get("/image/{run_id}")
def get_image(run_id: str, _auth: None = Depends(require_token)):
    artifacts_dir = Path(os.getenv("ARTIFACTS_DIR", "./artifacts"))
    ad_output_path = artifacts_dir / run_id / "05-ad-output.json"
    if not ad_output_path.exists():
        raise HTTPException(status_code=404, detail="Run not found")
    ad_output = json.loads(ad_output_path.read_text())
    png_path = ad_output.get("png_path")
    if not png_path or not Path(png_path).exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(png_path, media_type="image/png")
