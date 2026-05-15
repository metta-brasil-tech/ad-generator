# Como usar o bot de geração de anúncios

> Guia para qualquer pessoa usar o bot no Telegram, sem precisar saber termos técnicos.

---

## Duas formas de usar

### Forma 1 — Fluxo guiado (recomendado)

Digite `/novo` no Telegram. O bot vai fazer 6 perguntas com botões de resposta. Você só clica.

```
/novo
  ↓
[1] Qual a marca?
    🟡 Metta   |   👤 Tiago (pessoal)
  ↓
[2] Qual o tamanho?
    📱 Feed (1080×1350)   |   📽 Story (1080×1920)
    ⬛ Quadrado (1080×1080)   |   🎠 Carrossel
  ↓
[3] Para quem é? (funil)
    ❄️ Audiência fria   |   🌡 Já me conhece
    🔥 Pronto pra comprar   |   🔁 Já interagiu
  ↓
[4] Qual o objetivo?
    🏆 Case de cliente   |   😤 Dor / problema
    💡 Pergunta provocativa   |   📅 Convite / evento
    📊 Número / resultado   |   🏛 Posicionamento
  ↓
[5] Qual o tom?
    🎖 Credibilidade   |   ❤️ Emocional
    ⚡ Provocador   |   🏢 Institucional
    🎯 Direto   |   🧠 Intelectual
  ↓
[6] Me conta a ideia em 1-2 frases: (você digita)
  ↓
⏳ Gerando... (1-2 min)
  ↓
📸 PNG gerado no chat
```

---

### Forma 2 — Texto livre

Mande uma mensagem direta com o briefing completo. O bot entende e já gera.

**Modelo de briefing completo:**
```
Marca: Metta
Formato: story
Funil: MOFU
Objetivo: case de cliente
Tom: credibilidade
Tese: A Hiperzoo abriu 12 lojas em 18 meses sem perder margem usando nosso método.
```

**Versão curta (a IA infere o resto):**
```
story Metta, case da Hiperzoo, 12 lojas em 18 meses, credibilidade, MOFU
```

---

## Referência das opções

### Marca
| Opção | Quando usar |
|---|---|
| **Metta** | Anúncio institucional da empresa Metta |
| **Tiago** | Conteúdo do perfil pessoal do Tiago Alves |

> ⚠️ Nunca misture as duas marcas no mesmo anúncio.

---

### Tamanho
| Opção | Dimensão | Onde aparece |
|---|---|---|
| **Feed** | 1080×1350px | Grade do Instagram (foto de post) |
| **Story** | 1080×1920px | Story e Reels completo |
| **Quadrado** | 1080×1080px | Post quadrado no feed |
| **Carrossel** | 1080×1350px | Slides do carrossel (mesmo tamanho do feed) |

---

### Funil — para quem é o anúncio?
| Opção | Significado | Tipo de pessoa |
|---|---|---|
| **Audiência fria (TOFU)** | Nunca te viu antes | Novo público, ainda não te conhece |
| **Já me conhece (MOFU)** | Já interagiu, está avaliando | Seguidor, já viu seus posts |
| **Pronto pra comprar (BOFU)** | Está decidindo comprar | Lead quente, já conhece o produto |
| **Já interagiu (Retargeting)** | Já visitou site ou clicou em ad | Pixel/lista de remarketing |

---

### Objetivo — o que o anúncio comunica?
| Opção | Quando usar | Exemplo |
|---|---|---|
| **Case de cliente** | Tem nome de cliente real (Hiperzoo, Vivo...) | "A Hiperzoo abriu 12 lojas em 18 meses" |
| **Dor / problema** | Fala de sofrimento, exaustão, problema do empresário | "Você está refém da sua própria operação?" |
| **Pergunta provocativa** | Questiona o óbvio, desafia crença | "Gerente de vendas ou vendedor com crachá de chefe?" |
| **Convite / evento** | Tem data, webinário, evento presencial | "Evento Metta — 25 de junho em SP" |
| **Número / resultado** | Métrica em destaque | "+171% no pipeline da Vivo em 90 dias" |
| **Posicionamento** | Imagem institucional da marca | "Metta + Sicredi + Vivo + Korin" |

---

### Tom — como o anúncio soa?
| Opção | Quando usar |
|---|---|
| **Credibilidade** | Cases, dados, prova social — tom sóbrio e autoridade |
| **Emocional** | Dor, exaustão, transformação — bate no coração |
| **Provocador** | Questiona, desafia, polariza — faz pensar |
| **Institucional** | Metta + clientes grandes — tom de holding |
| **Direto** | Urgência, convite, ação imediata — sem rodeios |
| **Intelectual** | Diagnóstico, filosofia, análise — tom de especialista |

---

## Exemplos prontos para copiar

### Exemplo 1 — Case com cliente
```
/novo
→ Metta
→ Feed
→ Já me conhece (MOFU)
→ Case de cliente
→ Credibilidade
→ A Hiperzoo abriu 12 lojas em 18 meses sem perder margem com o método Metta.
```

### Exemplo 2 — Dor do empresário
```
/novo
→ Metta
→ Story
→ Audiência fria (TOFU)
→ Dor / problema
→ Emocional
→ Você trabalha 12 horas por dia mas a empresa não anda sem você. Isso não é crescimento, é uma prisão.
```

### Exemplo 3 — Big number
```
/novo
→ Metta
→ Feed
→ Já me conhece (MOFU)
→ Número / resultado
→ Credibilidade
→ +171% no pipeline da Vivo em 90 dias. Mesmo time, mesmo produto. Método diferente.
```

### Exemplo 4 — Pergunta provocativa (Tiago)
```
/novo
→ Tiago
→ Carrossel
→ Já me conhece (MOFU)
→ Pergunta provocativa
→ Intelectual
→ Seu gerente de vendas realmente gerencia, ou só tem o crachá do cargo?
```

### Exemplo 5 — Convite evento
```
/novo
→ Metta
→ Story
→ Já me conhece (MOFU)
→ Convite / evento
→ Institucional
→ Evento Metta em São Paulo — 25 de junho. Sicredi, Vivo e Korin confirmados. Vagas limitadas.
```

---

## Comandos disponíveis

| Comando | O que faz |
|---|---|
| `/novo` | Inicia o fluxo guiado passo a passo com botões |
| `/start` | Mesma coisa que /novo |
| `/help` | Mostra este resumo dentro do Telegram |
| `/cancelar` | Cancela o fluxo atual sem gerar |

---

## Perguntas frequentes

**O bot demorou mais de 2 minutos. Está travado?**
Não — o pipeline pode levar até 5 minutos em pico. Aguarde. Se passar de 5 min, aparece uma mensagem de erro.

**Posso mandar o briefing em inglês?**
Sim, mas PT-BR funciona melhor — o sistema foi treinado com briefings em português.

**Posso pedir dois tamanhos diferentes do mesmo anúncio?**
Por enquanto não — precisa fazer uma geração por vez. Use `/novo` duas vezes.

**Como peço a mesma imagem no estilo do xadrez ou troféu?**
Mencione o objeto no texto livre: "objeto 3D peças de xadrez" ou "troféu Copa do Mundo 3D".

**A imagem gerada não ficou boa. E agora?**
Use `/novo` e refine a tese — quanto mais específico o texto da ideia, melhor o resultado.

---

## Versão

`COMO-USAR-O-BOT_v1.0` · 2026-05-15
