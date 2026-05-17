# Image Prompt — Estilo A (Headline + foto pessoa)

> Herda de `_base.md`. Skill 04 escolhe a SEÇÃO correta abaixo conforme `IMAGE_GEN_PROVIDER`.

## Função da imagem nesse estilo

Foto serve como **âncora humana** — não como narrativa. A pessoa NÃO conta a história; o texto conta. A pessoa só comunica "quem está falando" ou "pra quem é esse ad". Banco indexado mostra que **17 de 21** ads do estilo A têm pessoa visível.

## O que o banco real mostra (informa o prompt)

- Persona: empresário brasileiro 40-55, postura confiante mas natural (não pose stock executive)
- Ambientes recorrentes: loja/showroom comercial, mesa de escritório, evento ao vivo
- Palette dominante: **mixed/light** (8 light-white + 7 mixed + 5 dark) — NÃO é só dark moody
- Mood real top: `informative urgency`, `confident professional`, `confident strategic warm`
- Composição padrão: pessoa central ou levemente à direita, espaço pra texto na esquerda/topo

---

## SEÇÃO PROD — gpt-image-1 (provider atual em prod)

> gpt-image-1 ignora jargão técnico de fotografia (Hasselblad, Leica, etc.). Funciona melhor com descrição visual concreta, persona detalhada, e negative inline ("without X").

### Template

```
Photograph of a Brazilian business owner in his/her {age_range}, {visual_persona},
{action_or_pose}, photographed in {environment_concrete},
{lighting_visual}, {composition_for_slot},
{palette_visual}, sharp focus on the subject's eyes, shallow background blur,
editorial business magazine quality, high detail,
without smiling, without stock photo pose, without ring light, without fake teeth-bleached smile, without text or logos in image
```

### Variáveis (preencher conforme briefing)

| Var | Opções concretas |
|---|---|
| `{age_range}` | "early 40s" / "mid-40s" / "late 40s" / "early 50s" |
| `{visual_persona}` | "light olive skin, dark wavy hair, well-trimmed beard" / "warm brown skin, short black hair, clean-shaven" / "light skin, short brown hair, glasses with thin metal frames" — varie pra dar diversidade brasileira real |
| `{action_or_pose}` | "leaning against a wooden counter with one hand resting on it, body slightly angled toward the camera" / "seated at a desk, hands clasped in front, looking thoughtful" / "standing with arms relaxed at sides in a retail store aisle" |
| `{environment_concrete}` | "inside a modern Brazilian retail store with shelves and merchandise softly blurred behind" / "in a small office with wooden furniture and natural light from a window on the left" / "at a podium during a business event with audience blurred in background" |
| `{lighting_visual}` | "warm afternoon sunlight from a window on the left casting soft long shadows" / "soft overhead diffused light with no harsh shadows" / "golden hour amber light from behind the subject creating a soft rim glow" |
| `{composition_for_slot}` | (ver §Composição-por-slot abaixo — depende do placement YAML) |
| `{palette_visual}` | "warm earth tones with brown and mustard accents" / "neutral palette with cool grays and one warm wood accent" / "muted desaturated tones with dark teal background" |

### Composição-por-slot (CRÍTICO pra encaixar foto no layout)

Quando o YAML do estilo A coloca o image_slot em `placement: right-bleed` (foto à direita, bleed canto):
```
subject positioned in the right 40% of the frame, occupying right side from waist up, with the left 60% of the frame showing softly blurred neutral background space (this empty area will be covered by text overlay), subject's gaze directed toward the left edge of the frame (looking off-camera into the empty space)
```

Quando o slot é `placement: bottom-bleed`:
```
subject positioned in the lower 50% of the frame, with the upper half showing softly blurred environmental ceiling/wall background (this empty top area will be covered by text overlay)
```

Quando o slot é `placement: fullbleed`:
```
subject centered, mid-shot from chest up, ample headroom and breathing space around the subject, background slightly out of focus to maintain readability of dark text overlay that will be applied in the lower third
```

### Exemplo preenchido — pergunta diagnóstica varejo

