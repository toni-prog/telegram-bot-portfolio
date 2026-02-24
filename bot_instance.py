import os
import telebot

# Берем токен из переменных окружения
TOKEN = os.environ.get('TELEGRAM_TOKEN')

if not TOKEN:
    raise ValueError("❌ Токен не найден! Добавьте TELEGRAM_TOKEN в переменные окружения на Render")

bot = telebot.TeleBot(TOKEN)