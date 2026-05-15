---
title: "brand-knowledge — Conhecimento estruturado pro Sistema de IA Geração de Ads"
aliases:
  - "brand-knowledge"
  - "AI Knowledge Base Metta"
tags:
  - marca/metta
  - marca/tiago
  - tema/ia
  - tema/design
  - tipo/indice
  - usado-por/skill-criar-com-bs
formato_consumo: indice
prioridade_carregamento: alta
versao: "2.0"
sucedido_por: null
complementar_com: "[[ai-ad-generation-system]] · [[banco-ads-figma]] · [[banco-tiago-conteudo]] · [[metta-tokens]] · [[tiago-tokens]] · [[playbook-ad]]"
summary: "Índice navegável da pasta brand-knowledge — conhecimento declarativo (modelos YAML, image prompts, skills markdown, JSON schemas) que alimenta o sistema model-agnostic de geração automática de ads. v2.0 adicionou namespace por marca: models/metta/ + models/tiago/ com isolamento estrutural duro."
created: 2026-05-13
updated: 2026-05-14
---

# brand-knowledge — Conhecimento estruturado pro Sistema de IA Geração de Ads

> **Esse é o índice da pasta `brand-knowledge/`.** Tudo aqui é consumido pelo Sistema de Geração Automática de Ads (ver [[ai-ad-generation-system]]).
>
> **Princípio:** conhecimento declarativo, versionável, model-agnostic. Tudo aqui funciona em Claude, OpenAI, Gemini ou qualquer LLM moderno.

## Mapa da pasta (v2.0 — namespace por marca)

```
brand-knowledge/
├── README.md                              # ESTE ARQUIVO — índice
├── models/                                # Catálogo de modelos por marca (YAML)
│   ├── _schema.yaml                       # Schema canônico (inclui campo `marca`)
│   ├── metta/                             # 19 estilos Metta institucional
│   │   ├── A-headline-foto-dark.yaml
│   │   ├── B-foto-top-headline-mixed.yaml
│   │   ├── C-tipografia-pura-dark.yaml
│   │   ├── D-foto-fullbleed-overlay.yaml
│   │   ├── H-fundo-branco-headline-gigante.yaml
│   │   ├── I-retrato-editorial-pb.yaml
│   │   ├── K-bold-dourado-urgencia.yaml
│   │   ├── LIGHT-SURREAL.yaml · LIGHT-TIPO.yaml
│   │   ├── YELLOW-BLOCO.yaml · YELLOW-DRAW.yaml · YELLOW-EDITORIAL.yaml
│   │   ├── YELLOW-FRAME.yaml · YELLOW-SPLIT.yaml
│   │   ├── DARK-CARTA.yaml · DARK-COLAGEM.yaml · DARK-OBJETO.yaml
│   │   └── NEWS-CARD.yaml · LOGO-WALL.yaml
│   └── tiago/                             # estilos marca pessoal Tiago Alves
│       └── TIAGO-TWITTER-CARD.yaml        # carrossel mock-Twitter feed 1080×1350
├── image-prompts/                         # Prompts pra image-gen, isolados por marca
│   ├── metta/
│   │   ├── _base.md                       # base universal Metta (editorial dark cinema)
│   │   ├── style-A.md · style-B.md · style-C.md · style-D.md
│   │   ├── style-YELLOW-BLOCO.md
│   │   └── style-LIGHT-SURREAL.md
│   └── tiago/
│       ├── _base-tiago.md                 # base Tiago (documental light snapshot)
│       └── style-twitter-card.md
├── skills/                                # 6 skills do pipeline (marca-aware)
│   ├── 01-briefing-parser.md              # Texto livre → JSON briefing (detecta marca)
│   ├── 02-style-selector.md               # Etapa 0: filtro duro por marca → top-3 estilos
│   ├── 03-layout-composer.md              # Briefing+estilo → layout spec (tokens da marca)
│   ├── 04-image-prompt-engineer.md        # Layout → image prompt (namespace por marca)
│   ├── 05-assembler.md                    # Layout+imagens → PNG/Figma
│   └── 06-qa-validator.md                 # Output → QA report (categoria brand_consistency)
├── schemas/                               # JSON Schemas dos contratos
│   ├── briefing.schema.json               # enum marca: metta | tiago
│   ├── style-recommendation.schema.json
│   ├── layout-spec.schema.json
│   ├── image-prompt.schema.json
│   ├── ad-output.schema.json
│   └── qa-report.schema.json
└── exemplars/                             # Few-shot library namespaced por marca
    ├── metta/
    │   ├── A/01-hiperzoo-12-lojas.json
    │   ├── B/01-refem-operacao.json
    │   └── …
    └── tiago/
        ├── cr6tiagoabril-{1,2}.png        # PNGs canônicos referência
        ├── cr6tiagoabril-{1,2}.svg
        └── TIAGO-TWITTER-CARD/
            ├── 01-cracha-gerente-vendedor.json    # variant cover
            └── 02-gerentes-comerciais-65pct.json  # variant content
```

## Como usar

### Sou um operador rodando o sistema em prod

Você não toca nessa pasta — você usa a UI/CLI que consome ela. Veja `apps/ad-generator/README` (a criar) pro fluxo.

