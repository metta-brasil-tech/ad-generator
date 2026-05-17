# Image Prompt — Estilo D (Foto fullbleed + overlay)

> Herda de `_base.md`. Skill 04 escolhe a seção correta abaixo conforme `IMAGE_GEN_PROVIDER`.

## Função da imagem nesse estilo

Foto **DOMINA** o frame inteiro. A pessoa É o ad — comunica pela presença. Imersão total. Funciona pra emoção forte (peso de decisão, foco, transformação).

## O que o banco real mostra

- 4 de 6 ads D têm pessoa (também aparecem silhuetas e objetos simbólicos)
- Mood real top: `motivational urgency`, `focused determination`, `confident transformative`
- Composição padrão: pessoa CENTRAL (não right-bleed), preenche frame, texto vem em overlay no topo OU base
- Palette: dark (5 de 6) — esse estilo é dominantemente escuro
- Variações: silhuetas, pessoa reclinada, retrato meio-corpo central

---

## SEÇÃO PROD — gpt-image-1

### Template

```
Cinematic photograph of a Brazilian {persona} in his/her {age_range}, {visual_persona},
{emotional_pose}, photographed in {environment},
{lighting_dramatic},
subject CENTERED in the frame, mid-shot from waist up or chest up, filling the central 60% of the frame,
{ambient_around_subject_for_overlay},
{palette_dark},
sharp focus on subject's eyes, shallow depth of field with background fall-off,
cinematic editorial photography, high contrast, high detail,
without smiling stock pose, without ring light, without dramatic backlight burst, without text or logos in image
```

### Variáveis

| Var | Opções |
|---|---|
| `{persona}` | "business owner deep in thought" / "decisive entrepreneur" / "leader at a turning point" |
| `{age_range}` | "early 40s" / "mid-40s" / "late 40s" |
| `{visual_persona}` | igual style-A — variar |
| `{emotional_pose}` | "leaning forward with elbows on a desk, hands clasped in front of mouth in deep thought" / "head slightly bowed, hand on temple in a moment of decision pressure" / "standing arms crossed looking off into the distance with focused determination" / "seated leaning back in a chair, gazing intensely off-camera" |
| `{environment}` | "in a dimly lit office at dusk with only ambient warm light from a desk lamp" / "in a quiet room with a single window providing dramatic side light" / "in a dark wood-paneled study with shadows" |
| `{lighting_dramatic}` | "dramatic chiaroscuro side lighting from a window, half the face in shadow" / "warm golden lamp light from below creating soft underlit mood" / "single overhead spotlight in an otherwise dark environment" |
| `{ambient_around_subject_for_overlay}` | "with dark empty space in the upper portion of the frame above the subject's head (this empty top area will be covered by light-colored text overlay)" / "with dark blurred ambient space surrounding the subject (text overlay will be applied to upper and lower thirds)" |
| `{palette_dark}` | "desaturated dark tones with deep blacks and one warm amber highlight" / "monochromatic dark teal and charcoal palette with subtle warm rim" / "high contrast dark palette dominated by blacks and one warm skin tone" |

### Exemplo preenchido — peso da decisão

```
Cinematic photograph of a Brazilian business owner in his late 40s, light olive skin, dark short hair with subtle gray at temples, well-trimmed beard, wearing a dark charcoal sweater, leaning forward with elbows on a wooden desk, hands clasped in front of his mouth in deep thought, photographed in a dimly lit office at dusk with only ambient warm light from a desk lamp on the right side, dramatic chiaroscuro side lighting, half of his face in shadow with the other half warmly lit, subject CENTERED in the frame, mid-shot from chest up filling the central 60% of the frame, with dark empty space in the upper portion of the frame above his head (this empty top area will be covered by light-colored text overlay), desaturated dark tones with deep blacks and one warm amber highlight, sharp focus on his eyes which are looking off-camera into the distance with focused determination, shallow depth of field, cinematic editorial photography, high contrast, high detail, without smiling stock pose, without ring light, without dramatic backlight burst, without text or logos
```

### Fallbacks

**v2 — silhueta:**
```
Cinematic photograph of a Brazilian business owner shown as a backlit silhouette, standing facing a large window overlooking a city at sunset, body and head shape clearly visible but features in shadow, subject CENTERED in the frame, with dark warm-toned ambient space surrounding him (text overlay will be applied), dramatic backlit silhouette photography, deep amber and dark blue palette, high contrast, editorial cinematic, without text or logos, without face details visible (silhouette only)
```

**v3 — close determinado:**
```
Cinematic close-up photograph of a Brazilian woman entrepreneur in her early 40s, warm light skin, dark hair, head and shoulders in frame, intense focused expression looking just slightly past the camera, photographed in a quiet dim environment with single dramatic side light from camera right, half face in shadow, dark space around the subject suitable for text overlay, desaturated dark palette with one warm rim light, sharp focus on her eyes, cinematic editorial portrait, high detail, without smile, without ring light, without text or logos
```

---

## SEÇÃO LEGACY — Nano Banana 2

```
[focused determination / quiet exhaustion / cinematic intimacy] full-bleed portrait of a brazilian {persona},
{age_range}, {clothing},
{deep_emotional_pose},
dramatic side lighting or chiaroscuro,
centered subject, fills frame from chest up,
desaturated dark editorial, low key,
photographed in {dim_environment},
shallow depth of field, shot on Canon R5 50mm f/1.2L,
cinematic editorial photography, 4K, sharp focus on eyes,
no text, no logos, sujeito íntegro
```

## Versão

`style-D_v2.0` · 2026-05-17 · seção dupla + corrigida composição (CENTRAL, não fullbleed-overlay distorcido)
