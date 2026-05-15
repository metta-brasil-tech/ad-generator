# Image Prompt — Base universal Metta

> **Esse doc é o substrato comum.** Todo prompt por estilo herda dele. Sobrescreve só o que precisa.

## Identidade visual da marca (NÃO sobrescrever)

- **Brasil.** Sempre decisor brasileiro — cor de pele, traço, idade 35-55, mood corporativo executivo. Nunca americano genérico, nunca asiático stock.
- **Editorial.** Estética de revista de negócios séria (HBR, Exame, Bloomberg Businessweek). Nunca lifestyle Instagram.
- **Decision-grade.** Olhar pensativo, reflexivo, em ação. Nunca sorriso fake stock. Nunca pose de "executivo bem-sucedido".
- **Sujeito íntegro.** JAMAIS recortar sujeito humano principal. Composição inclui rosto + ombros mínimo, idealmente até cintura.
- **Profundidade de campo rasa.** Background desfocado, sujeito em foco — exceto quando o cenário É a narrativa.
- **Luz natural.** Window light, golden hour, ou luz dura editorial. Nunca flash duro, nunca anel de LED.

## Constraints universais

- **Aspect ratio:** 9:16 (STORY) por default. Override em estilos específicos.
- **Resolução:** 4K (Nano Banana 2 entrega nativo). gpt-image-1 fallback 1024×1024 → upscale.
- **Negative prompt universal:**
  - no smiling-stock-pose
  - no cartoon, no illustration (exceto LIGHT-SURREAL que é colagem)
  - no anime, no 3d render generic
  - no logos visible (exceto quando explicitamente pedido)
  - no text in image (texto vem via overlay no Figma)
  - no recortes de sujeito principal
  - no ring light, no flash duro
  - no fake teeth-bleached smile

## Vocabulário de mood (escolher 1-2)

- `serious confidence` — autoridade tranquila, profissional
- `quiet exhaustion` — exaustão silenciosa, refém da operação
- `pensive reflection` — reflexão pensativa, decisão pesada
- `calm authority` — calma de quem decide
- `editorial gravitas` — peso de capa de revista
- `cinematic intimacy` — momento íntimo cinematográfico

## Tokens de iluminação (escolher 1)

- `warm window light, soft shadows` — luz quente de janela
- `golden hour rim light` — luz dourada de fim de tarde
- `editorial moody, hard side light` — luz dura lateral editorial
- `overhead diffused, neutral` — luz difusa neutra de cima
- `corporate window, cold backlight` — janela corporativa com contraluz

## Tokens de composição (escolher 1)

- `rule of thirds, subject right, decision-maker looking left` — clássica entrevista
- `centered composition, eye contact direct` — olhar direto (raro, só em assertivos)
- `subject left, environmental context right` — sujeito + contexto
- `cropped tight, shoulders up, paper texture wall` — close editorial
- `wide environmental, subject small in frame` — solidão na escala

## Tokens de paleta visual da foto (escolher 1)

- `warm earth tones, mustard accent` — terroso quente (combina yellow Metta)
- `cool steel blue, dim corporate` — azul aço corporativo
- `desaturated muted, editorial dark` — dessaturado moody
- `high contrast B&W` — preto-e-branco editorial (raro)
- `warm orange-amber, golden grading` — laranja-âmbar quente

## Estrutura padrão de prompt (use isso como template)

```
[mood] portrait of a brazilian {audience_descriptor},
{age_range}, {clothing}, {action_or_pose},
{lighting},
{composition},
{palette},
photographed in {environment},
shallow depth of field, shot on {camera},
editorial photography, 4K, sharp focus on eyes,
no text, no logos, sujeito íntegro
```

### Variáveis típicas por audiência

| Audience | descriptor | age | clothing |
|---|---|---|---|
| Empresário varejo | varejo retail entrepreneur | 40-55 | jaqueta lã, camisa social aberta |
| Diretor B2B serviços | service-business director | 38-52 | terno escuro, sem gravata |
| Empresária | woman entrepreneur, owner | 35-50 | blazer sóbrio, joia sutil |
| Líder comercial | commercial team leader | 32-48 | smart casual, mangas dobradas |
| Founder tech | tech founder | 30-45 | camiseta lisa, óculos minimalista |

## Câmeras de referência (escolher 1)

- `shot on Hasselblad H6D-100c, 80mm lens` — formato médio editorial
- `shot on Leica SL2, 35mm Summilux` — reportagem fina
- `shot on Sony A7R V, 85mm GM f/1.4` — retrato moderno limpo
- `shot on Canon R5, 50mm f/1.2L` — retrato cinematográfico

## Ambientes pré-aprovados

- Escritório corporativo com janela grande (estética de holding)
- Showroom de concessionária / loja física (varejo)
- Living moderno de casa de classe alta (founder-led / Tiago)
- Café/restaurante sofisticado em luz natural
- Sala de reunião pequena, mesa de madeira escura
- Industrial/galpão (logística, varejo distribuído)
- Studio neutro com paper texture wall (close editorial)

## Anti-padrões universais (NÃO incluir em prompt)

- ❌ "successful businessman" (gera pose fake)
- ❌ "happy" / "smiling" (destrói gravidade)
- ❌ "team meeting" / "high-five" (estética stock)
- ❌ "modern office with glass walls" (genérico)
- ❌ "professional headshot" (LinkedIn vibe)
- ❌ "thumbs up" / "celebration" (proibido)
- ❌ "looking at chart" / "graph in background" (cliché)

## Iteração

Se primeira geração não bater:
1. Tentar com `reference_image` diferente do banco
2. Ajustar mood (`serious confidence` → `pensive reflection`)
3. Trocar câmera (Hasselblad → Leica)
4. Reduzir verbosidade do prompt — Nano Banana 2 funciona melhor com prompts curtos + 2-3 refs

## Versão

`base_v1.0` · 2026-05-13 · Head de Design Metta
