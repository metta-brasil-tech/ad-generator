# Image Prompt — Estilo A (Headline + foto pessoa direita)

> Herda de `_base.md`. Use junto.

## Função da imagem nesse estilo

Foto serve como **âncora humana**, não como narrativa. Pessoa NÃO conta a história — o texto conta. A pessoa só ancora "quem está falando" ou "pra quem é esse ad".

Decisor olha headline primeiro, foto vem depois confirmar "esse cara é como eu" ou "esse cara entende o que eu vivo".

## Constraints do estilo A

- **Bleed à direita ou bottom.** Foto pode passar do canvas (X positivo além de 1080) — composição encaixa a pessoa "vindo de fora".
- **Mood serious confidence ou pensive reflection.** Nunca sorriso. Olhar pode estar fora de quadro (mais comum) ou direto na lente (assertivo, mais raro).
- **Filtros:** saturação -0.2, contrast +0.3 — moody mas legível.
- **Ratio:** livre, mas a pessoa ocupa ~30-40% do canvas total e ~60% da altura na zona de bleed.

## Template de prompt

```
[serious confidence / pensive reflection] portrait of a brazilian {audience},
{age_range}, {clothing},
{action_describing_decision_moment},
warm window light, soft shadows,
rule of thirds, subject right, decision-maker looking left out of frame,
warm earth tones with mustard accent,
photographed in {environment},
shallow depth of field, shot on Hasselblad H6D-100c, 80mm lens,
editorial photography, 4K, sharp focus on eyes,
no text, no logos, sujeito íntegro
```

## Exemplos preenchidos por persona

### Empresário varejo médio

```
serious confidence portrait of a brazilian retail entrepreneur,
45-50, wool jacket over open dress shirt,
hand resting on countertop, gaze out window,
warm window light, soft shadows,
rule of thirds, subject right, looking left out of frame,
warm earth tones with mustard accent,
photographed in a furniture showroom with wood textures,
shallow depth of field, shot on Hasselblad H6D-100c, 80mm lens,
editorial photography, 4K, sharp focus on eyes,
no text, no logos, sujeito íntegro
```

### Founder tech / Tiago founder-led

```
pensive reflection portrait of a brazilian tech founder,
38-45, plain dark t-shirt, minimal frame glasses,
seated at modern wooden desk, hand on chin,
golden hour rim light through large window,
subject right, looking left toward laptop slightly off-frame,
desaturated muted editorial dark,
photographed in a modern home office with paper texture wall,
shallow depth of field, shot on Leica SL2, 35mm Summilux,
editorial photography, 4K, sharp focus on eyes,
no text, no logos, sujeito íntegro
```

### Diretor B2B serviços

```
calm authority portrait of a brazilian service-business director,
50-55, navy suit jacket no tie,
hand on table edge, mid-thought expression,
overhead diffused neutral light,
rule of thirds, subject right, looking down at notes off-frame,
cool steel blue dim corporate palette,
photographed in a small meeting room with dark wood table,
shallow depth of field, shot on Sony A7R V, 85mm GM f/1.4,
editorial photography, 4K, sharp focus on eyes,
no text, no logos, sujeito íntegro
```

### Empresária

```
quiet exhaustion portrait of a brazilian woman entrepreneur,
40-48, sober blazer, subtle jewelry,
seated near window, paperwork blurred in background,
soft window light from left,
subject right, looking down at hands,
warm earth tones,
photographed in a small office with venetian blinds,
shallow depth of field, shot on Canon R5, 50mm f/1.2L,
editorial photography, 4K, sharp focus on eyes,
no text, no logos, sujeito íntegro
```

## Reference images (passar pro Nano Banana 2)

Quando rodar Nano Banana 2, anexar 1-2 destas referências do banco Figma:

- `figma://1:704` — homem pensativo em ação, bleed direita
- `figma://1:1204` — empresário em situação reflexiva
- `figma://1:1216` — close editorial vertical

URLs reais devem ser geradas via Figma API ao rodar (não hardcoded aqui — refs do banco mudam de posição).

## Negative prompt específico

Além do base, adicionar:

- no people facing camera with eye contact (raro)
- no group photo
- no laptop in foreground (cliché stock)
- no whiteboard / sticky notes background

## Iteração se não bater

1. Trocar mood pra outro vocabulário do `_base.md` §Mood
2. Mudar `subject right` pra `subject bottom` (bleed bottom em vez de direita)
3. Ajustar idade do persona ±5 anos
4. Trocar câmera (mais wide → 35mm; mais tight → 85mm)

## Versão

`style-A_v1.0` · 2026-05-13 · Head de Design Metta
