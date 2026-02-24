import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
bot.parse_mode = "Markdown"