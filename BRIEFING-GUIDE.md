# Guia completo — Como briefar a IA para gerar ads Metta e Tiago

> Referência para operadores. Tudo que você precisa saber para mandar um briefing pelo Telegram (ou CLI) e receber um ad gerado corretamente.

---

## 1. Como funciona o pipeline

Quando você manda um texto no Telegram, ele passa por **6 etapas automáticas**:

```
Seu texto
  ↓
[Skill 01] Briefing Parser   → Extrai: intenção, tese, funil, audiência, marca
  ↓
[Skill 02] Style Selector    → Escolhe top-3 estilos visuais do banco
  ↓
[Skill 03] Layout Composer   → Monta copy nos slots (headline, body, CTA...)
  ↓
[Skill 04] Image Prompt Eng. → Cria prompt para gerar a foto/imagem via IA
  ↓
[gpt-image-2]                → Gera a imagem
  ↓
[Skill 05] Assembler         → Renderiza o PNG final (1080×1920)
  ↓
PNG no Telegram
```

Se qualquer etapa falhar ou o briefing for ambíguo, a IA pede esclarecimento antes de continuar.

---

## 2. Estrutura do briefing

Você pode escrever em PT-BR informal. A IA extrai os campos abaixo automaticamente. **Quanto mais informação você der, menos ela precisa inferir.**

### Campos que a IA extrai

| Campo | O que é | Valores possíveis |
|---|---|---|
| **intent** | Qual é o objetivo do ad | Ver tabela abaixo |
| **tese_central** | A frase que resume o que o ad diz | Texto livre |
| **formato** | Tipo de peça | `feed` · `story` · `sqr` · `carrossel` — ver tabela de tamanhos abaixo |
| **funil** | Etapa do funil de vendas | `TOFU` · `MOFU` · `BOFU` · `retargeting` |
| **marca** | Qual marca | `metta` · `tiago` |
| **audiencia** | Pra quem | segmento + cargo + estado emocional |
| **tom** | Como a IA deve soar | credibilidade · emocional · provocador · intelectual · institucional · direto · poetico |

### Tamanhos de saída por formato

> **Você precisa especificar o formato no briefing.** A IA não adivinha.

| Formato | Diga no briefing | Canvas final | Geração gpt-image-2 | Onde aparece |
|---|---|---|---|---|
| **Feed/Imagem** (padrão) | "feed" ou "imagem" | 1080×1350px | 1024×1536 (portrait) | Grade do Instagram |
| **Story/Reels** | "story" ou "reels" | 1080×1920px | 1024×1536 (portrait) | Story completo |
| **Quadrado** | "quadrado" ou "1:1" | 1080×1080px | 1024×1024 (square) | Feed quadrado |
| **Carrossel** | "carrossel" | 1080×1350px | 1024×1536 (portrait) | Slides do carrossel |

**Observação:** feed e story usam a mesma geração de imagem pelo gpt-image-2 (1024×1536), mas o canvas final é diferente — 1350px de altura no feed e 1920px no story.

---

### Tabela de intents

| Intent | Quando usar |
|---|---|
| `prova_social_case_nominal` | Menciona cliente real (Hiperzoo, Sicredi, Vivo...) |
| `dor_pessoal` | "refém", "exausto", "sem tempo", "operação me engole" |
| `reframe_intelectual` | Tese filosófica, diagnóstico, questionar o óbvio |
| `convite_evento` | Webinário, evento, convite com data |
| `manifesto` | Posicionamento de marca, comunicado |
| `promessa_numerica` | "dobrou o faturamento", "R$2M", "+47%" |
| `case_metric` | Métrica + cliente ("+171% Vivo em 3 meses") |
| `reframe_mantra` | "todo mundo pensa que X mas na verdade..." |
| `autoridade_founder_led` | Voz do Tiago, founder-led |
| `posicionamento_institucional` | Metta + clientes grandes, ecossistema |

---

## 3. Funil — o que cada um significa

| Funil | Audiência | Objetivo do ad |
|---|---|---|
| **TOFU** | Fria — nunca te viu | Gerar consciência, identificação com dor/problema |
| **MOFU** | Morna — já te conhece | Mostrar método, cases, prova social |
| **BOFU** | Quente — está decidindo | Convite direto, urgência real, CTA de venda |
| **retargeting** | Já visitou/interagiu | Reforço, prova, empurrão final |

**Regra:** se não falar o funil, a IA infere. Mas você pode (e deve) especificar.

---

## 4. Modelos disponíveis — Marca METTA (19 estilos)

### Grupo DARK (fundo escuro #0C161B)

---

