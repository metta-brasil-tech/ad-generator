# Guia de Templates — Exemplos de Criativos para Teste

> Documento de referência para testar cada um dos 33 templates do ad-generator.
> Para cada template: quando usar, briefing de teste (input do pipeline), e o que esperar como output.

---

## Como usar este guia

```bash
# Rodar um template específico:
python pipeline.py "<briefing de teste>" --mock
python pipeline.py "<briefing de teste>"  # com LLM real
python pipeline.py "<briefing de teste>" --stop-at 03  # ver só o layout spec
```

---

# MARCA METTA — 21 templates

---

## A — A-headline-foto-dark

**Visual:** Fundo escuro (`#0C161B`) · Headline grande UPPER à esquerda · Foto pessoa cortada à direita · Body pequeno · CTA pill amarelo

**Quando brilha:** Case nominal com cliente identificado · Prova de resultado com número

**Briefing de teste:**
```
ad de prova social com Hiperzoo pra varejo de pet, story, tom credibilidade
```

**O que esperar:**
- `intent: prova_social_case_nominal`
- Headline UPPER com accent nas palavras de resultado (ex: accent em "12 lojas")
- `ranges[]` calculados na posição correta
- Foto com `image_prompt_ref: "image-prompts/style-A.md"`
- Body max 180 chars

**Variação para testar slot de accent:**
```
ad de prova social Sicredi pra agronegócio, story, destaque em "+171%"
```

---

## B — B-foto-top-headline-mixed

**Visual:** Foto no topo (acima da dobra) · Headline interpretando a cena abaixo · Body de explicação · CTA pill

**Quando brilha:** Imagem precede a tese · Narrativa foto → interpretação → ação

**Briefing de teste:**
```
story dor empresário — foto de corredor de escritório vazio às 23h, tom emocional MOFU
```

**O que esperar:**
- `intent: dor_pessoal`
- Foto ocupa topo (~55% do canvas)
- Headline interpreta a cena abaixo da foto
- Body max 150 chars

---

## C — C-tipografia-pura-dark

**Visual:** Puro texto escuro · Headline gigante multiline (até 7 linhas) · Sem foto · CTA pill

**Quando brilha:** Manifesto · Statement filosófico longo · Frase que precisa de espaço pra respirar

**Briefing de teste:**
```
story manifesto Metta sobre empresário que cresce com método, sem foto, tom provocador
```

**O que esperar:**
- Sem `image_slot`
- Headline ocupa a maior parte do canvas (max 180 chars / 7 linhas)
- Body opcional (max 100 chars)
- Fonte Zalando Sans Expanded Heavy UPPER

---

## D — D-foto-fullbleed-overlay

**Visual:** Foto sangramento total · Overlay gradiente escuro · Headline amarela sobre a foto · CTA pill

**Quando brilha:** Impacto emocional imediato · Imagem como emoção, não como prova

**Briefing de teste:**
```
story dor — empresário refém da operação, fullbleed emocional, funil TOFU cold
```

**O que esperar:**
- `image_slot` com bleed total (1080×1920)
- Headline amarela (`#FFBE18`) sobre overlay
- Body opcional e curto (max 100 chars)

---

## H — H-fundo-branco-headline-gigante

**Visual:** Fundo branco · Headline gigante preta Zalando Sans Expanded · Clean editorial

**Quando brilha:** Statement de autoridade limpo · Comparação de conceitos · Quando a frase já é o anúncio

**Briefing de teste:**
```
story statement Metta — frase de autoridade sobre gestão comercial, sem foto, tom intelectual MOFU
```

**O que esperar:**
- Fundo branco `#FFFFFF`
- Headline max 120 chars / 4 linhas, Zalando Sans Expanded Heavy
- Sem foto

---

## I — I-retrato-editorial-pb

**Visual:** Retrato em P&B editorial · Headline de autoridade · Body com quote ou explicação · Logo badge Metta

**Quando brilha:** Depoimento de cliente · Prova de autoridade humana · Case com rosto

**Briefing de teste:**
```
ad com retrato de empresário, prova social B2B serviços, story, tom credibilidade MOFU
```

**O que esperar:**
- Foto P&B editorial obrigatória
- `slot_name: logo_badge` incluído
- Body pode ser quote do cliente (max 140 chars)

---

