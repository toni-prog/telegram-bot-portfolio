import requests
import random
import xml.etree.ElementTree as ET
import os 
from datetime import datetime
from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from utils import get_text
from keyboards import parsing_keyboard, parsing_action_keyboard, projects_keyboard
from database import save_currency_rates, save_quote_query, save_joke_query, log_action

ADMIN_ID = os.environ.get('ADMIN_ID', '123456789')

def handle_parsing(message):
    """Обработчик для раздела парсинга"""
    user_id = message.from_user.id
    text = message.text
    lang = user_lang.get(user_id, 'ru')

    if text == get_text('back', user_id):
        # Возврат в меню проектов
        user_states[user_id]['current'] = State.PROJECTS
        user_states[user_id]['previous'] = State.GREET
        bot.send_message(
            user_id,
            get_text('back_to_projects', user_id),
            reply_markup=projects_keyboard(lang)
        )
        return

    if text == get_text('currency', user_id):
        # Переход в курсы валют
        user_states[user_id]['previous'] = State.PARSING
        user_states[user_id]['current'] = State.PARSING_CURRENCY
        get_currency_rates(message)
        
    elif text == get_text('quote', user_id):
        # Переход в цитаты
        user_states[user_id]['previous'] = State.PARSING
        user_states[user_id]['current'] = State.PARSING_QUOTE
        get_random_quote(message)
        
    elif text == get_text('joke', user_id):
        # Переход в анекдоты
        user_states[user_id]['previous'] = State.PARSING
        user_states[user_id]['current'] = State.PARSING_JOKE
        get_random_joke(message)
        
    else:
        bot.send_message(
            user_id,
            get_text('unknown_command', user_id),
            reply_markup=parsing_keyboard(lang)
        )

def get_currency_rates(message):
    """Получает курсы валют с сайта ЦБ РФ"""
    user_id = message.from_user.id
    lang = user_lang.get(user_id, 'ru')
    
    try:
        # Отправляем уведомление о загрузке
        bot.send_chat_action(user_id, 'typing')
        
        # Получаем курсы с сайта ЦБ РФ (XML)
        url = "http://www.cbr.ru/scripts/XML_daily.asp"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            # Парсим XML
            root = ET.fromstring(response.content)
            
            # Получаем дату
            date_str = root.get('Date', datetime.now().strftime('%d.%m.%Y'))
            
            # Словарь для хранения курсов
            rates = {}
            
            # Ищем нужные валюты
            for valute in root.findall('Valute'):
                char_code = valute.find('CharCode').text
                value = valute.find('Value').text.replace(',', '.')
                nominal = int(valute.find('Nominal').text)
                
                # Переводим в рубли за 1 единицу
                rate = float(value) / nominal
                
                if char_code == 'USD':
                    rates['usd'] = round(rate, 2)
                elif char_code == 'EUR':
                    rates['eur'] = round(rate, 2)
                elif char_code == 'CNY':
                    rates['cny'] = round(rate, 2)
                elif char_code == 'GBP':
                    rates['gbp'] = round(rate, 2)
                elif char_code == 'JPY':
                    rates['jpy'] = round(rate, 2)
            
            # Сохраняем в БД
            save_currency_rates(
                usd=rates.get('usd', 0),
                eur=rates.get('eur', 0),
                cny=rates.get('cny', 0),
                gbp=rates.get('gbp', 0),
                jpy=rates.get('jpy', 0),
                date=date_str
            )
            
            # Формируем сообщение
            message_text = get_text('currency_rates', user_id).format(date=date_str)
            message_text += f"\n\n{get_text('currency_usd', user_id).format(rate=rates.get('usd', 'N/A'))}"
            message_text += f"\n{get_text('currency_eur', user_id).format(rate=rates.get('eur', 'N/A'))}"
            message_text += f"\n{get_text('currency_cny', user_id).format(rate=rates.get('cny', 'N/A'))}"
            message_text += f"\n{get_text('currency_gbp', user_id).format(rate=rates.get('gbp', 'N/A'))}"
            message_text += f"\n{get_text('currency_jpy', user_id).format(rate=rates.get('jpy', 'N/A'))}"
            
            bot.send_message(user_id, message_text)
            
            # Логируем действие
            log_action(user_id, 'currency_rates_request')
            
        else:
            bot.send_message(
                user_id,
                get_text('currency_error', user_id)
            )
            
    except requests.exceptions.Timeout:
        bot.send_message(
            user_id,
            "⏰ Превышено время ожидания. Попробуйте позже."
        )
    except ET.ParseError:
        bot.send_message(
            user_id,
            "❌ Ошибка парсинга данных. Сервер вернул некорректный ответ."
        )
    except Exception as e:
        print(f"Ошибка получения курсов валют: {e}")
        bot.send_message(
            user_id,
            get_text('currency_error', user_id)
        )

    prompt_text = get_text('currency_prompt', user_id)

    bot.send_message(
        user_id,
        prompt_text,
        reply_markup=parsing_action_keyboard(lang)  # ← ВАЖНО: клавиатура с кнопкой "Назад"
    )

