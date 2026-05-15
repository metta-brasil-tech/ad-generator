# Image Prompt — Estilo B (Foto top + headline mixed bottom)

> Herda de `_base.md`. Use junto.

## Função da imagem nesse estilo

Foto top **abre o cenário emocional**. Pessoa na foto está VIVENDO a situação descrita na copy — é "cinema curto". Decisor reconhece a cena antes do texto bater.

A foto AQUI é narrativa, ao contrário do Estilo A onde foto é só âncora.

## Constraints do estilo B

- **Sempre evoca a tese literalmente.** "Refém do operacional" → pessoa exausta deitada no sofá com saco na cabeça. "Reunião sem fim" → pessoa em sala fechada com cara cansada. **A foto traduz a metáfora**.
- **Bleed top.** Foto preenche todo o top 40-50% do canvas. Sem margem entre foto e borda superior.
- **Gradiente fade-to-black** no bottom 30% pra texto ficar legível.
- **Mood quiet exhaustion ou pensive reflection.** Raramente serious confidence (B é mais emocional).
- **Filtros:** saturação 0 (natural), contrast +0.2.
- **Ratio:** próximo a 16:9 horizontal (cena cinematográfica).

## Template de prompt

```
[quiet exhaustion / pensive reflection] {scene_description},
brazilian {audience}, {age_range}, {clothing},
{specific_situation_metaphor},
{lighting},
{composition_cinematic},
{palette},
photographed in {environment_specific_to_metaphor},
shallow depth of field, shot on Leica SL2, 35mm Summilux,
editorial photography, 4K, cinematic intimacy,
no text, no logos, sujeito íntegro
```

## Exemplos preenchidos por tese

### "Refém do operacional / exaustão visível"

```
quiet exhaustion cinematic scene,
brazilian retail entrepreneur, 45-50, wrinkled dress shirt rolled sleeves,
slumped on dark leather couch, head in hands, work bag spilling papers on floor,
warm window light from left, late afternoon,
wide environmental shot, subject centered, room context visible,
desaturated muted editorial dark,
photographed in a tired home office with closed venetian blinds,
shallow depth of field, shot on Leica SL2, 35mm Summilux,
editorial photography, 4K, cinematic intimacy,
no text, no logos, sujeito íntegro
```

### "Pressão do calendário / agenda imposta"

```
pensive reflection cinematic scene,
brazilian service-business director, 42-48, dark turtleneck,
standing by office window, looking at watch with concern, phone face-down on desk,
golden hour rim light through window,
subject right, environmental context left (papers scattered desk),
warm orange-amber golden grading,
photographed in a high-floor corporate office at sunset,
shallow depth of field, shot on Sony A7R V, 85mm GM f/1.4,
editorial photography, 4K, cinematic intimacy,
no text, no logos, sujeito íntegro
```

### "Mantra-algema desmontado / questionando o próprio modelo"

```
pensive reflection cinematic scene,
brazilian woman entrepreneur, 40-48, simple white blouse,
seated at café table, coffee gone cold, notebook open with crossed-out lines,
soft diffused window light,
centered composition, subject medium close, hands visible,
warm earth tones with mustard accent,
photographed in a quiet morning café with wooden interior,
shallow depth of field, shot on Hasselblad H6D-100c, 80mm lens,
editorial photography, 4K, cinematic intimacy,
no text, no logos, sujeito íntegro
```

### "Solidão da decisão / peso de liderar"

```
quiet exhaustion cinematic scene,
brazilian founder, 38-45, dark hoodie zipped halfway,
seated alone in empty conference room, chair facing window away from camera, view of city dusk,
cold backlight from window,
wide environmental, subject small in frame,
cool steel blue dim corporate palette,
photographed in a high-rise empty meeting room after hours,
shallow depth of field, shot on Leica SL2, 35mm Summilux,
editorial photography, 4K, cinematic intimacy,
no text, no logos, sujeito íntegro
```

## Reference images (passar pro Nano Banana 2)

- `figma://1:229` — homem deitado no sofá com saco na cabeça (mais icônico)
- `figma://1:566` — Tiago pensativo (founder-led)
- `figma://1:865` — provocação direta com foto

## Negative prompt específico

Além do base:

- no anonymous suit-and-tie generic (precisa de roupa específica que ancora o personagem)
- no faces blurred / hidden completely (vê metade do rosto mínimo)
- no obvious stock posing (mãos no quadril, cruzando os braços confidente)
- no team setting (B é solitário)

## Iteração se não bater

1. **Foto muito stock** → adicionar detalhes específicos do ambiente (papers scattered, coffee gone cold)
2. **Metáfora fraca** → reescrever `{specific_situation_metaphor}` com cena mais literal da tese
3. **Mood errado** → trocar entre exhaustion / reflection / authority — B é predominantemente exhaustion+reflection
4. **Foto plana** → mudar pra wide environmental e ler "solidão na escala"

## Versão

`style-B_v1.0` · 2026-05-13 · Head de Design Metta
