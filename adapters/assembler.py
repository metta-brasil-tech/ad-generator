"""Assembler — renderiza layout-spec em PNG/JPEG (entregável final).

Implementação nativa via Pillow. Sem Chrome/Playwright. Sem Figma.
Output: PNG (default) ou JPEG em artifacts/outputs/.

Mantém HTML como side-output pra inspeção/debug, mas o entregável é sempre imagem.
"""
from __future__ import annotations

import io
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import httpx

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
    _PIL_OK = True
except ImportError:
    _PIL_OK = False


# Caches
_FONT_CACHE: dict[tuple, ImageFont.FreeTypeFont] = {}
_IMAGE_CACHE: dict[str, Image.Image] = {}


# Map "SF Pro" / style → font filenames (Windows + fallbacks)
FONT_FILE_MAP = {
    # SF Pro Expanded variants (installed via Apple SF Pro family)
    ("SF Pro", "Expanded Heavy"): ["SF-Pro-Expanded-Heavy.otf", "SFProExpanded-Heavy.otf"],
    ("SF Pro", "Expanded Bold"): ["SF-Pro-Expanded-Bold.otf", "SFProExpanded-Bold.otf"],
    ("SF Pro", "Expanded Semibold"): ["SF-Pro-Expanded-Semibold.otf", "SFProExpanded-Semibold.otf"],
    ("SF Pro", "Expanded Medium"): ["SF-Pro-Expanded-Medium.otf", "SFProExpanded-Medium.otf"],
    ("SF Pro", "Expanded Regular"): ["SF-Pro-Expanded-Regular.otf", "SFProExpanded-Regular.otf"],
    ("SF Pro", "Heavy"): ["SF-Pro-Heavy.otf"],
    ("SF Pro", "Heavy Italic"): ["SF-Pro-HeavyItalic.otf"],
    # Inter fallback (always available if user runs pip install)
    ("Inter", "Regular"): ["Inter-Regular.ttf"],
    ("Inter", "Medium"): ["Inter-Medium.ttf"],
    ("Inter", "Semi Bold"): ["Inter-SemiBold.ttf"],
    ("Inter", "Bold"): ["Inter-Bold.ttf"],
    ("Inter", "Black"): ["Inter-Black.ttf"],
}

# Standard system locations to search
FONT_SEARCH_DIRS = [
    Path(r"C:\Windows\Fonts"),
    Path.home() / "AppData/Local/Microsoft/Windows/Fonts",
    Path("/Library/Fonts"),
    Path("/System/Library/Fonts"),
    Path("/usr/share/fonts"),
    Path("/usr/local/share/fonts"),
    Path(__file__).parent.parent / "assets/fonts",  # bundled fallback
]


@dataclass
class AssembleResult:
    destination: str
    png_path: str | None = None
    jpeg_path: str | None = None
    html_path: str | None = None
    figma_url: str | None = None
    elapsed_ms: int = 0
    warnings: list = None


def _find_font_file(family: str, style: str) -> Path | None:
    """Locate a font file on disk by family+style."""
    candidates = list(FONT_FILE_MAP.get((family, style), []))
    # Generic variations
    candidates += [
        f"{family}-{style.replace(' ', '')}.ttf",
        f"{family.replace(' ', '')}-{style.replace(' ', '')}.otf",
        f"{family} {style}.ttf",
    ]
    # Windows lowercase variants for Arial
    if family.lower() == "arial":
        if "Bold" in style and "Italic" in style:
            candidates += ["arialbi.ttf"]
        elif "Bold" in style:
            candidates += ["arialbd.ttf"]
        elif "Italic" in style:
            candidates += ["ariali.ttf"]
        else:
            candidates += ["arial.ttf"]

    for d in FONT_SEARCH_DIRS:
        if not d.exists():
            continue
        for name in candidates:
            p = d / name
            if p.exists():
                return p
    return None


def _is_heavy(style: str) -> bool:
    s = style.lower()
    return any(k in s for k in ["heavy", "bold", "black", "semibold"])


