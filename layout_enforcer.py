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
    """Load the YAML spec for a given model_id. Matches against `id` and `alias` array."""
    kp = Path(knowledge_path or os.getenv("BRAND_KNOWLEDGE_PATH", "../../brand-knowledge"))
    candidates = list((kp / "models").glob("*.yaml"))
    model_id_lc = model_id.lower().strip()
    for path in candidates:
        if path.name.startswith("_"):
            continue
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if not data:
                continue
            if data.get("id") == model_id:
                return data
            # Match against aliases (case-insensitive)
            aliases = data.get("alias", []) or []
            if any(a.lower() == model_id_lc for a in aliases):
                return data
            # Fallback: match if model_id is a prefix of id (e.g., "C" matches "C-tipografia-pura-dark")
            file_id = data.get("id", "")
            if file_id.lower().startswith(model_id_lc + "-") or file_id.lower() == model_id_lc:
                return data
        except Exception:
            continue
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

    # 3b) COLOR ENFORCEMENT — snap text/cta colors to YAML palette
    for el in elements:
        slot = el.get("slot_name", "")
        if el.get("type") == "text":
            # Force role-based color
            if slot == "headline":
                expected = fg_authoritative
            elif slot == "body":
                expected = body_authoritative
            elif slot in ("tag", "tag_eyebrow"):
                expected = body_authoritative
            else:
                expected = fg_authoritative
            cur = el.get("color", "")
            if cur.startswith("var(") or _luminance_distance(cur, bg_authoritative) < 0.25:
                # Off-palette or low-contrast — snap to authoritative
                log.append(f"FIX: {slot} color {cur} -> {expected}")
                el["color"] = expected
            elif cur != expected and _looks_offbrand(cur, [fg_authoritative, body_authoritative, accent_authoritative]):
                log.append(f"FIX: {slot} color {cur} -> {expected} (snap to palette)")
                el["color"] = expected
            # Snap ranges to accent if any
            for rng in el.get("ranges", []) or []:
                if rng.get("fill", "").startswith("var(") or _looks_offbrand(rng.get("fill", ""), [accent_authoritative]):
                    rng["fill"] = accent_authoritative

        elif el.get("type") == "pill_cta":
            cur_bg_pill = el.get("background", "")
            cur_text_pill = el.get("text_color", "")
            if cur_bg_pill.startswith("var(") or cur_bg_pill != cta_bg_auth:
                log.append(f"FIX: CTA bg {cur_bg_pill} -> {cta_bg_auth}")
                el["background"] = cta_bg_auth
            if cur_text_pill.startswith("var(") or cur_text_pill != cta_text_auth:
                log.append(f"FIX: CTA text {cur_text_pill} -> {cta_text_auth}")
                el["text_color"] = cta_text_auth

    # 4) COORDINATE IMAGE_SLOT + TEXT positions — preserve relative spacing
    image_slots = [e for e in elements if e.get("type") == "image_slot"]
    text_pills = [e for e in elements if e.get("type") in ("text", "pill_cta")]

    # 4.0) ALWAYS sequence text blocks based on text height — even without images
    if not image_slots:
        sorted_texts = sorted(
            [el for el in text_pills if el.get("type") == "text"],
            key=lambda e: e.get("y", 0)
        )
        if sorted_texts:
            cursor_y = max(sorted_texts[0].get("y", 100) or 100, 100)
            for el in sorted_texts:
                font_cfg = el.get("font", {})
                size = font_cfg.get("size", 32)
                lh_pct = font_cfg.get("line_height_pct", 120)
                style_cur = font_cfg.get("style", "")
                if "Expanded" in style_cur and any(k in style_cur for k in ["Heavy", "Bold"]):
                    cw = 0.78
                elif "Expanded" in style_cur:
                    cw = 0.70
                elif any(k in style_cur for k in ["Heavy", "Bold", "Black"]):
                    cw = 0.62
                else:
                    cw = 0.55
                width = el.get("width") or (target_w - 160)
                cpl = max(6, int(width / (size * cw)))
                txt = el.get("text", "")
                wrapped = 0
                for line in txt.split("\n"):
                    wrapped += max(1, -(-len(line) // cpl)) if line else 1
                # Pillow font metrics typically render lines with extra space — use 1.35x buffer
                line_h = size * max(lh_pct / 100, 1.0)  # min 100% line-height
                est_h = int(line_h * wrapped * 1.35)
                if el.get("y") != cursor_y:
                    log.append(f"FIX: {el.get('slot_name')} y {el.get('y')} -> {cursor_y} (seq lines={wrapped} est_h={est_h})")
                    el["y"] = cursor_y
                gap = 80 if el.get("slot_name") == "headline" else (40 if el.get("slot_name") in ("tag", "tag_eyebrow") else 32)
                cursor_y += est_h + gap

    for img in image_slots:
        img_y, img_h = img.get("y", 0), img.get("height", 0)
        img_w = img.get("width", 0)
        img_bottom = img_y + img_h

        # Image is top-anchored (y<=80, large width)
        is_top_image = img_y <= 80 and img_w >= target_w * 0.7
        is_full_bleed = is_top_image and img_h >= target_h * 0.7

        # Determine text safe zone start (where text can begin)
        if is_full_bleed:
            text_safe_top = int(target_h * 0.62)
        elif is_top_image:
            text_safe_top = img_bottom + 80  # margin below image
        else:
            text_safe_top = 100  # default top margin

        # Sort text elements by current y to preserve their order/relative spacing
        sorted_texts = sorted(
            [el for el in text_pills if el.get("type") == "text"],
            key=lambda e: e.get("y", 0)
        )
        cta = next((e for e in text_pills if e.get("type") == "pill_cta"), None)

        # If any text is above the safe zone, rebuild positions
        needs_rebuild = any(el.get("y", 0) < text_safe_top for el in sorted_texts)
        if needs_rebuild and sorted_texts:
            cursor_y = text_safe_top
            for el in sorted_texts:
                font = el.get("font", {})
                size = font.get("size", 32)
                line_height_pct = font.get("line_height_pct", 120)
                style = font.get("style", "")
                # Char width factor varies by typeface family + width axis
                # SF Pro Expanded / Heavy / Bold = wider glyphs
                if "Expanded" in style:
                    char_w_factor = 0.72 if any(k in style for k in ["Heavy", "Bold"]) else 0.65
                elif any(k in style for k in ["Heavy", "Bold", "Black"]):
                    char_w_factor = 0.60
                else:
                    char_w_factor = 0.52
                width = el.get("width") or (target_w - 160)
                if isinstance(width, (int, float)) and size > 0:
                    chars_per_line = max(6, int(width / (size * char_w_factor)))
                    explicit_lines = max(1, len(el.get("text", "").split("\n")))
                    # Count line breaks needed by wrapping each explicit line independently
                    wrapped = 0
                    for line in el.get("text", "").split("\n"):
                        wrapped += max(1, -(-len(line) // chars_per_line))  # ceil division
                    est_lines = max(explicit_lines, wrapped)
                else:
                    est_lines = max(1, len(el.get("text", "").split("\n")))
                line_h = size * (line_height_pct / 100)
                est_h = int(line_h * est_lines * 1.20)  # +20% safety
                if el.get("y", 0) != cursor_y:
                    log.append(f"FIX: {el.get('slot_name')} y {el.get('y')} -> {cursor_y} (lines={est_lines} est_h={est_h})")
                    el["y"] = cursor_y
                # Gap between blocks: larger for headline→body
                gap = 56 if el.get("slot_name") == "headline" else (40 if el.get("slot_name") in ("tag", "tag_eyebrow") else 32)
                cursor_y += est_h + gap

    # Ensure CTA is near bottom
    cta_els = [e for e in elements if e.get("type") == "pill_cta"]
    for cta in cta_els:
        if cta.get("y", 0) < target_h - 250 or cta.get("y", 0) > target_h - 100:
            new_y = target_h - 200
            log.append(f"FIX: CTA y {cta.get('y')} -> {new_y} (bottom anchor)")
            cta["y"] = new_y

    # Z-ORDER: image_slot must render FIRST (background), then text/pills on top.
    image_slots_z = [e for e in elements if e.get("type") == "image_slot"]
    other_z = [e for e in elements if e.get("type") != "image_slot"]
    new_order = image_slots_z + other_z
    if new_order != elements:
        log.append(f"FIX: reordered z-stack — image_slots ({len(image_slots_z)}) first, then text/CTAs ({len(other_z)})")
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
