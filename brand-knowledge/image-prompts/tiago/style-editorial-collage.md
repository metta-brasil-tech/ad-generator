# Image Prompt — Estilo TIAGO-EDITORIAL-HERO / TIAGO-EDITORIAL-CARD

> Herda de `_base-tiago.md` mas com mood **completamente diferente**: cinema editorial colagem surreal,
> NÃO documental snap. Use este template SOMENTE pros estilos editoriais (HERO, CARD).

## Função da imagem nesse estilo

Colagem cinema surreal/editorial que serve de **metáfora visual** pra tese do slide. NUNCA fotografia
documental aqui — o estilo pede figura recortada estilo revista anos 60-70 com elementos surreais:

- Sujeito decapitado/sem rosto (cabeça substituída por fumaça, raio amarelo, TV, fogo)
- Sujeito com PARTES DO CORPO pintadas em amarelo solid #FFCC00 (estilo recorte editorial vintage)
- Animal ou objeto com elemento estranho (peixe com nadadeira de tubarão amarrada, esqueleto T-Rex)
- Múltiplas mãos saindo de torso (sobrecarga, multitarefa)
- Objeto-metáfora isolado sobre fundo neutro (caveira animal, pedra, poltrona com sujeito sem rosto)

Mood: B&W base + selective yellow paint + grain noise. Visual de magazine editorial brasileira premium.

## Constraints do estilo

- **Aspect-ratio:** livre (1:1, 4:5, 3:4). Vai entrar em zonas de bleed do canvas.
- **Mood:** noir editorial cinema, surreal, B&W base, accent amarelo solid.
- **Subject:** humano decapitado/sem rosto OU objeto-metáfora isolado.
- **Background:** quando isolado, fundo neutro cinza claro com grain noise. Quando integrado, transparente.
- **Filter:** dessaturação heavy (-0.5 a -0.7), contrast +0.3, grain noise, selective yellow paint.

## Template de prompt

```
Editorial collage in the style of a 1960s-70s Brazilian premium magazine,
{subject_description},
photographed in high-contrast black and white,
with selective yellow paint (Pantone Yellow 012, #FFCC00) applied flatly over {body_parts_yellow},
grainy magazine print texture,
neutral light gray background with paper grain noise,
isolated subject with hard cut-out edges (vintage collage feel),
surreal magazine art direction (think: New York Times Magazine, Folha Magazine),
overhead diffused studio light, deep shadows controlled,
no realistic full-color rendering, no photo-real skin tone outside yellow paint zones,
no logos, no text in image,
Fujifilm GFX 100 100mm equivalent, magazine editorial 4K
```

## Exemplos preenchidos

### Exemplo 1 — Homem decapitado com fumaça (Geração Z capa)

> Tese: "A Geração Z não quer trabalhar" (citação a desmontar)

```
Editorial collage in the style of a 1960s-70s Brazilian premium magazine,
A man in a dark formal black business suit kneeling on one knee, holding a briefcase,
HEAD COMPLETELY REPLACED BY THICK DARK SMOKE rising from the suit collar,
photographed in high-contrast black and white grayscale,
with selective yellow paint (Pantone Yellow 012) applied flatly over the shirt collar pattern,
grainy magazine print texture, paper grain visible,
neutral light gray background with paper grain noise,
isolated subject with hard cut-out edges,
surreal magazine art direction,
overhead diffused studio light, deep shadows,
no realistic head, no face visible (smoke replaces head entirely),
no logos, no text in image,
Fujifilm GFX 100, magazine editorial 4K
```

### Exemplo 2 — Peixe com nadadeira de tubarão amarrada (Liderança capa)

> Tese: "Liderança não é fantasia"

```
Editorial collage in the style of a 1960s-70s Brazilian premium magazine,
A common goldfish or small white fish underwater,
with a LARGE BLACK SHARK FIN strapped to its back using two visible leather belts with metal buckles,
photographed in high-contrast black and white grayscale,
half submerged with waterline visible mid-image,
grainy magazine print texture, paper grain visible,
neutral light gray background with paper grain noise above water,
isolated subject with hard cut-out edges (vintage collage feel),
surreal magazine art direction,
soft natural overhead light from above water,
no real shark, no realistic ocean,
no logos, no text in image,
Fujifilm GFX 100, magazine editorial 4K
```

### Exemplo 3 — Homem sem rosto em poltrona amarela (Método de Jesus capa)

