# Image Prompt — Base universal Metta

> **Esse doc é o substrato comum.** Todo prompt por estilo herda dele.
> Skill 04 escolhe a SEÇÃO PROD ou LEGACY conforme `IMAGE_GEN_PROVIDER`.

## Identidade visual da marca (NÃO sobrescrever, sempre presente)

- **Brasil.** Sempre decisor brasileiro — pele variando (light olive, warm brown, light), idade 35-55, mood corporativo executivo. Nunca americano genérico, nunca asiático stock, nunca "Hollywood entrepreneur".
- **Editorial.** Estética de revista de negócios séria (HBR, Exame, Bloomberg Businessweek). Nunca lifestyle Instagram, nunca corporate stock.
- **Decision-grade.** Olhar pensativo, reflexivo, em ação. Nunca sorriso fake stock. Nunca pose de "executivo bem-sucedido".
- **Sujeito íntegro.** JAMAIS recortar sujeito humano principal pelo meio. Composição inclui rosto + ombros mínimo, idealmente até cintura.
- **Profundidade de campo rasa.** Background desfocado, sujeito em foco — exceto quando o cenário É a narrativa.
- **Luz natural.** Window light, golden hour, ou luz dura editorial. Nunca flash duro, nunca anel de LED.

## REGRA INVIOLÁVEL: composição-por-slot

A foto precisa **encaixar no slot que o layout reservou**. Se o layout coloca a foto em `right-bleed corner` ocupando 40% do canvas direito, a foto não pode ter o sujeito centralizado — o sujeito tem que estar à direita da foto, com espaço vazio à esquerda pra texto.

Skill 04 deve LER o `image_slot.placement` do layout_spec e INJETAR a instrução de composição correspondente no prompt. Mapeamento:

| placement YAML | Instrução obrigatória no prompt |
|---|---|
| `right-bleed`, `corner-bleed-right` | "subject positioned in the right 40% of the frame, with the left 60% showing softly blurred neutral background space (this empty area will be covered by text overlay)" |
| `left-bleed`, `corner-bleed-left` | "subject positioned in the LEFT 45% of the frame, with the right 55% showing softly blurred neutral background space" |
| `top-bleed` | "subject positioned in the upper 50% of the frame, with the lower half showing softly blurred environmental floor/desk space (this empty bottom will be covered by text overlay)" |
| `bottom-bleed` | "subject positioned in the lower 50% of the frame, with the upper half showing softly blurred environmental ceiling/wall background (this empty top area will be covered by text overlay)" |
| `fullbleed`, `full-bleed` | "subject CENTERED in the frame, mid-shot from chest up, ample headroom and breathing space, background slightly out of focus to maintain readability of dark text overlay applied to upper third / lower third (per layout)" |
| `center` | "subject CENTERED in the frame, with empty space surrounding for text overlay" |
| (não especificado) | usar default `subject centered, ambient space around for potential text overlay` |

**IMPORTANTE:** mesmo quando o estilo (style-X.md) traz seu próprio bloco "Composição-por-slot", essa tabela aqui é o fallback se faltar — nunca enviar prompt SEM instrução de composição quando o layout tem image_slot.

## Constraints universais

- **Aspect ratio:** STORY 9:16, FEED 4:5, SQR 1:1 — usar exatamente o do briefing
- **Resolução:** alta detail/fidelity — explicitar "high detail" no prompt
- **Negative inline (gpt-image-1 não tem campo `negative_prompt` separado — anexar com "without X, Y, Z" no prompt principal):**
  - without smiling stock pose
  - without cartoon, without 3D render look generic
  - without anime, without children's book illustration
  - without ring light, without flash, without harsh lighting
  - without text or logos in image
  - without fake teeth-bleached smile
  - without recortes de sujeito principal (subject must be fully visible from chest up or wider)

(Skill 04 deve concatenar esses negatives ao negative_prompt da resposta — quando provider for gpt-image-1, eles também entram inline no prompt principal via "without X" syntax. Quando NB2, vão no campo negative_prompt nativo.)

## Vocabulário de mood (escolher 1-2)

Versão visual descritiva (pra gpt-image-1):
- `confident professional` — postura confiante, olhar direto profissional
- `confident urgency` — ar de urgência decisiva, expressão alerta
- `informative urgency` — postura de quem comunica algo importante
- `focused determination` — olhar focado, traços tensos de decisão
- `motivational empowerment` — pose convidativa, expressão encorajadora
- `inviting confidence` — gesto aberto, postura receptiva
- `thoughtful liberation` — postura relaxada após decisão pensada
- `quiet exhaustion` — ombros levemente caídos, expressão cansada mas digna

