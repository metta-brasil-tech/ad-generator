#!/bin/bash
# run_all_models.sh — roda os 33 modelos em sequência com briefings de teste
set -e

export ANTHROPIC_API_KEY="$ANTHROPIC_API_KEY"
export OPENAI_API_KEY="$OPENAI_API_KEY"
export OPENAI_IMAGE_API_KEY="$OPENAI_API_KEY"
export IMAGE_GEN_PROVIDER=openai
export LLM_PROVIDER=claude
export LLM_MODEL_CLAUDE=claude-opus-4-7
export ASSEMBLER=png
export OUTPUT_FORMAT=png
export BRAND_KNOWLEDGE_PATH=./brand-knowledge
export ARTIFACTS_DIR=./artifacts

PYTHON=".venv/bin/python3"
LOG_DIR="artifacts/test-run-all"
mkdir -p "$LOG_DIR"

PASS=0
FAIL=0
SKIP=0
RESULTS=()

run_model() {
  local model="$1"
  local briefing="$2"
  echo ""
  echo "═══════════════════════════════════════════"
  echo "  MODELO: $model"
  echo "═══════════════════════════════════════════"
  local log="$LOG_DIR/${model}.log"
  if $PYTHON pipeline.py "$briefing" 2>&1 | tee "$log" | grep -q "PNG salvo"; then
    local png=$(grep "PNG salvo:" "$log" | tail -1 | sed 's/.*PNG salvo: //')
    echo "  ✅ PASS → $png"
    RESULTS+=("PASS|$model|$png")
    ((PASS++)) || true
  else
    echo "  ❌ FAIL — veja $log"
    RESULTS+=("FAIL|$model|$log")
    ((FAIL++)) || true
  fi
}

# ── METTA ────────────────────────────────────────────────
run_model "A-headline-foto-dark" \
  "story metta prova social: Hiperzoo cresceu 340% no tráfego orgânico em 90 dias. CEO Ricardo Alves. Use modelo A-headline-foto-dark."

run_model "B-foto-top-headline-mixed" \
  "story metta: empresário que era refém da operação, hoje tem equipe que roda sozinha. Use modelo B-foto-top-headline-mixed."

run_model "C-tipografia-pura-dark" \
  "story metta tipografia dark: Você está gerenciando ou está liderando? Use modelo C-tipografia-pura-dark."

run_model "D-foto-fullbleed-overlay" \
  "story metta cinema: o momento em que um empresário decide parar de trabalhar no negócio e começar a trabalhar nele. Use modelo D-foto-fullbleed-overlay."

run_model "DARK-CARTA" \
  "story metta convite elite: programa Método Metta Q3 2026, apenas 8 vagas. Use modelo DARK-CARTA."

run_model "DARK-COLAGEM" \
  "story metta colagem dark: 3 anos de metodologia, 127 empresas transformadas. Use modelo DARK-COLAGEM."

run_model "DARK-OBJETO" \
  "story metta objeto 3d: clareza estratégica é o ativo mais raro no varejo hoje. Use modelo DARK-OBJETO."

run_model "FOTO-PILL-CASUAL" \
  "story metta casual: bastidores do workshop de ontem — sala lotada, energia incrível. Use modelo FOTO-PILL-CASUAL."

run_model "H-fundo-branco-headline-gigante" \
  "story metta tipografia branca: Método. Não sorte. Use modelo H-fundo-branco-headline-gigante."

run_model "I-retrato-editorial-pb" \
  "story metta retrato pb editorial: o empresário que não delega não tem empresa, tem emprego. Use modelo I-retrato-editorial-pb."

run_model "K-bold-dourado-urgencia" \
  "story metta urgência: últimas 3 vagas para o Método Metta julho/2026. Use modelo K-bold-dourado-urgencia."

run_model "LIGHT-SURREAL" \
  "story metta surreal abstrato: quando você para de vender e começa a atrair. Use modelo LIGHT-SURREAL."

run_model "LIGHT-TIPO" \
  "story metta tipografia light: dados não mentem. Feeling sim. Use modelo LIGHT-TIPO."

run_model "LOGO-WALL" \
  "story metta logo wall: mais de 80 empresas já aplicaram o método Metta. Use modelo LOGO-WALL."

run_model "METTA-TWEET-CARD" \
  "tweet card metta: varejo sem processo é um negócio que depende de heroísmo diário. Use modelo METTA-TWEET-CARD."