def _load_font(family: str, style: str, size: int) -> ImageFont.FreeTypeFont:
    """Load font with caching + graceful fallback chain.

    Priority for Metta brand fidelity:
    1. SF Pro Variable (canonical Metta typeface) — width/weight axes set per style
    2. Inter Variable bundled (Metta official fallback for Regular axis)
    3. System Arial/Helvetica
    4. Pillow default
    """
    key = (family, style, size)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]

    # 1) Try SF Pro Variable when family é uma variante SF Pro.
    #    Metta primary: SF Pro Expanded (heads/CTAs) + SF Pro Regular (body).
    #    Tiago primary: SF Pro Condensed Semibold/Light (heads) + SF Pro Regular (body orgânico).
    #    family hint informa o wdth axis correto quando style sozinho é ambíguo
    #    (ex: 'Semibold' precisa de wdth 75 se family for SF Pro Condensed).
    sf_pro_families = ("SF Pro", "SF Pro Condensed", "SF Pro Expanded", "SF Pro Compressed")
    if family in sf_pro_families:
        f = _load_sf_pro_variable(style, size, family=family)
        if f:
            _FONT_CACHE[key] = f
            sentinel = ("_warned_sf", family, style)
            if sentinel not in _FONT_CACHE:
                print(f"  [info] using SF Pro Variable for '{family} / {style}'")
                _FONT_CACHE[sentinel] = None
            return f

    # 2) Try literal font file match (older static font files if installed)
    path = _find_font_file(family, style)
    if path:
        try:
            f = ImageFont.truetype(str(path), size)
            _FONT_CACHE[key] = f
            return f
        except Exception:
            pass

    # 3) Try bundled Inter variable font (Metta official Regular-axis fallback)
    f = _load_inter_variable(style, size)
    if f:
        _FONT_CACHE[key] = f
        sentinel = ("_warned", family, style)
        if (family, style) != ("Inter", style) and sentinel not in _FONT_CACHE:
            print(f"  [info] using Inter variable as fallback for '{family} / {style}' (install SF Pro Variable for full brand fidelity)")
            _FONT_CACHE[sentinel] = None
        return f

    # 4) Fallback chain — try at REQUESTED size (not default!)
    heavy = _is_heavy(style)
    italic = "italic" in style.lower()
    fallback_chain = [
        ("Inter", "Bold" if heavy else ("Medium" if "Medium" in style else "Regular")),
        ("Inter", "Regular"),
        ("Arial", "Bold" if heavy else "Regular"),
        ("Helvetica", "Bold" if heavy else "Regular"),
        ("Verdana", "Bold" if heavy else "Regular"),
        ("Tahoma", "Bold" if heavy else "Regular"),
    ]
    for fam, sty in fallback_chain:
        path = _find_font_file(fam, sty)
        if path:
            try:
                f = ImageFont.truetype(str(path), size)
                _FONT_CACHE[key] = f
                if (family, style) != (fam, sty):
                    # Only warn once per unique (family, style) — store sentinel
                    sentinel = ("_warned", family, style)
                    if sentinel not in _FONT_CACHE:
                        print(f"  ⚠ font '{family} / {style}' not found — falling back to '{fam} / {sty}' (install Inter or SF Pro for production quality)")
                        _FONT_CACHE[sentinel] = None
                return f
            except Exception:
                continue

    # 3) Last resort — Pillow default (tiny bitmap, but at least it won't crash)
    print(f"  ⚠⚠ NO truetype font found anywhere for '{family} / {style}' size {size} — using Pillow default (will look bad). Install Inter: see docs/06-providers.md", file=sys.stderr)
    f = ImageFont.load_default()
    _FONT_CACHE[key] = f
    return f


INTER_VARIABLE_URL = "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf"
INTER_VARIABLE_FILENAME = "Inter-Variable.ttf"

# SF Pro Variable — Apple's official font (Metta primary).
# Axes: Width (30-150), Optical Size (17-28), Weight (1-1000)
SF_PRO_VARIABLE_PATHS = [
    Path.home() / "AppData/Local/Microsoft/Windows/Fonts/SF-Pro-Variable-Official.ttf",
    Path.home() / "AppData/Local/Microsoft/Windows/Fonts/SF-Pro.ttf",
    Path("/Library/Fonts/SF-Pro.ttf"),  # macOS
    Path("/System/Library/Fonts/SFPro.ttf"),
    Path(__file__).parent.parent / "assets/fonts/SF-Pro-Variable-Official.ttf",
]


