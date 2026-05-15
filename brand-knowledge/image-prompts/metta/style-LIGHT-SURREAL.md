# Image Prompt — Estilo LIGHT-SURREAL

> Herda de `_base.md`. **OBS:** este estilo NÃO usa foto realista — usa COLAGEM SURREAL. Prompt difere do padrão.

## Função da imagem nesse estilo

Colagem surreal **personifica visualmente a metáfora da dor descrita na copy**. Homem com cabeça de pedra = "pesa pensar". Cabeça de monitor = "vive plugado no operacional". Balão saindo do crânio = "ideia voando solta".

A imagem é THUMBNAIL EDITORIAL — entende-se em 1 segundo. Estética HBR/Exame, não cartoon.

## Constraints do estilo LIGHT-SURREAL

- **Foto-base + justaposição surreal.** SEMPRE foto real recortada e remontada com elemento incongruente. NUNCA ilustração vetorial chapada. NUNCA cartoon. NUNCA 3D render.
- **Background neutro claro.** Fundo de papel texture, parede off-white ou cinza muito claro.
- **Mood editorial gravitas** — peso de capa de revista séria. Não brincadeira.
- **Filtros sutis.** Saturação 0, contrast +0.1.
- **Composição centrada ou rule-of-thirds** — colagem é o protagonista visual.
- **Ratio livre** — geralmente quadrado ou 4:5.

## Template de prompt

```
editorial collage surreal portrait, brazilian style HBR-Exame magazine,
photo-real base of {subject_with_metaphor_element_swapped},
{specific_collage_concept},
neutral light flat editorial,
centered composition or rule of thirds,
clean cut-out edges visible, intentional collage aesthetic,
warm paper texture background, slight cream tint,
shot on medium format,
editorial gravitas, 4K, magazine cover quality,
no cartoon, no vector illustration, no 3D render, no anime,
no text, no logos
```

## Exemplos preenchidos por metáfora

### "Vive plugado no operacional / cabeça-monitor"

```
editorial collage surreal portrait, brazilian style HBR-Exame magazine,
photo-real base of a man in business shirt seated at desk,
his head replaced with a vintage CRT computer monitor showing static, body remaining photorealistic,
the monitor head tilts slightly as if 'thinking',
neutral overhead diffused light, flat editorial,
centered composition,
clean cut-out edges visible where monitor meets neck, intentional collage aesthetic,
warm paper texture background off-white with cream tint,
medium format quality,
editorial gravitas, 4K, magazine cover quality,
no cartoon, no vector illustration, no 3D render, no anime,
no text, no logos
```

### "Pesa pensar / cabeça de pedra"

```
editorial collage surreal portrait, brazilian style HBR-Exame magazine,
photo-real base of a man in dark sweater seated forward at table,
his head replaced with a heavy gray boulder, body posture sagging slightly under weight,
hands clasped supporting the boulder head,
neutral side light editorial flat,
rule of thirds composition, subject slightly left,
clean cut-out edges visible where boulder meets neck,
warm paper texture background light gray,
medium format quality,
editorial gravitas, 4K, magazine cover quality,
no cartoon, no vector illustration, no 3D render, no anime,
no text, no logos
```

### "Ideia voando solta / balão saindo do crânio"

```
editorial collage surreal portrait, brazilian style HBR-Exame magazine,
photo-real base of a woman entrepreneur in profile against neutral wall,
the top of her head opens like a hinge, a single helium balloon escapes upward toward the sky,
her gaze unfocused as if accepting the escape,
warm flat editorial light,
profile composition subject left, balloon trail upper right,
clean cut-out edges visible at the hinge, intentional collage,
warm paper texture background slightly cream,
medium format quality,
editorial gravitas, 4K, magazine cover quality,
no cartoon, no vector illustration, no 3D render, no anime,
no text, no logos
```

### "Família esquecida / jantar como holograma"

```
editorial collage surreal portrait, brazilian style HBR-Exame magazine,
photo-real base of a man in suit jacket seated at dining table,
the dinner table and family chairs appear as translucent semi-faded photographic ghosts,
the man solid and present but everyone else partially erased,
warm dim window light, late evening,
centered composition,
clean cut-out edges where family fades, intentional editorial collage,
warm paper texture background slightly cream-yellow,
medium format quality,
editorial gravitas, 4K, magazine cover quality,
no cartoon, no vector illustration, no 3D render, no anime,
no text, no logos
```

## Reference images (passar pro Nano Banana 2)

- `figma://1:220` — homem-pedra no computador (jantar com filhos vs reunião)
- `figma://1:477` — colagem familiar (negócio saúde família)
- `figma://1:1151` — metáfora de crescimento (varejistas dobram tamanho)

## Negative prompt específico

Além do base, ESPECIAL pra esse estilo:

- no cartoon, no vector illustration, no anime style
- no 3D rendered scenes, no CGI
- no Pixar style, no Dreamworks style
- no minimalist flat design
- no chapado / no flat color blocks
- no Photoshop obvious filter (oil paint, watercolor)
- no AI-generic surrealism (giant moon, floating eye) — precisa ser metáfora ESPECÍFICA da copy

## O que faz diferente vs Photoshop random surrealism

LIGHT-SURREAL Metta é:

1. **Foto-real base.** Tudo começa de foto real, depois UM elemento é trocado.
2. **Metáfora literal da copy.** Não é estética genérica, é a tradução visual da tese.
3. **Cut-out edges visíveis.** Não esconde a colagem — celebra como editorial print.
4. **Editorial gravitas.** Peso de capa de revista. Não é brincalhão.

## Iteração se não bater

1. **Saiu cartoon** → reforçar `photo-real base`, `medium format quality`, listar todos os negative prompts de estilo
2. **Metáfora literal demais (sem surreal)** → especificar mais o elemento trocado: "head replaced with X", "Y instead of Z"
3. **Surreal sem ancoragem** → reforçar `body remaining photorealistic`, `clean cut-out edges visible`
4. **Mood errado (festivo)** → reforçar `editorial gravitas`, `magazine cover quality`, mudar palette pra mais neutro

## Versão

`style-LIGHT-SURREAL_v1.0` · 2026-05-13 · Head de Design Metta
