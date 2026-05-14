"""Demo CLI — gera 3 ads exemplares ponta-a-ponta e cria HTML preview navegável.

Uso típico:

  # Gera mock LLM + image-gen REAL (precisa OPENAI_API_KEY ou GEMINI_API_KEY)
  python demo.py

  # Gera mock LLM + image-gen mock (zero custo, instantâneo)
  python demo.py --image-gen mock

  # Gera live LLM + image-gen real (full pipeline)
  python demo.py --live

  # Só image-gen, sem rodar pipeline (testa só a imagem)
  python demo.py --image-only "serious confidence portrait of brazilian entrepreneur..."
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
import webbrowser
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from skills_runner import SkillRunner
from validators import validate
from adapters.llm import LLMAdapter, MockLLMAdapter
from adapters.image_gen import ImageGenAdapter
from adapters.assembler import AssemblerAdapter

# Mock fixtures (compartilhado com pipeline.py)
from pipeline import MOCK_FIXTURES, write_artifact, log_event


DEMO_BRIEFINGS = [
    {
        "name": "case_hiperzoo",
        "briefing": "ad de prova social com Hiperzoo pra varejo de pet, story",
        "expected_style": "A-headline-foto-dark",
    },
    {
        "name": "dor_refem_operacao",
        "briefing": "story de dor pra empresário refém do operacional, tom emocional",
        "expected_style": "B-foto-top-headline-mixed",
    },
    {
        "name": "convite_evento",
        "briefing": "convite pra webinário de junho com logos Sicredi Vivo Korin, story institucional",
        "expected_style": "YELLOW-BLOCO",
    },
]


def run_one(briefing_input: dict, mock_llm: bool, image_gen_provider: str, artifacts_dir: Path) -> dict:
    """Roda 1 briefing através do pipeline. Retorna dict com paths/URLs gerados."""
    run_id = datetime.now().strftime("%H%M%S") + "_" + briefing_input["name"]
    print(f"\n=== {briefing_input['name']} ===")
    print(f"briefing: {briefing_input['briefing']}")

    # Setup
    if mock_llm:
        llm = MockLLMAdapter(fixtures=MOCK_FIXTURES)
    else:
        llm = LLMAdapter()

    runner = SkillRunner(llm=llm)

    # Skill 01
    print("  → 01 briefing-parser")
    r = runner.run("01-briefing-parser", briefing_input["briefing"])
    if not r.ok:
        return {"name": briefing_input["name"], "ok": False, "error": f"briefing-parser: {r.error}"}
    briefing = r.output
    write_artifact(run_id, "01-briefing", briefing, artifacts_dir)

    # Skill 02
    print("  → 02 style-selector")
    r = runner.run("02-style-selector", briefing)
    if not r.ok:
        return {"name": briefing_input["name"], "ok": False, "error": f"style-selector: {r.error}"}
    style_rec = r.output
    chosen = style_rec["recommended"][0]["model_id"]
    print(f"     style chosen: {chosen}")
    write_artifact(run_id, "02-style-recommendation", style_rec, artifacts_dir)

    # Skill 03
    print("  → 03 layout-composer")
    layout_input = {"briefing": briefing, "model_id": chosen, "copy": {"_note": "demo"}}
    r = runner.run("03-layout-composer", layout_input,
                   extra_context="Generate the copy yourself. Use the model's slot constraints.")
    if not r.ok:
        return {"name": briefing_input["name"], "ok": False, "error": f"layout-composer: {r.error}"}
    layout = r.output
    write_artifact(run_id, "03-layout-spec", layout, artifacts_dir)

    # Skill 04 — image-prompt-engineer
    image_slots = [el for el in layout.get("elements", []) if el.get("type") == "image_slot"]
    image_urls: dict[str, str] = {}
    image_paths: dict[str, str] = {}

    if image_slots:
        print("  → 04 image-prompt-engineer")
        r = runner.run("04-image-prompt-engineer",
                       {"layout_spec": layout, "briefing": briefing, "image_slots": image_slots})
        if not r.ok:
            return {"name": briefing_input["name"], "ok": False, "error": f"image-prompt: {r.error}"}
        image_spec = r.output
        write_artifact(run_id, "04-image-prompt", image_spec, artifacts_dir)

        if not image_spec.get("skip"):
            print(f"  → image-gen ({image_gen_provider})")
            image_gen = ImageGenAdapter(provider=image_gen_provider)
            for p in image_spec.get("prompts", []):
                try:
                    res = image_gen.generate(
                        prompt=p["prompt"],
                        negative_prompt=p.get("negative_prompt", ""),
                        aspect_ratio=p.get("aspect_ratio", "9:16"),
                        reference_images=None,  # demo: pular refs (precisa Figma API)
                    )
                    image_urls[p["slot_name"]] = res.url
                    image_paths[p["slot_name"]] = res.local_path
                    print(f"     ✓ {p['slot_name']} → {res.url} ({res.elapsed_ms}ms)")
                except Exception as e:
                    print(f"     ✗ {p['slot_name']} failed: {e}")
                    image_urls[p["slot_name"]] = "https://placehold.co/1080x1920/0C161B/FFBE18?text=ERROR"

    # Skill 05 — assembler (PNG output)
    print("  → 05 assembler (PNG)")
    assembler = AssemblerAdapter(destination="png")
    asm = assembler.assemble(layout, image_urls)
    write_artifact(run_id, "05-ad-output", {
        "png_path": asm.png_path,
        "destination": "png",
        "warnings": asm.warnings or [],
    }, artifacts_dir)
    if asm.warnings:
        for w in asm.warnings:
            print(f"     ⚠ {w}")
    print(f"     ✓ PNG: {asm.png_path}")

    return {
        "name": briefing_input["name"],
        "briefing": briefing_input["briefing"],
        "style_chosen": chosen,
        "layout_path": str(artifacts_dir / run_id / "03-layout-spec.json"),
        "png_path": asm.png_path,
        "image_paths": image_paths,
        "image_urls": image_urls,
        "ok": True,
    }


def build_index_html(results: list[dict], out_path: Path) -> Path:
    """HTML preview consolidado — lado a lado todos os ads gerados."""
    cards = []
    for r in results:
        if not r.get("ok"):
            cards.append(f"""