#### A — Headline impactante + foto pessoa direita
**Quando usar:** Cases nominais, prova social com foto de pessoa, statements com âncora humana.
**Funil:** MOFU, BOFU
**Teses:** case nominal (Hiperzoo, AMBI...), promessa numérica, autoridade founder-led
**NÃO usar:** tese abstrata sem cena humana, big number puro (número se perde)
**Exemplo de briefing:**
> "ad de prova social com Hiperzoo pra varejo de pet, story, mofo, credibilidade"

---

#### B — Foto top + headline mixed-weight + body bottom
**Quando usar:** Dor pessoal, exaustão, reframe de mantra — a foto "abre o cenário emocional" antes da copy bater.
**Funil:** TOFU, MOFU
**Teses:** dor_pessoal · statement_provocativo · reframe_mantra · lista_sintomas
**NÃO usar:** tese abstrata sem cena visual, big number (foto dilui o número)
**Exemplo:**
> "story de dor pra empresário refém do operacional, tom emocional, TOFU"

---

#### C — Tipografia pura sobre escuro
**Quando usar:** Pergunta diagnóstica seca, manifesto, frase de impacto. SEM foto — só texto sobre fundo dark.
**Funil:** MOFU, BOFU, retargeting
**Teses:** pergunta_diagnostica · manifesto · reframe_seco
**NÃO usar:** case nominal (não comporta logo), tese que precisa de imagem para funcionar
**Exemplo:**
> "pergunta provocativa: 'seu time sabe o que fazer quando bate a meta?' fundo dark puro, story"

---

#### D — Foto fullbleed overlay
**Quando usar:** Drama máximo, cinema editorial — foto ocupa o canvas inteiro com overlay escuro. Mood de capa de documentário.
**Funil:** TOFU, MOFU
**Teses:** dor_pessoal intensa · manifesto visual · retrato founder
**NÃO usar:** agenda de evento (não comporta data+CTA), big number

---

#### I — Retrato editorial P&B + logo badge
**Quando usar:** Autoridade pura. Foto do Tiago ou líder Metta em P&B com badge institucional. Tom de capa da Harvard Business Review.
**Funil:** MOFU, BOFU
**Teses:** quote_lider · autoridade_founder_led · posicionamento_editorial
**Exemplo:**
> "retrato editorial do Tiago, preto e branco, com badge Metta, quote de autoridade sobre gestão comercial"

---

#### DARK-CARTA — Carta/contrato em ângulo + selo
**Quando usar:** Convite Elite, capacity-limited, programa exclusivo. Mockup de carta sobre fundo dark.
**Funil:** BOFU, retargeting
**Teses:** convite_elite · vagas_limitadas_reais · programa_exclusivo
**NÃO usar:** tom descontraído, escassez fake (destrói marca), TOFU frio
**Exemplo:**
> "convite exclusivo pra programa Elite com vagas limitadas reais, BOFU, lista proprietária"

---

#### DARK-OBJETO — Objeto 3D conceito em destaque
**Quando usar:** Metáfora física do método. Objeto 3D (dominó, engrenagem, peças de xadrez) sobre fundo dark ancora o conceito.
**Funil:** MOFU, BOFU
**Teses:** metodo_etapas · efeito_cascata · framework_visual
**NÃO usar:** tese sem objeto-conceito claro, foto humana (não combina)
**Exemplo:**
> "ad sobre a diferença entre empresa que cresce e empresa que sobrevive, objeto 3D peças de xadrez, dark"

---

#### DARK-COLAGEM — Colagem fotográfica conceitual escura
**Quando usar:** Metáfora de encaixe ou transformação sistêmica. Múltiplos elementos em colagem.
**Funil:** MOFU
**Teses:** metafora_encaixe · transformacao_sistemica

---

### Grupo YELLOW (fundo ou elemento amarelo)

---

#### YELLOW-BLOCO — Bloco amarelo + foto pessoa direita + bullets
**Quando usar:** Cases com cliente nomeado + logo bar + resultados em bullets. Tom mais "flyer institucional" que storytelling.
**Funil:** MOFU, BOFU
**Teses:** case com bullets de resultado · logo bar com clientes
**NÃO usar:** tese de dor intensa (amarelo festivo mata gravidade), audiência exausta

---

#### YELLOW-EDITORIAL — Fundo amarelo + colagem P&B + número gigante
**Quando usar:** Big number é a tese. "+171%", "R$2.3M", "47 lojas". Número ocupa 40% do canvas.
**Funil:** MOFU, BOFU, retargeting
**Teses:** big_number_prova · market_share · data_institucional
**Exemplo:**
> "ad com o resultado da Vivo: +171% no pipeline em 90 dias, yellow editorial"

