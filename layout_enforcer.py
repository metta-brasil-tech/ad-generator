"""Layout enforcer — pós-processa layout-spec do LLM pra garantir conformidade com YAML do estilo.

Problema que resolve: LLM (especialmente modelos baratos) frequentemente esquece
de incluir image_slot, ou usa frame size errado, ou omite background. Enforcer
corrige automaticamente baseado no model YAML.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml


def load_model_yaml(model_id: str, knowledge_path: str | None = None) -> dict | None:
    """Load the YAML spec for a given model_id. Tolerates LLM hallucinations.

    Lookup order:
      1. exact id match
      2. alias array case-insensitive
      3. prefix match (model_id IS prefix of YAML id, e.g. "C" → "C-tipografia-pura-dark")
      4. first-segment match (LLM hybrid like "B-light-provocador" → "B" → B-foto-top-headline-mixed)
    """
    kp = Path(knowledge_path or os.getenv("BRAND_KNOWLEDGE_PATH", "./brand-knowledge"))
    candidates = list((kp / "models").glob("*.yaml"))
    model_id_lc = model_id.lower().strip()
    # Get the FIRST SEGMENT before "-" — handles hybrids like "B-something" → "B"
    first_segment = model_id_lc.split("-", 1)[0]

    all_models = []
    for path in candidates:
        if path.name.startswith("_"):
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not data:
                continue
            all_models.append(data)
        except Exception:
            continue

    # 1) Exact id match
    for data in all_models:
        if data.get("id") == model_id:
            return data

    # 2) Alias match
    for data in all_models:
        aliases = data.get("alias", []) or []
        if any(a.lower() == model_id_lc for a in aliases):
            return data

    # 3) Prefix match: model_id is a prefix of yaml.id
    for data in all_models:
        file_id = data.get("id", "").lower()
        if file_id.startswith(model_id_lc + "-") or file_id == model_id_lc:
            return data

    # 4) First-segment match: yaml.id starts with first_segment
    for data in all_models:
        file_id = data.get("id", "").lower()
        if file_id.startswith(first_segment + "-") or file_id == first_segment:
            return data
        # Also try aliases starting with first_segment
        aliases = data.get("alias", []) or []
        if any(a.lower() == first_segment for a in aliases):
            return data

    return None


def _format_to_dimensions(formato: str) -> tuple[int, int]:
    """Map formato string to (width, height) pixels."""
    mapping = {
        "STORY": (1080, 1920),
        "story": (1080, 1920),
        "story_video": (1080, 1920),
        "FEED": (1080, 1350),
        "feed": (1080, 1350),
        "feed_video": (1080, 1350),
        "SQR": (1080, 1080),
        "sqr": (1080, 1080),
        "CARROSSEL": (1080, 1080),
        "carrossel": (1080, 1080),
    }
    return mapping.get(formato, (1080, 1920))


def _resolve_color_token(token: str, model_yaml: dict) -> str:
    """Resolve color tokens like 'var(--metta-...)' to hex."""
    if not token:
        return "#0C161B"
    if token.startswith("#"):
        return token
    # Common token map
    token_map = {
        "var(--metta-sys-color-primary)": "#FFBE18",
        "var(--metta-ref-palette-yellow-50)": "#FFBE18",
        "var(--metta-ref-palette-yellow-55)": "#FFB618",
        "var(--metta-ref-palette-night-10)": "#0C161B",
        "var(--metta-ref-palette-night-5)": "#0A1013",
        "var(--metta-ref-palette-night-100)": "#FFFFFF",
        "var(--metta-ref-palette-night-95)": "#EBF3F7",
        "var(--metta-ref-palette-night-85)": "#B0CAD8",
        "var(--metta-ref-palette-night-40)": "#435965",
        "var(--metta-sys-color-on-primary)": "#0C161B",
        "var(--metta-sys-color-surface)": "#0C161B",
    }
    return token_map.get(token, "#0C161B")


def enforce(layout_spec: dict, briefing: dict, knowledge_path: str | None = None) -> tuple[dict, list[str]]:
    """Enforce model YAML constraints on the LLM-generated layout-spec.

    Authoritative source: model YAML. LLM-suggested values lose to YAML defaults
    when they conflict (e.g., off-palette colors are snapped to YAML colors).

    Returns (corrected_layout, log_messages).
    """
    log: list[str] = []
    model_id = layout_spec.get("model_id", "")
    model = load_model_yaml(model_id, knowledge_path)
    if not model:
        log.append(f"WARN: no YAML found for model_id={model_id}, skipping enforcement")
        return layout_spec, log

    # Resolve all canonical colors from YAML once
    yaml_colors = model.get("colors", {})
    bg_authoritative = _resolve_color_token(yaml_colors.get("bg_primary", "#0C161B"), model)
    fg_authoritative = _resolve_color_token(yaml_colors.get("fg_primary", "#FFFFFF"), model)
    body_authoritative = _resolve_color_token(yaml_colors.get("body_text", fg_authoritative), model)
    accent_authoritative = _resolve_color_token(yaml_colors.get("accent", "#FFBE18"), model)
    cta_bg_auth = _resolve_color_token(yaml_colors.get("cta_bg", accent_authoritative), model)
    cta_text_auth = _resolve_color_token(yaml_colors.get("cta_text", bg_authoritative), model)

    # 1) FRAME — force size + bg
    formato = briefing.get("formato", model.get("formato", "story"))
    target_w, target_h = _format_to_dimensions(formato)
    frame = layout_spec.setdefault("frame", {})
    cur_w, cur_h = frame.get("width", 0), frame.get("height", 0)
    if (cur_w, cur_h) != (target_w, target_h):
        log.append(f"FIX: frame {cur_w}x{cur_h} -> {target_w}x{target_h}")
        frame["width"], frame["height"] = target_w, target_h

    cur_bg = (frame.get("background") or {}).get("value", "")
    if cur_bg != bg_authoritative:
        log.append(f"FIX: bg {cur_bg or '(none)'} -> {bg_authoritative} (from YAML)")
        frame["background"] = {"type": "solid", "value": bg_authoritative}

    elements = layout_spec.setdefault("elements", [])

    # 2) IMAGE_SLOT — inject if YAML says required but layout missing
    has_image_slot = any(e.get("type") == "image_slot" for e in elements)
    image_cfg = model.get("image", {})
    image_required = image_cfg.get("required", False)

    if image_required and not has_image_slot:
        slot = _default_image_slot(model, target_w, target_h)
        elements.append(slot)
        log.append(f"FIX: injected missing image_slot (placement={image_cfg.get('placement', 'auto')})")

    # 2b) Attach gradient overlay spec from YAML to image_slot (so assembler renders it)
    image_overlay = image_cfg.get("filters", {}).get("overlay", "") if image_cfg else ""
    if image_overlay and image_overlay.lower() not in ("none", ""):
        for el in elements:
            if el.get("type") == "image_slot" and not el.get("overlay"):
                el["overlay"] = image_overlay
                log.append(f"FIX: applied YAML overlay '{image_overlay}' to {el.get('slot_name')}")

    # 2c) Force image_slot dimensions from YAML placement (LLM often picks wrong size)
    placement = (image_cfg.get("placement") or "").lower() if image_cfg else ""
    for el in elements:
        if el.get("type") != "image_slot":
            continue
        # Compute target dims from placement
        target_slot = _default_image_slot(model, target_w, target_h)
        # Override only if LLM's dims diverge significantly from YAML intent
        cur_x, cur_y = el.get("x", 0), el.get("y", 0)
        cur_w, cur_h = el.get("width", 0), el.get("height", 0)
        target_x, target_y = target_slot["x"], target_slot["y"]
        tgt_w, tgt_h = target_slot["width"], target_slot["height"]
        if "full-bleed" in placement:
            # Force 100% canvas coverage
            if (cur_x, cur_y, cur_w, cur_h) != (0, 0, target_w, target_h):
                log.append(f"FIX: image_slot {cur_x},{cur_y} {cur_w}x{cur_h} -> 0,0 {target_w}x{target_h} (full-bleed)")
                el["x"], el["y"], el["width"], el["height"] = 0, 0, target_w, target_h
        elif "top" in placement and "bleed" in placement:
            if cur_y != 0 or cur_w < target_w * 0.8:
                log.append(f"FIX: image_slot top-bleed -> 0,0 {target_w}x{tgt_h}")
                el["x"], el["y"], el["width"], el["height"] = 0, 0, target_w, tgt_h
        elif placement and (cur_w < tgt_w * 0.5 or cur_h < tgt_h * 0.5):
            # LLM picked tiny slot — replace with YAML default
            log.append(f"FIX: image_slot too small {cur_w}x{cur_h} -> {tgt_w}x{tgt_h} ({placement})")
            el.update({k: target_slot[k] for k in ("x", "y", "width", "height")})

    # 3a) TYPOGRAPHY ENFORCEMENT — overwrite font from YAML's typography spec
    typo = model.get("typography", {})

    def _resolve_role(slot_name: str) -> dict | None:
        """Map slot_name → YAML typography role."""
        if slot_name == "headline":
            return typo.get("headline")
        if slot_name == "body":
            return typo.get("body")
        if slot_name in ("tag", "tag_eyebrow"):
            return typo.get("tag_eyebrow") or typo.get("eyebrow")
        if slot_name == "cta":
            return typo.get("cta")
        return None

    for el in elements:
        slot = el.get("slot_name", "")
        role = _resolve_role(slot)
        if role and el.get("type") in ("text", "pill_cta"):
            cur_font = el.get("font", {}) or {}
            cur_family = cur_font.get("family", "")
            cur_style = cur_font.get("style", "")

            # Force family to YAML's specified family (default SF Pro)
            yaml_family = role.get("family", "SF Pro")
            if cur_family != yaml_family:
                log.append(f"FIX: {slot} font family '{cur_family}' -> '{yaml_family}'")
                cur_font["family"] = yaml_family

            # Force style to YAML's specified style (e.g., "Expanded Heavy")
            yaml_style = role.get("style", "")
            if yaml_style and cur_style != yaml_style:
                log.append(f"FIX: {slot} font style '{cur_style}' -> '{yaml_style}'")
                cur_font["style"] = yaml_style

            # Force size to be within YAML range AND fit the actual text
            yaml_size_range = role.get("size_range") or [16, 200]
            cur_size = cur_font.get("size", 0)
            text_content = el.get("text", "")

            # Find slot config (max_lines from YAML slots)
            yaml_slot_cfg = next((s for s in model.get("slots", []) if s.get("name") == slot), {})
            yaml_max_chars = yaml_slot_cfg.get("max_chars") or 999
            max_lines = yaml_slot_cfg.get("max_lines") or 4
            available_w = (el.get("width") if isinstance(el.get("width"), (int, float)) else (target_w - 160))

            # Detect style-content mismatch: text WAY longer than YAML expects
            text_len = len(text_content)
            mismatch = text_len > yaml_max_chars * 2.5  # 2.5x tolerance

            # Semantic fallback ranges (used when YAML range doesn't fit the actual text)
            # These keep impact + readability for typical story 1080×1920
            SEMANTIC_RANGES = {
                "headline": [56, 84],    # impactful but readable
                "body":     [24, 32],
                "tag":      [18, 22],
                "tag_eyebrow": [18, 22],
                "cta":      [22, 28],
            }
            SEMANTIC_MAX_LINES = {"headline": 5, "body": 4, "tag": 1, "tag_eyebrow": 1, "cta": 1}

            if mismatch:
                size_range = SEMANTIC_RANGES.get(slot, yaml_size_range)
                max_lines = SEMANTIC_MAX_LINES.get(slot, max_lines)
                log.append(f"INFO: style-content mismatch on {slot} (text {text_len} chars >> YAML max_chars {yaml_max_chars}). Using semantic range {size_range[0]}-{size_range[1]} / max_lines {max_lines}")
            else:
                size_range = yaml_size_range

            # Char-width factor depends on style (Expanded is wider)
            cw_factor = 0.72 if "Expanded" in yaml_style and any(k in yaml_style for k in ["Heavy", "Bold"]) else (0.65 if "Expanded" in yaml_style else 0.55)

            # Compute MAX size that lets the text fit in max_lines
            _ml = max_lines  # snapshot to avoid closure issues
            _aw = available_w
            _cwf = cw_factor
            _txt = text_content

            def _fits_in_lines(test_size: int, ml=_ml, aw=_aw, cwf=_cwf, txt=_txt) -> bool:
                cpl = max(4, int(aw / (test_size * cwf)))
                total_lines = 0
                for line in txt.split("\n"):
                    if not line:
                        total_lines += 1
                        continue
                    total_lines += max(1, -(-len(line) // cpl))
                return total_lines <= ml

            # Search: start from YAML max, shrink until it fits
            best_size = None
            for candidate in range(size_range[1], size_range[0] - 1, -4):
                if _fits_in_lines(candidate):
                    best_size = candidate
                    break

            if best_size is None:
                # YAML range too big for text. Go below min size (but not below readable floor).
                readable_floor = SEMANTIC_RANGES.get(slot, [16, 200])[0]
                for candidate in range(size_range[0] - 4, readable_floor - 1, -2):
                    if _fits_in_lines(candidate):
                        best_size = candidate
                        break
                if best_size is None:
                    # Text doesn't fit even at readable floor — keep readable size, will overflow lines
                    best_size = readable_floor
                    log.append(f"WARN: {slot} text overflows max_lines at readable floor {best_size}px (text wraps to more lines than expected)")

            if cur_size != best_size:
                log.append(f"FIX: {slot} font size {cur_size} -> {best_size} (fit '{text_content[:30]}...' in {max_lines}L · range {size_range[0]}-{size_range[1]})")
                cur_font["size"] = best_size

            # Overwrite typography props from YAML role (not just fill missing)
            for prop in ("line_height_pct", "letter_spacing_pct", "text_case", "weight", "stretch_pct"):
                if prop in role:
                    if cur_font.get(prop) != role[prop]:
                        log.append(f"FIX: {slot} font.{prop} {cur_font.get(prop)} -> {role[prop]}")
                    cur_font[prop] = role[prop]

            el["font"] = cur_font

    # 3b) COLOR ENFORCEMENT — force role-based color per YAML (unconditional override)
    for el in elements:
        slot = el.get("slot_name", "")
        if el.get("type") == "text":
            # Force role-based color from YAML (LLM choice is overridden)
            if slot == "headline":
                expected = fg_authoritative
            elif slot == "body":
                expected = body_authoritative
            elif slot in ("tag", "tag_eyebrow"):
                expected = body_authoritative
            else:
                expected = fg_authoritative
            cur = el.get("color", "")
            if cur != expected:
                log.append(f"FIX: {slot} color {cur or '(none)'} -> {expected} (YAML role)")
                el["color"] = expected
            # Snap ranges to accent if any
            for rng in el.get("ranges", []) or []:
                if rng.get("fill", "") != accent_authoritative:
                    rng["fill"] = accent_authoritative

        elif el.get("type") == "pill_cta":
            cur_bg_pill = el.get("background", "")
            cur_text_pill = el.get("text_color", "")
            if cur_bg_pill != cta_bg_auth:
                log.append(f"FIX: CTA bg {cur_bg_pill} -> {cta_bg_auth}")
                el["background"] = cta_bg_auth
            if cur_text_pill != cta_text_auth:
                log.append(f"FIX: CTA text {cur_text_pill} -> {cta_text_auth}")
                el["text_color"] = cta_text_auth

    # 3c) CTA language normalization — fix PT/ES typos from LLM
    CTA_LANG_FIXES = {
        # Spanish leak → PT-BR
        "INSCRIBIR-SE": "INSCREVER-SE",
        "INSCRIBIRSE": "INSCREVER-SE",
        "INSCRÍBIR-SE": "INSCREVER-SE",
        "REGISTRAR-SE": "CADASTRAR-SE",
        "DESCUBRIR": "DESCUBRA",
        "APRENDER MÁS": "SAIBA MAIS",
        "APRENDER MAS": "SAIBA MAIS",
        "PARTICIPAR AHORA": "PARTICIPAR AGORA",
        "ENVIAR AHORA": "ENVIAR AGORA",
        # Anglicisms
        "SIGN UP": "INSCREVER-SE",
        "LEARN MORE": "SAIBA MAIS",
        "BUY NOW": "COMPRAR AGORA",
        "GET STARTED": "COMECE AGORA",
    }
    for el in elements:
        if el.get("type") == "pill_cta":
            t = (el.get("text") or "").strip().upper()
            if t in CTA_LANG_FIXES:
                fixed = CTA_LANG_FIXES[t]
                log.append(f"FIX: CTA text '{el['text']}' -> '{fixed}' (PT-BR normalization)")
                el["text"] = fixed

    # 3d) YELLOW-BLOCO container injection — yellow rect behind headline+bullets
    yaml_id = (model.get("id") or "").lower()
    is_yellow_bloco = "yellow-bloco" in yaml_id or "yellow_bloco" in yaml_id
    has_yellow_rect = any(e.get("type") == "rect" and e.get("role") == "yellow_container" for e in elements)
    if is_yellow_bloco and not has_yellow_rect:
        # Yellow rect occupies left 60% of canvas, vertically centered (~ y 400-1500)
        rect_x, rect_y = 60, 380
        rect_w, rect_h = int(target_w * 0.65), 1100
        elements.append({
            "type": "rect",
            "role": "yellow_container",
            "x": rect_x, "y": rect_y,
            "width": rect_w, "height": rect_h,
            "fill": accent_authoritative,
            "corner_radius": 24,
        })
        log.append(f"FIX: injected YELLOW-BLOCO yellow container rect ({rect_x},{rect_y}) {rect_w}x{rect_h}")

    # 3e) Yellow band divider — for styles with ornament:"yellow-band-divider" (e.g., K)
    yaml_ornament = (model.get("composicao", {}).get("ornament") or "").lower()
    has_yellow_band = any(e.get("type") == "rect" and e.get("role") == "yellow_band" for e in elements)
    if "yellow-band-divider" in yaml_ornament and not has_yellow_band:
        # Inserted between headline and body — assembler positions it by sequencing
        elements.append({
            "type": "rect",
            "role": "yellow_band",
            "x": 80, "y": 0,  # y set by tight_block placement
            "width": 120, "height": 6,
            "fill": accent_authoritative,
            "corner_radius": 3,
        })
        log.append(f"FIX: injected yellow-band divider")

    # 4) TIGHT BLOCK POSITIONING — group h1+h2+body+CTA close together in computed text zone
    image_slots = [e for e in elements if e.get("type") == "image_slot"]
    primary_image = image_slots[0] if image_slots else None

    text_zone = _compute_text_zone(model, target_w, target_h, primary_image, image_cfg)
    log.append(f"INFO: text_zone x={text_zone['x']} y={text_zone['y']} w={text_zone['w']} h={text_zone['h']} align={text_zone['align']}")

    _layout_tight_block(elements, text_zone, log, target_w)

    # Z-ORDER: image_slots (bg) → rects (mid) → text/pills (top)
    images_z = [e for e in elements if e.get("type") == "image_slot"]
    rects_z = [e for e in elements if e.get("type") == "rect"]
    text_z = [e for e in elements if e.get("type") in ("text", "pill_cta")]
    others = [e for e in elements if e.get("type") not in ("image_slot", "rect", "text", "pill_cta")]
    new_order = images_z + rects_z + text_z + others
    if new_order != elements:
        log.append(f"FIX: z-stack — images({len(images_z)}) + rects({len(rects_z)}) + text({len(text_z)})")
        layout_spec["elements"] = new_order

    return layout_spec, log


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#") if h.startswith("#") else h
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return (0, 0, 0)
    try:
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return (0, 0, 0)


def _luminance(rgb: tuple[int, int, int]) -> float:
    r, g, b = [c / 255 for c in rgb]
    return 0.299 * r + 0.587 * g + 0.114 * b


def _luminance_distance(c1: str, c2: str) -> float:
    if not c1 or not c2:
        return 1.0
    l1, l2 = _luminance(_hex_to_rgb(c1)), _luminance(_hex_to_rgb(c2))
    return abs(l1 - l2)


def _looks_offbrand(color: str, palette: list[str]) -> bool:
    """Returns True if color is far from any palette color."""
    if not color or color.startswith("var("):
        return True
    target = _hex_to_rgb(color)
    for p in palette:
        pr = _hex_to_rgb(p)
        dist = sum(abs(a - b) for a, b in zip(target, pr)) / 3
        if dist < 30:
            return False
    return True


def _compute_text_zone(model: dict, target_w: int, target_h: int, image_slot: dict | None, image_cfg: dict) -> dict:
    """Compute where the text block (h1+h2+body+CTA) should live, based on image placement.

    Returns dict: {x, y, w, h, align}
      align ∈ {"top", "center", "bottom"}: where in the zone to anchor the block.
    """
    margin_x = 80
    margin_top = 120
    margin_bot = 120

    if not image_slot:
        # No image — text fills the canvas, top-aligned
        return {
            "x": margin_x, "y": margin_top,
            "w": target_w - 2 * margin_x,
            "h": target_h - margin_top - margin_bot,
            "align": "top",
        }

    placement = (image_cfg.get("placement") or "").lower()
    img_x, img_y = image_slot["x"], image_slot["y"]
    img_w, img_h = image_slot["width"], image_slot["height"]

    # Full bleed (image covers nearly whole canvas) — text in bottom 38%
    is_full_bleed = (img_y <= 80 and img_h >= target_h * 0.75 and img_w >= target_w * 0.85)
    is_top = img_y <= 80 and img_w >= target_w * 0.7 and img_h < target_h * 0.6
    is_bottom = (img_y >= target_h * 0.4 and img_y + img_h >= target_h - 100)
    is_right_or_corner = img_x >= target_w * 0.35 and img_w < target_w * 0.85

    if is_full_bleed or "full-bleed" in placement:
        text_top = int(target_h * 0.62)
        return {
            "x": margin_x, "y": text_top,
            "w": target_w - 2 * margin_x,
            "h": target_h - text_top - margin_bot,
            "align": "bottom",
        }
    if is_bottom or "bottom" in placement:
        # Text above image
        return {
            "x": margin_x, "y": margin_top,
            "w": target_w - 2 * margin_x,
            "h": img_y - margin_top - 40,
            "align": "top",
        }
    if is_top or "top" in placement:
        # Text below image, tight to it
        text_top = img_y + img_h + 60
        return {
            "x": margin_x, "y": text_top,
            "w": target_w - 2 * margin_x,
            "h": target_h - text_top - margin_bot,
            "align": "top",
        }
    if is_right_or_corner or "right" in placement or "corner" in placement:
        # Text on the left, image bleeds right
        text_right = img_x - 30
        return {
            "x": margin_x, "y": margin_top,
            "w": text_right - margin_x,
            "h": target_h - margin_top - margin_bot,
            "align": "top",
        }
    # Default — top
    return {
        "x": margin_x, "y": margin_top,
        "w": target_w - 2 * margin_x,
        "h": target_h - margin_top - margin_bot,
        "align": "top",
    }


def _estimate_element_height(el: dict, zone_width: int) -> int:
    """Estimate rendered height of a text or pill element."""
    if el.get("type") == "pill_cta":
        font = el.get("font", {})
        size = font.get("size", 24)
        padding_y = el.get("padding_y", 22)
        return int(size * 1.0 + padding_y * 2 + 4)  # text + 2*padding + small fudge
    if el.get("type") == "text":
        font = el.get("font", {})
        size = font.get("size", 28)
        lh_pct = font.get("line_height_pct", 120)
        style = font.get("style", "")
        # Char-width factor — Expanded glyphs are wider, Heavy/Bold add to it
        if "Expanded" in style and any(k in style for k in ["Heavy", "Bold"]):
            cw = 0.78
        elif "Expanded" in style:
            cw = 0.70
        elif any(k in style for k in ["Heavy", "Bold", "Black"]):
            cw = 0.62
        else:
            cw = 0.55
        cpl = max(6, int(zone_width / (size * cw)))
        txt = el.get("text", "")
        wrapped = 0
        for line in txt.split("\n"):
            wrapped += max(1, -(-len(line) // cpl)) if line else 1
        # Pillow renders ascenders/descenders adding ~30-40% on top of nominal size
        line_h = size * max(lh_pct / 100, 1.0)
        return int(line_h * wrapped * 1.30)
    return 60


def _layout_tight_block(elements: list, text_zone: dict, log: list, target_w: int):
    """Stack text + CTA tightly within text_zone with the alignment direction.

    Also positions yellow_band divider between headline and body if present.
    """
    role_order = {"tag": 0, "tag_eyebrow": 0, "headline": 1, "body": 2, "cta": 3}

    block_items = [e for e in elements if e.get("type") in ("text", "pill_cta")]
    yellow_band = next((e for e in elements if e.get("type") == "rect" and e.get("role") == "yellow_band"), None)
    if not block_items:
        return

    def _sort_key(el):
        slot = el.get("slot_name", "")
        if el.get("type") == "pill_cta":
            return (3, el.get("y", 9999))
        return (role_order.get(slot, 2), el.get("y", 0))

    block_items.sort(key=_sort_key)

    # Compute heights and gaps
    heights = []
    gaps = []
    for i, el in enumerate(block_items):
        h = _estimate_element_height(el, text_zone["w"])
        heights.append(h)
        # Gaps: tag→headline 32, headline→body 40, body→CTA 56, before CTA when no body 48
        if i < len(block_items) - 1:
            cur = el.get("slot_name", "")
            nxt = block_items[i + 1]
            nxt_slot = nxt.get("slot_name", "")
            nxt_is_cta = nxt.get("type") == "pill_cta"
            if cur in ("tag", "tag_eyebrow") and nxt_slot == "headline":
                gaps.append(36)
            elif cur == "headline" and nxt_slot == "body":
                gaps.append(40)
            elif cur == "headline" and nxt_is_cta:
                gaps.append(56)
            elif cur == "body" and nxt_is_cta:
                gaps.append(56)
            else:
                gaps.append(32)
        else:
            gaps.append(0)

    total_h = sum(heights) + sum(gaps)

    # Position block based on alignment
    if text_zone["align"] == "bottom":
        cursor_y = text_zone["y"] + text_zone["h"] - total_h
    elif text_zone["align"] == "center":
        cursor_y = text_zone["y"] + max(0, (text_zone["h"] - total_h) // 2)
    else:  # top
        cursor_y = text_zone["y"]

    # Ensure block doesn't overflow canvas top
    cursor_y = max(cursor_y, 80)

    # Place each element + insert yellow_band between headline and body
    for i, el in enumerate(block_items):
        new_x = text_zone["x"]
        new_y = int(cursor_y)
        if el.get("x") != new_x:
            el["x"] = new_x
        if el.get("y") != new_y:
            log.append(f"FIX: {el.get('slot_name')} pos -> ({new_x}, {new_y}) [h={heights[i]}]")
            el["y"] = new_y
        if el.get("type") == "text":
            el["width"] = text_zone["w"]
        cursor_y += heights[i] + gaps[i]

        # If this was the headline and we have a yellow_band, insert it after with extra gap
        if yellow_band and el.get("slot_name") == "headline":
            yellow_band["x"] = text_zone["x"]
            yellow_band["y"] = int(cursor_y - 16)  # tight after headline
            cursor_y += yellow_band.get("height", 6) + 24
            log.append(f"FIX: yellow_band positioned at y={yellow_band['y']}")


def _default_image_slot(model: dict, frame_w: int, frame_h: int) -> dict:
    """Generate a reasonable default image_slot based on model's image placement.

    Uses YAML's `composicao.proporcao.image_area` (e.g. "30-35%") when available.
    """
    placement = (model.get("image", {}).get("placement") or "right-bleed").lower()
    image_prompt_ref = model.get("image", {}).get("prompt_template_ref", "")
    slot_name = "photo" if "photo" in model.get("image", {}).get("type", "") or model.get("image", {}).get("type") in ("photo-editorial", "photo") else "image"

    # Try to read image_area % from YAML
    image_area_pct = 0.35  # default
    prop_str = model.get("composicao", {}).get("proporcao", {}).get("image_area", "")
    if prop_str:
        # Parse "30-35%" or "60-70%" — take the average
        import re
        nums = re.findall(r"(\d+)", prop_str)
        if len(nums) >= 2:
            image_area_pct = (int(nums[0]) + int(nums[1])) / 200  # avg / 100
        elif len(nums) == 1:
            image_area_pct = int(nums[0]) / 100

    if "full-bleed" in placement:
        slot = {"x": 0, "y": 0, "width": frame_w, "height": frame_h, "scale_mode": "FILL"}
    elif "top" in placement:
        h = max(400, int(frame_h * image_area_pct))
        slot = {"x": 0, "y": 0, "width": frame_w, "height": h}
    elif "right" in placement or "corner" in placement:
        slot = {"x": int(frame_w * 0.50), "y": int(frame_h * 0.40), "width": int(frame_w * 0.55), "height": int(frame_h * 0.50), "bleed_right": True}
    elif "bottom" in placement:
        h = max(400, int(frame_h * image_area_pct))
        slot = {"x": 0, "y": frame_h - h, "width": frame_w, "height": h}
    elif "center" in placement:
        h = max(400, int(frame_h * image_area_pct))
        slot = {"x": int(frame_w * 0.1), "y": int(frame_h * 0.20), "width": int(frame_w * 0.8), "height": h}
    else:
        slot = {"x": int(frame_w * 0.45), "y": int(frame_h * 0.35), "width": int(frame_w * 0.6), "height": int(frame_h * 0.50), "bleed_right": True}

    slot.update({
        "type": "image_slot",
        "slot_name": slot_name,
        "image_prompt_ref": image_prompt_ref,
        "url_placeholder": "pending",
    })
    return slot
