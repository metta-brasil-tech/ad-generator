# ad-generator — Pipeline model-agnostic de geração automática de ads Metta

> Implementação operacional do sistema descrito em [[ai-ad-generation-system]].

## TL;DR

```bash
# 1) setup
cp .env.example .env
# preencher LLM_PROVIDER, LLM_API_KEY, etc.
pip install -r requirements.txt
docker compose up -d  # sobe Qdrant em localhost:6333

# 2) indexar modelos no Qdrant
python indexer.py --re-index

# 3) gerar ad
python pipeline.py "ad de prova social com Hiperzoo pra varejo de pet, story"

# 4) mock mode (sem chamar LLM real — pra testar dataflow)
python pipeline.py "ad de prova social com Hiperzoo, story" --mock
```

**Output final:** PNG em `artifacts/outputs/{model_id}_{timestamp}.png` (1080×1920 story).

## Arquitetura

```
pipeline.py             # CLI orchestrator
├── skills_runner.py    # carrega skill .md + roda contra LLM
├── validators.py       # JSON Schema validation entre etapas
├── indexer.py          # vetoriza models/*.yaml no Qdrant
└── adapters/
    ├── llm.py          # LiteLLM (Claude/OpenAI/Gemini)
    ├── vector_store.py # Qdrant client
    ├── image_gen.py    # Nano Banana 2 / gpt-image-1
    └── assembler.py    # PNG/JPEG via Pillow (entregável final)
```

Pipeline executa as 6 skills do sistema em sequência:

1. **briefing-parser** → texto livre PT-BR vira `briefing.schema.json`
2. **style-selector** → busca semântica + LLM ranking dos top-3 estilos
3. **layout-composer** → encaixa copy nos slots do estilo escolhido
4. **image-prompt-engineer** → gera prompt pra image-gen API
5. **assembler** → renderiza no Figma ou HTML
6. **qa-validator** → checa contra DS rules

Cada skill recebe e devolve JSON validado contra schema. Tudo em `brand-knowledge/` no vault.

## Modos de execução

### `--mock` (sem LLM real)

Útil pra testar o dataflow sem queimar tokens. Cada skill retorna resposta hardcoded compatível com o schema. Roda local em <2s.

```bash
python pipeline.py "<briefing>" --mock
```

### `--provider <name>` (override do LLM)

```bash
python pipeline.py "<briefing>" --provider openai
python pipeline.py "<briefing>" --provider claude
python pipeline.py "<briefing>" --provider gemini
```

Lê `LLM_MODEL_{PROVIDER}` do `.env`.

### `--stop-at <skill>` (parcial)

```bash
python pipeline.py "<briefing>" --stop-at 02  # roda só até style-selector
```

Útil pra inspecionar output intermediário antes do pipeline todo rodar.

### `--input briefing.json` (sem reparseaer texto livre)

```bash
python pipeline.py --input artifacts/briefings/hiperzoo.json
```

Pula skill 01, começa direto do briefing estruturado.

## Estrutura de arquivos

```
apps/ad-generator/
├── README.md                  ESTE
├── requirements.txt           dependências Python
├── .env.example               template de env vars
├── docker-compose.yml         Qdrant single-container
├── pipeline.py                CLI principal
├── skills_runner.py           Skill loader + LLM caller
├── validators.py              JSON Schema runtime validation
├── indexer.py                 Vetoriza modelos pro Qdrant
├── adapters/
│   ├── __init__.py
│   ├── llm.py                 LiteLLM wrapper (model-agnostic)
│   ├── vector_store.py        Qdrant client
│   ├── image_gen.py           image-gen adapters
│   └── assembler.py           Figma + HTML output
├── tests/
│   └── test_fixtures.py       Casos de teste sintéticos
└── artifacts/                 Outputs ignored em .gitignore
    ├── briefings/             JSON briefings gerados
    ├── layouts/               layout specs gerados
    └── outputs/               final ads
```

## Requisitos

| Componente | Versão |
|---|---|
| Python | ≥3.11 |
| Docker (Qdrant) | qualquer recente |
| Node 20+ (opcional, pra Figma plugin) | LTS |

## Princípios de implementação

1. **Skills são markdown puro** — código carrega `brand-knowledge/skills/{N}-{name}.md` e usa como system prompt
2. **Schemas validam tudo** — entrada e saída de cada skill é validada contra `brand-knowledge/schemas/*.schema.json`
3. **Model-agnostic** — LiteLLM abstrai 30+ providers, trocar provider = trocar env var
4. **Falha visível** — qualquer skill que retorne JSON inválido aborta o pipeline com erro claro
5. **Idempotente** — mesmo input gera mesmo output (com temperature=0)
6. **Logs estruturados** — JSON Lines em `artifacts/logs/` pra telemetria

## Telemetria

Cada run gera:

```jsonl
{"ts": "...", "run_id": "...", "skill": "01-briefing-parser", "provider": "claude", "tokens_in": 234, "tokens_out": 187, "latency_ms": 1850, "status": "ok"}
{"ts": "...", "run_id": "...", "skill": "02-style-selector", ...}
```

Em `artifacts/logs/{date}.jsonl`. Pra agregação fácil em PostHog/CSV futuramente.

## Status

| Componente | Status |
|---|---|
| README + estrutura | ✅ |
| LLM adapter (LiteLLM) | ✅ |
| Vector store adapter (Qdrant) | ✅ |
| Skill runner | ✅ |
| JSON Schema validator | ✅ |
| Pipeline orchestrator | ✅ |
| Indexer | ✅ |
| Mock mode | ✅ |
| Image-gen adapter (DALL-E 3 / Nano Banana 2 / Imagen 3) | ✅ |
| **PNG Assembler (Pillow nativo)** | ✅ — entregável final |
| Figma Assembler | ⬜ (stub — opcional) |
| Tests | ⬜ (parcial) |

## Versão

`ad-generator_v0.1` · 2026-05-13 · Head de Design Metta