> Tese: "Por que o seu time não bate meta mesmo quando você cobra todo dia"

```
Editorial collage in the style of a 1960s-70s Brazilian premium magazine,
A man in dark formal business suit sitting CROSS-LEGGED in a YELLOW vintage armchair,
HEAD COMPLETELY ERASED or replaced by FLAT MUSTARD YELLOW PAINT silhouette,
hands visible holding the armchair sides,
photographed in high-contrast black and white grayscale,
with selective yellow paint (Pantone Yellow 012, #FFCC00) applied flatly over the armchair upholstery,
grainy magazine print texture,
neutral light gray background with paper grain noise,
isolated subject with hard cut-out edges,
surreal magazine art direction,
overhead diffused studio light, deep shadows,
no realistic face, no head visible (yellow paint blob replaces it),
no logos, no text in image,
Fujifilm GFX 100, magazine editorial 4K
```

### Exemplo 4 — Esqueleto T-Rex (Geração Z slide intermediário "jurássico")

> Tese: "O padrão de formar vendedor no Brasil é jurássico"

```
Editorial photograph in the style of a 1960s-70s magazine science section,
A complete T-Rex fossil skeleton, side profile, mouth open showing teeth,
photographed in high-contrast black and white grayscale,
grainy magazine print texture,
neutral light gray background with paper grain noise,
isolated subject with sharp cut-out edges,
museum exhibit lighting (overhead soft diffused),
no color, no modern museum signage, no logos, no text,
slight magazine paper grain texture overlay,
Fujifilm GFX 100, magazine editorial 4K
```

### Exemplo 5 — Sujeito multitarefa (Funcionário slide 3 "apagador de incêndio")

> Tese: "Você vira o melhor vendedor. O gerente de fato. O apagador de incêndio."

```
Editorial collage in the style of a 1960s-70s Brazilian premium magazine,
A man in dark business suit sitting with crossed legs,
WITH SIX EXTRA ARMS extending from his torso each holding different objects:
old rotary telephone, vintage calculator, stack of cash bills, fire extinguisher, briefcase, pen,
HEAD VISIBLE with glasses and serious expression looking down,
photographed in high-contrast black and white grayscale,
with selective yellow paint (Pantone Yellow 012, #FFCC00) applied flatly on the suit lapels and the cash bills,
grainy magazine print texture,
neutral light gray background with paper grain noise,
isolated subject with hard cut-out edges (vintage Dada collage feel),
surreal magazine art direction,
overhead diffused studio light, deep shadows controlled,
no logos, no text in image,
Fujifilm GFX 100, magazine editorial 4K
```

## Reference images (passar pro Nano Banana 2)

Quando disponíveis no exemplar set, passar 1-2 PNGs de `brand-knowledge/exemplars/tiago/TIAGO-EDITORIAL-HERO/` ou `TIAGO-EDITORIAL-CARD/` pra style transfer.

## Negative prompt específico

```
no realistic color photography, no full-color skin, no smile, no eye contact with camera,
no studio fashion glamour, no commercial polish, no modern HDR look,
no AI-render plastic skin, no symmetric staged composition,
no clean white background (use grain noise neutral gray),
no clean cut digital edges (prefer torn-paper vintage cut),
no Hasselblad cinema mood (this is magazine editorial, NOT cinema),
no logos visible, no brand markings, no readable text in image,
no full-saturation yellow (selective only)
```

## Iteração se não bater

- **v1:** prompt principal acima
- **v2 (fallback):** reduzir `selective yellow paint` pra só 1 elemento (ex: só armchair OU só shirt collar) — Nano Banana às vezes pinta tudo
- **v3 (fallback):** simplificar sujeito pra apenas a metáfora visual sem corpo humano (ex: só "armchair empty in spotlight" em vez de "man in armchair")

## Quando NÃO usar este prompt

- Variant `content` puro de qualquer estilo Tiago — `image_required: false`
- TIAGO-TWITTER-CARD — usa `style-twitter-card.md` (snapshot documental)
- TIAGO-EDITORIAL-DARK — usa `style-editorial-dark.md` (close-up noir cinema, não colagem)
- TIAGO-EDITORIAL-CTA variant B — usa foto REAL do Tiago (não gerada)

## Versão

`style-editorial-collage_v1.0` · 2026-05-14 · Head de Design Metta
