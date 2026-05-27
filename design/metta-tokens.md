# Metta Brand Tokens

> Fonte canônica de design tokens da marca Metta Brasil.
> Referenciado por: skill 03 (layout-composer), assembler, QA validator.

---

## Identidade

- **Marca:** Metta Brasil — marca institucional
- **Tagline:** "Meta Batida"
- **Voz:** Credibilidade, autoridade, provocação intelectual. UPPER CASE nas headlines.

---

## Cores

| Token | Hex | Uso |
|---|---|---|
| `--metta-ref-palette-night-10` | `#0C161B` | Fundo escuro primário (dark bg) |
| `--metta-ref-palette-night-100` | `#FFFFFF` | Branco puro |
| `--metta-ref-palette-night-85` | `#B0CAD8` | Cinza azulado (body text em dark) |
| `--metta-ref-palette-night-40` | `#435965` | Cinza médio |
| `--metta-ref-palette-yellow-50` | `#FFBE18` | Amarelo Metta (accent primário) |
| `--metta-sys-color-primary` | `#FFBE18` | Amarelo — CTA background, accent words |
| `--metta-sys-color-on-primary` | `#0C161B` | Texto sobre amarelo |
| `--metta-sys-color-surface` | `#0C161B` | Surface escura |
| `--metta-color-bg` | `#0C161B` | Fundo padrão dark |
| `--metta-color-text-primary` | `#FFFFFF` | Texto primário (sobre dark) |
| `--metta-color-text-secondary` | `#B0CAD8` | Texto secundário (body em dark) |
| `--metta-color-accent` | `#FFBE18` | Amarelo — accent words, pill CTA |
| `--metta-color-light-bg` | `#FFFFFF` | Fundo claro (templates H, NEWS, LOGO-WALL) |
| `--metta-color-light-text` | `#0C161B` | Texto sobre fundo claro |
| `--metta-color-yellow-bg` | `#FFBE18` | Fundo amarelo (YELLOW-EDITORIAL, YELLOW-BLOCO) |
| `--metta-color-yellow-text` | `#0C161B` | Texto sobre fundo amarelo |
| `--metta-color-bege` | `#EDF2F5` | Fundo bege claro (LIGHT-TIPO) |

---

## Tipografia

### Família principal: Zalando Sans Expanded

| Uso | Family | Style | Weight | Width |
|---|---|---|---|---|
| Headline principal | Inter | Expanded Heavy | 870 | 132 |
| Headline secundária | Inter | Expanded Bold | 700 | 132 |
| Sub-headline | Inter | Expanded Semibold | 650 | 132 |
| Body / texto | Inter | Expanded Regular | 400 | 132 |
| Tag / eyebrow / CTA | Inter | Expanded Medium | 540 | 132 |
| CTA pill | Inter | Expanded Bold | 700 | 132 |

> **Atenção:** Metta usa Inter **Expanded** (width 132) em quase todos os elementos.
> Nunca usar Inter/Condensed nos templates Metta — esses são da marca Tiago.

### Tamanhos por tipo de slot

| Slot | Size range | Line height | Case |
|---|---|---|---|
| Headline display (hero, manifesto) | 80–180px | 88–95% | UPPER |
| Headline padrão | 56–80px | 90–100% | UPPER |
| Big number (YELLOW-EDITORIAL) | 180–280px | 88% | UPPER |
| Body / framing | 24–34px | 120–130% | sentence |
| Tag / eyebrow | 18–24px | 100% | UPPER |
| CTA pill | 20–26px | 100% | UPPER |
| Tweet statement (METTA-TWEET-CARD) | 36–48px | 130% | sentence |

---

## Espaçamento

| Token | Valor | Uso |
|---|---|---|
| `--metta-spacing-safe-x` | `80px` | Margem lateral padrão STORY |
| `--metta-spacing-safe-top` | `100px` | Margem superior padrão |
| `--metta-spacing-safe-bot` | `130px` | Margem inferior (acima do CTA) |
| `--metta-spacing-gap-headline-body` | `48px` | Gap headline → body |
| `--metta-spacing-gap-body-cta` | `40–56px` | Gap body → CTA |

---

## Shapes

| Token | Valor | Uso |
|---|---|---|
| `--metta-sys-shape-corner-pill` | `999px` | Pill CTA (fully rounded) |
| `--metta-sys-shape-corner-lg` | `24px` | Card containers |
| `--metta-sys-shape-corner-sm` | `8px` | Elementos menores |

---

## Formatos de canvas

| Formato | Dimensões | Templates |
|---|---|---|
| STORY | 1080 × 1920px | A, B, C, D, H, K, DARK-CARTA, DARK-COLAGEM, DARK-OBJETO, FOTO-PILL-CASUAL, I, LIGHT-SURREAL, LIGHT-TIPO, NEWS-CARD, YELLOW-BLOCO, YELLOW-DRAW, YELLOW-EDITORIAL, YELLOW-FRAME, YELLOW-SPLIT |
| FEED (4:5) | 1080 × 1350px | LOGO-WALL, METTA-TWEET-CARD |
| SQR | 1080 × 1080px | Quando `formato: sqr` no briefing |

---

## Regras de isolamento

- ❌ `var(--tiago-*)` nunca em layout `marca=metta`
- ❌ Inter/Condensed como headline — Metta usa Expanded
- ❌ Fundo branco `#FFFFFF` como bg padrão em dark templates
- ❌ Amarelo Tiago `#FFCC00` nunca no Metta (amarelo Metta é `#FFBE18`)
- ❌ Sentence case nas headlines de anúncio — Metta é UPPER (exceto tweet card e news)

---

*Criado: 2026-05-19 · Extraído dos YAMLs dos 21 modelos Metta · ad-generator v0.1*
