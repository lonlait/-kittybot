# app.py - Flask приложение для PythonAnywhere
import os
import logging
from flask import Flask, request
from telebot import TeleBot, types
import requests
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# Получаем токен
secret_token = os.getenv('TOKEN')
if not secret_token:
    raise RuntimeError("TELEGRAM TOKEN not set in .env!")

# Инициализируем бота
bot = TeleBot(token=secret_token)

# URL для получения изображений котиков
CAT_API_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_API_URL = 'https://api.thedogapi.com/v1/images/search'

# Flask приложение
app = Flask(__name__)


def get_new_image():
    """Получает случайное изображение котика"""
    try:
        response = requests.get(CAT_API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data and len(data) > 0:
            return data[0].get('url')
        else:
            raise Exception("Пустой ответ от API")
    except Exception as error:
        logger.warning(f"Ошибка при получении изображения котика: {error}")
        # Пробуем резервный API
        try:
            response = requests.get(DOG_API_URL, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data and len(data) > 0:
                return data[0].get('url')
        except Exception as backup_error:
            logger.error(f"Ошибка при получении резервного изображения: {backup_error}")
            # Возвращаем заглушку, если оба API не сработали
            return "https://via.placeholder.com/600x400?text=Котик+убежал+😿"


@bot.message_handler(commands=['start'])
def wake_up(message):
    """Обработчик команды /start"""
    chat = message.chat
    name = message.chat.first_name
    
    # Создаем клавиатуру с кнопками
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    button_newcat = types.KeyboardButton('🐱 Новый котик')
    button_help = types.KeyboardButton('❓ Помощь')
    keyboard.add(button_newcat, button_help)

    welcome_text = f"Привет, {name}! 😊\n\nЯ CatSuperpositionBot - бот, который присылает милых котиков! 🐈\n\nИспользуй кнопку '🐱 Новый котик' или команду /newcat чтобы получить изображение котика."

    bot.send_message(
        chat_id=chat.id,
        text=welcome_text,
        reply_markup=keyboard,
    )

    # Отправляем первое изображение котика
    cat_image = get_new_image()
    if cat_image:
        bot.send_photo(chat.id, cat_image, caption="Вот твой первый котик! 🐱")
    else:
        bot.send_message(chat.id, "Извините, не удалось загрузить изображение котика. Попробуйте позже.")


@bot.message_handler(commands=['newcat'])
def new_cat(message):
    """Обработчик команды /newcat"""
    chat = message.chat
    
    # Отправляем сообщение о загрузке
    loading_msg = bot.send_message(chat.id, "Ищу котика для тебя... 🐱")
    
    cat_image = get_new_image()
    if cat_image:
        bot.delete_message(chat.id, loading_msg.message_id)
        bot.send_photo(chat.id, cat_image, caption="Вот твой котик! 🐱")
    else:
        bot.edit_message_text(
            "Извините, не удалось найти котика. Попробуйте позже! 😿",
            chat.id,
            loading_msg.message_id
        )


@bot.message_handler(commands=['help'])
def help_command(message):
    """Обработчик команды /help"""
    help_text = """
🐱 CatSuperpositionBot - бот с котиками!

Доступные команды:
/start - Начать работу с ботом
/newcat - Получить нового котика
/help - Показать это сообщение

Просто нажми на кнопку "🐱 Новый котик" или отправь команду /newcat!
    """
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    """Обработчик текстовых сообщений"""
    text = message.text.lower()
    
    if text in ['🐱 новый котик', 'новый котик', 'котик', 'кот', 'cat']:
        new_cat(message)
    elif text in ['❓ помощь', 'помощь', 'help']:
        help_command(message)
    else:
        bot.send_message(
            message.chat.id, 
            "Отправь /newcat или нажми кнопку '🐱 Новый котик' чтобы получить котика! 🐱"
        )


@app.route('/')
def home():
    """Главная страница"""
    return """
    <h1>🐱 CatSuperpositionBot</h1>
    <p>Telegram бот для отправки случайных изображений котиков</p>
    <p>Найдите бота в Telegram: <a href="https://t.me/CatSuperpositionBot">@CatSuperpositionBot</a></p>
    <p>Статус: ✅ Работает</p>
    """


@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook для Telegram Bot API"""
    if request.method == 'POST':
        bot.process_new_updates([types.Update.de_json(request.stream.read().decode("utf-8"))])
        return 'ok', 200


@app.route('/set_webhook')
def set_webhook():
    """Установка webhook"""
    try:
        # Получаем URL вашего сайта на PythonAnywhere
        webhook_url = f"https://{os.getenv('PYTHONANYWHERE_SITE', 'yourusername.pythonanywhere.com')}/webhook"
        bot.set_webhook(url=webhook_url)
        return f"Webhook установлен: {webhook_url}"
    except Exception as e:
        return f"Ошибка установки webhook: {e}"


@app.route('/remove_webhook')
def remove_webhook():
    """Удаление webhook"""
    try:
        bot.remove_webhook()
        return "Webhook удален"
    except Exception as e:
        return f"Ошибка удаления webhook: {e}"


if __name__ == '__main__':
    logger.info("Запуск CatSuperpositionBot на Flask...")
    # Для локальной разработки используем polling
    bot.polling(none_stop=True, interval=0) 
