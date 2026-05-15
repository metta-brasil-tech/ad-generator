# Image Prompt — DARK-OBJETO variante: Peças de xadrez 3D (carrossel diferença)

> Herda de `_base.md`. Variante específica do DARK-OBJETO para o carrossel
> "A diferença entre empresa que cresce e empresa que sobrevive".

## Conceito visual do slide

Duas peças de xadrez 3D em destaque no centro do frame sobre fundo dark moody.
O contraste entre a peça dourada (empresa que cresce = cavalo/knight) e
a peça prateada/comum (empresa que sobrevive = peão/pawn) **é a metáfora**.
A iluminação de rim-light dourado separa as duas peças e cria tensão.
Fundo tem marca d'água tipográfica levíssima (texto repetido em loop, quase
invisível — ≤5% opacidade).

## Prompt principal (gpt-image-2)

```
Photorealistic 3D render of two chess pieces centered on a dark moody background.
Left piece: a golden knight chess piece, highly detailed, metallic gold with warm
reflections, rim light from right side creating a sharp gold edge highlight.
Right piece: a standard silver pawn chess piece, matte silver-gray, slightly
smaller than the knight, in shadow, flat rim light only.
Both pieces rest on a very subtle dark surface (near invisible), slight reflection
on surface.
Background: deep dark #0C161B, near-black with very subtle film grain texture.
Faint watermark text pattern repeated diagonally across background at 4% opacity
(illegible, only texture).
Cinematic rim lighting setup: primary light from top-right (warm golden key),
fill from left (cold blue), no overhead.
Render style: Cinema 4D + Octane quality, 4K, ultra-sharp focus on pieces,
slight depth of field at edges.
Composition: two pieces centered horizontally with slight breathing space between,
golden knight slightly taller and forward, pawn slightly behind.
No text, no logos, no humans, no watermarks visible, pure product render.
```

## Variações por objeto-conceito

### Variante: Troféu Copa do Mundo (slide escassez de processo)

```
Photorealistic 3D render of a FIFA World Cup trophy, golden, ultra-detailed,
centered on dark moody background.
Trophy: solid gold metallic, two human figures holding the globe base, intricate
surface detail, highly polished with reflections.
Background: deep dark #0C161B with very subtle film grain.
Faint diagonal text watermark at 4% opacity across background.
Cinematic lighting: warm golden key light from top-front, cold blue rim from behind
creating separation, dark moody atmosphere.
Render: Cinema 4D / Octane quality, 4K, trophy occupies 50-60% of canvas height.
Slight lens flare on top highlight.
No text, no logos, no humans.
```

### Variante: Engrenagem / mecanismo (slide método/processo)

```
Photorealistic 3D render of a large brass mechanical gear, single piece,
centered floating slightly above dark surface.
Gear: antique brass/bronze finish, intricate teeth detail, visible machined surface.
Background: deep dark #0C161B moody.
Lighting: warm amber key from upper-right, cold secondary from lower-left.
Render: Cinema 4D quality, 4K, sharp focus, no text, no logos, no humans.
```

### Variante: Dominó dourado (slide efeito cascata)

```
Photorealistic 3D render of a single golden domino tile, fallen at 45 degrees,
as if mid-fall, centered on dark background.
Domino: solid gold metallic, dots in platinum, sharp edges.
Background: deep dark #0C161B, minimal reflection on surface.
Cinematic lighting: sharp rim from top, warm and cold split.
No text, no logos, no humans.
```

## Negative prompt

```
no text overlay, no watermark, no human figures, no hands, no tables visible,
no white background, no bright backgrounds, no cartoon style, no illustration,
no flat design, no generic stock, no soft focus on pieces, no oversaturated
colors, no neon lights
```

## Nota de composição

A imagem gerada pela IA **não deve ter texto**. Todo o texto do slide
(headline "A DIFERENÇA ENTRE", labels das peças, CTA pill "ARRASTA PRO LADO")
é adicionado pelo assembler em cima da imagem. A IA só gera o background visual.

## Referência de modelo YAML

- Modelo base: `DARK-OBJETO`
- Slots de texto no YAML `DARK-OBJETO.yaml`
- Carrossel slide 1 copy:
  - tag: "A DIFERENÇA ENTRE"
  - headline: "EMPRESA QUE CRESCE"
  - body: "e empresa que sobrevive em 2026"
  - label_left: "empresa que cresce" (sob cavalo dourado)
  - label_right: "empresa que sobrevive" (sob peão)
  - cta: "ARRASTA PRO LADO"

## Versão

`style-DARK-OBJETO-chess_v1.0` · 2026-05-15 · Head de Design Metta
