# Image Prompt — Estilo TIAGO-TWITTER-CARD

> Herda de `_base-tiago.md`.

## Função da imagem nesse estilo

Variante `cover` do TIAGO-TWITTER-CARD termina com uma foto/imagem retangular (radius 28px) na base do slide. Essa foto **ilustra** ou **ancora** o tweet headline — não é decoração. Tipicamente:

- Foto-documental de um objeto/cena que o tweet menciona (ex: crachá, vitrine, painel, tela)
- Screenshot mockado (printscreen de outro tweet, métrica, sistema)
- Detalhe humano contextual (mãos, gesto, recorte) — nunca rosto centralizado em pose ad

A imagem aqui **não** carrega o peso emocional. O tweet headline carrega. A foto só prova/aterriça.

## Constraints do estilo

- **Aspect-ratio:** livre — funciona 1:1, 4:3, 16:9. Vira card embed.
- **Mood:** observacional, documental, snap-style — não cinemático.
- **Lighting:** natural difusa. Sem golden hour dramática.
- **Subject:** preferir **objeto/cena** sobre **pessoa**. Quando pessoa, evitar rosto direto à câmera.
- **Filtro:** levíssima saturação +0.0, contraste +0.1, sem grade colorimétrica forte.
- **Bleed:** não. Foto entra dentro do card com radius — não passa do padding.

## Template de prompt

```
documentary phone-snapshot of {subject},
{context_brief},
{lighting} natural lighting, soft shadows,
{palette} neutral palette with one accent,
shot as if grabbed mid-moment without setup,
iPhone 15 Pro main lens, editorial 4K, sharp on subject,
slight imperfection (off-center / casual framing),
no text overlay, no logos visible, no studio look,
no dramatic editorial mood, no Hasselblad cinema
```

## Exemplos preenchidos

### Exemplo 1 — Crachá "Gerente VENDEDOR" (ref cr6tiagoabril-1)

> Tese: "Você tem um gerente de vendas ou um vendedor com crachá de chefe?"

```
documentary phone-snapshot of a worn paper id-badge clipped to a denim shirt,
the badge reads 'Gerente' typed and 'VENDEDOR' handwritten in bold red marker over it,
warm overhead natural light from store ceiling, soft shadows on fabric,
desaturated whites and warm beige palette,
shot as if grabbed mid-moment without setup,
iPhone 15 Pro main lens, editorial 4K, sharp on badge text,
casual off-center framing,
no studio look, no professional lighting, no logos visible other than badge text,
no dramatic editorial mood
```

### Exemplo 2 — Mesa de gerência vazia

> Tese: "65% dos gerentes comerciais não batem meta. E o problema não é a meta."

```
documentary phone-snapshot of a simple sales-floor manager's desk,
empty office chair pulled back, a closed notebook with pen on top,
laptop screen showing a sales dashboard slightly out of focus,
overhead diffused fluorescent and soft window daylight,
muted whites and warm gray neutrals with one accent (notebook color),
shot from waist height as if walking past,
iPhone 15 Pro main lens, editorial 4K, sharp on notebook,
slight motion-cue, casual framing,
no people in frame, no logos visible, no over-saturation,
no studio look, no dramatic editorial mood
```

### Exemplo 3 — Detalhe humano (mãos)

> Tese: "Um gestor de alta performance assume um time que não performa, e em meses esse time bate meta."

```
documentary phone-snapshot of a hand gesturing during a 1-on-1 meeting,
forearm in plain shirt sleeve resting on a notebook,
a coffee cup in the periphery slightly out of focus,
warm window daylight from the left, soft natural shadows,
muted neutral palette with warm beige,
shot from across the table at chest height,
iPhone 15 Pro main lens, editorial 4K, sharp on hand,
no faces visible, no logos, no studio look,
no over-saturation, no dramatic editorial mood
```

## Reference images (passar pro Nano Banana 2)

- `brand-knowledge/exemplars/tiago/cr6tiagoabril-1.png` (foto crachá — exemplar canônico cover)
- Em produção, indexar mais 3-5 cover-images do feed do Tiago à medida que aparecem

## Negative prompt específico

```
no professional studio lighting,
no business stock photo aesthetics,
no dark moody Metta editorial (different brand),
no Hasselblad cinema look,
no perfectly centered subject,
no eye contact with camera,
no fake business smile,
no over-styled scene,
no surreal collage, no AI render artifacts,
no over-sharpened HDR,
no Brand logos in foreground
```

## Iteração se não bater

- **v1:** prompt principal acima
- **v2 (fallback):** simplificar — descrever só o subject sem `context_brief`, deixar Nano Banana mais livre
- **v3 (fallback):** mudar câmera pra `Fujifilm X-T5 35mm` e mood pra `quiet still life`

## Quando pular geração de imagem

Variant `content` do TIAGO-TWITTER-CARD não tem foto — só emoji transition. Skill 04 retorna `skip: true` quando layout-spec não tem `image_slot`.

## Versão

`style-twitter-card_v1.0` · 2026-05-14 · Head de Design Metta
