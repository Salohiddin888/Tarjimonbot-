from flask import Flask, request
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
from googletrans import Translator

TOKEN = "8148077100:AAGu5yAI0JgB2dYvWY9idjQAYVWATjvuBq8"

app = Flask(__name__)
translator = Translator()
bot_app = ApplicationBuilder().token(TOKEN).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Tarjimon botga xush kelibsiz.")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    translated = translator.translate(text, dest='en')
    await update.message.reply_text(translated.text)


bot_app.add_handler(CommandHandler("start", start))
bot_app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), translate))


@app.route("/setwebhook")
def set_webhook(https://tarjimonbot-baij.onrender.com):
    url = "https://tarjimonbot-baij.onrender.com/webhook"
    bot_app.bot.set_webhook(url)
    return "Webhook set"

@app.route("/webhook", methods=["POST"])
async def webhook():
    await bot_app.update_queue.put(Update.de_json(request.get_json(force=True), bot_app.bot))
    return "ok"


if __name__ == "__main__":
    bot_app.run_polling()
    
