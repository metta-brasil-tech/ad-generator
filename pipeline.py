"""ad-generator pipeline — CLI orchestrator das 6 skills."""
from __future__ import annotations

import json
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path

import click
from dotenv import load_dotenv

load_dotenv()

from skills_runner import SkillRunner
from validators import validate
from adapters.llm import LLMAdapter, MockLLMAdapter
from adapters.image_gen import ImageGenAdapter
from adapters.assembler import AssemblerAdapter

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.json import JSON
    console = Console()
    def info(msg): console.print(f"[cyan][info][/cyan] {msg}")
    def ok(msg): console.print(f"[green][ok][/green] {msg}")
    def err(msg): console.print(f"[red][err][/red] {msg}")
    def panel(title, data): console.print(Panel(JSON(json.dumps(data, ensure_ascii=False)), title=title))
except ImportError:
    def info(msg): print(f"[info] {msg}")
    def ok(msg): print(f"[ok] {msg}")
    def err(msg): print(f"[err] {msg}")
    def panel(title, data): print(f"=== {title} ===\n{json.dumps(data, ensure_ascii=False, indent=2)}")


SKILL_ORDER = [
    "01-briefing-parser",
    "02-style-selector",
    "03-layout-composer",
    "04-image-prompt-engineer",
    "05-assembler",
    "06-qa-validator",
]

