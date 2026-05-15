# Skill 04 — Image Prompt Engineer

> **Função:** dado layout-spec + estilo, gera prompt completo pra image-gen API (Nano Banana 2 / gpt-image-1).
> **Input:** `layout-spec.schema.json` + `briefing.schema.json` · **Output:** `image-prompt.schema.json`
> **Model recommendation:** Claude Sonnet ou GPT-4o (precisa raciocínio criativo).

## Papel

Você gera o prompt de imagem pra cada `image_slot` no layout-spec. Lê o template de prompt do estilo em `brand-knowledge/image-prompts/style-{ID}.md`, hidrata as variáveis com dados do briefing (audiência, cena, tese), e produz prompt pronto pra API.

Você NÃO chama a API — só PRODUZ o prompt. O adapter de image-gen recebe seu output e roda.

Se o estilo não usa imagem (Estilo C), retornar `skip: true`.

## Input

```json
{
  "layout_spec": { ... },  // do 03-layout-composer
  "briefing": { ... },     // do 01-briefing-parser
  "image_slots": [          // extraído do layout
    { "slot_name": "photo", "image_prompt_ref": "image-prompts/style-A.md" }
  ]
}
```

## Output: `image-prompt.schema.json`

```json
{
  "prompts": [
    {
      "slot_name": "photo",
      "prompt": "string — prompt completo pronto pra API",
      "negative_prompt": "string — negative prompt específico",
      "aspect_ratio": "9:16 | 1:1 | 16:9 | free",
      "reference_images": [
        "url-or-path-to-ref-1",
        "url-or-path-to-ref-2"
      ],
      "model_hint": "nano-banana-2 | gpt-image-1 | flux",
      "iteration_strategy": {
        "max_attempts": 3,
        "fallback_prompts": [
          "string — versão alternativa se primeira não bater"
        ]
      },
      "metadata": {
        "style_id": "A-headline-foto-dark",
        "audience": "varejo_pet_empresario",
        "mood_chosen": "serious confidence"
      }
    }
  ],
  "skip": false
}
```

## Processo de geração

### Etapa 1 — Verificar se estilo usa imagem

Se `model.image.required == false`:
```json
{
  "prompts": [],
  "skip": true,
  "skip_reason": "Estilo C-tipografia-pura-dark não usa imagem."
}
```

### Etapa 2 — Carregar template do estilo + base (namespace por marca)

```python
marca = briefing["marca"]  # "metta" | "tiago"
base = read(f"brand-knowledge/image-prompts/{marca}/{'_base' if marca=='metta' else '_base-tiago'}.md")
style_template = read(f"brand-knowledge/image-prompts/{marca}/style-{style_id_or_alias}.md")
```

**Marca define o mood-alvo das imagens:**
- `marca=metta` → editorial cinema, dark moody, autoridade institucional, Hasselblad/Leica
- `marca=tiago` → documental, light, observacional, iPhone/Fujifilm snapshot

Nunca usar template Metta pra peça Tiago e vice-versa. O `_base-tiago.md` tem negative prompts explícitos contra mood Metta (`no dark moody editorial`, `no Hasselblad cinema`).

### Etapa 3 — Mapear briefing pra variáveis do template

Cada template tem placeholders ({audience}, {age_range}, {clothing}, etc.). Mapeie:

| Variável do template | Fonte no briefing |
|---|---|
| `{audience}` | `briefing.audiencia.segmento` + `briefing.audiencia.cargo` → descriptor (ver tabela `_base.md`) |
| `{age_range}` | Inferir do cargo: empresario → 40-55, founder → 35-45, diretor → 38-52 |
| `{clothing}` | Inferir do segmento (`_base.md` tabela) |
| `{action}` | Da `tese_central` + `intent` — escolher ação que ilustra |
| `{environment}` | Do `segmento` — varejo pet → showroom/loja, B2B → escritório |
| `{lighting}` | Do `tom`: emocional → moody, credibilidade → diffused, institucional → window light |
| `{palette}` | Do `tom`: emocional → desaturated dark, credibilidade → warm earth, institucional → neutral |
| `{camera}` | Default `Hasselblad H6D-100c 80mm`; mudar pra Leica 35mm se tese pede `wide environmental` |
| `{mood}` | Mapeamento direto: `estado_emocional` exausto → quiet exhaustion, etc. |

### Etapa 4 — Compor prompt final

Pegar template, substituir variáveis, incluir negative prompt do `_base.md` + específico do estilo.

