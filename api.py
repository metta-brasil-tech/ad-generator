"""FastAPI HTTP wrapper para o ad-generator pipeline.

Expõe POST /generate para o n8n chamar via HTTP Request node.
O n8n manda o briefing estruturado, o pipeline processa as 6 etapas
e devolve o PNG em base64 + metadados.

Rodar:
    uvicorn api:app --host 0.0.0.0 --port 8000
    # ou via docker-compose / systemd
"""
from __future__ import annotations

import asyncio
import base64
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from pipeline import run_pipeline, PipelineResult

app = FastAPI(title="ad-generator API", version="1.0.0")


# ── Request / Response schemas ────────────────────────────────────────────────

class GenerateRequest(BaseModel):
    marca: str = Field(..., description="'metta' ou 'tiago'")
    formato: str = Field(..., description="'story' | 'card' | 'carrossel' | 'reels'")
    headline: str = Field(..., description="Texto principal que vai na imagem")
    visual_ref: str | None = Field(
        None,
        description="Referência visual — URL pública ou data URI base64 (image/jpeg ou image/png)",
    )
    extra_specs: str | None = Field(None, description="Especificações adicionais em texto livre")
    mock: bool = Field(False, description="Usar mock LLM/image-gen (sem custo, para testes)")


class GenerateResponse(BaseModel):
    run_id: str
    ok: bool
    image_b64: str | None = Field(None, description="PNG em base64 (sem prefixo data:)")
    model_id: str | None
    qa_status: str | None
    warnings: list[str]
    elapsed_ms: int
    error: str | None = None


# ── Helpers ───────────────────────────────────────────────────────────────────

_FORMATO_MAP = {
    "story": "story",
    "stories": "story",
    "card": "feed_quadrado",
    "card único": "feed_quadrado",
    "carrossel": "carrossel",
    "carousel": "carrossel",
    "reels": "capa_reels",
    "capa de reels": "capa_reels",
    "capa_reels": "capa_reels",
}

_MARCA_MAP = {
    "metta": "metta_institucional",
    "metta_institucional": "metta_institucional",
    "tiago": "tiago_pessoal",
    "tiago_pessoal": "tiago_pessoal",
}


def _build_briefing_text(req: GenerateRequest) -> str:
    """Converte o input estruturado do n8n em texto livre para o skill 01."""
    marca = _MARCA_MAP.get(req.marca.lower(), req.marca)
    formato = _FORMATO_MAP.get(req.formato.lower(), req.formato)

    lines = [
        f"Criar criativo para a marca {marca}.",
        f"Formato: {formato}.",
        f'Headline principal: "{req.headline}".',
    ]
    if req.extra_specs:
        lines.append(f"Especificações adicionais: {req.extra_specs}")

    return " ".join(lines)


def _resolve_visual_ref(visual_ref: str | None) -> str | None:
    """Resolve visual_ref para URL ou path local.

    - Se for URL HTTP/HTTPS: retorna como está.
    - Se for data URI base64: decodifica, salva em temp file, retorna path.
    - Se None: retorna None.
    """
    if not visual_ref:
        return None

    if visual_ref.startswith(("http://", "https://")):
        return visual_ref

    # data URI: "data:image/jpeg;base64,/9j/4AAQ..."
    if visual_ref.startswith("data:"):
        try:
            header, b64data = visual_ref.split(",", 1)
            ext = "jpg" if "jpeg" in header else "png"
            img_bytes = base64.b64decode(b64data)
            # Salva em arquivo temporário que persiste durante o request
            tmp = tempfile.NamedTemporaryFile(
                suffix=f".{ext}", delete=False,
                dir=Path(os.getenv("ARTIFACTS_DIR", "./artifacts")) / "images",
                prefix="ref_",
            )
            tmp.write(img_bytes)
            tmp.close()
            return tmp.name
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"visual_ref base64 inválido: {e}")

    # Assume que é um path local (caso de uso interno)
    if Path(visual_ref).exists():
        return visual_ref

    raise HTTPException(
        status_code=400,
        detail="visual_ref deve ser uma URL HTTP/HTTPS ou data URI base64 (data:image/...;base64,...)",
    )


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    return {"status": "ok", "service": "ad-generator"}


@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    """Gera um criativo a partir do briefing estruturado do n8n.

    Retorna PNG em base64 pronto para enviar via Telegram Bot node do n8n.
    """
    briefing_text = _build_briefing_text(req)
    reference_image_url = _resolve_visual_ref(req.visual_ref)

    # Executa o pipeline síncrono em thread pool para não bloquear o event loop
    try:
        result: PipelineResult = await asyncio.to_thread(
            run_pipeline,
            briefing_text,
            mock=req.mock,
            reference_image_url=reference_image_url,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline exception: {e}")

    if not result.ok and not result.png_path:
        raise HTTPException(
            status_code=422,
            detail=result.error or "Pipeline failed sem imagem gerada",
        )

    # Lê o PNG e converte para base64
    image_b64 = None
    if result.png_path and Path(result.png_path).exists():
        image_b64 = base64.b64encode(Path(result.png_path).read_bytes()).decode("ascii")

    return GenerateResponse(
        run_id=result.run_id,
        ok=result.ok,
        image_b64=image_b64,
        model_id=result.model_id,
        qa_status=result.qa_status,
        warnings=result.qa_warnings,
        elapsed_ms=result.elapsed_ms,
        error=result.error if not result.ok else None,
    )
