import os
import requests
from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from utils import get_text
from keyboards import weather_keyboard, projects_keyboard
from database import save_weather_query, get_user_weather_history, log_action

ADMIN_ID = os.environ.get('ADMIN_ID', '123456789')
OPENWEATHER_API_KEY = os.environ.get('OPENWEATHER_API_KEY')

def handle_weather(message):
    """Обработчик для погоды"""
    user_id = message.from_user.id
    text = message.text
    lang = user_lang.get(user_id, 'ru')

    # Кнопка "Назад" обрабатывается в main_handler.py
    if text == get_text('back', user_id):
        return
    
    # Здесь мы только проверяем, не является ли текст командой "Назад"
    if text == get_text('back', user_id):
        # Эта часть не должна выполняться, так как "Назад" перехватывается в main_handler
        return

    # Получаем город из сообщения
    city = text.strip()
    
    try:
        # Запрос к API OpenWeatherMap
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric&lang={lang}"
        print(f"Запрос к API: {url}")
        
        response = requests.get(url, timeout=10)
        data = response.json()
        
        print(f"Ответ API: {data}")
        
        if data['cod'] == 200:
            # Успешный запрос
            temp = data['main']['temp']
            description = data['weather'][0]['description']
            
            # Сохраняем в БД
            save_weather_query(
                user_id=user_id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                city=city,
                temperature=temp,
                description=description
            )
            
            # Получаем историю запросов
            history = get_user_weather_history(user_id)
            
            # Формируем сообщение о текущей погоде
            result_message = get_text('weather_result', user_id).format(
                city=city,
                description=description,
                temp=str(temp)
            )
            
            # Добавляем историю запросов
            if history and len(history) > 0:
                result_message += "\n\n📜 Последние запросы:"
                for h in history[:3]:
                    result_message += f"\n• {h['city']}: {h['temperature']}°C, {h['description']}"
            
            bot.send_message(user_id, result_message)
            
            # Логируем действие
            log_action(user_id, f'weather_query city={city}')
            
            # Остаемся в режиме ввода города для нового запроса
            # Не меняем состояние, просто ждем следующий город
            bot.send_message(
                user_id,
                get_text('weather_enter_city', user_id),
                reply_markup=weather_keyboard(lang)
            )
            
        else:
            # Город не найден
            error_msg = data.get('message', 'Unknown error')
            bot.send_message(
                user_id,
                f"{get_text('weather_not_found', user_id)} ({error_msg})"
            )
            
    except requests.exceptions.Timeout:
        bot.send_message(
            user_id,
            "⏰ Превышено время ожидания. Попробуйте позже."
        )
    except requests.exceptions.ConnectionError:
        bot.send_message(
            user_id,
            "🔌 Ошибка подключения. Проверьте интернет."
        )
    except KeyError as e:
        print(f"Ошибка ключа в ответе API: {e}")
        bot.send_message(
            user_id,
            "❌ Ошибка формата данных от сервера погоды."
        )
    except Exception as e:
        print(f"Ошибка погоды: {e}")
        bot.send_message(
            user_id,
            get_text('weather_error', user_id)
        )