## K — K-bold-dourado-urgencia

**Visual:** Fundo escuro dourado · Headline de convite formal · Body de fundamento · CTA pill

**Quando brilha:** Convite exclusivo · Evento fechado · Tom de carta formal

**Briefing de teste:**
```
convite webinário exclusivo Metta, junho 2026, B2B decisores, story BOFU
```

**O que esperar:**
- `intent: convite_evento`
- Slot `tag` como "EXCLUSIVO · JUN/2026"
- Headline formal (max 100 chars)
- CTA forte (ex: "GARANTIR MINHA VAGA")

---

## DARK-CARTA

**Visual:** Fundo escuro · Tipografia de carta formal · Headline de convite · Body fundamento

**Quando brilha:** Convite com exclusividade de carta · Tom "você foi selecionado"

**Briefing de teste:**
```
story convite formal para empresário selecionado para diagnóstico Metta, BOFU quente
```

**O que esperar:**
- Headline de convite (max 90 chars / 4 linhas)
- Body fundamento do convite (max 120 chars)
- Tag de exclusividade no topo

---

## DARK-COLAGEM

**Visual:** Fundo escuro · Colagem de fotos/recortes PB · Headline decodificando a metáfora visual

**Quando brilha:** Tese intelectual · Metáfora visual forte · Conteúdo de reframe

**Briefing de teste:**
```
story reframe intelectual — colagem sobre gestor que confunde atividade com resultado, tom provocador
```

**O que esperar:**
- `image_slot` de colagem
- Headline decodifica a colagem (max 100 chars)
- Body de aplicação opcional

---

## DARK-OBJETO

**Visual:** Fundo escuro · Objeto isolado como metáfora · Headline nomeando o conceito

**Quando brilha:** Metáfora de objeto concreto · Conceito do método · "Isso é o [objeto]. No negócio, é [conceito]."

**Briefing de teste:**
```
story analogia método Metta — objeto que representa processo comercial, tom intelectual MOFU
```

**O que esperar:**
- `image_slot` com objeto isolado em dark
- Tag do método (ex: "PROTOCOLO 3")
- Headline nomeando o conceito (max 80 chars)

---

## FOTO-PILL-CASUAL

**Visual:** Foto casual (não editorial) · Headline leve · Body de contextualização · CTA pill

**Quando brilha:** Tom mais acessível · Conteúdo orgânico brandado · "Bastidores" de método

**Briefing de teste:**
```
story casual Metta — foto de reunião de equipe, tom direto, engajamento orgânico TOFU
```

**O que esperar:**
- Foto casual (não PB, não editorial)
- Tag contexto leve (max 30 chars)
- Headline (max 80 chars)
- Body opcional

---

## LIGHT-SURREAL

**Visual:** Fundo claro · Colagem surreal/metafórica PB · Headline decodifica · Body de aplicação

**Quando brilha:** Tese provocativa filosófica · Formato "HBR editorial" · Audiência culta

**Briefing de teste:**
```
story reframe intelectual Metta — metáfora surreal sobre gestão, audiência decisor B2B, tom intelectual
```

**O que esperar:**
- Fundo claro
- `image_slot` com colagem surreal
- Headline max 100 chars / 3 linhas
- Body obrigatório (max 120 chars)

---

## LIGHT-TIPO

**Visual:** Fundo bege/cinza claro · Duas palavras/frases opostas GIGANTES com bleed · Bloco amarelo em uma palavra

**Quando brilha:** Frase Lovebrand de 2 conceitos opostos · Manifesto filosófico minimal

**Briefing de teste:**
```
story manifesto Metta — frase de 2 conceitos opostos sobre faturamento vs lucro, sem foto, TOFU
```

**O que esperar:**
- ⚠ Layout frágil — verificar se o comprimento da copy bate com o template original
- Só slots `headline` e `cta` opcional
- Headline UPPER com bleed lateral (ex: "FATURAMENTO É EGO.\nLUCRO É LIBERDADE.")
- Warning no output se copy tiver comprimento diferente do template

---

## LOGO-WALL

**Visual:** Fundo branco · Grade 3x3 de logos clientes B&W · Número gigante de volume · Card escuro com prova · CTA pill

**Quando brilha:** BOFU retargeting · Credibilidade por volume · "+1000 empresas confiam"