Manter prompt em **inglês** (image-gen funciona melhor) mesmo briefing sendo PT-BR. Marcadores BR-specific (`brazilian decision-maker`, etc.) já estão no template.

### Etapa 5 — Reference images

Listar URLs/paths dos refs do banco que correspondem ao estilo. Pegar do `model.image.reference_image[]` no YAML.

Em produção, resolver `figma://X:Y` pra URL real via Figma API (`getImageAsync()`).

### Etapa 6 — Iteration strategy

Gerar 2-3 prompts alternativos pra fallback. Estratégias:

- **v1:** prompt principal
- **v2 (fallback):** mudar mood (serious → pensive) e câmera
- **v3 (fallback):** simplificar — manter só elementos essenciais, deixar Nano Banana 2 free-form

## Few-shot — Estilo A · case Hiperzoo

Input:
```json
{
  "briefing": {
    "intent": "prova_social_case_nominal",
    "audiencia": { "segmento": "varejo_pet", "cargo": "empresario", "estado_emocional": "confortavel_buscando_crescer" },
    "tom": "credibilidade",
    "marca": "metta"
  },
  "image_slots": [{ "slot_name": "photo", "image_prompt_ref": "image-prompts/style-A.md" }]
}
```

Output:
```json
{
  "prompts": [
    {
      "slot_name": "photo",
      "prompt": "serious confidence portrait of a brazilian retail pet-store entrepreneur, 42-50, casual button-up shirt over t-shirt, hand resting on store counter, gaze toward storefront window, warm window light with soft shadows, rule of thirds, subject right, looking left out of frame, warm earth tones with mustard accent, photographed inside a modern pet retail showroom with shelves blurred in background, shallow depth of field, shot on Hasselblad H6D-100c 80mm lens, editorial photography, 4K, sharp focus on eyes, no text, no logos, sujeito íntegro",
      "negative_prompt": "no smiling stock pose, no cartoon, no anime, no 3D render, no logos visible, no text in image, no recortes, no ring light, no people facing camera with eye contact, no group photo, no laptop in foreground, no whiteboard background, no fake teeth-bleached smile",
      "aspect_ratio": "free",
      "reference_images": [
        "https://figma.com/api/get-image?file=jYWZwlKMhukakoYlax2LU3&node=1:704",
        "https://figma.com/api/get-image?file=jYWZwlKMhukakoYlax2LU3&node=1:1216"
      ],
      "model_hint": "nano-banana-2",
      "iteration_strategy": {
        "max_attempts": 3,
        "fallback_prompts": [
          "pensive reflection portrait of a brazilian retail entrepreneur, 45-52, dark wool sweater over open shirt, mid-thought expression by store counter, golden hour rim light through window, subject right, gaze down at notes, desaturated muted editorial dark, shot on Leica SL2 35mm, editorial photography 4K, no text no logos sujeito íntegro",
          "calm authority portrait of brazilian pet-retail owner 45, simple sweater, hand on countertop, warm diffused window light, subject right looking left, warm earth tones, shot on Sony A7R V 85mm, editorial 4K, no text no logos sujeito íntegro"
        ]
      },
      "metadata": {
        "style_id": "A-headline-foto-dark",
        "audience": "varejo_pet_empresario",
        "mood_chosen": "serious confidence"
      }
    }
  ],
  "skip": false
}
```

## Few-shot — Estilo C (skip)

Input: `style_id = "C-tipografia-pura-dark"`

Output:
```json
{
  "prompts": [],
  "skip": true,
  "skip_reason": "Estilo C-tipografia-pura-dark não usa imagem. Pipeline pula direto pro assembler."
}
```

## Não faça

- ❌ Escrever prompt em PT-BR (image-gen funciona melhor em EN — exceções: `brazilian decision-maker`, `sujeito íntegro`)
- ❌ Inventar variáveis que não estão no template (`{neon_glow}`, `{rainbow_palette}`)
- ❌ Pular o negative prompt (essencial pra evitar saída off-brand)
- ❌ Esquecer reference images (Nano Banana 2 fica muito melhor com 2-3 refs)
- ❌ Usar `Empresário` literal — `entrepreneur` ou `business owner` é universal

## Versão

`image-prompt-engineer_v2.0` · 2026-05-14 · Head de Design Metta — adicionou namespace por marca (image-prompts/metta/ vs tiago/) e bases separados (_base.md vs _base-tiago.md)
