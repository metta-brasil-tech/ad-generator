# Image Prompt — Estilo D (Foto full-bleed + overlay escuro)

> Herda de `_base.md`. Use junto.

## Função da imagem nesse estilo

Foto **DOMINA** o frame inteiro. A pessoa É o ad — ela te conta a mensagem pela presença. Imersão total. Funciona pra emoção forte (dor pessoal, peso de decisão).

Diferença vs B: em B a foto é cena CONTEXTUALIZADA (com ambiente, objetos); em D a foto é RETRATO IMERSIVO (close ou meio-close, pessoa preenche o frame).

## Constraints do estilo D

- **Full-bleed.** Foto ocupa 100% do canvas. Não tem margem.
- **Overlay gradient fade-to-black** nos 40-50% inferiores pra texto ficar legível.
- **Filtros pesados.** Saturação -0.3, contrast +0.5 — moody, cinematográfico.
- **Olhar fora-de-quadro ou pra baixo.** NUNCA olhando direto pra câmera (rouba autoridade do leitor).
- **Mood pensive reflection ou cinematic intimacy.** Carrega peso emocional.
- **Ratio 9:16 fixo.** É um story imersivo.

## Template de prompt

```
[pensive reflection / cinematic intimacy] vertical portrait of a brazilian {audience},
{age_range}, {clothing},
{introspective_action},
{moody_lighting},
medium close-up vertical, subject fills frame,
gaze looking down or out of frame, never direct to camera,
{moody_palette},
photographed in {ambient_environment},
shallow depth of field, shot on {cinematic_camera},
cinematic moody editorial, 4K, dark grading,
designed for 9:16 story format, lower 40% area composition should work with dark overlay,
no text, no logos, sujeito íntegro
```

## Exemplos preenchidos por tese

### "Dor pessoal — exaustão da solidão do CEO"

```
pensive reflection vertical portrait of a brazilian retail entrepreneur,
45-52, simple dark sweater, no tie,
hands clasped, looking down at the floor with slight forward lean,
hard side light editorial moody, single window source from camera left,
medium close-up vertical, subject fills frame from chest up,
gaze down and slightly away from camera,
desaturated muted editorial dark with steel blue undertone,
photographed in a dim home office at night, single lamp behind subject,
shallow depth of field f/1.4, shot on Leica SL2 35mm Summilux,
cinematic moody editorial, 4K, dark grading,
designed for 9:16 story format, lower 40% area should be empty for dark text overlay,
no text, no logos, sujeito íntegro
```

### "Peso da decisão / momento antes de virar a página"

```
cinematic intimacy vertical portrait of a brazilian woman entrepreneur,
40-50, structured black blazer over simple top,
mid-action of slowly turning notebook page, eyes tracking the gesture,
warm window light editorial moody from camera right,
medium close-up vertical, subject from waist up,
gaze on the page in hand, never camera,
warm earth tones with deep amber shadows,
photographed in a wood-paneled office with old books in background blur,
shallow depth of field, shot on Hasselblad H6D-100c 80mm lens,
cinematic moody editorial, 4K, dark grading,
designed for 9:16 story format, lower 40% area should be empty for dark text overlay,
no text, no logos, sujeito íntegro
```

### "Tese poética / Lovebrand intimista"

```
cinematic intimacy vertical portrait of a brazilian founder,
38-45, plain dark crew-neck,
seated against textured concrete wall, deep exhale moment captured,
golden hour rim light from camera left, single source moody,
medium close-up vertical, subject from shoulders up,
gaze unfocused into middle distance off-camera,
warm orange-amber golden grading with deep shadows,
photographed in a converted industrial loft, raw concrete texture wall,
shallow depth of field f/1.2, shot on Canon R5 50mm f/1.2L,
cinematic moody editorial, 4K, dark grading,
designed for 9:16 story format, lower 40% area should be empty for dark text overlay,
no text, no logos, sujeito íntegro
```

## Reference images (passar pro Nano Banana 2)

- `figma://1:487` — homem refém da operação, moody
- `figma://1:1159` — método tira loja das costas, emocional
- `figma://538:105` — limite da exaustão, Aplicação

## Negative prompt específico

Além do base:

- no direct eye contact with camera (rouba autoridade do leitor)
- no bright lighting (D é moody)
- no busy background (subject DOMINATES)
- no group, no second person in frame
- no luxury markers (relógio caro, marca aparente) — gravidade > status
- no smile, no half-smile

## Iteração se não bater

1. **Foto muito brilhante** → reforçar `moody`, `dark grading`, `shadows`, `single source lighting`
2. **Sujeito sumido no fundo** → mudar pra `subject fills frame`, `close-up`
3. **Olhar errado** → reforçar `gaze down`, `gaze out of frame`, `never direct to camera`
4. **Sem peso emocional** → trocar mood entre `pensive reflection` ↔ `cinematic intimacy` ↔ `quiet exhaustion`

## Versão

`style-D_v1.0` · 2026-05-13 · Head de Design Metta
