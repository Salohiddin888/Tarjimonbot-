from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, filters, ApplicationBuilder
from deep_translator import GoogleTranslator
import os

TOKEN = "8148077100:AAGu5yAI0JgB2dYvWY9idjQAYVWATjvuBq8"
bot = Bot(token=TOKEN)
app = Flask(__name__)

async def start(update: Update, context):
    await update.message.reply_text("Salom! Matn yuboring va men uni tarjima qilaman.")

async def translate(update: Update, context):
    original = update.message.text
    translated = GoogleTranslator(source='auto', target='uz').translate(original)
    await update.message.reply_text(translated)

application = ApplicationBuilder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))

if __name__ == '__main__':
    application.run_polling()
