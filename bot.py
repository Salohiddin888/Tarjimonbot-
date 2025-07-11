# bot.py — updated with your token and BASE_URL
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
from googletrans import Translator

# Static environment variables (⚠️ in real use, set them in Render ENV)
TOKEN = "8148077100:AAGu5yAI0JgB2dYvWY9idjQAYVWATjvuBq8"
BASE_URL = "https://tarjimonbot-baij.onrender.com"
WEBHOOK_PATH = "/webhook"

translator = Translator()
app = Flask(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! TarjimonBot ishga tayyor. Matn yuboring.")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    result = translator.translate(text, dest="en")
    await update.message.reply_text(result.text)

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

@app.route("/")
def index():
    return "TarjimonBot is running."

@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

@app.route("/setwebhook")
async def set_webhook():
    full_url = f"{BASE_URL}{WEBHOOK_PATH}"
    success = await application.bot.set_webhook(full_url)
    return f"Webhook set: {success}"

if __name__ == "__main__":
    application.run_polling()

    
