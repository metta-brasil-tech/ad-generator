"""Telegram bot — recebe briefings e devolve o anúncio gerado."""
from __future__ import annotations

import logging
import os
from pathlib import Path

import httpx
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
API_URL = os.environ.get("API_URL", "http://api:8000")
# Timeout generoso — o pipeline pode demorar ~2 min em live mode
REQUEST_TIMEOUT = 300.0


async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Olá! Sou o gerador de anúncios da Metta. 🎯\n\n"
        "Me envie um briefing em texto e eu gero o anúncio para você.\n\n"
        "Exemplo:\n"
        "_ad de prova social com Hiperzoo pra varejo pet, story_",
        parse_mode="Markdown",
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "*Como usar:*\n"
        "Envie uma mensagem de texto descrevendo o anúncio.\n\n"
        "*Exemplos:*\n"
        "• `ad de prova social com Hiperzoo, story`\n"
        "• `story de dor pra empresário refém da operação`\n"
        "• `convite pra webinário de junho, tom institucional`\n\n"
        "*Comandos:*\n"
        "/start — boas-vindas\n"
        "/help — este menu",
        parse_mode="Markdown",
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    briefing = update.message.text.strip()
    if not briefing:
        return

    msg = await update.message.reply_text("⏳ Gerando seu anúncio... aguarde (pode levar 1-2 min).")

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            response = await client.post(
                f"{API_URL}/generate",
                json={"briefing": briefing},
            )

        if response.status_code != 200:
            detail = response.json().get("detail", response.text)
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
                    caption=f"`{run_id}`",
                    parse_mode="Markdown",
                )
        else:
            await msg.edit_text(
                f"✅ Anúncio gerado, mas imagem não encontrada localmente.\n"
                f"Run ID: `{run_id}`",
                parse_mode="Markdown",
            )

    except httpx.TimeoutException:
        await msg.edit_text("❌ Timeout: o pipeline demorou mais que 5 minutos.")
    except Exception as e:
        logger.exception("Unexpected error generating ad")
        await msg.edit_text(f"❌ Erro inesperado: {e}")


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Telegram bot iniciado (polling)...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