def _find_sf_pro_variable() -> Path | None:
    """Locate SF Pro Variable font on disk."""
    for p in SF_PRO_VARIABLE_PATHS:
        if p.exists() and p.stat().st_size > 1_000_000:
            return p
    return None


# Map (family, peso) → axes. Tiago usa Condensed (wdth 75), Metta usa Expanded (wdth 132).
# Family hint determina wdth default quando style é só o peso ("Semibold", "Light", etc.).
FAMILY_TO_WDTH = {
    "SF Pro":            100,  # standard (Regular)
    "SF Pro Expanded":   132,  # Metta primary — heads/CTAs
    "SF Pro Condensed":  75,   # Tiago primary — heads
    "SF Pro Compressed": 60,
}

# Style string → weight axis. Width vem do family hint OU do próprio style (se for "Expanded X").
STYLE_TO_WEIGHT = {
    "Heavy": 870, "Heavy Italic": 870,
    "Black": 900, "Black Italic": 900,
    "Bold": 700, "Bold Italic": 700,
    "Semibold": 650, "Semibold Italic": 650,
    "Medium": 540, "Medium Italic": 540,
    "Regular": 400, "Italic": 400,
    "Light": 270, "Light Italic": 270,
    "Thin": 100, "Ultralight": 100,
}


def _load_sf_pro_variable(style: str, size: int, family: str = "SF Pro") -> ImageFont.FreeTypeFont | None:
    """Load SF Pro Variable com axes corretas combinando family hint + style.

    family='SF Pro Condensed' + style='Semibold' → wdth=75, wght=650 (Tiago heads)
    family='SF Pro Expanded'  + style='Bold'     → wdth=132, wght=700 (Metta heads)
    family='SF Pro'           + style='Regular'  → wdth=100, wght=400 (Body)
    family='SF Pro'           + style='Expanded Bold' → wdth=132 (style override), wght=700
    """
    sf_path = _find_sf_pro_variable()
    if not sf_path:
        return None
    try:
        font = ImageFont.truetype(str(sf_path), size)

        # Width: style override (ex: "Expanded Bold") tem precedência sobre family hint
        if "Expanded" in style:
            wdth = 132
        elif "Condensed" in style:
            wdth = 75
        elif "Compressed" in style:
            wdth = 60
        else:
            wdth = FAMILY_TO_WDTH.get(family, 100)

        # Weight: look up no map, ou parse por palavra-chave do style
        # Remove qualificador de width pra ficar só o peso (ex: "Expanded Bold" → "Bold")
        style_weight = style
        for w in ("Expanded ", "Condensed ", "Compressed "):
            style_weight = style_weight.replace(w, "")
        wght = STYLE_TO_WEIGHT.get(style_weight)
        if wght is None:
            # Parse por palavra-chave
            sl = style.lower()
            if "heavy" in sl or "black" in sl: wght = 870
            elif "bold" in sl: wght = 700
            elif "semibold" in sl: wght = 650
            elif "medium" in sl: wght = 540
            elif "light" in sl or "thin" in sl or "ultralight" in sl: wght = 270
            else: wght = 400

        opsz = 17 if size < 18 else 28
        try:
            font.set_variation_by_axes([wdth, opsz, wght])
        except Exception:
            try:
                font.set_variation_by_axes([wdth, wght])
            except Exception:
                pass
        return font
    except Exception:
        return None


def install_inter_fonts(target_dir: Path | None = None) -> bool:
    """Download Inter variable font (single file covers all weights via axes).

    Inter no Google Fonts oficial é só variable. Pillow suporta axes via
    set_variation_by_axes([wght]). _load_inter_variable() abaixo lida com isso.
    """
    target = target_dir or (Path(__file__).parent.parent / "assets" / "fonts")
    target.mkdir(parents=True, exist_ok=True)
    out = target / INTER_VARIABLE_FILENAME

    if out.exists() and out.stat().st_size > 100_000:
        print(f"  [ok] {INTER_VARIABLE_FILENAME} (already present)")
        return True

    try:
        r = httpx.get(INTER_VARIABLE_URL, timeout=60, follow_redirects=True)
        r.raise_for_status()
        out.write_bytes(r.content)
        print(f"  [ok] {INTER_VARIABLE_FILENAME} ({len(r.content) // 1024} KB)")
        return True
    except Exception as e:
        print(f"  [fail] {INTER_VARIABLE_FILENAME}: {e}")
        return False