Versão jargão técnico (pra Nano Banana 2):
- `serious confidence` · `quiet exhaustion` · `pensive reflection` · `calm authority` · `editorial gravitas` · `cinematic intimacy`

## Tokens de iluminação (escolher 1)

Versão descritiva (gpt-image-1):
- "warm afternoon sunlight from a window on the left casting soft long shadows"
- "soft overhead diffused light with no harsh shadows"
- "dramatic chiaroscuro side lighting from a window, half the face in shadow"
- "golden hour amber light from behind the subject creating soft rim glow"
- "even soft natural daylight with no directional shadows"
- "dim ambient warm light from a desk lamp in an otherwise dark environment"

Versão jargão (NB2):
- `warm window light, soft shadows` · `golden hour rim light` · `editorial moody, hard side light` · `overhead diffused, neutral` · `corporate window, cold backlight`

## Tokens de composição (escolher 1 — sempre ALÉM da instrução de slot)

Versão descritiva:
- "mid-shot from waist up, body slightly angled toward the camera"
- "three-quarter shot, body in profile, head turned toward camera"
- "close-up from chest up, intimate framing"
- "wide shot showing subject and surrounding environment"

Versão jargão (NB2):
- `rule of thirds subject right` · `centered composition eye contact` · `cropped tight shoulders up` · `wide environmental small in frame`

## Tokens de paleta visual (escolher 1)

Versão descritiva (gpt-image-1):
- "warm earth tones with brown and mustard accents"
- "neutral palette with cool grays and one warm wood accent"
- "muted desaturated tones with dark teal background"
- "high contrast palette with deep blacks and one warm amber highlight"
- "monochromatic warm sepia tones"
- "clean light palette with soft whites and neutral grays"

Versão jargão (NB2):
- `warm earth tones, mustard accent` · `cool steel blue, dim corporate` · `desaturated muted, editorial dark` · `high contrast B&W`

## Personas brasileiras pré-aprovadas (varie pra diversidade real)

| Persona | Descrição visual concreta |
|---|---|
| Empresário varejo médio | "Brazilian man, light olive skin, dark short hair, well-trimmed beard, wearing casual button-up shirt in navy or wool jacket over open shirt" |
| Empresário serviços | "Brazilian man, warm brown skin, short black hair, clean-shaven, wearing smart business shirt with sleeves rolled up or navy suit jacket no tie" |
| Empresária varejo/serviços | "Brazilian woman, warm light skin, dark hair pulled back, minimal jewelry, wearing structured camel-colored blazer over silk blouse or dark navy blazer" |
| Líder comercial | "Brazilian man, light skin, short brown hair, glasses with thin metal frames, wearing dark gray sweater over white t-shirt" |
| Founder tech | "Brazilian man, mixed skin tone, longer dark hair, casual plain dark t-shirt, minimal frame glasses" |

## Ambientes pré-aprovados

- "modern Brazilian retail store with shelves and merchandise softly blurred"
- "small office with wooden furniture and natural light from a window"
- "executive lounge with warm wood textures"
- "co-working space with soft architectural lines"
- "podium during a business event with audience blurred in background"
- "industrial warehouse with concrete and metal textures (logística)"
- "in front of clean off-white textured wall in a modern studio (clean editorial)"

## Anti-padrões universais (NÃO incluir em prompt — sempre via "without X")

- "successful businessman" → gera pose fake
- "happy" / "smiling" → destrói gravidade
- "team meeting" / "high-five" → estética stock
- "modern office with glass walls" → genérico
- "professional headshot" → vibe LinkedIn
- "thumbs up" / "celebration" → proibido
- "looking at chart" / "graph in background" → cliché
- "Hollywood entrepreneur" / "Silicon Valley founder" → quebra brasilidade

## Iteração se não bater (independente de provider)

1. Trocar mood pra outro vocabulário do §Mood
2. Mudar `subject right` pra `subject left` ou `centered`
3. Ajustar idade do persona ±5 anos
4. Trocar lighting (window → golden hour, etc.)
5. Simplificar background ("clean off-white textured wall")

## Versão

`base_v2.0` · 2026-05-17 · adicionou seção dupla NB2/gpt-image-1 + tabela inviolável de composição-por-slot + personas brasileiras concretas
