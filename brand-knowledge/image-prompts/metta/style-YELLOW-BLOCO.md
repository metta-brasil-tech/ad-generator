# Image Prompt — Estilo YELLOW-BLOCO

> Herda de `_base.md`. Use junto.

## Função da imagem nesse estilo

Foto pessoa **à direita bleed corner** comunica "eu" (founder-led ou líder identificável). Não é narrativa, é assinatura humana. Logo bar no topo carrega a credibilidade institucional — a foto é só "quem está falando com você".

Diferença vs A: aqui o bloco amarelo é o protagonista, foto é coadjuvante. Em A a foto é segundo elemento mais importante.

## Constraints do estilo YELLOW-BLOCO

- **Right-corner bleed.** Foto sai pela direita E pelo bottom. Tipo "saindo do retrato pra apertar a mão de quem lê".
- **Mood calm authority ou serious confidence.** Convite institucional — não pode ser exhaustion (destrói a oferta).
- **Roupa profissional.** Smart-casual ou business casual. Nunca camiseta lisa, nunca terno completo de gala.
- **Olhar pode ser direto** (assertivo institucional) **ou pra dentro do canvas** (engajamento com o conteúdo amarelo).
- **Filtros leves.** Saturação 0, contrast +0.15 — pessoa parece natural, não moody.
- **Background neutro claro** (combina com fundo branco/cinza claro do ad).

## Template de prompt

```
[calm authority / serious confidence] portrait of a brazilian {audience},
{age_range}, {smart_casual_clothing},
{engaged_posture},
warm diffused light or overhead diffused neutral,
right-corner composition, subject occupies right 40% of frame,
gaze toward camera or slightly into left frame (engaging with content),
warm earth tones or neutral with slight warm cast,
photographed in {neutral_professional_environment},
shallow depth of field, shot on Sony A7R V 85mm GM f/1.4,
clean editorial portrait, 4K, sharp focus on eyes,
background simple and uncluttered to keep focus on subject,
no text, no logos, sujeito íntegro
```

## Exemplos preenchidos

### Tiago founder-led — convite institucional

```
calm authority portrait of a brazilian tech founder Tiago Alves,
40-45, navy blazer over white t-shirt,
relaxed standing pose, hands in pockets, slight smile of confidence,
warm diffused window light from camera left,
right-corner composition, subject occupies right 40% of frame from waist up,
gaze toward camera, direct but warm engagement,
neutral palette with slight warm cast,
photographed against a clean off-white textured wall in a modern studio,
shallow depth of field, shot on Sony A7R V 85mm GM f/1.4,
clean editorial portrait, 4K, sharp focus on eyes,
background simple and uncluttered,
no text, no logos, sujeito íntegro
```

### Líder comercial — convite pra evento

```
serious confidence portrait of a brazilian commercial team leader,
38-45, smart business shirt rolled sleeves, no tie,
arms crossed lightly, professional engaged posture,
overhead diffused neutral light,
right-corner composition, subject right 40% of frame,
gaze slightly into left frame (toward where event info will go),
warm earth tones,
photographed in a modern co-working space with subtle bokeh background,
shallow depth of field, shot on Canon R5 50mm f/1.2L,
clean editorial portrait, 4K, sharp focus on eyes,
background simple and uncluttered,
no text, no logos, sujeito íntegro
```

### Empresária — oferta com sub-benefícios

```
calm authority portrait of a brazilian woman entrepreneur,
42-48, structured camel blazer over silk blouse, minimal jewelry,
seated edge-of-chair posture, engaged forward lean, hands on knee,
warm window light from camera left,
right-corner composition, subject right 40% of frame from waist up,
gaze direct to camera with slight smile of confidence,
warm earth tones with mustard accent,
photographed in a quiet executive lounge with wood textures,
shallow depth of field, shot on Hasselblad H6D-100c 80mm lens,
clean editorial portrait, 4K, sharp focus on eyes,
background simple and uncluttered,
no text, no logos, sujeito íntegro
```

## Reference images (passar pro Nano Banana 2)

- `figma://1:78` — flagship com Sicredi/Vivo (mais icônico)
- `figma://1:1021` — variação institucional com líder mulher
- `figma://1:987` — convite com bullets, founder-led

## Negative prompt específico

Além do base:

- no moody dark grading (YELLOW-BLOCO é claro)
- no dramatic shadows
- no exhaustion / quiet exhaustion mood
- no full-bleed background (precisa de neutro pra não competir com bloco amarelo)
- no industrial / raw environment (estética é "executiva profissional", não "founder roots")

## Diferença visual chave vs A

| Aspecto | A | YELLOW-BLOCO |
|---|---|---|
| Mood | serious / pensive | calm authority |
| Bg da foto | dark moody | neutro claro |
| Olhar | quase sempre off-camera | pode ser direto |
| Saturação | -0.2 | 0 (natural) |
| Função | âncora humana sobre dark | assinatura sobre claro |

## Iteração se não bater

1. **Foto muito moody** → reduzir saturation delta pra 0, aumentar brightness
2. **Background competindo** → simplificar `{neutral_professional_environment}` (paper texture wall, off-white concrete)
3. **Pessoa rígida demais** → mudar `engaged_posture` pra mais relaxada
4. **Foto não combina com vibe institucional** → reforçar `clean editorial portrait`, `professional engaged`

## Versão

`style-YELLOW-BLOCO_v1.0` · 2026-05-13 · Head de Design Metta
