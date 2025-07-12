from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from deep_translator import GoogleTranslator

TOKEN = "8148077100:AAGu5yAI0JgB2dYvWY9idjQAYVWATjvuBq8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Matn yuboring va men uni tarjima qilaman.")

async def translate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    original = update.message.text
    translated = GoogleTranslator(source='auto', target='uz').translate(original)
    await update.message.reply_text(translated)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate))
    app.run_polling()
    
