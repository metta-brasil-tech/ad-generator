"""QA Vision — análise visual de PNGs gerados via gpt-4o-mini.

Detecta problemas visuais nos criativos: texto sobreposto, canvas vazio,
placeholder mock, imagem faltando, contraste baixo, CTA ausente, etc.
"""
from __future__ import annotations

import base64
import json
import time
from pathlib import Path

import httpx


_QA_ISSUES = [
    "TEXT_OVERLAP",
    "HEADLINE_CLIPPED",
    "EMPTY_CANVAS",
    "MOCK_PLACEHOLDER",
    "IMAGE_MISSING",
    "LOW_CONTRAST",
    "STRUCTURAL_MISSING",
    "CONTENT_TOPHEAVY",
    "CTA_MISSING",
    "BRAND_MISMATCH",
]

_QA_PROMPT = """You are a visual QA reviewer for advertising creatives.
Analyze this image and return a JSON object with:
{{
  "score": 0-10,
  "issues": ["ISSUE_CODE", ...],
  "notes": "brief comment"
}}

Possible issue codes: {issues}

TEXT_OVERLAP: two text blocks visually overlap or are illegibly close
HEADLINE_CLIPPED: headline text is cut off at canvas edge
EMPTY_CANVAS: canvas is blank or near-blank
MOCK_PLACEHOLDER: placehold.co or generic placeholder image visible
IMAGE_MISSING: template requires a real photo but none is present (plain color bg only)
LOW_CONTRAST: text is unreadable against background
STRUCTURAL_MISSING: expected layout zones (headline, body, CTA) are absent
CONTENT_TOPHEAVY: all content crammed in top half, bottom is empty
CTA_MISSING: no call-to-action button or text visible
BRAND_MISMATCH: colors/fonts clearly don't match expected brand

Return ONLY valid JSON, no markdown.
""".format(issues=", ".join(_QA_ISSUES))


def analyze_png(png_path: str | Path, api_key: str | None = None) -> dict:
    """Analyze a single PNG and return QA result dict."""
    import os
    key = api_key or os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_IMAGE_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY not set")

    data = Path(png_path).read_bytes()
    b64 = base64.b64encode(data).decode()

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                {"type": "text", "text": _QA_PROMPT},
            ],
        }],
        "max_tokens": 300,
    }

    r = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    if r.status_code != 200:
        raise RuntimeError(f"OpenAI QA {r.status_code}: {r.text[:200]}")

    content = r.json()["choices"][0]["message"]["content"]
    try:
        return json.loads(content)
    except Exception:
        return {"score": 0, "issues": ["PARSE_ERROR"], "notes": content}


def run_batch_qa(png_dir: str | Path, delay: float = 2.5) -> list[dict]:
    """Run QA on all PNGs in a directory. Returns list of result dicts."""
    results = []
    for png in sorted(Path(png_dir).glob("**/*.png")):
        try:
            result = analyze_png(png)
        except Exception as e:
            result = {"score": 0, "issues": ["ERROR"], "notes": str(e)}
        result["file"] = str(png)
        results.append(result)
        score = result.get("score", 0)
        emoji = "✅" if score >= 7 else ("⚠️" if score >= 5 else "❌")
        print(f"{emoji} {png.name}: {score}/10  {result.get('issues', [])}")
        time.sleep(delay)
    return results