run_model "NEWS-CARD" \
  "story metta news card: nova turma Método Metta — inscrições abertas julho 2026. Use modelo NEWS-CARD."

run_model "YELLOW-BLOCO" \
  "story metta yellow bloco: 3 decisões que mudam o resultado de qualquer varejo. Use modelo YELLOW-BLOCO."

run_model "YELLOW-DRAW" \
  "story metta yellow draw: o funil de aquisição que funciona para o varejo físico em 2026. Use modelo YELLOW-DRAW."

run_model "YELLOW-EDITORIAL" \
  "story metta editorial: empresas que crescem 3x mais usam dados, não feeling. Use modelo YELLOW-EDITORIAL."

run_model "YELLOW-FRAME" \
  "story metta yellow frame: prova social agregada — 340% tráfego, 2.1x conversão, -45% CAC. Use modelo YELLOW-FRAME."

run_model "YELLOW-SPLIT" \
  "story metta yellow split: antes × depois da metodologia. CAC caiu 45%, LTV dobrou. Use modelo YELLOW-SPLIT."

# ── TIAGO ────────────────────────────────────────────────
run_model "TIAGO-DARK-SURREAL" \
  "story tiago surreal dark: quando o empresário para de apagar incêndio e começa a construir sistema. Use modelo TIAGO-DARK-SURREAL."

run_model "TIAGO-EDITORIAL-CARD" \
  "card tiago editorial: a diferença entre crescer e escalar é ter processo ou ter heroísmo. Use modelo TIAGO-EDITORIAL-CARD."

run_model "TIAGO-EDITORIAL-CTA" \
  "story tiago editorial cta: diagnóstico gratuito de 1h para empresários de varejo. Vagas limitadas. Use modelo TIAGO-EDITORIAL-CTA."

run_model "TIAGO-EDITORIAL-DARK" \
  "story tiago editorial dark: você não tem problema de tráfego. Você tem problema de oferta. Use modelo TIAGO-EDITORIAL-DARK."

run_model "TIAGO-EDITORIAL-HERO" \
  "story tiago hero: minha metodologia para transformar varejo físico em máquina de crescimento. Use modelo TIAGO-EDITORIAL-HERO."

run_model "TIAGO-NOTES-MOCKUP" \
  "story tiago notes mockup: 5 perguntas que todo dono de varejo deveria responder antes de investir em tráfego. Use modelo TIAGO-NOTES-MOCKUP."

run_model "TIAGO-PHOTO-RAW" \
  "story tiago foto raw: bastidores do evento de ontem — obrigado a todos que vieram. Use modelo TIAGO-PHOTO-RAW."

run_model "TIAGO-STORY-COVER-HERO" \
  "story tiago cover hero: novo episódio do podcast — como triplicar o faturamento do varejo sem aumentar o CAC. Use modelo TIAGO-STORY-COVER-HERO."

run_model "TIAGO-STORY-MINIMAL-QUESTION" \
  "story tiago minimal: você está crescendo ou está correndo? Use modelo TIAGO-STORY-MINIMAL-QUESTION."

run_model "TIAGO-STORY-YELLOW-BLOCK" \
  "story tiago yellow block: 3 erros que impedem o varejo de escalar. Use modelo TIAGO-STORY-YELLOW-BLOCK."

run_model "TIAGO-TWITTER-CARD" \
  "tweet card tiago: a maioria contrata tráfego antes de ter copy. Resultado: dinheiro no ralo. Use modelo TIAGO-TWITTER-CARD."

run_model "TIAGO-TYPO-PURE" \
  "story tiago tipografia pura: processo vence talento. Sempre. Use modelo TIAGO-TYPO-PURE."

# ── RELATÓRIO ────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════════════"
echo "  RESULTADO FINAL: $PASS ✅  $FAIL ❌  de 33 modelos"
echo "════════════════════════════════════════════════════"
echo ""
echo "PASS:"
for r in "${RESULTS[@]}"; do
  [[ "$r" == PASS* ]] && echo "  ✅ $(echo $r | cut -d'|' -f2)"
done
echo ""
echo "FAIL:"
for r in "${RESULTS[@]}"; do
  [[ "$r" == FAIL* ]] && echo "  ❌ $(echo $r | cut -d'|' -f2) → $(echo $r | cut -d'|' -f3)"
done

echo ""
echo "PNGs gerados em: artifacts/outputs/"
ls artifacts/outputs/*.png 2>/dev/null | wc -l | xargs echo "Total de PNGs:"
