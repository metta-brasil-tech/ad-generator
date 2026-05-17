# Image Prompt — Estilo LIGHT-SURREAL

> Herda de `_base.md`. Skill 04 escolhe a seção correta abaixo conforme `IMAGE_GEN_PROVIDER`.

## Função da imagem nesse estilo

Colagem/composição surreal **personifica visualmente a metáfora da dor descrita na copy**. Homem com pedra na cabeça = "pesa pensar". Cabeça-monitor = "vive plugado no operacional". A imagem é THUMBNAIL EDITORIAL — entende-se em 1 segundo. Estética HBR/Exame, não cartoon.

## O que o banco real mostra

- 3 de 4 LIGHT-SURREAL têm pessoa (com elemento surreal anexado)
- Mood real top: `urgent reflection`, `thoughtful liberation`, `thoughtful urgency`
- Composição: figura central com objeto simbólico sobre a cabeça, fundo claro/branco neutro
- Palette: light-white (4 de 4) — SEMPRE fundo claro
- Tema recorrente: peso/responsabilidade visualizado como objeto físico

---

## SEÇÃO PROD — gpt-image-1

> gpt-image-1 é melhor em surrealismo conceitual fotográfico que em colagem clássica. Foca em "figura real + objeto incongruente" estilo Magritte editorial.

### Template

```
Surreal editorial photograph in a clean minimalist style on a plain off-white background, of a Brazilian business owner in his/her {age_range}, {visual_persona}, {body_pose},
WITH {surreal_metaphor_object} {placement_of_object},
clean studio lighting, soft even shadows on the off-white background,
subject CENTERED in the frame, full or three-quarter body shot,
{ambient_around_subject_for_overlay},
muted desaturated palette dominated by whites and neutral grays with one subtle accent color, sharp focus throughout, editorial conceptual photography in the style of Harvard Business Review or The New Yorker covers, high detail,
without cartoon style, without 3D render look, without anime, without children's book illustration, without dark moody lighting, without text or logos in image
```

### Variáveis

| Var | Opções |
|---|---|
| `{age_range}` | "early 40s" / "mid-40s" |
| `{visual_persona}` | "Brazilian man, light olive skin, dark hair, wearing business casual gray sweater and dark trousers" / "Brazilian woman, warm light skin, hair pulled back, wearing dark navy blazer and black trousers" |
| `{body_pose}` | "seated upright in a simple wooden chair facing the camera" / "standing upright in a neutral posture, arms relaxed at sides" / "seated at a small bare desk with hands resting on the surface, looking forward" |
| `{surreal_metaphor_object}` | "a large rough gray stone the size of a watermelon" / "a vintage CRT computer monitor with cables hanging" / "a heavy iron anchor" / "a cage with small mechanical gears inside" / "a stack of folders that defies gravity" — depende da metáfora da copy |
| `{placement_of_object}` | "balanced on top of the subject's head replacing or covering the head area" / "floating above the subject's head" / "hovering close to the subject's chest as if attached" |
| `{ambient_around_subject_for_overlay}` | "with significant empty white space above the subject and to the sides (text overlay will be applied to upper area)" |

### Exemplo preenchido — "pesa pensar"

```
Surreal editorial photograph in a clean minimalist style on a plain off-white background, of a Brazilian business owner in his early 40s, light olive skin, dark short hair, wearing a business casual gray sweater and dark trousers, seated upright in a simple wooden chair facing the camera with hands resting on his thighs, WITH a large rough gray stone the size of a watermelon balanced on top of his head replacing the head area, clean studio lighting with soft even shadows on the off-white background, subject CENTERED in the frame, three-quarter body shot, with significant empty white space above the subject and to the sides (text overlay will be applied to upper area), muted desaturated palette dominated by whites and neutral grays with one subtle warm wood accent from the chair, sharp focus throughout, editorial conceptual photography in the style of Harvard Business Review or The New Yorker covers, high detail, without cartoon style, without 3D render look, without anime, without children's book illustration, without dark moody lighting, without text or logos
```

### Fallbacks

**v2 — cabeça-monitor:**
```
Surreal editorial photograph on a clean off-white background, of a Brazilian business owner in his late 40s, warm brown skin, wearing a dark navy suit, seated at a bare wooden desk with hands typing on a laptop, but his head is replaced by a vintage CRT computer monitor showing a frozen blue screen, clean studio lighting, subject centered, three-quarter shot, lots of empty white space above and to the sides, muted neutral palette, sharp focus, HBR editorial conceptual photography, without cartoon, without 3D render, without text or logos
```

**v3 — peso em correntes:**
```
Surreal editorial photograph on a clean off-white background, of a Brazilian woman entrepreneur in her early 40s, light skin, dark hair pulled back, wearing a dark navy blazer, standing upright in neutral posture but with several heavy iron chains attached to her ankles trailing on the floor, clean studio lighting, subject centered full body shot, empty white space surrounding her, muted desaturated grays with one accent of warm wood from the floor, sharp focus, editorial conceptual photography New Yorker style, without cartoon, without dark moody mood, without text or logos
```

---

## SEÇÃO LEGACY — Nano Banana 2

### Template

```
editorial surreal collage on white background, brazilian {persona},
{age_range}, {body_pose_simple},
{surreal_element_on_body},
single light source, soft shadows on white background,
centered composition, full-body or 3/4,
muted palette, off-white + one accent,
in the style of HBR / Harvard Business Review cover art,
clean editorial collage, conceptual, no text, no logos
```

### Reference images (NB2)

- `figma://1:1452` — pedra na cabeça
- `figma://1:1487` — cabeça-monitor
- `figma://1:1521` — corrente nos pés

## Versão

`style-LIGHT-SURREAL_v2.0` · 2026-05-17 · seção dupla, gpt-image-1 reformulado pra surrealismo fotográfico (não colagem clássica)
