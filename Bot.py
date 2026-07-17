import os
import telebot
import google.generativeai as genai
from flask import Flask, request

# Configuração
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
PORT = int(os.environ.get('PORT', 5000))

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name='gemini-pro',
    system_instruction="Você é um colaborador inteligente, leve, amigo e um excelente professor. Você tem memória das conversas anteriores."
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)
chat_histories = {}

@app.route('/')
def index():
    return "Bot está rodando!"

@app.route('/' + TELEGRAM_TOKEN, methods=['POST'])
def getMessage():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@bot.message_handler(func=lambda message: True)
def responder_tudo(message):
    chat_id = message.chat.id
    if chat_id not in chat_histories:
        chat_histories[chat_id] = model.start_chat(history=[])
    try:
        response = chat_histories[chat_id].send_message(message.text)
        bot.reply_to(message, response.text)
    except:
        bot.reply_to(message, "Estou processando muita informação, pode repetir?")

if __name__ == '__main__':
    # Configurar o webhook ao iniciar
    bot.remove_webhook()
    bot.set_webhook(url=f"https://mah-bot.onrender.com/{TELEGRAM_TOKEN}")
    app.run(host="0.0.0.0", port=PORT)
    
