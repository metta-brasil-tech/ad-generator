"""Telegram bot — fluxo guiado passo a passo para gerar anúncios."""
from __future__ import annotations

import logging
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, filters, ContextTypes,
)

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API_URL = os.environ.get("API_URL", "http://api:8000")
REQUEST_TIMEOUT = 300.0

# Estados do fluxo
STEP_MARCA, STEP_FORMATO, STEP_FUNIL, STEP_OBJETIVO, STEP_TOM, STEP_TESE = range(6)


def _kb(buttons: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    """Cria teclado inline com 2 botões por linha."""
    rows = []
    row = []
    for i, (label, data) in enumerate(buttons):
        row.append(InlineKeyboardButton(label, callback_data=data))
        if len(row) == 2:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return InlineKeyboardMarkup(rows)


# ─── /start ─────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text(
        "👋 Olá! Vou te guiar para criar seu anúncio.\n\n"
        "Você pode responder às perguntas abaixo *ou* enviar o briefing direto em texto.\n\n"
        "Vamos começar. Qual é a *marca*?",
        parse_mode="Markdown",
        reply_markup=_kb([
            ("🟡 Metta", "marca:metta"),
            ("👤 Tiago (pessoal)", "marca:tiago"),
        ]),
    )
    return STEP_MARCA


# ─── /novo ──────────────────────────────────────────────────────────────────

async def cmd_novo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return await cmd_start(update, context)


# ─── PASSO 1 — Marca ────────────────────────────────────────────────────────

