import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# Configurações usando Variáveis de Ambiente (que você vai colocar no Render)
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# Configuração do Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Configuração de logs
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Olá! Sou o seu bot. Como posso te ajudar hoje?")

async def responder_gemini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    response = model.generate_content(user_text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response.text)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), responder_gemini)
    
    application.add_handler(start_handler)
    application.add_handler(message_handler)
    
    application.run_polling()
  
