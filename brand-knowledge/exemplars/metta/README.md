# Exemplars — Few-shot library

Pares input→output canônicos, usados como referência pelos skills via in-context learning ou pra validação de regressão.

## Estrutura

```
exemplars/
├── README.md
├── {style-id}/
│   ├── 01-{tema-curto}.json    # briefing + style-rec + layout-spec + final ad
│   └── 02-{tema-curto}.json
```

## Schema do exemplar

```json
{
  "exemplar_id": "A-hiperzoo-12-lojas",
  "tags": ["case-nominal", "varejo-pet", "MOFU"],
  "stages": {
    "briefing_input": "ad de prova social com Hiperzoo pra varejo de pet, story",
    "briefing_output": { /* briefing.schema.json */ },
    "style_selected": "A-headline-foto-dark",
    "layout_spec": { /* layout-spec.schema.json */ },
    "image_prompt": { /* image-prompt.schema.json */ },
    "ad_output": { /* ad-output.schema.json */ },
    "qa_report": { /* qa-report.schema.json */ }
  },
  "final_url": "https://...",
  "performance": {
    "human_accepted": true,
    "edits_required": "minor: tweak headline word break",
    "ad_metrics": { "ctr": 2.1, "cpa": 45.80 }
  },
  "created": "2026-05-13"
}
```

## Como skills usam

1. **briefing-parser** em modo "rich mode" pode receber 1-3 exemplars como few-shot in-context (sample briefing in → sample briefing out)
2. **style-selector** pode usar exemplars passados pra calibrar score
3. **layout-composer** consulta exemplars do mesmo estilo pra calibrar fit de copy similar
4. **qa-validator** usa exemplars como referência de "PASS visual"

Em produção, indexar também os exemplars no Qdrant (collection `ad-exemplars`) pra busca semântica.

## Status

| Estilo | Exemplars |
|---|---|
| A | 1 (Hiperzoo seed) |
| B | 1 (dor refém operacional) |
| C | 0 (TBD) |
| D | 0 (TBD) |
| YELLOW-BLOCO | 0 (TBD) |
| LIGHT-SURREAL | 0 (TBD) |
| Outros | 0 |

Meta Fase 2: 5 exemplars por estilo robusto = 30 total.
