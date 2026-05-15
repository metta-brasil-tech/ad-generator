# Image Prompt — Estilo TIAGO-STORY-MINIMAL-QUESTION

> Herda de `_base-tiago.md`. Story 9:16 ultra-minimalista — foto contemplativa + texto leve solto.

## Função da imagem nesse estilo

A foto **carrega o mood inteiro**. O texto entra leve, sutilmente, quase como sussurro. A foto precisa ser contemplativa, baixa saturação, sem call-to-action visual. Mood: pensamento privado, momento de pausa.

Exemplos: mesa noturna com luminária acesa, vista urbana ao entardecer, livro aberto na mão, sala iluminada por luz natural, paisagem urbana de janela.

## Constraints do estilo

- **Aspect-ratio:** 9:16 obrigatório
- **Mood:** contemplativo, intimista, baixo volume — slow life
- **Lighting:** sempre natural difusa, golden hour leve aceito, evitar luz dura
- **Subject:** ambiente / detalhe / paisagem. Pessoas só se forem detalhe (mãos, silhueta), nunca rosto direto.
- **Filtro:** desat -0.2 (mais que outros estilos — quer mood sussurrado), contraste +0.05
- **Bleed:** sim, 100%
- **Saturação:** muito baixa — quase B&W mas mantendo cor sutil

## Template de prompt

```
quiet contemplative phone-snapshot of {detalhe_ou_paisagem},
{atmosfera},
{lighting} natural diffuse lighting, soft long shadows,
desaturated muted palette with single warm accent,
shot vertically 9:16 from {angulo_intimista},
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slow-life mood, slight grain texture, contemplative tone,
no people in main focus, no logos visible,
no high-contrast, no over-saturation,
no commercial mood, no advertisement aesthetic
```

## Exemplos preenchidos

### Exemplo 1 — Mesa de trabalho noturna (ref Frame 1321317326)

> Pergunta: "o que você não abre mão pra se manter produtivo?"

```
quiet contemplative phone-snapshot of a home office desk at night,
open laptop screen dimly glowing, table lamp casting warm pool of light,
notebook and pen barely visible at the edge, plant silhouette on the side,
warm desk-lamp light from left side, deep ambient shadow elsewhere,
desaturated warm browns and ambers with deep navy night palette,
shot vertically 9:16 from across-the-desk angle slightly low,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slow-life intimate mood, slight grain texture,
no people, no logos visible, no over-saturation,
no commercial product-shot, no aspirational productivity aesthetic
```

### Exemplo 2 — Vista do Rio (Pão de Açúcar) (ref Frame 1321317330)

> Tese: "A vida de quem bate a meta é diferente — aproveitando essa vista do RJ"

```
quiet contemplative phone-snapshot of Rio de Janeiro skyline,
Pão de Açúcar mountain in distance over the bay, sailboats and small islands,
view from a high vantage point with railing slightly in foreground out of focus,
late afternoon natural diffuse light, golden hour soft warm tones,
desaturated greens, blues and warm sand palette with subtle golden accent,
shot vertically 9:16 from balcony angle,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slow-life contemplative mood, slight grain texture,
no people in frame, no logos visible,
no postcard tourism aesthetic, no over-saturation, no HDR cinema look
```

### Exemplo 3 — Livro aberto / página citação (ref Frame 1321317334)

> Reflexão: "No futuro, você agradecerá por ter considerado e respeitado hoje o significado e a relevância do tempo."

```
quiet contemplative phone-snapshot of an open book in someone's hand,
two pages visible with a single highlighted quote in the center,
slight shadow from the binding crease, hand holding the page edge,
warm natural daylight from window, soft long shadows on paper,
desaturated cream and warm sepia palette with paper texture visible,
shot vertically 9:16 from above slightly diagonal,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slow reading mood, slight grain texture,
no full hand or face visible, no logos visible,
no commercial book-photo aesthetic, no over-saturation
```

### Exemplo 4 — Sala com luz natural / canto íntimo

> Reflexão: "o silêncio é onde o pensamento aparece"

```
quiet contemplative phone-snapshot of a quiet living room corner,
single armchair near a window, soft cushion, a book on the seat,
natural sunlight pouring in from the side, long shadows on wooden floor,
desaturated cream and warm wood palette with single muted blue accent,
shot vertically 9:16 from across-the-room angle low,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slow-life intimate mood, slight grain texture,
no people, no logos visible,
no interior-design-magazine aesthetic, no over-saturation
```

## Reference images

- `brand-knowledge/exemplars/tiago/STORY-MINIMAL/01-mesa-noturna-laptop.png`
- `brand-knowledge/exemplars/tiago/STORY-MINIMAL/02-vista-rj-pao-de-acucar.png`

## Negative prompt específico

```
no high saturation,
no commercial mood,
no Apple keynote lighting,
no Hasselblad cinema look,
no professional architecture/interior photography,
no real-estate listing aesthetic,
no advertising product-shot,
no people in main focus, no faces visible,
no surreal collage, no AI render artifacts,
no over-styled scene, no HDR, no high contrast,
no brand logos in foreground
```

## Iteração se não bater

- **v1:** prompt principal
- **v2:** aumentar `desat -0.3` e remover lighting específico
- **v3:** trocar pra `Fujifilm X100V 23mm` se quiser mais "filme" / grão

## Versão

`style-story-minimal_v1.0` · 2026-05-15 · Head de Design Metta
