from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
from googletrans import Translator

TOKEN = "8148077100:AAGu5yAI0JgB2dYvWY9idjQAYVWATjvuBq8"
WEBHOOK_URL = "https://tarjimonbot-baij.onrender.com/webhook"

app = Flask(__name__)
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, None, workers=4)
translator = Translator()

def start(update, context):
    update.message.reply_text("Assalomu alaykum! Matn yuboring, men tarjima qilaman.")

def translate(update, context):
    text = update.message.text
    result = translator.translate(text, src='auto', dest='en')
    update.message.reply_text(f"Tarjima: {result.text}")

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, translate))

@app.route('/')
def index():
    return "Bot is alive!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

@app.route('/setwebhook')
def set_webhook():
    success = bot.set_webhook(WEBHOOK_URL)
    return f"Webhook set: {success}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
    
