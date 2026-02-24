from bot_instance import bot
import handlers
from database import init_db



if __name__ == "__main__":
  init_db()
  print("Бот запущен...")
  bot.infinity_polling()
else:
  print("Произошла ошибка!")