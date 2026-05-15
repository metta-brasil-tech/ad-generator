# Image Prompt — Estilo TIAGO-PHOTO-RAW

> Herda de `_base-tiago.md`. Foto crua sem texto — bastidor de vida real.

## Função da imagem nesse estilo

A foto **É** o post. Não tem copy, não tem overlay, não tem produção. Selfie ou flagrante real do Tiago em contexto pessoal — treino (jiu-jitsu, academia), viagem, família, comunidade, refeição, ritual cotidiano.

Esse estilo serve pra **humanização alta**, prova social comunitária, "olha o que ele tá fazendo na vida". Engajamento via curtida/comentário, não via leitura.

## Constraints do estilo

- **Aspect-ratio:** livre — 1:1, 4:5, 9:16 conforme o momento natural da foto
- **Mood:** autêntico, sem edição, capturado mid-moment
- **Lighting:** natural — luz de academia, luz de viagem, luz de mesa. NÃO golden hour, NÃO studio.
- **Subject:** Tiago em contexto pessoal — pode ser ele sozinho (selfie), com amigos, com família, com time
- **Filtro:** zero — saturação e contraste naturais. Não tem grade colorimétrica.
- **Bleed:** sim, 100%
- **Edição:** mínima. Pode haver levíssimo crop, mas nada de retoque facial, dodge/burn, color grade

## Template de prompt

```
candid phone selfie of a brazilian businessman in his 40s,
{contexto_pessoal} with {pessoas_ou_objetos},
{ambiente},
natural existing lighting, no studio setup,
unedited candid moment, slight motion blur acceptable,
shot with iPhone 15 main camera in normal photo mode,
casual happy expression, not posed for ad,
no professional retouch, no color grade, no filter,
no brand logos visible, no text overlay
```

## Exemplos preenchidos

### Exemplo 1 — Jiu-jitsu com amigos (ref image 25)

> Momento: pós-treino com a turma

```
candid phone selfie of a brazilian businessman in his 40s,
wearing a blue jiu-jitsu gi (kimono), arm around three teammates also in white gis,
inside a martial arts academy with mats and equipment slightly out of focus behind,
fluorescent overhead lighting natural, soft shadows on faces,
muted blue and white palette with natural skin tones,
shot vertically 4:5 selfie-style arm-extended angle,
iPhone 15 main camera normal mode, unedited candid moment,
all wearing happy post-training smiles, sweat visible, not posed for ad,
no professional retouch, no color grade, no filter,
no brand logos visible, no overstyled scene
```

### Exemplo 2 — Viagem família

> Momento: férias com a esposa em destino brasileiro

```
candid phone selfie of a brazilian businessman in his 40s with his wife,
both wearing casual vacation clothes (linen shirt, sundress),
brazilian coastal background with sea and palm trees out of focus,
warm afternoon natural light, soft natural shadows,
warm coastal palette with natural skin tones,
shot square 1:1 selfie-style arm-extended angle,
iPhone 15 main camera normal mode, unedited candid moment,
both wearing relaxed happy expressions (not influencer-posed),
slight motion in hair from sea breeze, slight grain,
no professional retouch, no color grade, no filter,
no logos visible, no overstyled vacation aesthetic
```

### Exemplo 3 — Mesa refeição com time

> Momento: jantar pós-evento com mentorados

```
candid phone photo of a dinner table at a brazilian restaurant,
six people sitting around the table with plates and wine glasses,
warm overhead pendant lighting from above center,
warm brown and amber palette with natural food and skin tones,
shot square 1:1 from the end of the table chest-height,
iPhone 15 main camera normal mode, unedited candid moment,
all in mid-conversation, not posed, some looking at camera some not,
slight motion blur on a gesture, lo-fi authentic mood,
no professional retouch, no color grade, no filter,
no logos visible, no restaurant-marketing aesthetic
```

### Exemplo 4 — Ritual pessoal cedo (corrida, academia, etc.)

> Momento: começo de dia disciplinado

```
candid phone photo of a brazilian businessman in his 40s after a morning run,
sweating in athletic shirt and shorts standing on a quiet urban sidewalk,
brazilian residential street with low buildings and trees in background,
early morning natural daylight, long natural shadows,
muted earth tones with natural skin tones,
shot vertically 9:16 selfie-style arm-extended angle,
iPhone 15 main camera normal mode, unedited candid moment,
slight motion blur, casual breathless smile (not posed for ad),
no professional retouch, no color grade, no fitness-influencer aesthetic,
no logos visible, no studio look
```

## Reference images

- `brand-knowledge/exemplars/tiago/PHOTO-RAW/01-jiu-jitsu-amigos.png`

## Negative prompt específico

```
no professional studio lighting,
no Hasselblad cinema,
no color grade or LUT,
no influencer-pose aesthetic,
no advertisement scene,
no perfectly framed composition,
no eye contact perfect-smile pose,
no over-styled outfit,
no editorial magazine look,
no AI-render artifacts,
no over-sharpened HDR,
no brand logos in foreground
```

## Iteração se não bater

- **v1:** prompt principal
- **v2:** simplificar — só `subject` + `ambiente` + `iPhone candid`
- **v3:** trocar pra `iPhone 13 normal mode` se Nano Banana der look novo demais

## Versão

`style-photo-raw_v1.0` · 2026-05-15 · Head de Design Metta