### Sou desenvolvedor integrando provider novo

1. Lê [[ai-ad-generation-system]] §5 (Stack)
2. Implementa adapter em `adapters/llm/{provider}.ts` cumprindo interface `LLMAdapter`
3. Cada skill em `skills/*.md` é markdown puro — passe direto pro completion
4. Cada schema em `schemas/*.json` é JSON Schema padrão — funciona em function calling / structured output de qualquer provider

### Sou designer adicionando estilo novo

1. Lê [[ai-ad-generation-system]] §7 (Protocolo de adição)
2. Decide a marca (`metta` ou `tiago`) — define todo o namespace
3. Documenta DNA narrativo em `design/banco-ads-figma.md` (Metta) ou `design/banco-tiago-conteudo.md` (Tiago)
4. Cria YAML em `models/{marca}/{ID}.yaml` seguindo `models/_schema.yaml` (campo `marca` obrigatório)
5. Cria image prompt em `image-prompts/{marca}/style-{ID}.md` (se usa foto)
6. Adiciona 3-5 exemplars em `exemplars/{marca}/{ID}/`
7. Re-indexa Qdrant collection `ad-styles` (`indexer.py` faz recurse automático)

### Sou prompt engineer iterando skill

1. Skills são markdown puro — edita direto
2. Cada skill tem few-shot examples — atualize se mudar comportamento
3. Versionar via git — bump `versão` no header e changelog ao final
4. Testar em 2+ providers antes de mergear (model-agnostic é regra)

## Princípios não-negociáveis

1. **Markdown puro nos prompts.** Sem `<thinking>`, `<artifact>`, ou features proprietárias.
2. **JSON Schema nos contratos.** Validável em qualquer linguagem/runtime.
3. **YAML nos modelos.** Versionável, diff-friendly, parseável por humano e LLM.
4. **Banco é referência, não template.** Skills CRIAM ads novos do zero usando DNA. Nunca clonam template Figma.
5. **PT-BR no briefing, EN no image prompt.** LLMs entendem briefing em PT-BR melhor; image-gen entende EN melhor.
6. **Human-in-the-loop em v1.** Output vai pra review queue, não direto pra publicação.

## Stack de runtime esperado

| Camada | Implementação primária | Fallback |
|---|---|---|
| LLM orchestration | LiteLLM (Python) | Vercel AI SDK (TS) |
| Vector DB | Qdrant self-hosted | Pinecone |
| Image gen | Nano Banana 2 | gpt-image-1 |
| Output | Figma Plugin API | HTML+Playwright |
| Storage | Supabase | Local FS (dev) |

## Status atual (2026-05-14)

| Componente | Status |
|---|---|
| Doc mestre arquitetural | ✅ feito (v2.0) |
| Schema YAML canônico (com campo `marca`) | ✅ feito |
| 19 modelos Metta | ✅ feito (organizados em `models/metta/`) |
| 1 modelo Tiago (TIAGO-TWITTER-CARD) | ✅ feito |
| Image prompts Metta (6) | ✅ feito (em `image-prompts/metta/`) |
| Image prompts Tiago (_base + style-twitter-card) | ✅ feito |
| Tokens Tiago (`design/tiago-tokens.md`) | ✅ feito |
| Banco narrativo Tiago (`design/banco-tiago-conteudo.md`) | ✅ feito |
| 6 skills do pipeline (marca-aware, v2.0) | ✅ feito |
| 6 JSON schemas (enum marca renomeado) | ✅ feito |
| Few-shot library Metta | 🟡 2 seed (A, B) |
| Few-shot library Tiago | ✅ 2 seed (TIAGO-TWITTER-CARD variant cover + content) |
| Setup Qdrant + indexação (recurse + marca payload) | ✅ feito |
| Adapters (LLM, image-gen, assembler) | ✅ feito |
| Pipeline end-to-end | ✅ feito |
| Review queue UI | ⬜ pendente |

## Próximos passos imediatos

1. **Validar em LLM real:** rodar briefing-parser num Claude + GPT, comparar outputs
2. **Setup Qdrant local:** docker container + script de indexação dos 6 YAMLs
3. **First-pass MVP:** pipeline manual (chama 6 skills em sequência via curl/Python), gera 1 ad de teste
4. **Iteração:** baseado no resultado, refinar prompts dos skills mais problemáticos
5. **Fase 2:** preencher 12 modelos raros + first 30 exemplars (3-5 por estilo robusto)

## Versão

`brand-knowledge_v2.0` · 2026-05-14 · Head de Design Metta

## Changelog

| Data | Versão | Mudança |
|---|---|---|
| 2026-05-13 | **1.0** | Estrutura inaugural — 6 YAMLs + 6 image prompts + 6 skills + 6 schemas + doc mestre |
| 2026-05-14 | **2.0** | Namespace por marca. 19 Metta YAMLs movidos pra `models/metta/`. 1º estilo Tiago: TIAGO-TWITTER-CARD em `models/tiago/`. Image-prompts e exemplars também namespaced. Schema `_schema.yaml` ganhou campo `marca`. Enum simplificado `metta`/`tiago`. Skills 01-06 atualizadas (marca-aware). Indexer faz recurse + grava marca no payload Qdrant. |