def get_random_quote(message):
    """Получает случайную цитату с сайта forismatic.com"""
    user_id = message.from_user.id
    lang = user_lang.get(user_id, 'ru')
    
    try:
        # Отправляем уведомление о загрузке
        bot.send_chat_action(user_id, 'typing')
        
        # API forismatic (поддерживает русский и английский)
        api_lang = 'ru' if lang == 'ru' else 'en'
        url = f"https://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang={api_lang}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            quote_text = data.get('quoteText', '').strip()
            quote_author = data.get('quoteAuthor', 'Unknown').strip()
            
            if not quote_author:
                quote_author = "Unknown"
            
            # Сохраняем в БД
            save_quote_query(
                user_id=user_id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                quote_text=quote_text,
                quote_author=quote_author
            )
            
            # Формируем сообщение
            message_text = f"{get_text('quote_title', user_id)}\n\n"
            message_text += f"“{quote_text}”\n\n"
            message_text += get_text('quote_author', user_id).format(author=quote_author)
            
            bot.send_message(user_id, message_text)
            
            # Логируем действие
            log_action(user_id, 'quote_request')
            
        else:
            # Если API не работает, используем локальные цитаты
            send_local_quote(user_id, lang)
            
    except Exception as e:
        print(f"Ошибка получения цитаты: {e}")
        # Запасной вариант - локальные цитаты
        send_local_quote(user_id, lang)

    prompt_text = get_text('quote_prompt', user_id)
    
    bot.send_message(
        user_id,
        prompt_text,
        reply_markup=parsing_action_keyboard(lang)  # ← ВАЖНО: клавиатура с кнопкой "Назад"
    )
    
