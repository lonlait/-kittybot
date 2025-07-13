#!/usr/bin/env python3
# run_bot.py - Скрипт для запуска бота через cron на PythonAnywhere

import os
import sys
import logging
from telebot import TeleBot, types
import requests
from dotenv import load_dotenv

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/home/yourusername/kittybot/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Загружаем переменные окружения
load_dotenv()

# Получаем токен
secret_token = os.getenv('TOKEN', '8080191792:AAGsMYDNl4qkCA6DrV--kxap-DKYFS4Ndic')
bot = TeleBot(token=secret_token)

# URL для получения изображений котиков
CAT_API_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_API_URL = 'https://api.thedogapi.com/v1/images/search'


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
            return None


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


def main():
    """Основная функция запуска бота"""
    logger.info("Запуск CatSuperpositionBot через cron...")
    try:
        logger.info("Бот успешно запущен!")
        # Запускаем бота на короткое время для обработки сообщений
        bot.polling(none_stop=False, timeout=60, interval=1)
        logger.info("Бот завершил работу")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")


if __name__ == '__main__':
    main() 