---

#### YELLOW-FRAME — Cartão escuro central em fundo amarelo
**Quando usar:** Pergunta que segmenta audiência + resposta rápida. Contraste de fundo amarelo com card dark central.
**Funil:** TOFU, MOFU
**Teses:** pergunta_segmentada · prova_rapida_pergunta

---

#### YELLOW-SPLIT — Split horizontal preto+amarelo
**Quando usar:** Statement de drama com oferta. Metade da tela de cada cor criando tensão visual.
**Funil:** MOFU, BOFU
**Teses:** statement_drama_oferta · convite_com_gancho

---

#### YELLOW-DRAW — Fundo amarelo + ilustração desenhada
**Quando usar:** Conceito visualmente simples, tese leve, TOFU de educação.
**Funil:** TOFU
**NÃO usar:** tese pesada, dor intensa, BOFU

---

### Grupo LIGHT (fundo claro)

---

#### H — Fundo branco + headline gigante
**Quando usar:** Statement seco, prova concreta com objeto (print, screenshot). Tipografia ocupa quase tudo.
**Funil:** TOFU, MOFU
**Teses:** prova_concreta_objeto · statement_seco

---

#### LIGHT-SURREAL — Fundo claro + colagem ilustrativa surreal
**Quando usar:** Dor pessoal com metáfora visual não-realista. Colagem conceitual leve sobre fundo claro.
**Funil:** TOFU, MOFU
**NÃO usar:** case nominal (não comporta logo)

---

#### LIGHT-TIPO — Fundo bege/cinza claro 100% tipográfico
**Quando usar:** Frase memorável de opostos, manifesto filosófico. Só tipografia sobre fundo neutro.
**Funil:** TOFU, retargeting
**Teses:** frase_memoravel_opostos · manifesto_filosofico

---

### Grupo INSTITUCIONAL

---

#### LOGO-WALL — Grade de logos + número grande
**Quando usar:** Prova de volume — 6+ clientes, ecossistema Metta. Logo grid + big number ao lado.
**Funil:** BOFU, retargeting
**Teses:** credibilidade_volume · ecossistema_agregado
**NÃO usar:** menos de 6 logos (dilui), case individual (use A)

---

#### NEWS-CARD — Manchete jornalística
**Quando usar:** Análise setorial, dado de mercado, estudo. Formato de manchete de jornal.
**Funil:** MOFU, retargeting
**Teses:** analise_setorial · panorama_dado · estudo_publicado
**Exemplo:**
> "manchete sobre empresas do varejo que perderam market share em 2025, news card, MOFU"

---

#### K — Bold dourado / urgência fundamentada
**Quando usar:** Fechamento de vagas, urgência real. Tipografia bold dourada, sem foto.
**Funil:** BOFU, retargeting
**Teses:** convite_exclusivo · escassez_real · fechamento_inscricoes
**NÃO usar:** escassez fake (destrói marca)

---

### Modelos NOVOS (adicionados 2026-05-15)

---

#### FOTO-PILL-CASUAL — Foto fullbleed light + headline casual + pill CTA
**Quando usar:** Resultado positivo, case de transformação leve, TOFU clean. Fundo BRANCO com foto editorial no topo e headline dark.
**Funil:** TOFU, MOFU
**Teses:** case_resultado_positivo · transformacao_visible · identificacao_leve
**NÃO usar:** tese de dor intensa (contraste emocional quebra o visual light), foto genérica stock

---

#### METTA-TWEET-CARD — Tweet-card tipográfico com avatar + statement
**Quando usar:** Quotes de autoridade, dados de impacto curtos, provocações virais. Avatar Metta no topo, statement em tipografia enorme.
**Funil:** TOFU, viral
**Teses:** provocacao_pensamento · dado_impacto_credencial · quote_autoridade
**NÃO usar:** copy longa (máx 160 chars), foto como background, tom corporativo genérico

---

## 5. Modelos disponíveis — Marca TIAGO (12 estilos)

> **Regra absoluta:** nunca pedir modelo Metta com `marca: tiago` ou vice-versa. São catálogos completamente separados.

### Camada Editorial-Cinema (carrosseis premium)

---

#### TIAGO-EDITORIAL-HERO — Capa editorial cinema
**Uso:** Capa (slide 1) de carrossel. Headline gigante + colagem surreal noir. Abre o gancho.
**Teses:** mantra_a_desmontar · statement_identidade · pergunta_diagnostica_abertura
**Quando:** "abre o carrossel do Tiago sobre gestão..."

---