_STYLE_TO_WGHT = {
    "Thin": 100, "ExtraLight": 200, "Light": 300, "Regular": 400,
    "Medium": 500, "SemiBold": 600, "Semibold": 600, "Bold": 700,
    "ExtraBold": 800, "Black": 900, "Heavy": 900,
    "Expanded Light": 300, "Expanded Regular": 400, "Expanded Medium": 500,
    "Expanded Semibold": 600, "Expanded Bold": 700, "Expanded Heavy": 900,
    "Heavy Italic": 900, "Bold Italic": 700,
}


def _load_inter_variable(style: str, size: int) -> ImageFont.FreeTypeFont | None:
    """Try to load Inter variable font from bundled assets, setting weight axis.

    Inter's variable axes order is [opsz, wght]. We pick opsz based on size
    (display vs body) and wght based on style.
    """
    target = Path(__file__).parent.parent / "assets" / "fonts" / INTER_VARIABLE_FILENAME
    if not target.exists():
        return None
    try:
        font = ImageFont.truetype(str(target), size)
        wght = _STYLE_TO_WGHT.get(style, 400)
        # opsz: 14 for body (<24px), 32 for display (≥56px), interpolated otherwise
        opsz = 14 if size < 24 else (32 if size >= 56 else max(14, min(32, size)))
        # Try in order: by axes (correct order opsz, wght), then by name
        ok = False
        for axes_attempt in ([opsz, wght], [wght, opsz]):
            try:
                font.set_variation_by_axes(axes_attempt)
                ok = True
                break
            except Exception:
                continue
        if not ok:
            # Last attempt: try named instance (Inter has Regular, Bold, etc.)
            named = "Bold" if wght >= 700 else ("Medium" if wght >= 500 else "Regular")
            try:
                font.set_variation_by_name(named)
            except Exception:
                pass
        return font
    except Exception:
        return None