**Briefing de teste:**
```
story retargeting Metta — grade de logos clientes, "+1200 empresas", prova de escala, BOFU
```

**O que esperar:**
- `logo_slot` com logos dos clientes reais
- `headline_number: "+1200"` (max 12 chars, apenas número)
- `proof_card` com linha de prova (max 100 chars)
- ⚠ Não inventar logos — usar só clientes reais do briefing

---

## METTA-TWEET-CARD

**Visual:** Fundo branco · Mock de tweet · Avatar Metta + byline · Statement central · Credencial opcional

**Quando brilha:** Quote de autoridade · Dado de impacto · Provocação viral · Slide de carrossel com break tipográfico

**Briefing de teste:**
```
story tweet card Metta — provocação sobre gestão comercial, dado de impacto, TOFU viral
```

**O que esperar:**
- `byline_name: "Metta"`, `byline_handle: "@mettaoficial"` (padrão)
- `statement`: max 160 chars / 5 linhas, sentence case
- `accent_words` com max 3 palavras em amarelo
- `credencial` opcional (ex: "Dados: pesquisa interna Metta 2026")

---

## NEWS-CARD

**Visual:** Fundo branco · Tag editorial amarela · Manchete jornalística · Body lead objetivo · CTA pill opcional

**Quando brilha:** Análise setorial · Estudo publicado · Panorama de mercado · Tom Exame/Forbes

**Briefing de teste:**
```
story análise Metta — panorama varejo pet 2026, dado de mercado, tom jornalístico MOFU decisor culto
```

**O que esperar:**
- Tag `"#VAREJO · MAI/2026"`
- Headline manchete (max 110 chars)
- Body lead jornalístico (max 160 chars / 4 linhas)
- ⚠ Sem foto stock pose feliz

---

## YELLOW-BLOCO

**Visual:** Fundo escuro · Logo bar de clientes no topo · Bloco amarelo com headline · Bullets de benefícios · CTA pill

**Quando brilha:** Convite a evento com agenda · Posicionamento "ecossistema de marcas grandes" · Oferta com sub-benefícios

**Briefing de teste:**
```
story convite webinário Metta + Sicredi + Vivo + Korin, junho 2026, 3 benefícios da agenda, MOFU B2B
```

**O que esperar:**
- `logo_slot` com logos dos clientes
- Headline no bloco amarelo (max 50 chars / 3 linhas)
- Bullets: 3-5 linhas, cada uma começa com `•`, max 60 chars each
- CTA (ex: "QUERO PARTICIPAR")

---

## YELLOW-DRAW

**Visual:** Fundo amarelo · Ilustração/draw como elemento · Headline de conceito leve · Body opcional

**Quando brilha:** Conteúdo mais leve · Conceito com metáfora desenhada · Engajamento de marca

**Briefing de teste:**
```
story conceito Metta com ilustração, frase leve sobre crescimento, TOFU orgânico
```

**O que esperar:**
- `image_slot` com ilustração
- Headline leve (max 70 chars / 3 linhas)
- Body opcional e curto (max 100 chars)

---

## YELLOW-EDITORIAL

**Visual:** Fundo amarelo total · Colagem PB de executivos desfocada no topo · Número GIGANTE 180-280px · Body contexto · CTA pill preto

**Quando brilha:** Prova de mercado com número massivo · Market share · Volume de faturamento

**Briefing de teste:**
```
story Metta — R$8,5bi em faturamento gerado pelos clientes, big number institucional, BOFU
```

**O que esperar:**
- ⚠ `headline` é SÓ o número: `"R$8,5bi"` (max 12 chars)
- Body contextualiza o número (max 120 chars / 3 linhas)
- Sem foto de pessoa — colagem PB de executivos desfocada
- CTA pill preto (não amarelo, pois fundo é amarelo)

---

## YELLOW-FRAME

**Visual:** Fundo com frame amarelo geométrico · Tag de segmento · Headline pergunta crítica

**Quando brilha:** Pergunta diagnóstica · "Você tem isso no seu negócio?" · Engajamento reflexivo

**Briefing de teste:**
```
story pergunta crítica para varejo — tem sistema de gestão comercial ou improviso?, TOFU
```

