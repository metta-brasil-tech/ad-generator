# Image Prompt — Estilo TIAGO-STORY-COVER-HERO

> Herda de `_base-tiago.md`. Capa de carrossel story 9:16 com Tiago como sujeito real.

## Função da imagem nesse estilo

A foto **É** o slide. Headline e assinatura entram como overlay leve. Tiago é o sujeito principal — palestrando, em casa, em viagem, lendo, em ritual cotidiano. Sensação: "isso é a vida dele agora, sem produção".

A foto carrega o peso emocional. Headline ancora a tese verbal.

## Constraints do estilo

- **Aspect-ratio:** 9:16 obrigatório (1080×1920 story)
- **Mood:** documental, lo-fi, capturado de celular. Sem cinema, sem editorial-noir.
- **Lighting:** natural — luz de janela, luz de palco real, luz noturna cozy de casa
- **Subject:** Tiago como pessoa REAL em contexto autêntico. Pode estar em foco principal ou em ângulo lateral. Evitar pose-publicitária / olhar direto pra câmera.
- **Filtro:** levíssima desat -0.1, contraste +0.1. Sem grade colorimétrica forte.
- **Bleed:** sim, foto preenche 100% do canvas
- **Headline-safe area:** scrim 25% no canto onde o headline vai (geralmente center-left), preserva legibilidade sem destruir foto

## Template de prompt

```
documentary phone-style portrait of a brazilian businessman in his 40s,
{contexto}, {acao}, {ambiente},
{lighting} natural lighting, soft shadows,
{palette} muted natural palette,
shot vertically 9:16 as if grabbed mid-moment,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slight imperfection (off-center / casual framing / motion blur subtle),
no studio look, no professional retouch, no posed smile,
no overstyled grade, no cinema lighting,
no logos visible, no text overlay
```

## Exemplos preenchidos

### Exemplo 1 — Tiago palestrando (ref Frame 1321317322)

> Tese: "O que todo empresário precisa saber sobre gestão comercial"

```
documentary phone-style portrait of a brazilian businessman in his 40s,
on stage at a business conference holding a microphone mid-speech,
dark navy stage backdrop with soft blue spotlights,
warm stage lighting from above-right, natural shadows on his face,
deep blue and warm beige palette with subtle yellow accent,
shot vertically 9:16 from audience angle slightly low,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slight motion blur on his hand gesture, casual framing,
no studio retouch, no posed smile, no logos visible,
no over-saturation, no cinema lighting
```

### Exemplo 2 — Tiago em casa com família (ref Frame 1321317323)

> Tese: "as 4 coisas que precisei mudar na minha vida"

```
documentary phone-style portrait of a brazilian businessman in his 40s,
at home with his teenage son in a casual moment,
warm home interior with soft afternoon window light,
both wearing casual clothes (t-shirt, soft tones),
warm beige and cream palette with natural skin tones,
shot vertically 9:16 selfie-style angle,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slight off-center casual framing, no posed look,
no studio retouch, no logos visible, no over-saturation,
no cinema lighting, no professional family-shoot aesthetic
```

### Exemplo 3 — Tiago lendo / estudando (ref Frame 1321317333)

> Tese: "6 lições do livro que mudou minha visão sobre performance"

```
documentary phone-style still life with hands of a man in his 40s,
reading an open book ('Hábitos Atômicos') on a dark wooden table,
ceramic coffee cup steaming on the side,
warm overhead light from desk lamp, soft shadows on wood texture,
warm wood brown and cream palette with subtle yellow accent,
shot vertically 9:16 from above slightly diagonal,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
casual framing, slight imperfection in book angle,
no studio retouch, no aspirational reading-pose,
no logos visible, no over-saturation, no cinema lighting
```

### Exemplo 4 — Tiago em viagem / paisagem (ref Frame 1321317327)

> Tese: "5 coisas que me tornaram um empresário melhor"

```
documentary phone-style selfie portrait of a brazilian businessman in his 40s with his wife,
on a mountain trail at high altitude with clouds and rocky peaks behind them,
both wearing dark outdoor gear (jacket, beanie),
natural overcast daylight, soft cool tones,
muted gray-blue and earth-tone palette,
shot vertically 9:16 selfie-style with arm-extended angle,
iPhone 15 Pro main lens, editorial 4K but lo-fi,
slight wind motion in hair, casual happy expression (not posed),
no studio retouch, no logos visible, no over-saturation,
no cinema lighting, no adventure-brand-ad aesthetic
```

## Reference images (passar pro Nano Banana 2)

- `brand-knowledge/exemplars/tiago/STORY-COVER-HERO/01-palestra-azul.png`
- `brand-knowledge/exemplars/tiago/STORY-COVER-HERO/02-casa-familia.png`
- Indexar 3-5 fotos reais do dia-a-dia Tiago à medida que aparecem

## Negative prompt específico

```
no professional studio lighting,
no business stock photo aesthetics,
no editorial-collage noir (different style — TIAGO-EDITORIAL-HERO),
no Hasselblad cinema look, no Sony A7 pose,
no perfectly centered subject, no eye contact with camera,
no fake business smile, no over-styled scene,
no surreal collage, no AI render artifacts,
no over-sharpened HDR, no brand logos in foreground,
no glossy magazine cover finish
```

## Iteração se não bater

- **v1:** prompt principal acima
- **v2 (fallback):** simplificar — descrever só `subject` + `ambiente`, sem `lighting` específico
- **v3 (fallback):** mudar pra `iPhone 14 stock` e remover `editorial 4K` pra forçar mais lo-fi

## Quando pular geração de imagem

Nunca — o slot `foto_bleed` é `required: true` neste estilo.

## Versão

`style-story-cover-hero_v1.0` · 2026-05-15 · Head de Design Metta