def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    """Convert #RRGGBB to (r, g, b). Accepts CSS var() — returns black if unparseable."""
    if not hex_color:
        return (0, 0, 0)
    s = hex_color.strip()
    if s.startswith("var("):
        # CSS variable — should have been resolved upstream. Fall back to known map.
        var_map = {
            "var(--metta-sys-color-primary)": "#FFBE18",
            "var(--metta-ref-palette-yellow-50)": "#FFBE18",
            "var(--metta-ref-palette-night-10)": "#0C161B",
            "var(--metta-ref-palette-night-100)": "#FFFFFF",
            "var(--metta-ref-palette-night-85)": "#B0CAD8",
            "var(--metta-ref-palette-night-40)": "#435965",
            "var(--metta-sys-color-on-primary)": "#0C161B",
            "var(--metta-sys-color-surface)": "#0C161B",
        }
        s = var_map.get(s, "#000000")
    if s.startswith("#"):
        s = s[1:]
    if len(s) == 3:
        s = "".join(c * 2 for c in s)
    if len(s) != 6:
        return (0, 0, 0)
    try:
        return tuple(int(s[i : i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        return (0, 0, 0)


def _load_image_from_url(url: str) -> Image.Image | None:
    """Fetch image from local path or HTTP URL. Cached."""
    if url in _IMAGE_CACHE:
        return _IMAGE_CACHE[url]
    try:
        if url.startswith(("http://", "https://")):
            r = httpx.get(url, timeout=30, follow_redirects=True)
            r.raise_for_status()
            img = Image.open(io.BytesIO(r.content)).convert("RGBA")
        elif url.startswith("file://"):
            img = Image.open(url.replace("file://", "")).convert("RGBA")
        else:
            img = Image.open(url).convert("RGBA")
        _IMAGE_CACHE[url] = img
        return img
    except Exception as e:
        print(f"  ⚠ could not load image {url}: {e}")
        return None


def _wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Word-wrap text to fit max_width pixels. Respects explicit \\n."""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words = paragraph.split(" ")
        current = ""
        for w in words:
            test = (current + " " + w).strip()
            bbox = font.getbbox(test)
            if bbox[2] - bbox[0] <= max_width or not current:
                current = test
            else:
                lines.append(current)
                current = w
        if current:
            lines.append(current)
    return lines


def _draw_text_with_ranges(
    draw: ImageDraw.ImageDraw,
    text: str,
    font: ImageFont.FreeTypeFont,
    x: int,
    y: int,
    base_color: tuple,
    ranges: list[dict] | None,
    line_height: int,
    align: str = "left",
    max_width: int | None = None,
    text_case: str = "sentence",
):
    """Draw text with optional per-character-range fills (accent words).

    Wraps to max_width if given. Handles \\n explicitly. Returns total height drawn.
    """
    if text_case == "UPPER":
        text = text.upper()
    elif text_case == "lower":
        text = text.lower()

    # Convert ranges char-positions to wrapped-line char-positions
    # Simplified: we wrap, but ranges still reference original text indices.
    # We'll iterate chars and track current position.
    if max_width:
        lines = _wrap_text(text, font, max_width)
    else:
        lines = text.split("\n")

    # If ranges are not provided, fast path
    if not ranges:
        cy = y
        for line in lines:
            if align == "center" and max_width:
                bbox = font.getbbox(line)
                lw = bbox[2] - bbox[0]
                draw.text((x + (max_width - lw) // 2, cy), line, font=font, fill=base_color)
            elif align == "right" and max_width:
                bbox = font.getbbox(line)
                lw = bbox[2] - bbox[0]
                draw.text((x + max_width - lw, cy), line, font=font, fill=base_color)
            else:
                draw.text((x, cy), line, font=font, fill=base_color)
            cy += line_height
        return cy - y

    # Slow path: char-by-char drawing with ranges (only for accented headlines)
    # Rebuild char position map across wrapped lines
    flat_chars: list[tuple[str, int]] = []  # (char, orig_idx)
    orig_idx = 0
    line_idx_map: list[int] = []  # index into flat_chars where each wrapped line starts

    # We need to map original char indices to wrapped line positions.
    # Easier: just iterate the original text once and break by lines based on _wrap_text output.
    # For simplicity and correctness on typical use cases, draw line by line ignoring exact range fidelity if wrapping changes positions.

    cy = y
    cursor_orig = 0
    for line in lines:
        cx = x
        for ch in line:
            # Find this char's original index (search forward from cursor)
            try:
                while cursor_orig < len(text) and text[cursor_orig] != ch:
                    cursor_orig += 1
            except IndexError:
                pass
            color = base_color
            for rng in ranges:
                if rng["start"] <= cursor_orig < rng["end"]:
                    color = _hex_to_rgb(rng["fill"])
                    break
            draw.text((cx, cy), ch, font=font, fill=color)
            bbox = font.getbbox(ch)
            cx += bbox[2] - bbox[0]
            cursor_orig += 1
        cy += line_height
        # Skip whitespace between wrapped lines
        while cursor_orig < len(text) and text[cursor_orig] in " \n":
            cursor_orig += 1

    return cy - y


def _draw_pill(
    draw: ImageDraw.ImageDraw,
    x: int, y: int,
    text: str,
    font: ImageFont.FreeTypeFont,
    bg_color: tuple,
    text_color: tuple,
    padding_x: int = 38,
    padding_y: int = 22,
    text_case: str = "UPPER",
) -> tuple[int, int]:
    """Draw a pill (rounded rectangle with text). Returns (width, height)."""
    label = text.upper() if text_case == "UPPER" else text
    bbox = font.getbbox(label)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    pill_w = tw + padding_x * 2
    pill_h = th + padding_y * 2
    radius = pill_h // 2

    # Pillow rounded_rectangle (Pillow ≥ 8.2)
    try:
        draw.rounded_rectangle((x, y, x + pill_w, y + pill_h), radius=radius, fill=bg_color)
    except Exception:
        # Manual fallback
        draw.rectangle((x + radius, y, x + pill_w - radius, y + pill_h), fill=bg_color)
        draw.ellipse((x, y, x + 2 * radius, y + 2 * radius), fill=bg_color)
        draw.ellipse((x + pill_w - 2 * radius, y, x + pill_w, y + 2 * radius), fill=bg_color)

    # Center text vertically (account for baseline)
    text_y = y + (pill_h - th) // 2 - bbox[1]
    draw.text((x + padding_x, text_y), label, font=font, fill=text_color)
    return pill_w, pill_h


class PNGAssembler:
    """Render layout-spec to PNG (entregável final) and JPEG (optional)."""

    def __init__(self, format: str = "png", quality: int = 92):
        if not _PIL_OK:
            raise ImportError("Pillow not installed. Run: pip install Pillow")
        self.format = format.lower()
        self.quality = quality

    def assemble(self, layout_spec: dict, image_urls: dict[str, str]) -> AssembleResult:
        import time
        t0 = time.time()
        warnings: list[str] = []

        frame = layout_spec["frame"]
        W, H = int(frame["width"]), int(frame["height"])

        # Background
        bg = frame["background"]
        if bg["type"] == "solid":
            canvas = Image.new("RGB", (W, H), _hex_to_rgb(bg["value"]))
        elif bg["type"] == "gradient":
            # Simple linear gradient fallback
            canvas = Image.new("RGB", (W, H), _hex_to_rgb(bg.get("value", "#0C161B")))
        else:
            canvas = Image.new("RGB", (W, H), (12, 22, 27))  # night-10 fallback

        draw = ImageDraw.Draw(canvas)

        elements = layout_spec.get("elements", [])
        # Draw image_slots first (backgrounds), then text/pill on top
        for layer in ("image_slot", "other"):
            for el in elements:
                etype = el.get("type")
                is_image = etype == "image_slot"
                if layer == "image_slot" and not is_image:
                    continue
                if layer == "other" and is_image:
                    continue
                try:
                    if etype == "text":
                        self._draw_text(canvas, draw, el)
                    elif etype == "image_slot":
                        self._draw_image(canvas, el, image_urls, warnings, W, H)
                    elif etype == "pill_cta":
                        self._draw_pill_cta(canvas, draw, el)
                    elif etype == "rect":
                        self._draw_rect(canvas, draw, el)
                    else:
                        warnings.append(f"unknown element type: {etype}")
                except Exception as e:
                    warnings.append(f"error on {etype}/{el.get('slot_name', '?')}: {e}")
        draw = ImageDraw.Draw(canvas)  # refresh draw after image pastes

        # Save
        out_dir = Path(os.getenv("ARTIFACTS_DIR", "./artifacts")) / "outputs"
        out_dir.mkdir(parents=True, exist_ok=True)
        model_id = layout_spec.get("model_id", "ad")
        ts = int(time.time())

        png_path = out_dir / f"{model_id}_{ts}.png"
        canvas.save(png_path, "PNG", optimize=True)

        jpeg_path = None
        if self.format == "jpeg" or self.format == "both":
            jpeg_path = out_dir / f"{model_id}_{ts}.jpg"
            # Re-flatten with white bg if needed (JPEG has no alpha)
            canvas.convert("RGB").save(jpeg_path, "JPEG", quality=self.quality, optimize=True)

        return AssembleResult(
            destination="png",
            png_path=str(png_path),
            jpeg_path=str(jpeg_path) if jpeg_path else None,
            elapsed_ms=int((time.time() - t0) * 1000),
            warnings=warnings,
        )

    def _draw_text(self, canvas, draw, el):
        font = _load_font(
            el["font"]["family"],
            el["font"]["style"],
            int(el["font"]["size"]),
        )
        line_height = int(el["font"]["size"] * (el["font"].get("line_height_pct", 120) / 100))
        max_w = el.get("width") if isinstance(el.get("width"), (int, float)) else None
        _draw_text_with_ranges(
            draw,
            el["text"],
            font,
            int(el["x"]),
            int(el["y"]),
            _hex_to_rgb(el["color"]),
            el.get("ranges"),
            line_height,
            align=el.get("align", "left"),
            max_width=int(max_w) if max_w else None,
            text_case=el["font"].get("text_case", "sentence"),
        )

    def _draw_image(self, canvas, el, image_urls, warnings, canvas_w=1080, canvas_h=1920):
        url = image_urls.get(el["slot_name"])
        if not url:
            warnings.append(f"no image for slot {el['slot_name']} — drawing placeholder")
            self._draw_placeholder_rect(canvas, el)
            return
        img = _load_image_from_url(url)
        if not img:
            warnings.append(f"image fetch failed for {el['slot_name']}")
            self._draw_placeholder_rect(canvas, el)
            return
        # fullbleed: stretch image to cover the entire canvas (used as background)
        placement = el.get("placement", "")
        slot_w = el.get("width") or 0
        slot_h = el.get("height") or 0
        auto_fullbleed = (int(slot_w) >= canvas_w) or (not slot_w and not slot_h)
        is_fullbleed = (
            el.get("fullbleed", False)
            or placement in ("fullbleed", "full-bleed", "background")
            or auto_fullbleed
        )
        if is_fullbleed:
            img = ImageOps.fit(img, (canvas_w, canvas_h), method=Image.LANCZOS, centering=(0.5, 0.3))
            paste_x, paste_y = 0, 0
            target_w, target_h = canvas_w, canvas_h
        else:
            target_w = int(el.get("width") or canvas_w)
            target_h = int(el.get("height") or canvas_h)
            img = ImageOps.fit(img, (target_w, target_h), method=Image.LANCZOS, centering=(0.5, 0.0))
            paste_x, paste_y = int(el.get("x", 0)), int(el.get("y", 0))

        # Corner radius opcional pra image_slot (mock-twitter card embed = 28px)
        corner_radius = int(el.get("corner_radius", 0))
        if corner_radius > 0:
            mask = Image.new("L", (target_w, target_h), 0)
            ImageDraw.Draw(mask).rounded_rectangle(
                (0, 0, target_w, target_h), radius=corner_radius, fill=255
            )
            rgba = img.convert("RGBA")
            rgba.putalpha(mask)
            img = rgba

        if img.mode == "RGBA":
            canvas.paste(img, (paste_x, paste_y), mask=img)
        else:
            canvas.paste(img, (paste_x, paste_y))

        # Apply gradient overlay (for text legibility on top of image)
        overlay_spec = el.get("overlay")
        if overlay_spec:
            self._apply_gradient_overlay(canvas, paste_x, paste_y, target_w, target_h, overlay_spec)

    def _apply_gradient_overlay(self, canvas, x: int, y: int, w: int, h: int, overlay_spec):
        """Draw gradient overlay on canvas above image area.

        overlay_spec can be a string like "gradient-fade-to-black-bottom-50%"
        OR a dict like {direction: "bottom", color: "#000000", extent_pct: 50}
        """
        import re
        # Parse string spec
        if isinstance(overlay_spec, str):
            s = overlay_spec.lower()
            if "none" in s or not s:
                return
            if "gradient" not in s and "fade" not in s:
                return
            direction = "bottom"
            for d in ("top", "bottom", "left", "right"):
                if d in s:
                    direction = d
                    break
            m = re.search(r"(\d+)%", s)
            extent_pct = int(m.group(1)) if m else 50
            # Color: default black, accept "to-black" / "to-white" hints
            color = "#FFFFFF" if "to-white" in s else "#000000"
            spec = {"direction": direction, "color": color, "extent_pct": extent_pct}
        elif isinstance(overlay_spec, dict):
            spec = overlay_spec
        else:
            return

        direction = spec.get("direction", "bottom")
        color_rgb = _hex_to_rgb(spec.get("color", "#000000"))
        extent_pct = spec.get("extent_pct", 50) / 100.0

        # Build alpha gradient as L-mode image and composite a solid color via the alpha mask
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ovd = ImageDraw.Draw(overlay)

        if direction == "bottom":
            zone_h = int(h * extent_pct)
            zone_start = h - zone_h
            for i in range(zone_start, h):
                progress = (i - zone_start) / max(1, zone_h - 1)
                # Ease-in for darker contrast at the very bottom
                alpha = int(255 * (progress ** 1.15))
                ovd.line([(0, i), (w, i)], fill=(*color_rgb, min(255, alpha)))
        elif direction == "top":
            zone_h = int(h * extent_pct)
            for i in range(0, zone_h):
                progress = 1 - (i / max(1, zone_h - 1))
                alpha = int(255 * (progress ** 1.15))
                ovd.line([(0, i), (w, i)], fill=(*color_rgb, min(255, alpha)))
        elif direction == "right":
            zone_w = int(w * extent_pct)
            zone_start = w - zone_w
            for i in range(zone_start, w):
                progress = (i - zone_start) / max(1, zone_w - 1)
                alpha = int(255 * (progress ** 1.15))
                ovd.line([(i, 0), (i, h)], fill=(*color_rgb, min(255, alpha)))
        elif direction == "left":
            zone_w = int(w * extent_pct)
            for i in range(0, zone_w):
                progress = 1 - (i / max(1, zone_w - 1))
                alpha = int(255 * (progress ** 1.15))
                ovd.line([(i, 0), (i, h)], fill=(*color_rgb, min(255, alpha)))

        canvas.paste(overlay, (x, y), mask=overlay)

    def _draw_placeholder_rect(self, canvas, el):
        from PIL import ImageDraw as _ID
        d = _ID.Draw(canvas)
        x, y, w, h = int(el["x"]), int(el["y"]), int(el["width"]), int(el["height"])
        d.rectangle((x, y, x + w, y + h), fill=(19, 31, 37), outline=(255, 190, 24), width=3)
        # Center label
        try:
            f = _load_font("Inter", "Bold", 18)
            label = f"[ {el['slot_name'].upper()} ]"
            bbox = f.getbbox(label)
            tw = bbox[2] - bbox[0]
            d.text((x + (w - tw) // 2, y + h // 2 - 12), label, font=f, fill=(255, 190, 24))
        except Exception:
            pass

    def _draw_rect(self, canvas, draw, el):
        """Draw a filled rectangle (used for yellow_container, yellow_band, etc.)"""
        x, y = int(el.get("x", 0)), int(el.get("y", 0))
        w, h = int(el.get("width", 100)), int(el.get("height", 100))
        fill = _hex_to_rgb(el.get("fill", "#FFBE18"))
        radius = int(el.get("corner_radius", 0))
        if radius > 0:
            try:
                draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill)
            except Exception:
                draw.rectangle((x, y, x + w, y + h), fill=fill)
        else:
            draw.rectangle((x, y, x + w, y + h), fill=fill)

    def _draw_pill_cta(self, canvas, draw, el):
        font = _load_font(
            el["font"]["family"],
            el["font"]["style"],
            int(el["font"]["size"]),
        )
        _draw_pill(
            draw,
            int(el["x"]), int(el["y"]),
            el["text"],
            font,
            _hex_to_rgb(el["background"]),
            _hex_to_rgb(el["text_color"]),
            padding_x=int(el.get("padding_x", 38)),
            padding_y=int(el.get("padding_y", 22)),
            text_case=el["font"].get("text_case", "UPPER"),
        )


class HTMLAssembler:
    """Optional HTML side-output for inspection/debug. Not the main deliverable."""

    def assemble(self, layout_spec: dict, image_urls: dict[str, str]) -> AssembleResult:
        # ... (HTML rendering retained for debug) ...
        # Implementation in legacy assembler — kept minimal here
        out_dir = Path(os.getenv("ARTIFACTS_DIR", "./artifacts")) / "outputs"
        out_dir.mkdir(parents=True, exist_ok=True)
        model_id = layout_spec.get("model_id", "ad")
        path = out_dir / f"{model_id}_debug.html"
        # Simple HTML for debug
        frame = layout_spec["frame"]
        bg = frame["background"]["value"]
        html = f"<html><body style='margin:0'><div style='width:{frame['width']}px;height:{frame['height']}px;background:{bg};color:#fff;font-family:system-ui'>"
        html += f"<pre>{json.dumps(layout_spec, ensure_ascii=False, indent=2)[:2000]}</pre></div></body></html>"
        path.write_text(html, encoding="utf-8")
        return AssembleResult(destination="html", html_path=str(path), elapsed_ms=10)


class AssemblerAdapter:
    """Unified entry point. Default = PNG. Other options for debug/Figma."""

    def __init__(self, destination: str | None = None, format: str | None = None):
        self.destination = (destination or os.getenv("ASSEMBLER", "png")).lower()
        self.format = (format or os.getenv("OUTPUT_FORMAT", "png")).lower()

        if self.destination == "png" or self.destination == "jpeg":
            self.backend = PNGAssembler(format=self.format if self.destination == "png" else "jpeg")
        elif self.destination == "html":
            self.backend = HTMLAssembler()
        elif self.destination == "figma":
            # Legacy stub
            self.backend = HTMLAssembler()  # falls back to HTML for now
        else:
            raise ValueError(f"Unknown assembler destination: {self.destination}")

    def assemble(self, layout_spec: dict, image_urls: dict[str, str]) -> AssembleResult:
        return self.backend.assemble(layout_spec, image_urls)