<div class="card error">
  <h3>{r['name']}</h3>
  <p>❌ {r.get('error', 'unknown error')}</p>
</div>""")
            continue

        png_url = f"file://{r['png_path']}" if r.get("png_path") else ""
        images_html = ""
        for slot, path in r.get("image_paths", {}).items():
            if path:
                images_html += f'<div class="img-strip"><span>{slot} (image-gen output)</span><img src="file://{path}"></div>'

        cards.append(f"""
<div class="card">
  <h3>{r['name']}</h3>
  <p class="briefing">"{r['briefing']}"</p>
  <p class="style">→ <strong>{r['style_chosen']}</strong></p>
  <div class="links">
    <a href="{png_url}" target="_blank">Abrir PNG</a>
    <span>·</span>
    <a href="file://{r['layout_path']}" target="_blank">layout-spec.json</a>
  </div>
  <img class="final-png" src="{png_url}" loading="lazy">
  {images_html}
</div>""")

    html = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>ad-generator demo — Metta</title>
<style>
  :root {{ --bg:#0C161B; --fg:#FAFCFD; --yellow:#FFBE18; --gray:#B0CAD8; --dim:#435965; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; padding:32px; background:var(--bg); color:var(--fg); font-family:-apple-system,'SF Pro',system-ui,sans-serif; }}
  h1 {{ font-size:32px; font-weight:870; font-stretch:132%; letter-spacing:-0.02em; margin:0 0 8px; }}
  h1 span {{ color:var(--yellow); }}
  .meta {{ color:var(--gray); font-size:14px; margin-bottom:32px; }}
  .grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(420px,1fr)); gap:24px; }}
  .card {{ background:#131F25; border-radius:20px; padding:24px; border:1px solid rgba(255,255,255,0.08); }}
  .card.error {{ border-color:#c44; }}
  .card h3 {{ font-size:18px; font-weight:700; margin:0 0 8px; color:var(--yellow); text-transform:uppercase; letter-spacing:0.04em; }}
  .briefing {{ color:var(--gray); font-style:italic; font-size:14px; margin:8px 0 4px; }}
  .style {{ font-size:14px; color:var(--gray); margin:0 0 16px; }}
  .style strong {{ color:var(--yellow); }}
  .links {{ font-size:13px; margin-bottom:16px; color:var(--dim); }}
  .links a {{ color:var(--yellow); text-decoration:none; }}
  .links a:hover {{ text-decoration:underline; }}
  .final-png {{ width:100%; aspect-ratio:9/16; object-fit:contain; border-radius:12px; background:#0A1013; display:block; }}
  .img-strip {{ margin-top:12px; }}
  .img-strip span {{ font-size:11px; color:var(--dim); text-transform:uppercase; letter-spacing:0.12em; }}
  .img-strip img {{ width:100%; max-height:300px; object-fit:contain; border-radius:8px; margin-top:6px; background:#000; opacity:0.7; }}
</style></head>
<body>
  <h1>ad-generator <span>·</span> demo</h1>
  <p class="meta">{len(results)} ads gerados · {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
  <div class="grid">{''.join(cards)}</div>
</body></html>
"""
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--live", action="store_true", help="Use real LLM (default: mock).")
    p.add_argument("--image-gen", default="openai",
                   help="openai | gemini | nano-banana-2 | imagen-3 | mock (default: openai)")
    p.add_argument("--image-only", help="Apenas geração de imagem com prompt direto, pula pipeline.")
    p.add_argument("--open", action="store_true", help="Abrir HTML preview no navegador ao final.")
    args = p.parse_args()

    artifacts_dir = Path(os.getenv("ARTIFACTS_DIR", "./artifacts"))
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    # === MODE 1: image-only ===
    if args.image_only:
        print(f"[demo] image-only mode → provider={args.image_gen}")
        ig = ImageGenAdapter(provider=args.image_gen)
        res = ig.generate(prompt=args.image_only, aspect_ratio="9:16")
        print(f"\n✓ image saved: {res.local_path}")
        print(f"  url: {res.url}")
        print(f"  elapsed: {res.elapsed_ms}ms")
        print(f"  cost: ~${res.cost_usd or 0:.3f}")
        if args.open and res.local_path:
            webbrowser.open(res.url)
        return

    # === MODE 2: full pipeline demo ===
    mock_llm = not args.live
    print(f"[demo] LLM={'LIVE' if args.live else 'MOCK'} | image-gen={args.image_gen}")

    results = []
    for briefing in DEMO_BRIEFINGS:
        try:
            r = run_one(briefing, mock_llm=mock_llm, image_gen_provider=args.image_gen,
                        artifacts_dir=artifacts_dir)
            results.append(r)
        except Exception as e:
            print(f"  ✗ {briefing['name']} failed: {e}")
            results.append({"name": briefing["name"], "briefing": briefing["briefing"],
                            "ok": False, "error": str(e)})

    # Index HTML
    index_path = artifacts_dir / "demo_preview.html"
    build_index_html(results, index_path)

    print(f"\n{'=' * 50}")
    print(f"✓ Demo complete. {sum(1 for r in results if r.get('ok'))}/{len(results)} succeeded")
    print(f"  Preview: file://{index_path.resolve()}")
    print(f"  Artifacts: {artifacts_dir.resolve()}")

    if args.open:
        webbrowser.open(f"file://{index_path.resolve()}")


if __name__ == "__main__":
    main()