```
Photograph of a Brazilian business owner in his mid-40s, light olive skin, dark short hair, well-trimmed beard, wearing a casual button-up shirt in dark navy, leaning against a wooden retail counter with one hand resting on it, body slightly angled toward camera, photographed inside a modern Brazilian retail store with shelves and merchandise softly blurred behind him, warm afternoon sunlight from a window on the left casting soft long shadows, subject positioned in the right 40% of the frame, occupying right side from waist up, with the left 60% of the frame showing softly blurred neutral background space (this empty area will be covered by text overlay), subject's gaze directed toward the left edge of the frame, warm earth tones with brown and mustard accents, sharp focus on the subject's eyes, shallow background blur, editorial business magazine quality, high detail, without smiling, without stock photo pose, without ring light, without text or logos in image
```

### Variações pra fallback (iteration_strategy.fallback_prompts)

**v2 — mudança de mood + ambiente:**
```
Photograph of a Brazilian business owner in his late 40s, warm brown skin, short black hair, wearing a dark gray sweater over a white t-shirt, seated at a wooden desk with hands clasped in front, looking thoughtful and slightly off-camera, photographed in a small office with paper documents and a closed laptop on the desk, soft overhead diffused light with no harsh shadows, subject positioned in the right 40% of the frame, with the left 60% as soft neutral background space, neutral palette with cool grays and warm wood accent, sharp focus on eyes, shallow depth of field, editorial documentary photography, high detail, without smiling, without stock pose, without ring light, without text or logos
```

**v3 — versão mais editorial dark:**
```
Photograph of a Brazilian woman business owner in her early 40s, light skin, dark hair pulled back, wearing a structured camel-colored blazer, standing in a quiet executive lounge with wooden textures and dim ambient light, hand resting on a side table, looking sideways into the distance, dramatic side lighting from a window on the left creating soft shadows on the right side of her face, subject positioned in the right 40% of the frame, with the left 60% showing the dim warm-toned interior, sharp focus on her eyes, shallow depth of field, editorial Bloomberg Businessweek quality, high detail, without smiling, without stock pose, without ring light, without text or logos
```

---

## SEÇÃO LEGACY — Nano Banana 2 (Gemini, não em prod ainda)

> Mantida pra quando IMAGE_GEN_PROVIDER=nano-banana-2. NB2 aceita reference_images nativamente e responde bem a jargão técnico de fotografia.

### Constraints do estilo A (Nano Banana)

- **Bleed à direita ou bottom.** Foto pode passar do canvas (X positivo além de 1080) — composição encaixa a pessoa "vindo de fora".
- **Mood serious confidence ou pensive reflection.**
- **Filtros:** saturação -0.2, contrast +0.3.

### Template

```
[serious confidence / pensive reflection] portrait of a brazilian {audience},
{age_range}, {clothing},
{action_describing_decision_moment},
warm window light, soft shadows,
rule of thirds, subject right, decision-maker looking left out of frame,
warm earth tones with mustard accent,
photographed in {environment},
shallow depth of field, shot on Hasselblad H6D-100c, 80mm lens,
editorial photography, 4K, sharp focus on eyes,
no text, no logos, sujeito íntegro
```

### Reference images (passar pro NB2)

- `figma://1:704` — homem pensativo em ação, bleed direita
- `figma://1:1204` — empresário em situação reflexiva
- `figma://1:1216` — close editorial vertical

(figma:// refs requerem resolver via FIGMA_TOKEN — ainda não implementado.
PNGs do banco indexado em `artifacts/banco/` funcionam direto.)

---

## Iteração se não bater (independente de provider)

1. Foto muito moody → reduzir saturação delta pra 0, aumentar brightness
2. Pessoa rígida demais → mudar pose pra mais relaxada
3. Composição não respeita slot → reforçar "subject in right 40% of frame" e "empty space on left"

## Versão

`style-A_v2.0` · 2026-05-17 · adicionou seção dupla NB2 + gpt-image-1, alinhou com sinais reais do banco indexado
