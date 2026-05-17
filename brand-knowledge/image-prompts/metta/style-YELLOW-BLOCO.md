# Image Prompt — Estilo YELLOW-BLOCO

> Herda de `_base.md`. Skill 04 escolhe a SEÇÃO correta abaixo conforme `IMAGE_GEN_PROVIDER`.

## Função da imagem nesse estilo

Foto pessoa **à direita bleed corner** comunica "eu" (founder-led ou líder identificável). Não é narrativa, é assinatura humana. Bloco amarelo no centro carrega a oferta — a foto é só "quem está falando com você".

Diferença vs A: aqui o bloco amarelo é o protagonista, foto é coadjuvante (em A a foto é segundo elemento mais importante).

## O que o banco real mostra

- **6 de 7** YELLOW-BLOCO têm pessoa (alta presença)
- Persona frequente: **apresentador em palco/evento**, ou líder comercial em escritório aberto
- Palette real: mixed (4) + yellow-bg (3) — pessoa precisa funcionar contra fundo claro/amarelo
- Mood: `confident urgency`, `engaging informative`, `motivational focus`
- Composição padrão: pessoa esquerda OU direita, postura aberta/engajada (NÃO pensativa-fora-de-câmera como estilo A)

---

## SEÇÃO PROD — gpt-image-1 (provider atual em prod)

### Template

```
Photograph of a Brazilian business owner/leader in his/her {age_range}, {visual_persona},
{engaged_pose}, photographed in {institutional_environment},
soft diffused natural light with no harsh shadows,
{composition_for_slot},
neutral palette with slight warm cast — designed to pair with bright yellow text blocks in the final design,
clean uncluttered background, sharp focus on subject's eyes,
clean editorial corporate portrait, high detail,
without smiling stock pose, without dramatic moody lighting, without dark editorial shadows, without ring light, without text or logos in image
```

### Variáveis

| Var | Opções concretas |
|---|---|
| `{age_range}` | "early 40s" / "mid-40s" / "late 40s" |
| `{visual_persona}` | "Brazilian man, light olive skin, dark short hair, well-trimmed beard, wearing navy blazer over white t-shirt" / "Brazilian woman, warm light skin, dark hair pulled back, wearing structured camel blazer over silk blouse" / "Brazilian man, warm brown skin, short black hair, wearing smart business shirt with sleeves rolled up" |
| `{engaged_pose}` | "standing relaxed with hands in pockets, slight forward lean of engagement" / "seated edge-of-chair with forward lean, hands resting on knee" / "standing at a podium speaking to an audience with confident open gesture" / "arms loosely crossed, professional and engaged stance" |
| `{institutional_environment}` | "in front of a clean off-white textured wall in a modern studio" / "in a corporate event setting with audience softly blurred in the background" / "in a quiet executive lounge with warm wood textures" / "in a co-working space with subtle architectural details" |
| `{composition_for_slot}` | (ver §Composição-por-slot — depende do placement) |

### Composição-por-slot

`placement: corner-bleed-right` (default YELLOW-BLOCO — pessoa direita-bottom bleed):
```
subject positioned in the right 40% of the frame from waist up, occupying right side with body bleeding slightly off the right edge and bottom edge, with the left 60% showing softly blurred neutral background, subject's gaze toward camera or slightly into the left frame (engaging with content area)
```

`placement: corner-bleed-left` (variação):
```
subject positioned in the left 40% of the frame, occupying left side, with the right 60% showing softly blurred neutral background
```

### Exemplo preenchido — convite institucional founder-led

```
Photograph of a Brazilian man in his mid-40s, light olive skin, dark short hair, well-trimmed beard, wearing a navy blazer over a clean white t-shirt, standing relaxed with hands in pockets, slight forward lean of engagement, photographed in front of a clean off-white textured wall in a modern studio, soft diffused natural light with no harsh shadows, subject positioned in the right 40% of the frame from waist up, occupying right side with body bleeding slightly off the right edge, with the left 60% showing softly blurred neutral background, subject's gaze toward camera with direct warm engagement, neutral palette with slight warm cast — designed to pair with bright yellow text blocks in the final design, clean uncluttered background, sharp focus on his eyes, clean editorial corporate portrait, high detail, without smiling stock pose, without dramatic moody lighting, without dark editorial shadows, without ring light, without text or logos
```

### Variações pra fallback

**v2 — líder comercial em palco:**
```
Photograph of a Brazilian man in his late 40s, warm brown skin, short black hair, clean-shaven, wearing a smart business shirt with sleeves rolled up, standing at a podium speaking to an audience with confident open gesture, photographed in a corporate event setting with audience softly blurred in the background, even overhead diffused event lighting, subject positioned in the right 40% of the frame from waist up, with the left 60% showing the warm-lit blurred audience as background space, subject looking slightly into the left frame as if addressing it, neutral palette suitable for yellow text overlay, sharp focus on eyes, editorial documentary photography, high detail, without stock smile, without ring light, without text or logos
```

**v3 — empresária:**
```
Photograph of a Brazilian woman in her early 40s, warm light skin, dark hair pulled back, minimal jewelry, wearing a structured camel-colored blazer over a silk cream blouse, seated edge-of-chair posture with forward lean, hands resting on knee, photographed in a quiet executive lounge with warm wood textures and a window providing soft afternoon light from camera left, subject positioned in the right 40% of the frame from waist up, with the left 60% showing the warm wooden interior softly blurred, gaze direct to camera with subtle smile of confidence, warm earth tones suitable for yellow text overlay, sharp focus on eyes, editorial corporate portrait, high detail, without overly bright stock smile, without ring light, without text or logos
```

---

## SEÇÃO LEGACY — Nano Banana 2

### Template

```
[calm authority / serious confidence] portrait of a brazilian {audience},
{age_range}, {smart_casual_clothing},
{engaged_posture},
warm diffused light or overhead diffused neutral,
right-corner composition, subject occupies right 40% of frame,
gaze toward camera or slightly into left frame (engaging with content),
warm earth tones or neutral with slight warm cast,
photographed in {neutral_professional_environment},
shallow depth of field, shot on Sony A7R V 85mm GM f/1.4,
clean editorial portrait, 4K, sharp focus on eyes,
background simple and uncluttered to keep focus on subject,
no text, no logos, sujeito íntegro
```

### Reference images (NB2)

- `figma://1:78` — flagship com Sicredi/Vivo
- `figma://1:1021` — variação institucional com líder mulher
- `figma://1:987` — convite com bullets, founder-led

---

## Diferença visual chave vs A

| Aspecto | A | YELLOW-BLOCO |
|---|---|---|
| Mood | informative urgency / confident professional | confident urgency / engaging informative |
| Bg da foto | mista (light/mixed/dark) | neutro claro (combina com bloco amarelo) |
| Olhar | quase sempre off-camera | pode ser direto (engaja com conteúdo) |
| Função | âncora humana sobre qualquer paleta | assinatura institucional sobre claro+amarelo |

## Iteração se não bater

1. Foto compete com bloco amarelo → simplificar background ("clean off-white textured wall")
2. Pessoa muito formal → mudar pra pose "relaxed standing, hands in pockets"
3. Lighting muito moody → trocar pra "soft diffused with no shadows"

## Versão

`style-YELLOW-BLOCO_v2.0` · 2026-05-17 · seção dupla NB2 + gpt-image-1, alinhado ao banco real
