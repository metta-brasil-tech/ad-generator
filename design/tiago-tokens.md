# Tiago Brand Tokens

> Fonte canônica de design tokens da marca pessoal Tiago Alves.
> Referenciado por: skill 03 (layout-composer), assembler, QA validator.

---

## Identidade

- **Marca:** Tiago Alves — marca pessoal
- **Tagline:** "Vendas é Ciência"
- **Voz:** Reflexiva, acolhedora, não acusatória. Sentence case obrigatório — sem UPPER nas headlines.

---

## Cores

| Token | Hex | Uso |
|---|---|---|
| `--tiago-color-bg` | `#FFFFFF` | Fundo padrão (branco puro) |
| `--tiago-color-text-primary` | `#0F1419` | Texto headline e body |
| `--tiago-color-text-secondary` | `#536471` | Handle @ · texto secundário |
| `--tiago-color-accent` | `#FFCC00` | Amarelo signature Tiago |
| `--tiago-color-accent-ring` | `#FFCC00` | Ring do avatar (10px) |
| `--tiago-color-accent-yellow` | `#FFCC00` | Marker, destaques amarelos |
| `--tiago-color-marker-bg` | `#FFE89E` | Background marker Notes (highlighter) |
| `--tiago-color-body-text` | `#6E6E73` | Sub-texto cinza (iOS-like) |
| `--tiago-color-fg-secondary` | `#6E6E73` | Texto de suporte leve |
| `--tiago-color-dark-bg` | `#0C0F0F` | Fundo escuro (TIAGO-DARK-SURREAL, TIAGO-EDITORIAL-DARK) |
| `--tiago-color-dark-text` | `#FFFFFF` | Texto sobre fundo escuro |
| `--tiago-color-speech-bubble-bg` | `#F7F9F9` | Fundo do speech bubble (EDITORIAL-HERO) |
| `--tiago-color-speech-bubble-fg` | `#0F1419` | Texto do speech bubble |
| `--tiago-color-verified-blue` | `#1D9BF0` | Badge verificado Twitter mock |
| `--tiago-color-handle` | `#536471` | Handle @tiago.alves.oliveira |
| `--tiago-color-blue-accent` | `#3D5762` | Destaque tipográfico azul-cinza (EDITORIAL-CTA) |
| `--tiago-color-yellow-block` | `#FFCC00` | Bloco amarelo (STORY-YELLOW-BLOCK) |

---

## Tipografia

### Família principal: SF Pro

| Uso | Family | Style | Weight | Width |
|---|---|---|---|---|
| Headline FEED editorial | SF Pro | Bold | 700 | 100 (standard) |
| Headline STORY cover | SF Pro | Bold | 700 | 100 |
| Headline Notes H1 | SF Pro Condensed | Semibold | 600 | 75 |
| Body/parágrafo | SF Pro | Regular | 400 | 100 |
| Handle / tag / eyebrow | SF Pro | Regular | 400 | 100 |
| Lista numerada (número+título) | SF Pro Condensed | Semibold | 600 | 75 |
| Sub-texto lista (Notes) | SF Pro | Regular | 400 | 100 |
| Footnote / transição | SF Pro | Regular | 400 | 100 |

> **Atenção:** Tiago usa SF Pro **standard** (width 100) e **Condensed** (width 75).
> **Nunca** usar SF Pro Expanded (width 132) — esse é o typeface Metta institucional.

### Tamanhos por template

| Template | Slot | Size | Line height |
|---|---|---|---|
| TIAGO-TWITTER-CARD | headline | 48–60px | 125% |
| TIAGO-TWITTER-CARD | body | 40–48px | 140% |
| TIAGO-TWITTER-CARD | handle | 28–32px | 120% |
| TIAGO-NOTES-MOCKUP | h1_marker | 40–52px | 110% |
| TIAGO-NOTES-MOCKUP | lista_numerada (título) | 24–30px | 120% |
| TIAGO-NOTES-MOCKUP | lista_numerada (sub) | 22–28px | 140% |
| TIAGO-EDITORIAL-CARD | stats_block | 40–56px | 130% |
| TIAGO-EDITORIAL-HERO | headline | 56–80px | 115% |
| TIAGO-EDITORIAL-HERO | subhead/body | 32–40px | 140% |
| TIAGO-TYPO-PURE | headline | 56–90px | 120% |

---

## Espaçamento

| Token | Valor | Uso |
|---|---|---|
| `--tiago-spacing-safe-x` | `64px` | Margem lateral padrão (FEED) |
| `--tiago-spacing-safe-x-notes` | `32px` | Margem lateral Notes (mock mais estreito) |
| `--tiago-spacing-safe-top` | `80px` | Margem superior padrão |
| `--tiago-spacing-safe-bot` | `80px` | Margem inferior padrão |
| `--tiago-spacing-gap-blocks` | `40px` | Gap entre blocos de texto |
| `--tiago-spacing-gap-notes-item` | `36px` | Gap entre itens da lista Notes |
| `--tiago-spacing-gap-notes-sub` | `12px` | Gap entre título e sub-texto Notes |

---

## Shapes

| Token | Valor | Uso |
|---|---|---|
| `--tiago-shape-corner-card` | `28px` | Radius foto embed Twitter Card |
| `--tiago-shape-corner-marker` | `0px` | Marker Notes é retângulo flat (highlighter) |
| `--tiago-shape-avatar-ring` | `10px` | Espessura do anel amarelo no avatar |

---

## Assets

| Asset | Path | Uso |
|---|---|---|
| Assinatura amarela | `assets/signatures-tiago/amarelo.png` | Fundo claro/branco |
| Assinatura branca | `assets/signatures-tiago/branco.png` | Fundo escuro |
| Assinatura cinza | `assets/signatures-tiago/cinza.png` | Fundo neutro |
| Assinatura escura | `assets/signatures-tiago/escuro.png` | Fundo amarelo |
| Twitter header | `assets/twitter-header-tiago.png` | Header mock Twitter Card |

---

## Regras de isolamento

- ❌ `var(--metta-*)` nunca em layout `marca=tiago`
- ❌ SF Pro Expanded nunca em layout `marca=tiago`
- ❌ Fundo escuro `#0C161B` (Metta night) nunca no Tiago padrão
- ❌ Amarelo Metta `#FFBE18` nunca no Tiago (amarelo Tiago é `#FFCC00`)
- ❌ UPPER CASE nas headlines — Tiago é sempre sentence case

---

*Criado: 2026-05-19 · Extraído dos YAMLs dos 12 modelos Tiago · ad-generator v0.1*
