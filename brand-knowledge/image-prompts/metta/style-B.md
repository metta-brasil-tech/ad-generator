# Image Prompt — Estilo B (Foto pessoa esquerda + texto direita)

> Herda de `_base.md`. Skill 04 escolhe a seção correta abaixo conforme `IMAGE_GEN_PROVIDER`.

## Função da imagem nesse estilo

Foto pessoa **à esquerda do canvas** (não top como o nome legado sugere) — é o "apresentador" do conteúdo. Pessoa é tão importante quanto headline; convite pessoal, conexão direta.

## O que o banco real mostra

- **9 de 9** ads B têm pessoa (presença total)
- Mood real top: `confident urgency`, `inviting confidence`, `motivational empowerment`, `serious urgency`
- Composição padrão CONFIRMADA: pessoa esquerda + texto direita
- Persona frequente: apresentador/líder em pose convidativa, postura aberta
- Palette: dark (4) + light (3) + mixed (2) — variado

---

## SEÇÃO PROD — gpt-image-1

### Template

```
Photograph of a Brazilian {gender_and_role} in his/her {age_range}, {visual_persona},
{inviting_pose}, photographed in {environment},
{lighting_visual},
subject positioned in the LEFT 45% of the frame from waist up, occupying the left side with body slightly angled toward the right side of the frame (where text will be), with the right 55% showing softly blurred environmental background space (this empty right area will be covered by text overlay),
subject's gaze directed toward the right side of the frame (engaging with the empty space where text lives),
{palette_visual}, sharp focus on subject's eyes, shallow depth of field,
editorial documentary photography, high detail,
without smiling stock pose, without ring light, without text or logos in image
```

### Variáveis

| Var | Opções |
|---|---|
| `{gender_and_role}` | "business owner" / "founder" / "commercial team leader" / "entrepreneur" |
| `{age_range}` | "early 40s" / "mid-40s" / "late 40s" / "early 50s" |
| `{visual_persona}` | igual style-A — variar diversidade |
| `{inviting_pose}` | "standing with one hand gesturing slightly open toward the camera" / "seated with forward lean, elbow on table, palm open" / "leaning against a wall arms loosely crossed in welcoming posture" / "mid-conversation with subtle hand gesture, mouth slightly open as if speaking" |
| `{environment}` | "modern co-working space with soft architectural lines" / "executive office with warm wood textures and natural side light" / "podium during a business event" / "in front of clean off-white concrete wall" |
| `{lighting_visual}` | "warm side light from a large window on the right casting soft shadows on the left side of the subject's face" / "even soft natural daylight from above" / "golden hour amber light from the right creating a warm rim glow on the subject's shoulders" |

### Exemplo preenchido — convite pessoal evento

```
Photograph of a Brazilian commercial team leader in his late 40s, warm brown skin, short black hair, clean-shaven, wearing a smart business shirt in white with sleeves rolled up, standing with one hand gesturing slightly open toward the camera, photographed in a modern co-working space with soft architectural lines, warm side light from a large window on the right casting soft shadows on the left side of his face, subject positioned in the LEFT 45% of the frame from waist up, body slightly angled toward the right side, with the right 55% showing softly blurred warm-lit office space (this empty right area will be covered by text overlay), subject's gaze directed toward the right side of the frame, neutral palette with warm accent, sharp focus on eyes, shallow depth of field, editorial documentary photography, high detail, without smiling stock pose, without ring light, without text or logos
```

### Fallbacks

**v2 — mais íntimo:**
```
Photograph of a Brazilian woman entrepreneur in her early 40s, light skin, dark hair pulled back, wearing a dark navy blazer over silk blouse, seated with forward lean and elbow on a wooden table, palm open in an inviting gesture, photographed in an executive office with warm wood textures and natural light from a window on the right, subject in left 45% of frame, gaze toward right side of frame, warm earth tones, sharp focus on eyes, editorial documentary quality, high detail, without stock smile, without ring light, without text or logos
```

---

## SEÇÃO LEGACY — Nano Banana 2

```
[inviting confidence / confident urgency] portrait of a brazilian {persona},
{age_range}, {clothing},
{inviting_pose_describing_invitation},
warm side light from right window,
subject left third, body angled right, gaze across the frame,
warm earth tones,
photographed in {institutional_environment},
shallow depth of field, shot on Sony A7R V 85mm GM f/1.4,
editorial photography, 4K, sharp focus on eyes,
no text, no logos, sujeito íntegro
```

## Versão

`style-B_v2.0` · 2026-05-17 · seção dupla + composição alinhada ao banco real (esquerda, não top)
