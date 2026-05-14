"""Convert banco SVGs to PNGs via Chrome headless.

Source: hardcoded local path to "Modelos de ADS" folder.
Output: artifacts/banco/<filename>.png at 1080x1920.

Usage: python scripts/convert_svgs.py [--limit N]
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SOURCE = Path(r"C:\Users\Usuario\Desktop\Renan\Clientes\Metta\Rebranding\01. Assets de Marca\Referências Design\Modelos de ADS")
OUTPUT = Path(__file__).resolve().parent.parent / "artifacts" / "banco"

CHROME_PATHS = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]


def find_chrome() -> Path | None:
    for p in CHROME_PATHS:
        if p.exists():
            return p
    return None


HTML_TMPL = """<!doctype html>
<html><head><meta charset="utf-8">
<style>
  html, body {{ margin:0; padding:0; background:#0C161B; overflow:hidden; }}
  body {{ display:flex; justify-content:center; align-items:flex-start; }}
  svg {{ width:1080px; height:1920px; display:block; }}
</style></head>
<body>
{svg_content}
</body></html>
"""


def convert_one(svg_path: Path, out_path: Path, chrome: Path) -> bool:
    """Render an SVG file to PNG via Chrome headless screenshot."""
    if out_path.exists() and out_path.stat().st_size > 5000:
        return True
    svg_content = svg_path.read_text(encoding="utf-8")
    # If width/height not 1080x1920, inject the viewBox-based sizing in our wrapper anyway
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as tmp:
        tmp.write(HTML_TMPL.format(svg_content=svg_content))
        tmp_path = Path(tmp.name)
    try:
        cmd = [
            str(chrome),
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-sandbox",
            "--window-size=1080,1920",
            "--virtual-time-budget=3000",
            f"--screenshot={out_path}",
            f"file://{tmp_path.resolve()}",
        ]
        result = subprocess.run(cmd, capture_output=True, timeout=60)
        if out_path.exists() and out_path.stat().st_size > 1000:
            return True
        else:
            print(f"  [fail] {svg_path.name}: stderr={result.stderr.decode(errors='replace')[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  [timeout] {svg_path.name}")
        return False
    finally:
        try:
            tmp_path.unlink()
        except Exception:
            pass


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=0, help="Limit number of conversions (for testing)")
    args = p.parse_args()

    chrome = find_chrome()
    if not chrome:
        print("Chrome/Edge not found", file=sys.stderr)
        sys.exit(1)

    OUTPUT.mkdir(parents=True, exist_ok=True)

    svgs = sorted(SOURCE.glob("*.svg"))
    if args.limit:
        svgs = svgs[: args.limit]

    print(f"Converting {len(svgs)} SVGs -> PNGs in {OUTPUT}")
    print(f"Using browser: {chrome.name}")

    ok = 0
    for i, svg in enumerate(svgs, 1):
        png = OUTPUT / (svg.stem + ".png")
        print(f"[{i}/{len(svgs)}] {svg.name}")
        if convert_one(svg, png, chrome):
            ok += 1
            size_kb = png.stat().st_size // 1024
            print(f"  -> {png.name} ({size_kb} KB)")

    print(f"\nDone: {ok}/{len(svgs)} converted")


if __name__ == "__main__":
    main()