#### TIAGO-EDITORIAL-CARD — Slide meio editorial (big stat / sintomas)
**Uso:** Slides 2-3. Prova quantitativa, lista de sintomas, dados contextualizados.
**Teses:** big_stat_contextualizado · lista_sintomas · prova_quantitativa_com_metodo

---

#### TIAGO-EDITORIAL-DARK — Slide noir investigativo
**Uso:** Slides do meio, tom psicológico/comportamental. Reframe diagnóstico pesado.
**Teses:** tese_psicologica · reframe_diagnostico_heavy · slide_noir_investigativo

---

#### TIAGO-EDITORIAL-CTA — Slide fechamento
**Uso:** Último slide. Engajamento ("Conta aqui..."), qualificação ("pra quem é/não é"), reveal de oferta.
**Variantes:** A (pergunta engajamento) · B (qualificação) · C (reveal + data)

---

#### TIAGO-TWITTER-CARD — Mock de tweet/X
**Uso:** Statement curto que cabe em ~120 chars, carrossel formato tweet. Card mock de post de Twitter.
**NÃO usar:** copy longa, quando carrossel editorial já foi escolhido (mistura quebra visual)

---

### Camada Lo-fi Cotidiano (feed/story dia a dia)

---

#### TIAGO-STORY-COVER-HERO — Foto lo-fi Tiago + headline + ARRASTA
**Uso:** Capa de story do dia a dia. Foto real do Tiago no ambiente + headline + "ARRASTA PRO LADO".

---

#### TIAGO-STORY-YELLOW-BLOCK — Foto ambiente + bloco amarelo central
**Uso:** Pergunta diagnóstica ancorada em ambiente real. Foto lo-fi do Tiago + bloco amarelo com texto.

---

#### TIAGO-STORY-MINIMAL-QUESTION — Foto contemplativa + texto leve
**Uso:** Reflexão baixo volume, pergunta aberta. Minimalista.

---

#### TIAGO-NOTES-MOCKUP — Mock iPhone Notes
**Uso:** Storytelling lista numerada ("Tomei 3 decisões:"), lições aprendidas como anotação pessoal.

---

#### TIAGO-TYPO-PURE — Tipográfico puro
**Uso:** Frase de impacto standalone, tese filosófica curta. Só tipografia.

---

#### TIAGO-DARK-SURREAL — Fundo preto + imagem surreal B&W
**Uso:** Intersticial entre slides pesados, capa estética sem copy.

---

#### TIAGO-PHOTO-RAW — Foto crua sem texto
**Uso:** Bastidor de vida (treino, viagem), humanização alta. Zero copy.

---

### Pareamento canônico de carrossel Tiago

**Sistema A — Editorial Cinema (premium):**
```
Slide 1: TIAGO-EDITORIAL-HERO (hook)
Slide 2-3: TIAGO-EDITORIAL-CARD (dado/dor) ou TIAGO-EDITORIAL-DARK (noir)
Slide final: TIAGO-EDITORIAL-CTA (fechamento)
```

**Sistema B — Lo-fi Cotidiano:**
```
Slide 1: TIAGO-STORY-COVER-HERO ou TIAGO-STORY-YELLOW-BLOCK
Slide 2-3: TIAGO-NOTES-MOCKUP ou TIAGO-STORY-MINIMAL-QUESTION
Intersticial opcional: TIAGO-DARK-SURREAL
Fechamento: TIAGO-PHOTO-RAW
```

**Regra:** nunca misturar sistema A com B no mesmo carrossel.

---

## 6. Exemplos de briefings prontos para copiar

### Metta — Case nominal (Estilo A)
```
Marca: Metta
Story pra Meta Ads.
Case da Hiperzoo — como abriram 12 lojas em 18 meses sem perder margem.
Funil: MOFU
Audiência: empresário do varejo, 40-55 anos, buscando crescer
Tom: credibilidade
```

### Metta — Dor pessoal (Estilo B ou LIGHT-SURREAL)
```
Marca: Metta
Story pra Meta Ads.
Empresário refém da própria operação — não tem como tirar férias porque se sair tudo para.
Funil: TOFU
Audiência: empresário de serviços, exausto, 40-55 anos
Tom: emocional
```

### Metta — Urgência / convite exclusivo (Estilo K ou DARK-CARTA)
```
Marca: Metta
Story pra Meta Ads.
Convite com vagas limitadas reais pro programa Elite — 8 vagas, fecham sexta.
Funil: BOFU
Audiência: lista proprietária quente, já conhece a Metta
Tom: direto, urgência real
```