# Mock fixtures pra --mock mode
MOCK_FIXTURES = {
    "briefing-parser": {
        "intent": "prova_social_case_nominal",
        "tese_central": "Hiperzoo como prova de método replicável em varejo pet",
        "formato": "story",
        "funil": "MOFU",
        "audiencia": {
            "segmento": "varejo_pet", "cargo": "empresario",
            "porte_revenue": "desconhecido", "estado_emocional": "confortavel_buscando_crescer"
        },
        "tom": "credibilidade",
        "constraints": {
            "tem_logo_cliente_nomeado": True, "case_nominal_id": "hiperzoo",
            "data_evento": None, "cta_obrigatorio": None, "plataforma_destino": "meta_ads"
        },
        "marca": "metta_institucional",
        "raw_request": "(mock)",
        "clarifying_questions": []
    },
    "style-selector": {
        "recommended": [
            {"rank": 1, "model_id": "A-headline-foto-dark",
             "yaml_path": "brand-knowledge/models/A-headline-foto-dark.yaml",
             "score": 0.92,
             "rationale": "Headline+foto pessoa encaixa caso nominal Hiperzoo. Paleta dark dá gravidade institucional.",
             "tradeoffs": "Não destaca o número (se for o foco, ir YELLOW-EDITORIAL)."},
            {"rank": 2, "model_id": "YELLOW-BLOCO",
             "yaml_path": "brand-knowledge/models/YELLOW-BLOCO.yaml",
             "score": 0.78,
             "rationale": "Logo Hiperzoo no logo bar + foto líder à direita + bullets de resultados.",
             "tradeoffs": "Mais 'flyer institucional' do que 'storytelling de caso'."},
            {"rank": 3, "model_id": "LOGO-WALL",
             "yaml_path": "brand-knowledge/models/LOGO-WALL.yaml",
             "score": 0.71,
             "rationale": "Prova agregada com Hiperzoo + outros pet stores se quiser variar.",
             "tradeoffs": "Dilui presença individual do Hiperzoo."}
        ],
        "rejected_with_explanation": [
            {"model_id": "LIGHT-SURREAL", "reason": "Estilo abstrato não comporta logo cliente."}
        ],
        "auto_select_recommendation": "ask_human",
        "campaign_context_note": None
    },
    "layout-composer": {
        "model_id": "A-headline-foto-dark",
        "frame": {"width": 1080, "height": 1920, "background": {"type": "solid", "value": "#0C161B"}},
        "elements": [
            {"type": "text", "slot_name": "tag", "text": "CASE · HIPERZOO",
             "x": 80, "y": 100, "width": 920,
             "font": {"family": "SF Pro", "style": "Expanded Medium", "weight": 540,
                      "stretch_pct": 132, "size": 22, "line_height_pct": 100,
                      "letter_spacing_pct": 11, "text_case": "UPPER"},
             "color": "#B0CAD8", "align": "left"},
            {"type": "text", "slot_name": "headline",
             "text": "Como a Hiperzoo\nabriu 12 lojas em\n18 meses sem perder\nmargem.",
             "ranges": [{"start": 25, "end": 33, "fill": "#FFBE18"},
                        {"start": 49, "end": 67, "fill": "#FFBE18"}],
             "x": 80, "y": 260, "width": 920,
             "font": {"family": "SF Pro", "style": "Expanded Heavy", "weight": 870,
                      "stretch_pct": 132, "size": 80, "line_height_pct": 90,
                      "letter_spacing_pct": -1, "text_case": "UPPER"},
             "color": "#FFFFFF", "align": "left"},
            {"type": "image_slot", "slot_name": "photo",
             "x": 540, "y": 1000, "width": 600, "height": 900, "bleed_right": True,
             "image_prompt_ref": "image-prompts/style-A.md", "url_placeholder": "pending"},
            {"type": "text", "slot_name": "body",
             "text": "Implementamos os 5 protocolos de gestão comercial e o resultado apareceu no terceiro mês.",
             "x": 80, "y": 1480, "width": 600,
             "font": {"family": "SF Pro", "style": "Expanded Regular", "weight": 510,
                      "stretch_pct": 100, "size": 28, "line_height_pct": 120,
                      "letter_spacing_pct": -1, "text_case": "sentence"},
             "color": "#B0CAD8", "align": "left"},
            {"type": "pill_cta", "slot_name": "cta", "text": "VER CASE COMPLETO",
             "x": 80, "y": 1700, "width": "auto", "height": 88,
             "padding_x": 38, "padding_y": 22,
             "background": "#FFBE18", "text_color": "#0C161B", "corner_radius": 999,
             "font": {"family": "SF Pro", "style": "Expanded Bold", "weight": 700,
                      "stretch_pct": 132, "size": 24, "line_height_pct": 100,
                      "letter_spacing_pct": 0, "text_case": "UPPER"}}
        ],
        "errors": [], "warnings": [],
        "fit_metrics": {"fit_score": 0.92}
    },
    "image-prompt-engineer": {
        "skip": False,
        "prompts": [{
            "slot_name": "photo",
            "prompt": "serious confidence portrait of a brazilian retail pet-store entrepreneur, 42-50, casual button-up shirt over t-shirt, hand resting on store counter, gaze toward storefront window, warm window light with soft shadows, rule of thirds subject right, warm earth tones with mustard accent, photographed inside a modern pet retail showroom, shallow depth of field, Hasselblad H6D-100c 80mm lens, editorial photography 4K, no text no logos sujeito íntegro",
            "negative_prompt": "no smiling stock pose, no cartoon, no anime, no 3D, no logos, no text in image, no recortes, no ring light",
            "aspect_ratio": "free",
            "reference_images": ["figma://1:704", "figma://1:1216"],
            "model_hint": "nano-banana-2",
            "iteration_strategy": {"max_attempts": 3, "fallback_prompts": []},
            "metadata": {"style_id": "A-headline-foto-dark", "audience": "varejo_pet_empresario", "mood_chosen": "serious confidence"}
        }]
    },
    "qa-validator": {
        "status": "PASS_WITH_WARNINGS",
        "issues": [],
        "warnings": [{
            "severity": "warning", "category": "spacing", "rule": "safe_margin_top_respected",
            "expected": ">=100", "actual": "100", "element": "tag",
            "fix_suggestion": "Tag está exatamente no limite — ok mas considere afastar."
        }],
        "metadata": {"rules_checked": 18, "passed": 17, "failed": 1}
    },
}


def write_artifact(run_id: str, step: str, data: dict, artifacts_dir: Path):
    out = artifacts_dir / run_id
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{step}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def log_event(run_id: str, event: dict, artifacts_dir: Path):
    log_dir = artifacts_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"run_id": run_id, "ts": datetime.now().isoformat(), **event}, ensure_ascii=False) + "\n")


