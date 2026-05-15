# Image Prompt — Estilo TIAGO-DARK-SURREAL

> Herda de `_base-tiago.md`. Intersticial atmosférico — fundo preto + imagem surreal isolada.

## Função da imagem nesse estilo

A imagem **É** o slide inteiro. Sem texto, sem copy. Mood noir-poster, B&W ou monocromática dark, surreal/onírica.

Funciona como:
- Intersticial entre slides pesados de carrossel
- Capa estética standalone
- Ponte simbólica (próximo slide explica a metáfora)

Exemplos canônicos: pessoa com máscara animal cobrindo metade do rosto, gato em frente a espelho oval iluminado, objeto cotidiano isolado por luz dura, busto/escultura em ambiente preto.

## Constraints do estilo

- **Aspect-ratio:** 1:1, 4:5 ou 9:16 — todos servem desde que IMAGEM CENTRADA + PRETO AROUND
- **Mood:** noir-poster, surreal, onírico, dramático mas quieto
- **Lighting:** luz dura única vinda de cima ou lateral — sculpting, cinematic
- **Subject:** UM elemento simbólico isolado — pessoa+máscara, animal+objeto, escultura, objeto onírico
- **Filtro:** B&W ou desat extrema (-0.8 a -1.0), contraste +0.3, grain noise leve
- **Bleed:** **não** — imagem ISOLADA centralizada com PRETO PURO ao redor (40-65% da área é preto)
- **Saturação:** quase zero — pode manter sutil tonalidade fria (azul-grafite) mas sem cor saturada

## Template de prompt

```
surreal black-and-white poster image of {sujeito_simbolico},
{detalhe_metaforico},
hard dramatic single-source lighting from above-left, deep cast shadows,
desaturated monochrome with cool blue-grey undertone,
isolated center composition with deep black negative space around 60% of frame,
{angulo} angle, studio-controlled mood,
medium format film aesthetic, slight grain texture,
mysterious surreal tone, dreamlike but quiet,
no text, no logos, no people in commercial pose,
no bright saturated colors, no advertising look
```

## Exemplos preenchidos

### Exemplo 1 — Máscara animal + pessoa (ref Frame 1321317329)

```
surreal black-and-white poster image of a young woman wearing a leather strap blindfold,
her left hand holding up a taxidermied deer head mask in front of her face,
half woman half animal composite isolated in deep black void,
hard dramatic single-source lighting from above-left, deep cast shadows on neck and hand,
desaturated monochrome with cool blue-grey undertone,
isolated center composition with deep black negative space around 60% of frame,
straight-on angle slightly low, studio-controlled mood,
medium format film aesthetic, slight grain texture,
mysterious surreal tone, dreamlike but quiet,
no text, no logos, no other elements, no color,
no bright lighting, no advertising aesthetic
```

### Exemplo 2 — Gato em frente a espelho (ref freepik)

```
surreal black-and-white poster image of a small black cat sitting in front of an oval mirror,
the mirror standing in deep empty space, cat's silhouette dimly reflected,
soft circular spotlight illuminating only the cat and mirror frame,
desaturated monochrome with cool blue-grey undertone,
isolated center composition with deep black negative space around 70% of frame,
ground-level eye-line angle, intimate mysterious mood,
medium format film aesthetic, slight grain texture,
dreamlike quiet tone,
no text, no logos, no other elements, no color,
no bright lighting, no commercial pet-photo aesthetic
```

### Exemplo 3 — Objeto isolado por luz dura

```
surreal black-and-white poster image of a single wooden chair toppled on its side,
isolated in deep black void with hard single beam of light from above,
long sharp shadow extending across the dark floor,
desaturated monochrome with cool grey undertone,
center composition with deep black negative space around 65% of frame,
slightly elevated angle, theatrical mysterious mood,
medium format film aesthetic, slight grain texture,
silent dramatic tone,
no text, no logos, no other elements,
no color, no bright lighting, no commercial product-shot aesthetic
```

### Exemplo 4 — Escultura / busto

```
surreal black-and-white poster image of a classical marble bust covered partially by black fabric,
fabric draping over one eye and one ear, isolated in deep black space,
hard sculpting light from upper-right, sharp shadows on facial features,
desaturated monochrome with cool grey undertone,
center composition with deep black negative space around 60% of frame,
straight-on chest-height angle, mysterious philosophical mood,
medium format film aesthetic, slight grain texture,
dreamlike quiet tone,
no text, no logos, no other elements, no color,
no bright lighting, no museum-catalog aesthetic
```

## Reference images

- `brand-knowledge/exemplars/tiago/DARK-SURREAL/01-mascara-animal.png`
- `brand-knowledge/exemplars/tiago/DARK-SURREAL/02-gato-espelho-oval.png`

## Negative prompt específico

```
no text in image,
no people smiling, no advertising aesthetic,
no bright colors, no commercial product shot,
no studio backdrop visible (only deep black void),
no full body landscape composition (only centered isolated subject),
no editorial-collage with yellow paint (different style — TIAGO-EDITORIAL-HERO),
no surreal-photoshop tackiness,
no AI render artifacts,
no oversharp HDR,
no flat ambient lighting (needs hard sculpting light)
```

## Iteração se não bater

- **v1:** prompt principal
- **v2:** trocar `medium format film` por `Hasselblad H6D` se quiser mais textura cinema
- **v3:** mudar `single beam of light` pra `chiaroscuro lighting` se Nano Banana achatar

## Versão

`style-dark-surreal_v1.0` · 2026-05-15 · Head de Design Metta