def send_local_quote(user_id, lang):
    """Отправляет цитату из локального хранилища (запасной вариант)"""
    
    quotes_ru = [
        {"text": "Единственный способ делать великую работу — любить то, что ты делаешь.", "author": "Стив Джобс"},
        {"text": "Жизнь — это то, что с тобой происходит, пока ты строишь планы.", "author": "Джон Леннон"},
        {"text": "Будь тем изменением, которое хочешь увидеть в мире.", "author": "Махатма Ганди"},
        {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма.", "author": "Уинстон Черчилль"},
        {"text": "Самая большая слава не в том, чтобы никогда не падать, а в том, чтобы вставать каждый раз, когда ты падаешь.", "author": "Конфуций"},
        {"text": "Если вы хотите иметь то, что никогда не имели, вам придется делать то, что никогда не делали.", "author": "Коко Шанель"},
        {"text": "Лучший способ предсказать будущее — создать его.", "author": "Питер Друкер"},
        {"text": "Путь в тысячу миль начинается с первого шага.", "author": "Лао-цзы"},
        {"text": "Не ошибается лишь тот, кто ничего не делает. Не бойтесь ошибаться — бойтесь повторять ошибки.", "author": "Теодор Рузвельт"},
        {"text": "Все, что нас не убивает, делает нас сильнее.", "author": "Фридрих Ницше"},
    ]
    
    quotes_en = [
        {"text": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
        {"text": "Life is what happens to you while you're busy making other plans.", "author": "John Lennon"},
        {"text": "Be the change that you wish to see in the world.", "author": "Mahatma Gandhi"},
        {"text": "Success is the ability to go from failure to failure without losing your enthusiasm.", "author": "Winston Churchill"},
        {"text": "The greatest glory is not in never falling, but in rising every time we fall.", "author": "Confucius"},
        {"text": "If you want to have something you never had, you have to do something you never did.", "author": "Coco Chanel"},
        {"text": "The best way to predict the future is to create it.", "author": "Peter Drucker"},
        {"text": "A journey of a thousand miles begins with a single step.", "author": "Lao Tzu"},
        {"text": "The only man who never makes a mistake is the man who never does anything.", "author": "Theodore Roosevelt"},
        {"text": "What does not kill us makes us stronger.", "author": "Friedrich Nietzsche"},
    ]
    
    quotes = quotes_ru if lang == 'ru' else quotes_en
    quote = random.choice(quotes)
    
    message_text = f"{get_text('quote_title', user_id)}\n\n"
    message_text += f"“{quote['text']}”\n\n"
    message_text += get_text('quote_author', user_id).format(author=quote['author'])
    
    bot.send_message(user_id, message_text)

def get_random_joke(message):
    """Получает случайный анекдот"""
    user_id = message.from_user.id
    lang = user_lang.get(user_id, 'ru')
    
    try:
        # Отправляем уведомление о загрузке
        bot.send_chat_action(user_id, 'typing')
        
        if lang == 'ru':
            # Используем API анекдотов (например, rzhunemogu.ru)
            url = "http://rzhunemogu.ru/RandJSON.aspx?CType=1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                # Ответ приходит в формате JSONP, нужно очистить
                content = response.text
                # Убираем лишние символы
                if content.startswith('{"content":"') and content.endswith('"}'):
                    joke_text = content[12:-2]
                    # Заменяем экранированные кавычки
                    joke_text = joke_text.replace('\\"', '"')
                    
                    # Сохраняем в БД
                    save_joke_query(
                        user_id=user_id,
                        username=message.from_user.username,
                        first_name=message.from_user.first_name,
                        joke_text=joke_text
                    )
                    
                    message_text = f"{get_text('joke_title', user_id)}\n\n{joke_text}"
                    bot.send_message(user_id, message_text)
                    
                    # Логируем действие
                    log_action(user_id, 'joke_request')
                else:
                    send_local_joke(user_id, lang)
            else:
                send_local_joke(user_id, lang)
        else:
            # Для английского используем другой API
            url = "https://official-joke-api.appspot.com/random_joke"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                setup = data.get('setup', '')
                punchline = data.get('punchline', '')
                joke_text = f"{setup}\n\n{punchline}"
                
                # Сохраняем в БД
                save_joke_query(
                    user_id=user_id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    joke_text=joke_text
                )
                
                message_text = f"{get_text('joke_title', user_id)}\n\n{joke_text}"
                bot.send_message(user_id, message_text)
                
                # Логируем действие
                log_action(user_id, 'joke_request')
            else:
                send_local_joke(user_id, lang)
            
    except Exception as e:
        print(f"Ошибка получения анекдота: {e}")
        send_local_joke(user_id, lang)

    prompt_text = get_text('joke_prompt', user_id)
    
    bot.send_message(
        user_id,
        prompt_text,
        reply_markup=parsing_action_keyboard(lang)  # ← ВАЖНО: клавиатура с кнопкой "Назад"
    )

def send_local_joke(user_id, lang):
    """Отправляет анекдот из локального хранилища (запасной вариант)"""
    
    jokes_ru = [
        "— Доктор, я буду жить?\n— А смысл?",
        "Встречаются два программиста:\n— Ты знаешь, вчера полчаса объяснял маме, что я не занимаюсь 'чисткой винды' каждый день...\n— И что?\n— Теперь она просит почистить посудомойку, потому что она 'тоже на Windows'.",
        "Приходит мужик к врачу, а у него вместо глаз — клавиатура. Врач спрашивает:\n— Давно у вас это?\nМужик отвечает:\n— Shift+Ctrl+Esc, Shift+Ctrl+Esc...",
        "— Почему программисты путают Хэллоуин и Рождество?\n— Потому что 31 Oct = 25 Dec.",
        "Админ звонит в службу поддержки:\n— У меня не работает интернет.\n— Вы пробовали перезагрузить роутер?\n— Я админ, я перезагружаю только по пятницам, и то если квартальный план выполнен.",
        "— Дорогая, я решил стать вегетарианцем.\n— Почему?\n— Потому что мясо дорогое.\n— А овощи дешевле?\n— Нет, но их хотя бы не жалко, когда я их сжигаю на гриле.",
        "— Ты веришь в любовь с первого взгляда?\n— А ты веришь, что я переустановлю Windows, просто посмотрев на твой компьютер?",
        "Идет заяц по лесу, видит — волк лежит, плачет.\n— Ты чего плачешь?\n— Да понимаешь, съел я трех поросят, а они оказались программистами. Теперь у меня в желуске сплошной windows.",
    ]
    
    jokes_en = [
        "Why do programmers prefer dark mode? Because light attracts bugs.",
        "A SQL query goes into a bar, walks up to two tables and asks: 'Can I join you?'",
        "How many programmers does it take to change a light bulb? None, that's a hardware problem.",
        "I told my computer I needed a break, and now it won't stop sending me vacation ads.",
        "Why was the JavaScript developer sad? Because he didn't know how to 'null' his feelings.",
        "A programmer's wife tells him: 'Go to the store and buy a loaf of bread. If they have eggs, buy a dozen.' He comes back with 12 loaves of bread.",
        "There are only 10 types of people in the world: those who understand binary and those who don't.",
        "Why do Java developers wear glasses? Because they can't C#.",
    ]
    
    jokes = jokes_ru if lang == 'ru' else jokes_en
    joke_text = random.choice(jokes)
    
    message_text = f"{get_text('joke_title', user_id)}\n\n{joke_text}"
    bot.send_message(user_id, message_text)