**O que esperar:**
- Tag obrigatório (max 30 chars): `"PARA VAREJISTAS"`
- Headline pergunta (max 80 chars / 4 linhas)
- Sem body — a pergunta é o anúncio

---

## YELLOW-SPLIT

**Visual:** Canvas dividido 50/50 · Top escuro com headline dramática · Bottom amarelo com oferta/pergunta + CTA

**Quando brilha:** Statement dramático + CTA forte na mesma peça · Audiência warm pronta pra ofertação

**Briefing de teste:**
```
story split Metta — drama emocional sobre time sem meta + oferta de diagnóstico, BOFU warm
```

**O que esperar:**
- `headline_top` no half escuro: statement dramático (max 80 chars / 3 linhas), accent em 1 palavra
- `body_bottom` no half amarelo: oferta ou pergunta (max 100 chars / 2 linhas)
- CTA pill preto dentro do half amarelo

---

# MARCA TIAGO — 12 templates

---

## TIAGO-DARK-SURREAL

**Visual:** Fundo ultra-escuro · Uma única imagem surreal/metafórica ocupando tudo · Sem texto

**Quando brilha:** Impacto visual puro · Abertura de carrossel · Provocação sem palavras

**Briefing de teste:**
```
feed Tiago — imagem surreal de empresário, sem texto, impacto visual, TOFU tiago
```

**O que esperar:**
- ⚠ `elements` terá APENAS `image_slot` — nenhum elemento texto
- Warning automático: "Modelo 100% visual"
- Prompt de imagem: metáfora surrealista, paleta escura

---

## TIAGO-EDITORIAL-CARD

**Visual:** Card escuro centralizado · Eyebrow label amarelo UPPER · Stats/texto multiline com mix de peso · Remate bold · Ornamentos pixel

**Quando brilha:** Slide de dados do carrossel · Stats numéricas que precisam respirar · Lista de sintomas de dor

**Briefing de teste:**
```
feed Tiago — card de estatísticas sobre turnover de gerentes, dados de mercado, MOFU empresário
```

**O que esperar:**
- `card_eyebrow`: `"O DADO CRU:"` ou `"A PROVA:"` (max 30 chars, UPPER)
- `stats_block`: max 320 chars / 8 linhas — **cada stat em linha separada com `\n`, stats separadas por `\n\n`**
- `remate`: fechamento bold (max 100 chars)
- Accent em números: `ranges[]` com `fill: "#FFCC00"`

---

## TIAGO-EDITORIAL-CTA

**Visual:** Assinatura Tiago gigante no topo · Headline de pergunta/engajamento · Variantes A/B/C

**Quando brilha:** Pedido de comentário · Reveal de protocolo · Convite ao diálogo

**Briefings de teste por variante:**

**Variante A (engajamento puro):**
```
feed Tiago — pergunta de engajamento sobre líder vs chefe para empresário, pede comentário, MOFU
```
Esperado: `headline` pergunta + `sub` convida comentário + `avatar_tiago_verified`

**Variante B (com foto real):**
```
feed Tiago — foto real de palestra, pergunta reflexiva, audiência warm perfil Tiago
```
Esperado: `headline` + `photo_real_tiago` + sem pill

**Variante C (reveal de protocolo):**
```
feed Tiago — reveal protocolo 5 etapas, data 30/05, CTA "comenta protocolo", BOFU
```
Esperado: `eyebrow_reveal_date: "NO DIA 30/05"` + `headline` + `cta_pill_gigante: "COMENTA PROTOCOLO"`

---

## TIAGO-EDITORIAL-DARK

**Visual:** Fundo muito escuro noir · Eyebrows esquerda/direita fixos · Imagem cinema noir opcional · Handwritten overlay · Headline · Sub · CTA pill

**Quando brilha:** Dor emocional pesada · Tom noir · Tensão narrativa

**Briefing de teste:**
```
feed Tiago — tema solidão do líder, foto noir, texto cursivo dentro da imagem, tom emocional pesado
```

**O que esperar:**
- `header_eyebrow_left` e `header_eyebrow_right` são **fixos** — não gerar
- `handwritten_overlay`: frase manuscrita curta dentro da imagem (max 80 chars)
- Headline noir (max 80 chars), accent em amarelo `#FFCC00`
- Sub opcional (max 150 chars)

---

## TIAGO-EDITORIAL-HERO