### Metta — Big number (YELLOW-EDITORIAL)
```
Marca: Metta
Story pra Meta Ads.
+171% no pipeline da Vivo em 90 dias com o método comercial Metta.
Funil: MOFU
Audiência: diretor comercial B2B, empresas grandes
Tom: credibilidade, dado puro
```

### Metta — Manchete de mercado (NEWS-CARD)
```
Marca: Metta
Story ou feed.
Análise: 67% das empresas do varejo que fecharam em 2025 não tinham processo comercial documentado.
Funil: MOFU
Tom: intelectual, análise de mercado
```

### Metta — Objeto 3D / conceito (DARK-OBJETO)
```
Marca: Metta
Story pra Meta Ads.
A diferença entre empresa que cresce e empresa que sobrevive em 2026 é ter um processo estruturado.
Visual: objeto 3D peças de xadrez — cavalo dourado (cresce) vs peão prateado (sobrevive).
Funil: TOFU
Tom: provocador
```

### Metta — Tweet-card quote (METTA-TWEET-CARD)
```
Marca: Metta
Story ou feed.
Quote curta: "Em 2026, quem não tiver processo vai sentir isso na veia."
Formato: tweet-card com avatar Metta, statement tipográfico
Funil: TOFU, viral
Tom: provocador, direto
```

### Tiago — Carrossel editorial (Sistema A)
```
Marca: Tiago
Carrossel feed Instagram orgânico.
Tese: gerente de vendas vs vendedor com crachá de chefe — a pergunta que separa os dois.
Funil: MOFU
Formato: carrossel editorial cinema completo (abertura + desenvolvimento + CTA)
Tom: intelectual, voz pessoal do Tiago
```

### Tiago — Story do dia (Sistema B)
```
Marca: Tiago
Story Instagram.
Foto real do Tiago + headline: "3 decisões que tomei quando o time bateu a meta mas o lucro sumiu."
Funil: TOFU
Tom: pessoal, direto, lo-fi
```

---

## 7. O que a IA NÃO faz — limites e proteções

| Regra | Motivo |
|---|---|
| Nunca mistura modelos Metta com Tiago | Namespace isolado — são marcas distintas |
| Nunca usa escassez fake | Destrói credibilidade da marca |
| Nunca cria foto genérica de stock (sorrindo no escritório) | Quebra identidade editorial |
| Nunca coloca texto embutido na imagem gerada | Texto vem via overlay do assembler |
| Nunca auto-seleciona estilo quando confiança < 85% | Pede confirmação humana |
| Nunca inventa caso nominal (Hiperzoo, Sicredi) se não foi mencionado | Erro de informação |
| Nunca usa emoji em peças Metta | Proibido no DS — só permitido em Tiago |

---

## 8. Campos que a IA infere automaticamente (você não precisa falar)

| Se não falar... | A IA infere |
|---|---|
| Funil | Baseado na tese + audiência |
| Marca | `metta` (default — especifique "Tiago" se for pra marca pessoal) |
| Tom | Baseado no intent |
| Idade da audiência | Baseado no cargo (empresario → 40-55, founder → 35-45) |
| Plataforma | `meta_ads` |

---

## 9. Quando a IA vai te pedir esclarecimento

A IA para e pergunta quando:

- O briefing não deixa claro se é case individual ou prova agregada
- A data de evento foi mencionada mas sem o dia específico
- O CTA não foi definido (ex: "agendar diagnóstico" vs "baixar e-book")
- O segmento de audiência é muito vago pra um estilo que precisa de foto específica
- A tese pode ser de marca Metta ou Tiago — ambiguidade real

**Ela NÃO vai pedir** formato, funil, tom ou plataforma — esses ela infere.

---

## 10. Dicas para briefings melhores

1. **Diga a tese em 1 frase** — "A diferença entre empresa que cresce e que sobrevive é processo." é melhor que "quero falar sobre gestão."

2. **Mencione o cliente se houver** — "Hiperzoo", "Sicredi", "Vivo" = case nominal. A IA muda o estilo automaticamente.

3. **Diga o funil** — TOFU, MOFU, BOFU mudam tudo: visual, tom, urgência, CTA.

4. **Diga a audiência** — "empresário de varejo exausto" vs "diretor B2B buscando crescer" são personas completamente diferentes.

5. **Especifique a marca** — Default é Metta. Se quiser para o perfil do Tiago, diga "Tiago" ou "marca pessoal".

6. **Sugira o estilo se souber** — "quero no estilo tweet-card" ou "quero com objeto 3D" afina direto.

---

## Versão

`BRIEFING-GUIDE_v1.0` · 2026-05-15 · Compilado por Claude Code a partir da brand-knowledge v2.0
