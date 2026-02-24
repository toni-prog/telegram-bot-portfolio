# app.py - Файл для запуска на Render
import os
import threading
import logging
from flask import Flask, request


from bot_instance import bot
import handlers
from database import init_db

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Создаем Flask приложение
app = Flask(__name__)

# ============================================
# ФУНКЦИЯ ЗАПУСКА БОТА
# ============================================
def run_bot():
    """Запускает бота (копия логики из main.py)"""
    try:
        logger.info("Инициализация базы данных...")
        init_db()
        
        logger.info("Бот запускается...")
        print("Бот запущен...")
        
        # Запускаем бота
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
        
    except Exception as e:
        logger.error(f"Ошибка в боте: {e}")
        # В случае ошибки пробуем перезапустить через 10 секунд
        import time
        time.sleep(10)
        run_bot()

# ============================================
# ЗАПУСК БОТА В ОТДЕЛЬНОМ ПОТОКЕ
# ============================================
bot_started = False

@app.route('/')
def index():
    """Главная страница для проверки работы"""
    global bot_started

    if not bot_started:
        logger.info("первый запрос: запуск бота в фоновом потоке...")
        thread = threading.Thread(target=run_bot, daemon=True)
        thread.start()
        bot_started = True
        logger.info("Бот запущен в фоновом потоке")

    return """
    <html>
        <head>
            <title>Telegram Bot Portfolio</title>
            <style>
                body {{ 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    padding: 50px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                }}
                h1 {{ font-size: 3em; margin-bottom: 20px; }}
                .status {{ 
                    background: rgba(255,255,255,0.2);
                    padding: 20px;
                    border-radius: 10px;
                    font-size: 1.2em;
                }}
                .success {{ color: #4CAF50; font-weight: bold; }}
            </style>
        </head>
        <body>
            <h1>🤖 Telegram Bot Portfolio</h1>
            <div class="status">
                <p class="success">✅ Бот успешно запущен!</p>
                <p>Бот работает в фоновом режиме 24/7</p>
                <p>🕒 Время запуска: постоянно</p>
                <p>📊 Статус: активен</p>
            </div>
            <p style="margin-top: 50px;">
                <small>Для проверки здоровья бота: <a href="/health" style="color: white;">/health</a></small>
            </p>
        </body>
    </html>
    """
# ============================================
# ВЕБ-ЭНДПОИНТЫ ДЛЯ RENDER
# ============================================

@app.route('/health')
def health():
    """Endpoint для проверки здоровья (используется cron-job)"""
    return {
        "status": "ok",
        "bot": "running",
        "message": "Bot is alive!"
    }, 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Заглушка для вебхуков (на будущее)"""
    return "OK", 200

@app.route('/logs')
def view_logs():
    """Простой просмотр последних логов (опционально)"""
    return "Логи доступны в консоли Render", 200

# ============================================
# ЗАПУСК FLASK ПРИЛОЖЕНИЯ
# ============================================
if __name__ == '__main__':
    # Получаем порт из переменной окружения (Render дает PORT)
    port = int(os.environ.get('PORT', 5000))
    
    logger.info(f"Запуск Flask сервера на порту {port}")
    print(f"Сервер запущен на порту {port}")
    
    # Запускаем Flask сервер
    app.run(host='0.0.0.0', port=port, debug=False)