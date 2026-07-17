import os
import telebot
import google.generativeai as genai

# Configuração
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)

# Configurando o "Cérebro" com personalidade
model = genai.GenerativeModel(
    model_name='gemini-pro',
    system_instruction="Você é um colaborador inteligente, leve, amigo e um excelente professor. Você sempre auxilia com paciência, clareza e um tom acolhedor. Você tem memória das conversas anteriores."
)

# Dicionário para guardar o histórico de cada usuário (Memória)
chat_histories = {}

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Estou aqui, pronto para aprender e conversar com você. Como posso te ajudar?")

@bot.message_handler(func=lambda message: True)
def responder_tudo(message):
    chat_id = message.chat.id
    user_text = message.text
    
    # Se o usuário não tem histórico, criamos uma nova sessão de chat
    if chat_id not in chat_histories:
        chat_histories[chat_id] = model.start_chat(history=[])
    
    try:
        # Envia a mensagem mantendo o histórico (memória)
        response = chat_histories[chat_id].send_message(user_text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Ops, parece que precisei de um tempo para processar. Pode repetir?")

if __name__ == '__main__':
    bot.polling()
    
