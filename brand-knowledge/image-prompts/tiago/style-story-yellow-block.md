# Image Prompt — Estilo TIAGO-STORY-YELLOW-BLOCK

> Herda de `_base-tiago.md`. Story 9:16 com foto de ambiente lo-fi + bloco amarelo overlay.

## Função da imagem nesse estilo

A foto **é contexto**, não protagonista. Ambiente cotidiano que ancora o tema do bloco amarelo: sala de reunião com vista urbana (→ empresa), academia vazia (→ disciplina/meta), mesa noturna (→ trabalho), paisagem urbana (→ rotina). Sem pessoas como sujeito principal.

A foto faz o "esse momento te lembra de pensar nisso?". O bloco amarelo carrega a pergunta/checklist.

## Constraints do estilo

- **Aspect-ratio:** 9:16 obrigatório
- **Mood:** observacional, ambiente vazio ou semi-vazio, lo-fi documental
- **Lighting:** natural — luz de janela, luz fluorescente de academia, luz de noite urbana
- **Subject:** ambiente / espaço / objeto. SEM pessoa como sujeito (pode ter pessoas ao fundo borradas)
- **Filtro:** desat -0.15, contraste +0.05. Sem grade colorimétrica forte.
- **Bleed:** sim, 100%
- **Bloco-safe area:** região central-vertical fica visualmente "vazia" pra o bloco amarelo overlay assentar limpo

## Template de prompt

```
documentary phone-snapshot of {ambiente},
{detalhe_contextual_opcional},
{lighting} natural lighting, soft shadows,
{palette} muted natural palette,
shot vertically 9:16 from {angulo},
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slight imperfection (off-center / casual framing),
no people in main focus, no logos visible,
center area visually quiet for overlay block,
no studio look, no professional architecture-shoot aesthetic
```

## Exemplos preenchidos

### Exemplo 1 — Sala de reunião com vista urbana (ref 442573)

> Pergunta: "Sua meta é realista?"

```
documentary phone-snapshot of an empty corporate meeting room on a high floor,
large floor-to-ceiling windows showing brazilian metropolitan skyline (buildings, distant streets),
modern conference table with chairs around it slightly out of focus in foreground,
warm afternoon natural daylight pouring in from windows, soft shadows on table,
muted gray-blue and warm beige palette,
shot vertically 9:16 from inside the room looking toward window,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slight off-center framing, casual perspective,
no people in main focus, center-vertical area visually quiet for overlay block,
no studio look, no logos visible, no over-saturation
```

### Exemplo 2 — Academia vazia (ref Frame 1321317324)

> Pergunta: "Já bateu sua meta diária hoje?"

```
documentary phone-snapshot of an empty modern gym interior,
rows of dumbbells and weight rack along a black wall, mirror on the side reflecting the space,
clean polished floor, single yellow accent on a piece of equipment,
overhead fluorescent diffused lighting, soft shadows,
desaturated grays with black mirrors and one yellow accent,
shot vertically 9:16 from waist height down the room,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slight off-center framing, casual perspective,
no people, center-vertical area visually quiet for overlay block,
no logos visible, no professional gym-ad aesthetic, no over-saturation
```

### Exemplo 3 — Mesa noturna trabalho

> Pergunta: "O que você precisa parar de fazer pra ter mais foco?"

```
documentary phone-snapshot of a home office desk at night,
wooden desk with closed laptop, table lamp glowing warm, open notebook with a pen,
window in background showing city lights soft out of focus,
warm desk-lamp light from left, deep ambient shadow elsewhere,
warm brown and amber palette with deep navy night background,
shot vertically 9:16 from desk-edge angle slightly low,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slight off-center framing, intimate quiet mood,
no people, no logos visible,
center-vertical area visually quiet for overlay block,
no studio look, no professional product-shot aesthetic
```

## Reference images

- `brand-knowledge/exemplars/tiago/STORY-YELLOW-BLOCK/01-sala-reuniao-vista.png`
- `brand-knowledge/exemplars/tiago/STORY-YELLOW-BLOCK/02-academia-vazia.png`

## Negative prompt específico

```
no people in main focus,
no professional architecture photography,
no real-estate listing aesthetic,
no editorial cinema mood,
no Hasselblad look, no over-styled scene,
no dramatic Apple keynote lighting,
no overhead drone shot,
no surreal collage, no AI render artifacts,
no brand logos in foreground,
no centered focus point (center should be quiet for overlay)
```

## Iteração se não bater

- **v1:** prompt principal
- **v2:** simplificar — só `ambiente` + `lighting`, deixar mais livre
- **v3:** trocar pra `Fujifilm X-T5 35mm` se Nano Banana der saturação demais

## Versão

`style-story-yellow-block_v1.0` · 2026-05-15 · Head de Design Metta