**Visual:** Header fixo com 3 elementos (eyebrow esquerda, assinatura, eyebrow direita) · Colagem cinema editorial · Headline de manchete · Subhead · Body remate

**Quando brilha:** Post de carrossel capa · Editorial premium · Conteúdo de destaque do perfil

**Briefing de teste:**
```
feed Tiago — manchete editorial sobre Geração Z no mercado de trabalho, colagem surreal, TOFU
```

**O que esperar:**
- `header_eyebrow_left`, `header_signature`, `header_eyebrow_right` são **fixos** — não gerar
- `speech_bubble`: incluir se headline for citação direta, omitir se statement
- Headline manchete (max 80 chars / 6 linhas), accent amarelo em 1-4 palavras
- Subhead opcional (max 180 chars)
- `collage_image` obrigatório

---

## TIAGO-NOTES-MOCKUP

**Visual:** Mock do app Notes do iPhone · Status bar 9:41 · Nav amarelo "Notas/OK" · H1 com marker amarelo · Lista numerada com sub-texto

**Quando brilha:** "3 decisões que tomei..." · "5 lições depois de..." · Storytelling de lista organizada

**Briefing de teste:**
```
feed Tiago — 3 decisões antes de contratar o primeiro gerente de vendas, MOFU empresário
```

**O que esperar:**
- `status_bar` e `nav_bar` são **fixos** — não gerar
- `h1_marker`: título com marker amarelo (max 60 chars / 2 linhas), ex: `"3 decisões que tomei\nantes de contratar."`
- `lista_numerada`: **3-6 itens**, formato:
  ```
  "1. Titulo do item.\nSub-texto explicativo do item.\n\n2. Titulo do item.\nSub-texto explicativo.\n\n3. ..."
  ```
- ⚠ Fundo obrigatoriamente branco `#FFFFFF`

---

## TIAGO-PHOTO-RAW

**Visual:** Foto real bruta de Tiago, sem tratamento editorial · Sem texto · Momento real

**Quando brilha:** Bastidores · Momento humano real · Quebra de feed

**Briefing de teste:**
```
feed Tiago — foto real bastidores, sem texto, momento real do Tiago, TOFU orgânico
```

**O que esperar:**
- ⚠ `elements` terá APENAS `image_slot` — zero elementos texto
- Foto real, não editorial, não PB

---

## TIAGO-STORY-COVER-HERO

**Visual:** Foto fullbleed · Assinatura Tiago no topo · Headline da tese · CTA pill "arrasta"

**Quando brilha:** Capa de carrossel story · Abertura de série de conteúdo

**Briefing de teste:**
```
story Tiago — capa de carrossel sobre os 5 erros de gestão de vendas, foto fullbleed, MOFU
```

**O que esperar:**
- `assinatura_tiago` é **fixo** — não gerar
- `foto_bleed`: imagem fullbleed obrigatória
- `headline`: tese do carrossel (max 90 chars / 5 linhas)
- `cta_pill`: "ARRASTA 👉" ou "VER PROTOCOLO"

---

## TIAGO-STORY-MINIMAL-QUESTION

**Visual:** Foto fullbleed contemplativa · Texto de reflexão/pergunta sobreposto · Linha secundária opcional

**Quando brilha:** Pergunta de engajamento no story · Reflexão leve · Tom meditativo

**Briefing de teste:**
```
story Tiago — pergunta reflexiva sobre solidão do líder, foto contemplativa, TOFU
```

**O que esperar:**
- `foto_bleed` obrigatória
- `texto_reflexao`: pergunta ou pensamento (max 100 chars / 4 linhas)
- `complemento` opcional: linha secundária (max 80 chars)

---

## TIAGO-STORY-YELLOW-BLOCK

**Visual:** Foto fullbleed · Bloco amarelo no centro/baixo · Headline pergunta ou checklist · Subhead · Timestamp opcional

**Quando brilha:** Pergunta com contexto de momento ("às 7h da manhã") · Checklist rápido · Conteúdo de engajamento com foto

**Briefing de teste:**
```
story Tiago — foto ambiente escritório manhã, pergunta sobre rotina de vendas, timestamp 07:30
```

**O que esperar:**
- `foto_bleed` obrigatória
- `headline` no bloco amarelo: pergunta ou título (max 60 chars / 3 linhas)
- `subhead` opcional: instrução curta (max 100 chars)
- `timestamp: "07:30"` quando presente (max 8 chars)

