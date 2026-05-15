# Image Prompt — Estilo TIAGO-EDITORIAL-DARK

> Herda de `_base-tiago.md`. Mood **cinema noir editorial**, não documental.

## Função da imagem nesse estilo

Imagem dark fullbleed que carrega o peso emocional do slide. Não é metáfora surreal (isso é HERO/CARD) —
é foto cinema **close-up** ou **silhueta**, B&W com tom warm sutil. A imagem domina o canvas; o texto entra
em zona safe centralizada-bottom com darkening overlay.

Tipos canônicos:
- **Close-up extremo** de olho humano (com texto cursivo dentro da pupila opcional)
- **Silhueta** de empresário em corredor escuro, mãos em sombra
- **Cena cinema** de figura solitária em ambiente corporativo dark
- **Solid dark gradient** quando o slide é só tipográfico (sem foto)

## Constraints do estilo

- **Aspect-ratio:** geralmente 4:5 ou 1:1 fullbleed (1080×1350)
- **Mood:** cinema noir editorial, B&W com tone warm sutil, NÃO surreal nem collage
- **Subject:** olho/rosto close-up OU silhueta OU corredor cinematográfico
- **Lighting:** controlada e cinema (overhead spot, single rim, side fill) — NÃO natural ambient
- **Filter:** dessaturação heavy, contrast +0.6, vinheta sutil
- **Foco:** sharp em ponto-âncora (íris, contorno), resto em deep shadow

## Template de prompt

```
Cinematic noir close-up photograph of {subject},
{key_detail},
deep dramatic side lighting from {direction}, hard shadows controlled,
extremely shallow depth of field, sharp focus on {focus_point},
desaturated black and white with subtle warm undertone (tint #2E1F0F),
heavy vignette,
no smile, no eye contact, no posed framing,
single subject isolated against dark background OR dark corporate environment,
no logos, no text in image, no commercial gloss,
Sony A7R V 85mm f/1.4, cinema editorial 4K, RAW
```

## Exemplos preenchidos

### Exemplo 1 — Olho humano close-up (Funcionário capa)

> Tese: "Seu funcionário sente o seu medo."

```
Cinematic noir close-up photograph of a single adult human eye,
brown/hazel iris with sharp focus on pupil,
eyelashes and skin pores visible,
deep dramatic side lighting from the right, hard shadow on left half of face,
extremely shallow depth of field, sharp focus on pupil reflection,
desaturated black and white with subtle warm undertone,
heavy vignette darkening the corners,
no smile, no movement, no other features visible,
isolated against deep black background,
no logos, no text in image,
Sony A7R V 85mm f/1.4, cinema editorial 4K, RAW
```

### Exemplo 2 — Silhueta empresário em corredor (Método de Jesus slide 3)

> Tese: "Eu já vi esse filme em mais de mil empresas. E o empresário sempre chega na mesma conclusão errada."

```
Cinematic noir photograph of a single male silhouette walking down a long dark corridor,
back to camera, slight motion blur on legs,
deep dramatic overhead spotlight from far end of corridor (silhouette in mid-distance),
hard shadow controlled, vanishing point in distance,
extremely shallow depth of field, sharp focus on shoulders/back of head,
desaturated black and white with subtle warm undertone,
heavy vignette,
no faces visible, no logos, no readable signage on walls,
isolated solitary figure, corridor walls in deep shadow,
Sony A7R V 35mm f/1.8, cinema editorial 4K, RAW
```

### Exemplo 3 — Mãos em sombra controlada

> Tese (genérico): "decisão pesada"

```
Cinematic noir close-up of male adult hands resting on a dark wooden desk,
fingers interlaced, slight tension visible in knuckles,
deep dramatic single side light from the left,
extremely shallow depth of field, sharp focus on the front hand,
desaturated black and white with subtle warm undertone,
heavy vignette, deep blacks crushing into the background,
no face visible, no logos, no commercial styling,
single subject isolated against dark desk surface and pitch-black background,
Sony A7R V 85mm f/1.4, cinema editorial 4K, RAW
```

### Exemplo 4 — Cenário corporativo dark (silhueta sentada)

```
Cinematic noir photograph of a male figure seated alone in a dark conference room,
back to camera, looking at a window with grayed-out skyline,
deep dramatic side light from the window,
silhouette against window, profile barely visible,
extremely shallow depth of field, focus on the silhouette outline,
desaturated black and white with subtle warm undertone,
heavy vignette darkening edges,
no face visible, no logos, no other people,
isolated solitary subject, corporate environment in deep shadow,
Sony A7R V 50mm f/1.4, cinema editorial 4K, RAW
```

## Reference images

`brand-knowledge/exemplars/tiago/TIAGO-EDITORIAL-DARK/` quando disponíveis.

## Negative prompt específico

```
no smile, no eye contact with camera, no posed business portrait,
no studio bright lighting, no commercial polish, no modern HDR look,
no logos visible, no readable text in image, no signage,
no group photo, no multiple subjects, no AI-render plastic skin,
no surreal collage (that's HERO/CARD style), no selective yellow paint here,
no documentary snap mood (this is cinema editorial),
no warm filter excess, no orange-teal cinematic grade (we want desaturated noir)
```

## Quando adicionar texto cursivo dentro da imagem

No slot `handwritten_overlay` do YAML, quando especificado:
- Frase manuscrita branca com opacity 0.75, fonte cursiva (Caveat / Permanent Marker)
- Posicionada DENTRO da área de foco da imagem (ex: dentro da pupila do olho)
- Tipicamente refere-se à voz interna do sujeito da foto

Esta camada de texto é aplicada em CSS/Pillow no assembler — **não** instruir o image-gen a renderizar texto.

## Iteração se não bater

- **v1:** prompt principal
- **v2 (fallback):** trocar `Sony A7R V` por `Leica SL2-S` e suavizar contraste
- **v3 (fallback):** simplificar pra solid dark gradient + texto em outro slot (sem imagem)

## Versão

`style-editorial-dark_v1.0` · 2026-05-14 · Head de Design Metta
