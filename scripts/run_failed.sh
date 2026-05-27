#!/bin/bash
set -e

export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
export OPENAI_API_KEY="$OPENAI_API_KEY"
export OPENAI_IMAGE_API_KEY="$OPENAI_API_KEY"
export IMAGE_GEN_PROVIDER=openai
export LLM_PROVIDER=openai
export LLM_MODEL_OPENAI=gpt-4o
export LLM_MODEL_CHEAP=gpt-4o-mini
export ASSEMBLER=png
export OUTPUT_FORMAT=png
export BRAND_KNOWLEDGE_PATH=./brand-knowledge
export ARTIFACTS_DIR=./artifacts

PYTHON=".venv/bin/python3"
LOG_DIR="artifacts/test-run-all"
mkdir -p "$LOG_DIR"

PASS=0; FAIL=0; RESULTS=()

run_model() {
  local model="$1"; local briefing="$2"
  echo ""; echo "═══  $model  ═══"
  local log="$LOG_DIR/${model}.log"
  if $PYTHON pipeline.py "$briefing" --no-clarify 2>&1 | tee "$log" | grep -q "PNG salvo"; then
    local png=$(grep "PNG salvo:" "$log" | tail -1 | sed 's/.*PNG salvo: //')
    echo "  ✅ PASS → $png"
    RESULTS+=("PASS|$model"); ((PASS++)) || true
  else
    echo "  ❌ FAIL"
    RESULTS+=("FAIL|$model"); ((FAIL++)) || true
  fi
}

# Modelos que falharam por clarificação ou ainda não rodaram
run_model "FOTO-PILL-CASUAL" \
  "story metta foto casual bastidores: foto de workshop interno metta com equipe, clima de bastidores, tom descontraído. produto: consultoria metta. audiencia: empresarios varejo. sem cta obrigatorio. Use modelo FOTO-PILL-CASUAL."

run_model "H-fundo-branco-headline-gigante" \
  "story metta tipografia fundo branco: headline gigante 'Método. Não sorte.' sem foto, sem imagem, só tipografia preta em fundo branco. produto: método metta. audiencia: empresario varejo. funil: MOFU. Use modelo H-fundo-branco-headline-gigante."

run_model "K-bold-dourado-urgencia" \
  "story metta urgência scarcity: últimas 3 vagas para o Método Metta julho 2026. programa trimestral, 8 vagas por turma, vagas reais limitadas. produto: Método Metta. audiencia: empresarios qualificados warm. funil: BOFU. cta: GARANTIR VAGA. Use modelo K-bold-dourado-urgencia."

run_model "LIGHT-SURREAL" \
  "story metta light surreal abstrato: quando você para de vender e começa a atrair. conceito: transformação de mindset comercial. produto: método metta. audiencia: empresario varejo MOFU. imagem abstrata surreal. Use modelo LIGHT-SURREAL."

run_model "LIGHT-TIPO" \
  "story metta tipografia light fundo claro: dados não mentem, feeling sim. sem foto, tipografia pura, fundo claro. produto: método metta analytics. audiencia: empresario varejo. funil: MOFU. Use modelo LIGHT-TIPO."

run_model "LOGO-WALL" \
  "story metta logo wall prova social: mais de 80 empresas aplicaram o método Metta nos últimos 3 anos. segmentos: varejo pet, moda, alimentos, serviços. produto: método metta. audiencia: empresario frio TOFU. Use modelo LOGO-WALL."

run_model "METTA-TWEET-CARD" \
  "tweet card metta brand: 'Varejo sem processo é um negócio que depende de heroísmo diário.' tweet do perfil @mettacomercial. produto: conteúdo orgânico metta. audiencia: empresarios varejo. Use modelo METTA-TWEET-CARD."

run_model "NEWS-CARD" \
  "story metta news card lançamento: nova turma Método Metta abertura julho 2026. data: 14 de julho 2026. vagas: 8. produto: método metta. audiencia: lista proprietária warm. funil: BOFU. cta: INSCREVER-SE. Use modelo NEWS-CARD."

run_model "YELLOW-BLOCO" \
  "story metta yellow bloco lista: 3 decisões que mudam o resultado de qualquer varejo: 1) parar de vender pra todo mundo 2) construir processo de qualificação 3) medir o que importa. produto: método metta. audiencia: empresario varejo MOFU. Use modelo YELLOW-BLOCO."

run_model "YELLOW-DRAW" \
  "story metta yellow draw diagrama: funil de aquisição do varejo físico em 2026 — tráfego orgânico, conversão na loja, recompra. produto: método metta. audiencia: empresario varejo. funil: MOFU educação. Use modelo YELLOW-DRAW."

run_model "YELLOW-EDITORIAL" \
  "story metta yellow editorial big number: empresas que crescem 3x mais usam dados, não feeling. número destaque: 3X. subtítulo: é quanto crescem mais as empresas que decidem com dados. produto: método metta analytics. funil: MOFU. Use modelo YELLOW-EDITORIAL."