---

## TIAGO-TWITTER-CARD

**Visual:** Mock de tweet · Header fixo com avatar Tiago + anel amarelo · Headline hook · Body com parágrafos · Footnote de transição

**Quando brilha:** Statement provocativo · Pergunta diagnóstica que abre carrossel · Dado com contexto

**Briefings de teste por variante:**

**Variante cover:**
```
feed Tiago — tweet cover com headline provocativa sobre gerente de vendas vs chefe, foto real, MOFU
```
Esperado: `header_mock` (fixo) + `headline` + `body` opcional + `media` (foto)

**Variante content:**
```
feed Tiago — tweet de desenvolvimento de tese, parágrafos sobre sistema vs motivação, slide de carrossel
```
Esperado: `header_mock` (fixo) + `headline` hook + `body` com parágrafos `\n\n` + `footnote` de transição

**Regra de body:**
```json
{ "text": "Todo mundo fala sobre motivação.\nNinguém fala sobre sistema.\n\nMotivação você depende do humor.\nSistema você depende da agenda." }
```
- Sentence case obrigatório
- Parágrafos separados por `\n\n`
- Max 450 chars / 8 linhas

---

## TIAGO-TYPO-PURE

**Visual:** Fundo branco · Headline tipográfica grande · Palavras-chave em azul-cinza `#3D5762` · Handle assinatura fixo

**Quando brilha:** Frase impactante isolada · Reframe de uma linha · Quote de autoridade pessoal

**Briefing de teste:**
```
feed Tiago — frase impactante sobre vendedor vs líder de vendas, tipografia pura, TOFU orgânico
```

**O que esperar:**
- `handle` é **fixo** — não gerar
- `headline`: frase impactante (max 90 chars / 4 linhas), sentence case
- Palavras-chave em `ranges[]` com `fill: "#3D5762"`
- Sem foto

---

# Resumo por tipo de slot especial

| Situação | Modelos | O que verificar no output |
|---|---|---|
| `\n` em headline multiline | Todos com `max_lines > 1` | `text` tem `\n` nas quebras |
| Lista numerada | TIAGO-NOTES-MOCKUP | `\n` entre título+sub, `\n\n` entre itens |
| Bullets com `•` | YELLOW-BLOCO | Cada linha começa com `•`, `\n` entre bullets |
| Stats multiline | TIAGO-EDITORIAL-CARD | `\n\n` entre stats, accent em números |
| Parágrafos tweet | TIAGO-TWITTER-CARD | `\n\n` entre parágrafos no body |
| Big number | YELLOW-EDITORIAL | `headline` = só número, ex: `"+47%"` |
| Zero texto | TIAGO-DARK-SURREAL, TIAGO-PHOTO-RAW | `elements` só tem `image_slot` |
| Slots fixos omitidos | NOTES-MOCKUP, EDITORIAL-HERO, TWITTER-CARD, TYPO-PURE | Não aparecem em `elements` |
| Logo slot | YELLOW-BLOCO, LOGO-WALL | Tipo `logo_slot` com array de logos |
| Layout frágil | LIGHT-TIPO | Warning se comprimento de copy diferir |
| Variante explícita | TIAGO-EDITORIAL-CTA, TIAGO-TWITTER-CARD | Só slots da variante escolhida |

---

## Sequência recomendada de testes

1. **Smoke test** — todos com `--mock` pra validar dataflow
2. **Slot padrão** — começar por A, B, C (mais simples)
3. **Multiline crítico** — TIAGO-NOTES-MOCKUP e TIAGO-EDITORIAL-CARD (testam `\n`)
4. **Zero texto** — TIAGO-DARK-SURREAL e TIAGO-PHOTO-RAW
5. **Slots especiais** — YELLOW-BLOCO (bullets + logos), LOGO-WALL, YELLOW-EDITORIAL (big number)
6. **Variantes** — TIAGO-EDITORIAL-CTA (A/B/C) e TIAGO-TWITTER-CARD (cover/content)
7. **Frágil** — LIGHT-TIPO (verificar warning de comprimento)

---

*Gerado em 2026-05-19 · Baseado em auditoria completa dos 33 modelos · ad-generator v0.1*
