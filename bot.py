import os
from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from deep_translator import GoogleTranslator

# Получаем переменные окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
BASE_URL = os.getenv("https://tarjimonbot-baij.onrender.com")  # пример: https://tarjimonbot-baij.onrender.com
WEBHOOK_PATH = "/webhook"

if not TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN не задан. Добавьте его в переменные окружения Render.")
if not BASE_URL:
    raise RuntimeError("BASE_URL не задан. Добавьте его в переменные окружения Render.")

app = Flask(__name__)
translator = GoogleTranslator(source="auto", target="en")
application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! TarjimonBot ishga tayyor. Matn yuboring.")

async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    translated = translator.translate(text)
    await update.message.reply_text(translated)

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))

@app.route("/")
def index():
    return "TarjimonBot is alive!"

@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

@app.route("/setwebhook")
async def set_webhook():
    success = await application.bot.set_webhook(f"{BASE_URL}{WEBHOOK_PATH}")
    return f"Webhook set: {success}"

if __name__ == "__main__":
    application.run_polling()
    