run_model "YELLOW-FRAME" \
  "story metta yellow frame stats: resultados consolidados 2025 — 340% crescimento tráfego orgânico, 2.1x aumento conversão, 45% redução CAC. produto: método metta. audiencia: empresario varejo MOFU. Use modelo YELLOW-FRAME."

run_model "YELLOW-SPLIT" \
  "story metta yellow split antes depois: antes do método — CAC alto, sem processo, dependência de tráfego pago. depois do método — CAC caiu 45%, LTV dobrou, equipe vende sozinha. produto: método metta. funil: MOFU. Use modelo YELLOW-SPLIT."

run_model "TIAGO-DARK-SURREAL" \
  "story tiago dark surreal editorial: quando o empresário para de apagar incêndio e começa a construir sistema. tiago alves, especialista varejo. imagem surrealista dark abstrata. audiencia: empresario varejo. funil: TOFU/MOFU. Use modelo TIAGO-DARK-SURREAL."

run_model "TIAGO-EDITORIAL-CARD" \
  "card tiago editorial 1080x1080: diferença entre crescer e escalar — crescer é trabalhar mais, escalar é ter processo. tiago alves consultor varejo. audiencia: empresario. funil: MOFU. Use modelo TIAGO-EDITORIAL-CARD."

run_model "TIAGO-EDITORIAL-CTA" \
  "story tiago editorial cta: diagnóstico gratuito 1h para empresários de varejo. tiago alves, consultor. vagas: 5 por semana. cta: AGENDAR DIAGNÓSTICO. audiencia: empresario varejo warm. funil: BOFU. Use modelo TIAGO-EDITORIAL-CTA."

run_model "TIAGO-EDITORIAL-DARK" \
  "story tiago editorial dark: você não tem problema de tráfego, você tem problema de oferta. tiago alves consultor varejo. sem cta. audiencia: empresario varejo. funil: TOFU/MOFU orgânico. Use modelo TIAGO-EDITORIAL-DARK."

run_model "TIAGO-EDITORIAL-HERO" \
  "story tiago editorial hero com foto: minha metodologia para transformar varejo físico em máquina de crescimento — 5 protocolos, 3 anos, 127 empresas. tiago alves fundador. foto do tiago. audiencia: empresario varejo. funil: MOFU. Use modelo TIAGO-EDITORIAL-HERO."

run_model "TIAGO-NOTES-MOCKUP" \
  "story tiago notes app mockup: 5 perguntas que todo dono de varejo deveria responder antes de investir em tráfego. formato: print de notes app. tiago alves. audiencia: empresario varejo. funil: TOFU educação. Use modelo TIAGO-NOTES-MOCKUP."

run_model "TIAGO-PHOTO-RAW" \
  "story tiago foto bastidores raw: foto do tiago alves em evento ao vivo, clima de bastidores, energia de palco. texto: obrigado a todos que vieram ontem. tom: autêntico, humano. audiencia: seguidores tiago. Use modelo TIAGO-PHOTO-RAW."

run_model "TIAGO-STORY-COVER-HERO" \
  "story tiago cover hero podcast: novo episódio — como triplicar o faturamento do varejo sem aumentar o CAC. foto do tiago. cta: OUVIR AGORA. audiencia: empresario varejo seguidores. Use modelo TIAGO-STORY-COVER-HERO."

run_model "TIAGO-STORY-MINIMAL-QUESTION" \
  "story tiago minimal pergunta provocação: você está crescendo ou está correndo? tipografia minimalista. fundo claro ou escuro. tiago alves. audiencia: empresario varejo. funil: TOFU orgânico. Use modelo TIAGO-STORY-MINIMAL-QUESTION."

run_model "TIAGO-STORY-YELLOW-BLOCK" \
  "story tiago yellow block lista: 3 erros que impedem o varejo de escalar — 1) depender de tráfego pago sem copy 2) crescer sem processo 3) vender pra todo mundo. tiago alves. audiencia: empresario varejo MOFU. Use modelo TIAGO-STORY-YELLOW-BLOCK."

run_model "TIAGO-TWITTER-CARD" \
  "tweet card tiago pessoal: 'A maioria contrata tráfego antes de ter copy. Resultado: dinheiro no ralo.' tweet de @tiago.alves.oliveira. perfil: tiago alves. verificado. audiencia: seguidores organico. Use modelo TIAGO-TWITTER-CARD."

run_model "TIAGO-TYPO-PURE" \
  "story tiago tipografia pura: 'Processo vence talento. Sempre.' sem foto, só tipografia. tiago alves. audiencia: empresario varejo. funil: TOFU orgânico. Use modelo TIAGO-TYPO-PURE."

echo ""
echo "════════════════════════════════════════"
echo "  FAILED RETRY: $PASS ✅  $FAIL ❌"
echo "════════════════════════════════════════"
for r in "${RESULTS[@]}"; do
  status=$(echo $r | cut -d'|' -f1); model=$(echo $r | cut -d'|' -f2)
  [[ "$status" == "PASS" ]] && echo "  ✅ $model" || echo "  ❌ $model"
done
echo ""
echo "Total PNGs gerados:"
ls /tmp/ad-generator-test/artifacts/outputs/*.png 2>/dev/null | wc -l