@click.command()
@click.argument("briefing_text", required=False)
@click.option("--mock", is_flag=True, help="Use mock LLM (no API calls).")
@click.option("--provider", help="Override LLM_PROVIDER env var.")
@click.option("--stop-at", help="Stop after this skill id (e.g. '02').")
@click.option("--input", "input_file", help="JSON file with structured briefing (skips skill 01).")
@click.option("--verbose/--quiet", default=True)
def main(briefing_text, mock, provider, stop_at, input_file, verbose):
    """ad-generator pipeline — gera ad Metta a partir de briefing PT-BR.

    Exemplos:

      python pipeline.py "ad de prova social com Hiperzoo, story" --mock

      python pipeline.py "story de dor pra empresário refém da operação"

      python pipeline.py --input artifacts/briefings/hiperzoo.json --stop-at 03
    """
    artifacts_dir = Path(os.getenv("ARTIFACTS_DIR", "./artifacts"))
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]

    info(f"run_id = {run_id}")
    info(f"mode = {'MOCK' if mock else 'LIVE'} | provider = {provider or os.getenv('LLM_PROVIDER', 'claude')}")

    # Setup LLM
    if mock:
        llm = MockLLMAdapter(fixtures=MOCK_FIXTURES)
    else:
        llm = LLMAdapter(provider=provider)

    runner = SkillRunner(llm=llm)

    # Skill 01 — briefing parser (or load from file)
    if input_file:
        briefing = json.loads(Path(input_file).read_text(encoding="utf-8"))
        info(f"Loaded briefing from {input_file}")
    else:
        if not briefing_text:
            err("Need either briefing_text argument or --input file.")
            sys.exit(1)
        info("Running 01-briefing-parser...")
        t0 = time.time()
        result = runner.run("01-briefing-parser", briefing_text)
        log_event(run_id, {"skill": "01", "ok": result.ok,
                           "tokens_in": result.llm_response.tokens_in if result.llm_response else 0,
                           "tokens_out": result.llm_response.tokens_out if result.llm_response else 0,
                           "latency_ms": int((time.time() - t0) * 1000)}, artifacts_dir)
        if not result.ok:
            err(f"briefing-parser failed: {result.error}")
            sys.exit(2)
        briefing = result.output
        if briefing.get("clarifying_questions"):
            ok("briefing-parser asked for clarification:")
            for q in briefing["clarifying_questions"]:
                console.print(f"  ? {q}") if 'console' in globals() else print(f"  ? {q}")
            err("Pipeline paused — fill clarifications and re-run.")
            write_artifact(run_id, "01-briefing", briefing, artifacts_dir)
            sys.exit(0)

    write_artifact(run_id, "01-briefing", briefing, artifacts_dir)
    vr = validate(briefing, "briefing.schema.json")
    if not vr.ok:
        err(f"briefing schema invalid: {vr.errors}")
        sys.exit(3)
    if verbose:
        panel("01 · briefing", briefing)

    if stop_at == "01":
        ok(f"stopped at 01. Output: {artifacts_dir / run_id / '01-briefing.json'}")
        return

    # Skill 02 — style selector (with optional vector search injection)
    info("Running 02-style-selector...")
    t0 = time.time()

    vector_context = ""
    if not mock:
        try:
            from vector_search import search_styles, candidates_to_context
            query = briefing.get("tese_central", "") + " | " + briefing.get("intent", "")
            candidates, status = search_styles(query, top_k=5)
            if candidates:
                info(f"vector search → top candidate: {candidates[0].model_id} (score={candidates[0].combined_score:.3f})")
                vector_context = candidates_to_context(candidates)
            else:
                info(f"vector search skipped: {status}")
        except Exception as e:
            info(f"vector search unavailable (graceful fallback): {e}")

    result = runner.run("02-style-selector", briefing, extra_context=vector_context)
    log_event(run_id, {"skill": "02", "ok": result.ok,
                       "latency_ms": int((time.time() - t0) * 1000)}, artifacts_dir)
    if not result.ok:
        err(f"style-selector failed: {result.error}")
        sys.exit(2)
    style_rec = result.output
    write_artifact(run_id, "02-style-recommendation", style_rec, artifacts_dir)
    if verbose:
        panel("02 · style recommendation", style_rec)
    if stop_at == "02":
        ok(f"stopped at 02. top1 = {style_rec['recommended'][0]['model_id']}")
        return

    # Pick top-1 (in v2: ask human)
    chosen_model_id = style_rec["recommended"][0]["model_id"]
    info(f"Chosen style: {chosen_model_id}")

    # Skill 03 — layout composer
    info("Running 03-layout-composer...")
    layout_input = {
        "briefing": briefing,
        "model_id": chosen_model_id,
        "copy": {
            # In production, copy generation is its own step (delegated to /copy-ad).
            # MVP: prompt LLM to generate copy now AND compose layout in one call.
            "_note": "MVP — generate copy inside layout composer for now"
        }
    }
    t0 = time.time()
    result = runner.run("03-layout-composer", layout_input,
                        extra_context="Note: this MVP also generates the copy. Compose appropriate headline/body/CTA aligned to the tese_central and the model's slot constraints.")
    log_event(run_id, {"skill": "03", "ok": result.ok,
                       "latency_ms": int((time.time() - t0) * 1000)}, artifacts_dir)
    if not result.ok:
        err(f"layout-composer failed: {result.error}")
        sys.exit(2)
    layout_spec = result.output

    # Enforce model YAML constraints (inject missing image_slot, fix frame size, resolve tokens)
    try:
        from layout_enforcer import enforce
        layout_spec, enforcer_log = enforce(layout_spec, briefing)
        for msg in enforcer_log:
            info(f"enforcer: {msg}")
    except Exception as e:
        info(f"enforcer skipped: {e}")

    write_artifact(run_id, "03-layout-spec", layout_spec, artifacts_dir)
    if verbose:
        panel("03 · layout spec (post-enforce)", layout_spec)
    if stop_at == "03":
        return

    # Skill 04 — image prompt engineer
    image_slots = [el for el in layout_spec.get("elements", []) if el.get("type") == "image_slot"]
    image_urls: dict[str, str] = {}
    if image_slots:
        info("Running 04-image-prompt-engineer...")
        prompt_input = {"layout_spec": layout_spec, "briefing": briefing, "image_slots": image_slots}
        t0 = time.time()
        result = runner.run("04-image-prompt-engineer", prompt_input)
        log_event(run_id, {"skill": "04", "ok": result.ok,
                           "latency_ms": int((time.time() - t0) * 1000)}, artifacts_dir)
        if not result.ok:
            err(f"image-prompt-engineer failed: {result.error}")
            sys.exit(2)
        image_spec = result.output
        write_artifact(run_id, "04-image-prompt", image_spec, artifacts_dir)
        if verbose:
            panel("04 · image prompts", image_spec)

        if not image_spec.get("skip"):
            image_gen = ImageGenAdapter()
            for p in image_spec.get("prompts", []):
                ig_result = image_gen.generate(
                    prompt=p["prompt"],
                    negative_prompt=p.get("negative_prompt", ""),
                    aspect_ratio=p.get("aspect_ratio", "9:16"),
                    reference_images=p.get("reference_images", []),
                )
                image_urls[p["slot_name"]] = ig_result.url
                info(f"image generated: {p['slot_name']} → {ig_result.url}")
    else:
        info("No image slots in layout — skipping skills 04 (image-prompt-engineer)")

    if stop_at == "04":
        return

    # Skill 05 — assembler (PNG default — entregável final)
    info("Running 05-assembler (PNG output)...")
    assembler = AssemblerAdapter()  # reads ASSEMBLER env var (default: png)
    t0 = time.time()
    asm_result = assembler.assemble(layout_spec, image_urls)
    log_event(run_id, {"skill": "05", "ok": True,
                       "latency_ms": int((time.time() - t0) * 1000)}, artifacts_dir)
    asm_output = {
        "destination": asm_result.destination,
        "png_path": asm_result.png_path,
        "jpeg_path": asm_result.jpeg_path,
        "html_path": asm_result.html_path,
        "figma": {"url": asm_result.figma_url} if asm_result.figma_url else None,
        "preview_url": f"file://{asm_result.png_path}" if asm_result.png_path else None,
        "metadata": {"style_id": layout_spec.get("model_id"),
                     "elapsed_ms": asm_result.elapsed_ms,
                     "warnings": asm_result.warnings or []}
    }
    if asm_result.png_path:
        ok(f"PNG salvo: {asm_result.png_path}")
    write_artifact(run_id, "05-ad-output", asm_output, artifacts_dir)
    ok(f"Ad assembled. {asm_output}")
    if stop_at == "05":
        return

    # Skill 06 — QA validator
    info("Running 06-qa-validator...")
    qa_input = {"ad_output": asm_output, "layout_spec": layout_spec, "model_id": chosen_model_id}
    t0 = time.time()
    result = runner.run("06-qa-validator", qa_input)
    log_event(run_id, {"skill": "06", "ok": result.ok,
                       "latency_ms": int((time.time() - t0) * 1000)}, artifacts_dir)
    if not result.ok:
        err(f"qa-validator failed: {result.error}")
        sys.exit(2)
    qa = result.output
    write_artifact(run_id, "06-qa-report", qa, artifacts_dir)
    if verbose:
        panel("06 · QA report", qa)

    if qa.get("status") == "FAIL":
        err(f"QA FAILED — {len(qa.get('issues', []))} issues")
        sys.exit(4)

    ok(f"Pipeline complete. Run dir: {artifacts_dir / run_id}")


if __name__ == "__main__":
    main()
