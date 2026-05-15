# Image Prompt Base — Marca Tiago Alves

> Equivalente ao `image-prompts/metta/_base.md`, mas pra namespace Tiago.
> Image prompts em `image-prompts/tiago/style-*.md` HERDAM esse base.

## Identidade visual da marca (NÃO sobrescrever)

A marca pessoal Tiago Alves é **light-first** (fundo claro), **neutra tipograficamente** (SF Pro Regular), **emocionalmente acolhedora** (voz que pensa em vez de acusar). Imagens nesse namespace seguem o mesmo princípio:

- **Não** são fotos editoriais dark moody (isso é Metta)
- **Não** mostram empresário exausto/refém (Tiago acolhe, não acusa)
- **São** fotos contextuais, ilustrativas, com mood pensativo/observacional
- **São** objetos, cenas, screenshots, momentos que ancoram o tweet
- Mood-alvo: "diary photo de pensamento", não "ad institucional"

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

```
no text, no logos, no over-saturation, no HDR look,
no dramatic golden hour, no cinematic teal-orange grade,
no group photo, no eye contact with camera,
no stock smile, no fake business pose,
no dark moody editorial (that's Metta brand), no Hasselblad cinema,
no AI-render artifacts, no surreal collage
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

Quando rodando via Nano Banana 2 (que aceita imagens de referência), passar 1-2 PNGs de `brand-knowledge/exemplars/tiago/` pra style transfer manter coerência light/quieto.

## Versão

`_base-tiago_v1.0` · 2026-05-14 · Head de Design Metta
