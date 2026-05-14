"""Generate structured descriptions of banco ads via GPT-4o-mini vision.

Output: artifacts/banco/<filename>.json with structured description fields.
Cost: ~$0.001 per image × 68 = ~$0.07 total.

Usage: python scripts/describe_ads.py [--limit N] [--force]
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import httpx

BANCO_DIR = Path(__file__).resolve().parent.parent / "artifacts" / "banco"

SYSTEM_PROMPT = """Você é analista de design de ads Metta. Recebe uma imagem de ad publicitário e produz descrição estruturada em JSON.

Foco em campos editoriais/visuais úteis pra busca semântica:

- `style_id`: detecte o estilo Metta usado (A | B | C | D | YELLOW-BLOCO | YELLOW-EDITORIAL | YELLOW-FRAME | YELLOW-DRAW | YELLOW-SPLIT | LIGHT-SURREAL | LIGHT-TIPO | NEWS-CARD | LOGO-WALL | DARK-COLAGEM | DARK-CARTA | DARK-OBJETO | H | I | K). Se não conseguir identificar, retorne "UNKNOWN".
- `tese_central`: 1 linha — o que esse ad COMUNICA (tese da copy + visual)
- `intent`: intent semantico (prova_social_case_nominal | dor_pessoal | reframe_intelectual | convite_evento | manifesto | promessa_numerica | case_metric | reframe_mantra | autoridade_founder_led | posicionamento_institucional)
- `palette`: dominante (dark | light-white | yellow-bg | mixed)
- `mood`: 2-4 palavras (ex: "serious confidence", "quiet exhaustion", "warm institutional")
- `composition`: descrição em 1-2 linhas (foto position, headline position, etc.)
- `headline_text`: transcreva headline visível (se houver)
- `body_text`: transcreva body curto (se houver)
- `cta_text`: transcreva CTA (se houver)
- `has_person_photo`: true/false
- `tags`: array de tags relevantes pra busca (ex: ["case-nominal", "varejo-pet", "dor-emocional"])
- `keywords_pt`: 5-10 palavras-chave em PT-BR pra busca
- `keywords_en`: mesmas keywords em EN

Retorne APENAS JSON válido, sem prose, sem markdown fences."""


def encode_image(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


import time as _time


def describe_one(png_path: Path, api_key: str, model: str = "gpt-4o-mini") -> dict | None:
    b64 = encode_image(png_path)
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": f"Analise este ad Metta. Filename: {png_path.name}"},
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "low"}},
                ],
            },
        ],
        "response_format": {"type": "json_object"},
        "temperature": 0,
        "max_tokens": 1000,
    }
    # Retry up to 3 times on rate limit
    for attempt in range(3):
        r = httpx.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            json=payload,
            timeout=120,
        )
        if r.status_code == 429:
            # Rate limit — sleep and retry
            wait = 30 * (attempt + 1)
            print(f"  [rate-limit] {png_path.name}: waiting {wait}s")
            _time.sleep(wait)
            continue
        if r.status_code != 200:
            print(f"  [fail] {png_path.name}: {r.status_code} {r.text[:200]}")
            return None
        try:
            content = r.json()["choices"][0]["message"]["content"]
            return json.loads(content)
        except Exception as e:
            print(f"  [parse-fail] {png_path.name}: {e}")
            return None
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=0)
    p.add_argument("--force", action="store_true", help="Re-describe even if JSON exists")
    args = p.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY missing", file=sys.stderr)
        sys.exit(1)

    pngs = sorted(BANCO_DIR.glob("*.png"))
    if args.limit:
        pngs = pngs[: args.limit]

    print(f"Describing {len(pngs)} ad images via gpt-4o-mini vision...")
    ok = 0
    skipped = 0
    for i, png in enumerate(pngs, 1):
        json_path = png.with_suffix(".json")
        if json_path.exists() and not args.force:
            skipped += 1
            continue
        # Skip the _embeddings.json store file
        if png.stem.startswith("_"):
            continue
        print(f"[{i}/{len(pngs)}] {png.name}")
        desc = describe_one(png, api_key)
        if desc:
            desc["_filename"] = png.name
            desc["_png_path"] = str(png)
            json_path.write_text(json.dumps(desc, ensure_ascii=False, indent=2), encoding="utf-8")
            ok += 1
            print(f"  -> style_id={desc.get('style_id')} mood='{desc.get('mood')}'")
            # Pace requests: sleep 2s between calls to avoid TPM burst
            _time.sleep(2)

    print(f"\nDone: {ok} described, {skipped} skipped (already done)")


if __name__ == "__main__":
    main()
