# Image Prompt — DARK-OBJETO variante: Peças de xadrez 3D

> Herda de `_base.md`. Skill 04 escolhe a seção correta abaixo conforme `IMAGE_GEN_PROVIDER`.
> Variante específica do DARK-OBJETO usada em carrosséis de comparação/diferença.

## Conceito visual

Duas peças de xadrez 3D em destaque no centro do frame sobre fundo dark moody.
O contraste entre as peças (uma dourada/destacada vs comum) **é a metáfora** —
ex: empresa que cresce vs empresa que sobrevive, founder estratégico vs apagador-de-incêndio.

## O que o banco real mostra (DARK-OBJETO em geral)

- 2 ads DARK-OBJETO, 0 com pessoa visível — objetos simbólicos são o protagonista
- Mood real: `assertive urgency`, `confident strategic`
- Composição padrão: objeto central em destaque, fundo escuro neutro, headline acima ou abaixo
- Exemplos do banco: mão segurando bandeja amarela, peças de dominó

---

## SEÇÃO PROD — gpt-image-1

> gpt-image-1 é bom em renderização fotorrealista de objetos com luz dramática. Funciona bem pra cena de objetos isolados em fundo escuro.

### Template

```
Cinematic photograph of {object_description}, photographed on a dark moody background,
{lighting_dramatic_on_objects},
objects positioned CENTRALLY in the lower third of the frame, leaving the upper two-thirds of the frame as empty dark space (this empty area will be covered by light-colored text headline overlay),
{palette_dark_with_accent},
sharp focus on the {hero_object} with shallow depth of field, soft background fall-off,
editorial product photography in the style of luxury magazine spreads, high detail, photorealistic,
without cartoon, without 3D render look generic, without bright lighting, without text or logos in image
```

### Variáveis

| Var | Opções |
|---|---|
| `{object_description}` | "two chess pieces sitting on a polished dark wooden chess board: a golden knight piece in the foreground catching warm rim light, and a plain silver pawn behind it in soft shadow" / "two stacks of folders on a wooden desk: one stack neat and aligned, the other chaotic and tipping" / "a row of dominoes mid-fall, the first one already toppled" |
| `{lighting_dramatic_on_objects}` | "single warm rim light from the right creating dramatic shadows behind the objects" / "soft amber spotlight from above creating focused pool of light on the objects" / "single light source from the left, half the scene in deep shadow" |
| `{hero_object}` | "the golden knight" / "the leading domino" / "the neat stack of folders" |
| `{palette_dark_with_accent}` | "dark teal and charcoal palette with one warm golden accent on the hero object" / "deep blacks with subtle amber highlights" |

### Exemplo preenchido — peças de xadrez (cresce vs sobrevive)

```
Cinematic photograph of two chess pieces sitting on a polished dark wooden chess board: a golden knight piece in the foreground catching warm rim light, and a plain silver pawn behind it in soft shadow, photographed on a dark moody background, single warm rim light from the right creating dramatic shadows behind the pieces, objects positioned CENTRALLY in the lower third of the frame, leaving the upper two-thirds of the frame as empty dark space (this empty area will be covered by light-colored text headline overlay), dark teal and charcoal palette with one warm golden accent on the knight, sharp focus on the golden knight with shallow depth of field, soft background fall-off, editorial product photography in the style of luxury magazine spreads, high detail, photorealistic, without cartoon, without 3D render look generic, without bright lighting, without text or logos
```

### Fallbacks

**v2 — dominós:**
```
Cinematic photograph of a row of dominoes mid-fall, the first one already toppled, the rest about to fall in sequence, photographed on a dark wooden surface with dark moody background, single amber spotlight from above creating focused pool of light, objects in the lower third of the frame, upper two-thirds empty dark space for text, dark palette with one warm accent, sharp focus on the leading domino, editorial product photography, photorealistic, without cartoon, without text or logos
```

**v3 — folders:**
```
Cinematic photograph of two stacks of folders on a wooden desk in dim lighting: one stack neat and aligned, the other chaotic and tipping, photographed on a dark background, single side light from the left with deep shadows, objects in lower portion of frame, upper area dark empty space for text, dark palette with subtle amber accent, sharp focus on the neat stack, editorial documentary photography, photorealistic, without cartoon, without bright lighting, without text or logos
```

---

## SEÇÃO LEGACY — Nano Banana 2

```
3D rendered chess pieces on dark moody background,
golden knight in foreground, plain silver pawn behind,
dramatic side lighting, chiaroscuro,
centered composition lower third, empty dark space top,
dark teal palette with warm gold accent,
editorial 3D product photography, Octane render quality,
shallow depth of field, sharp focus on knight,
no text, no logos
```

## Versão

`style-DARK-OBJETO-chess_v2.0` · 2026-05-17 · seção dupla, gpt-image-1 versão fotorrealista (não 3D render)
