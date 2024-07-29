import telebot
from telebot import TeleBot, types
from telebot.util import extract_arguments
import time

# Замените токен на свой
bot = TeleBot("7492548163:AAFe-oHply7uEDooOYKlztGllR7iI_ankTg")
admins = [] # список администраторов

# Счетчики ссылок для пользователей
link_counts = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Добавить в группу", url=f"https://t.me/Links_Remove_bot?startgroup=true")
    markup.add(button)
    bot.reply_to(message, "Привет! Я бот, который удаляет ссылки из группы. Чтобы начать, добавьте меня в группу!", reply_markup=markup)

@bot.message_handler(commands=['add_me'])
def add_me(message):
    chat_id = message.chat.id
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        bot.send_message(chat_id, "Я добавлен в эту группу! Теперь я буду удалять ссылки.")
        # Получить список администраторов
        get_admins(chat_id)
    else:
        bot.send_message(chat_id, "Я могу работать только в группах. Пожалуйста, добавьте меня в группу.")

def get_admins(chat_id):
    """Получает список администраторов группы."""
    global admins
    admins = []
    for member in bot.get_chat_administrators(chat_id):
        admins.append(member.user.id)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    if message.from_user.username:
        user_name = f"@{message.from_user.username}"
    else:
        user_name = f"[{user_name}](tg://user?id={user_id})"

    # Проверка, является ли сообщение ссылкой
    if 'http://' in text or 'https://' in text or '.me/' in text or '.com' in text or '.ru' in text or 'www.' in text:
        # Проверка на администратора
        if user_id not in admins:
            try:
                bot.delete_message(chat_id, message.message_id)

                # Отправка сообщения без использования reply_to
                bot.send_message(chat_id, f"{user_name}, реклама запрещена!", parse_mode="Markdown")
            except telebot.apihelper.ApiTelegramException as e:
                if e.error_code == 400 and "message to be replied not found" in e.description:
                    # Ignore the error, the message was likely deleted
                    pass
                else:
                    # Handle other errors as needed
                    print(f"Error: {e.description}")

# Запуск бота
bot.polling()