async def step_marca(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    q = update.callback_query
    await q.answer()
    context.user_data["marca"] = q.data.split(":")[1]

    await q.edit_message_text(
        f"✅ Marca: *{context.user_data['marca'].capitalize()}*\n\n"
        "Qual é o *tamanho* do anúncio?",
        parse_mode="Markdown",
        reply_markup=_kb([
            ("📱 Feed (1080×1350)", "formato:feed"),
            ("📽 Story (1080×1920)", "formato:story"),
            ("⬛ Quadrado (1080×1080)", "formato:sqr"),
            ("🎠 Carrossel", "formato:carrossel"),
        ]),
    )
    return STEP_FORMATO


# ─── PASSO 2 — Formato / Tamanho ────────────────────────────────────────────

async def step_formato(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    q = update.callback_query
    await q.answer()
    context.user_data["formato"] = q.data.split(":")[1]

    labels = {
        "feed": "Feed (1080×1350)",
        "story": "Story (1080×1920)",
        "sqr": "Quadrado (1080×1080)",
        "carrossel": "Carrossel",
    }
    await q.edit_message_text(
        f"✅ Tamanho: *{labels[context.user_data['formato']]}*\n\n"
        "Para quem é esse anúncio? Qual etapa do funil?",
        parse_mode="Markdown",
        reply_markup=_kb([
            ("❄️ Audiência fria (TOFU)", "funil:TOFU"),
            ("🌡 Já me conhece (MOFU)", "funil:MOFU"),
            ("🔥 Pronto pra comprar (BOFU)", "funil:BOFU"),
            ("🔁 Já interagiu (Retargeting)", "funil:retargeting"),
        ]),
    )
    return STEP_FUNIL


# ─── PASSO 3 — Funil ────────────────────────────────────────────────────────

async def step_funil(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    q = update.callback_query
    await q.answer()
    context.user_data["funil"] = q.data.split(":")[1]

    await q.edit_message_text(
        f"✅ Funil: *{context.user_data['funil']}*\n\n"
        "Qual é o *objetivo* do anúncio?",
        parse_mode="Markdown",
        reply_markup=_kb([
            ("🏆 Case de cliente", "objetivo:prova_social_case_nominal"),
            ("😤 Dor / problema", "objetivo:dor_pessoal"),
            ("💡 Pergunta provocativa", "objetivo:reframe_intelectual"),
            ("📅 Convite / evento", "objetivo:convite_evento"),
            ("📊 Número / resultado", "objetivo:promessa_numerica"),
            ("🏛 Posicionamento", "objetivo:posicionamento_institucional"),
        ]),
    )
    return STEP_OBJETIVO


# ─── PASSO 4 — Objetivo / Intent ────────────────────────────────────────────

async def step_objetivo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    q = update.callback_query
    await q.answer()
    context.user_data["intent"] = q.data.split(":")[1]

    labels = {
        "prova_social_case_nominal": "Case de cliente",
        "dor_pessoal": "Dor / problema",
        "reframe_intelectual": "Pergunta provocativa",
        "convite_evento": "Convite / evento",
        "promessa_numerica": "Número / resultado",
        "posicionamento_institucional": "Posicionamento",
    }
    await q.edit_message_text(
        f"✅ Objetivo: *{labels[context.user_data['intent']]}*\n\n"
        "Qual é o *tom* do anúncio?",
        parse_mode="Markdown",
        reply_markup=_kb([
            ("🎖 Credibilidade", "tom:credibilidade"),
            ("❤️ Emocional", "tom:emocional"),
            ("⚡ Provocador", "tom:provocador"),
            ("🏢 Institucional", "tom:institucional"),
            ("🎯 Direto", "tom:direto"),
            ("🧠 Intelectual", "tom:intelectual"),
        ]),
    )
    return STEP_TOM


# ─── PASSO 5 — Tom ──────────────────────────────────────────────────────────

async def step_tom(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    q = update.callback_query
    await q.answer()
    context.user_data["tom"] = q.data.split(":")[1]

    await q.edit_message_text(
        f"✅ Tom: *{context.user_data['tom'].capitalize()}*\n\n"
        "Agora me conta a *ideia principal* do anúncio em 1 ou 2 frases.\n\n"
        "_Exemplo: 'A Hiperzoo abriu 12 lojas em 18 meses usando nosso método. Foto do dono na loja.'_",
        parse_mode="Markdown",
    )
    return STEP_TESE


# ─── PASSO 6 — Tese (texto livre) → gera o ad ───────────────────────────────

async def step_tese(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    tese = update.message.text.strip()
    if not tese:
        await update.message.reply_text("Por favor, escreva a ideia do anúncio.")
        return STEP_TESE

    d = context.user_data
    briefing = (
        f"Marca: {d.get('marca', 'metta')}\n"
        f"Formato: {d.get('formato', 'feed')}\n"
        f"Funil: {d.get('funil', 'TOFU')}\n"
        f"Objetivo: {d.get('intent', 'dor_pessoal')}\n"
        f"Tom: {d.get('tom', 'direto')}\n"
        f"Tese: {tese}"
    )

    msg = await update.message.reply_text("⏳ Gerando seu anúncio... aguarde (1-2 min).")
    await _gerar_ad(update, context, msg, briefing)
    context.user_data.clear()
    return ConversationHandler.END


# ─── Briefing direto (texto livre sem fluxo guiado) ─────────────────────────

async def handle_texto_livre(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    briefing = update.message.text.strip()
    if not briefing:
        return
    msg = await update.message.reply_text("⏳ Gerando seu anúncio... aguarde (1-2 min).")
    await _gerar_ad(update, context, msg, briefing)


# ─── Geração em si ──────────────────────────────────────────────────────────

async def _gerar_ad(update, context, msg, briefing: str) -> None:
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                f"{API_URL}/generate",
                json={"briefing": briefing},
            )

        if response.status_code != 200:
            detail = response.json().get("detail", response.text[:300])
            await msg.edit_text(f"❌ Erro ao gerar anúncio:\n`{detail}`", parse_mode="Markdown")
            return

        result = response.json()
        png_path = result.get("png_path")
        run_id = result.get("run_id", "")

        if png_path and Path(png_path).exists():
            await msg.edit_text("✅ Pronto!")
            with open(png_path, "rb") as f:
                await update.message.reply_photo(
                    photo=f,
                    caption=f"Run: `{run_id}`\n\nUse /novo para criar outro.",
                    parse_mode="Markdown",
                )
        else:
            await msg.edit_text(
                f"✅ Gerado, mas imagem não encontrada localmente.\nRun: `{run_id}`",
                parse_mode="Markdown",
            )

    except httpx.TimeoutException:
        await msg.edit_text("❌ Timeout: o pipeline demorou mais que 5 minutos.")
    except Exception as e:
        logger.exception("Erro ao gerar anúncio")
        await msg.edit_text(f"❌ Erro inesperado: {e}")


# ─── /help ──────────────────────────────────────────────────────────────────

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "*Como usar o gerador:*\n\n"
        "▶️ /novo — inicia o fluxo guiado passo a passo\n"
        "✏️ Ou envie o briefing direto em texto livre\n\n"
        "*Tamanhos disponíveis:*\n"
        "• Feed — 1080×1350px\n"
        "• Story — 1080×1920px\n"
        "• Quadrado — 1080×1080px\n"
        "• Carrossel — 1080×1350px\n\n"
        "*Marcas:*\n"
        "• Metta (institucional)\n"
        "• Tiago (perfil pessoal)\n\n"
        "*Exemplo de texto livre:*\n"
        "`Marca Metta, story, MOFU, case da Hiperzoo — abriram 12 lojas em 18 meses sem perder margem, tom credibilidade`",
        parse_mode="Markdown",
    )


async def cmd_cancelar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data.clear()
    await update.message.reply_text("Cancelado. Use /novo para começar de novo.")
    return ConversationHandler.END


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", cmd_start),
            CommandHandler("novo", cmd_novo),
        ],
        states={
            STEP_MARCA:    [CallbackQueryHandler(step_marca,    pattern="^marca:")],
            STEP_FORMATO:  [CallbackQueryHandler(step_formato,  pattern="^formato:")],
            STEP_FUNIL:    [CallbackQueryHandler(step_funil,    pattern="^funil:")],
            STEP_OBJETIVO: [CallbackQueryHandler(step_objetivo, pattern="^objetivo:")],
            STEP_TOM:      [CallbackQueryHandler(step_tom,      pattern="^tom:")],
            STEP_TESE:     [MessageHandler(filters.TEXT & ~filters.COMMAND, step_tese)],
        },
        fallbacks=[CommandHandler("cancelar", cmd_cancelar)],
        allow_reentry=True,
    )

    app.add_handler(conv)
    app.add_handler(CommandHandler("help", cmd_help))
    # Texto livre fora do fluxo guiado — gera direto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_texto_livre))

    logger.info("Telegram bot iniciado (polling)...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
