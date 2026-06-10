# Image Prompt Base — Marca Tiago Alves

> Equivalente ao `image-prompts/metta/_base.md`, mas pra namespace Tiago.
> Image prompts em `image-prompts/tiago/style-*.md` HERDAM esse base.

## Identidade visual da marca (NÃO sobrescrever)

A marca pessoal Tiago Alves trabalha em **DOIS registros visuais** — o template de cada
`style-*.md` (archetype) decide qual usar. O base NÃO impõe um registro único: ele dá o
vocabulário dos dois e deixa o template do estilo mandar.

**Registro 1 — documental / lo-fi (light):** foto crua de celular, luz natural, mood
pensativo/observacional. Usado em `photo-raw`, `story-hero`, `story-yellow`,
`story-minimal`, `twitter`. Mood-alvo: "diary photo de pensamento", não "ad institucional".

**Registro 2 — cinema editorial / surreal (dark):** B&W cinemático com toque amarelo
seletivo, colagem surreal de revista, noir close-up. Usado em `editorial-hero` (colagem
surreal), `editorial-dark` (noir), `editorial-card`, `dark-surreal`. Esse registro É parte
do DNA do Tiago — **não** é Metta.

Princípios que valem nos DOIS registros:
- **Não** mostram empresário exausto/refém num tom acusatório (Tiago provoca, não humilha)
- **Sempre** carregam intenção editorial — nunca foto de banco de imagem genérica
- O amarelo seletivo (#FFCC00) é o único elemento que sobrevive ao B&W no Registro 2

## Como o prompt funciona

Image-gen do Tiago tipicamente recebe:
- `{subject}` — o que aparece na foto (objeto, cena, pessoa observando algo, screenshot mockado)
- `{mood}` — pensativo, observacional, calmo, irônico-leve
- `{lighting}` — natural difusa, daylight, soft window light (NÃO golden hour dramática)
- `{palette}` — neutras-claras (whites, soft grays, warm beige), sem saturação forte
- `{camera}` — leitura mais "iPhone-like" ou Fujifilm X — não Hasselblad cinema

## Template universal

```
{mood} composition of {subject},
{environment_or_context},
{lighting} lighting with soft natural shadows,
{palette} color palette,
{camera_hint}, editorial 4K,
shallow depth of field on key element,
no text in image, no logos visible, no over-saturation
```

## Vocabulário-padrão

### Mood
- `quiet observation` — pessoa olhando algo
- `contemplative still life` — objeto isolado em cena
- `mid-thought` — momento de pausa
- `documentary detail` — registro factual

### Environment / context
- `modest commercial backoffice` — sala de gerência
- `simple desk with notebook` — mesa enxuta
- `brazilian retail scene` — varejo brasileiro
- `corporate hallway` — corredor de empresa
- `coffee shop window seat` — café (cenário pensativo)

### Lighting
- `soft daylight through window`
- `overhead diffused fluorescent` (escritório real)
- `natural ambient`

### Palette
- `muted whites and soft grays`
- `warm neutrals with one accent`
- `desaturated daylight tones`

### Camera hint
- `iPhone 15 Pro main lens`
- `Fujifilm X-T5 35mm f/2`
- `Sony A7C 40mm f/2.5`

## Negative prompt base

> SÓ negativos que valem nos DOIS registros. Restrições de registro (ex.: "no dark cinema"
> no lo-fi, ou "no surreal collage" no editorial-dark) vivem no negative prompt do
> `style-*.md` do archetype — NUNCA aqui no base, senão briga com o template.

```
no text, no logos, no over-saturation, no HDR look,
no cinematic teal-orange grade,
no group photo, no eye contact with camera,
no stock smile, no fake business pose,
no AI-render artifacts, no plastic skin
```

## Quando o slot pede screenshot/objeto e não pessoa

Se a peça é um statement do Tiago sobre uma situação observada (ex: foto do crachá "Gerente VENDEDOR"), o prompt:

```
documentary detail of {object_or_scene},
captured as a phone snapshot in natural light,
slight imperfection (off-center, soft focus on edges),
desaturated daylight tones,
iPhone 15 Pro main lens, editorial 4K,
no text overlay, no logos, no studio look
```

## Reference images

> Provider atual em produção é **gpt-image-2** (texto→imagem, sem ref images). A passagem de
> PNGs de referência só se aplica a providers legacy (Nano Banana 2 / Gemini). Em gpt-image-2,
> a coerência de marca vem 100% do texto do prompt — não há style-transfer por imagem.
> Os exemplars em `brand-knowledge/exemplars/tiago/` ficam só como referência humana de curadoria.

## Versão

`_base-tiago_v1.0` · 2026-05-14 · Head de Design Metta
