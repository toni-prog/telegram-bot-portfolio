# handlers/projects_handler.py

from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from utils import get_text
from keyboards import (projects_keyboard, game_keyboard, weather_keyboard, 
                       greet_keyboard, parsing_keyboard, meme_keyboard, voice_keyboard
)

def handle_projects(message):
    """Обработчик для раздела 'Мои проекты'"""
    user_id = message.from_user.id
    text = message.text
    lang = user_lang.get(user_id, 'ru')

    # Кнопка "Назад" обрабатывается в main_handler.py
    if text == get_text('back', user_id):
        return

    if text == get_text('guess_game', user_id):
        # Переход в игру "Угадай число"
        user_states[user_id]['previous'] = State.PROJECTS  # Запоминаем, что пришли из проектов
        user_states[user_id]['current'] = State.GUESS_GAME
        from handlers.game_guess_handler import start_guess_game
        start_guess_game(user_id, lang)
        
    elif text == get_text('weather', user_id):
        # Переход в погоду
        user_states[user_id]['previous'] = State.PROJECTS  # Запоминаем, что пришли из проектов
        user_states[user_id]['current'] = State.WEATHER
        bot.send_message(
            user_id,
            get_text('weather_enter_city', user_id),
            reply_markup=weather_keyboard(lang)
        )

    elif text == get_text('parsing', user_id):
        user_states[user_id]['previous'] = State.PROJECTS
        user_states[user_id]['current'] = State.PARSING
        bot.send_message(
            user_id,
            "🕷 Выберите тип данных для парсинга:",
            reply_markup=parsing_keyboard(lang)
        )

    elif text == get_text('meme', user_id):  # НОВОЕ
        user_states[user_id]['previous'] = State.PROJECTS
        user_states[user_id]['current'] = State.MEME
        bot.send_message(
            user_id,
            "🎭 Выберите действие:" if lang == 'ru' else "🎭 Choose action:",
            reply_markup=meme_keyboard(lang)
        )
        
    elif text == get_text('voice', user_id):  # НОВОЕ
        user_states[user_id]['previous'] = State.PROJECTS
        user_states[user_id]['current'] = State.VOICE
        bot.send_message(
            user_id,
            "🎤 Выберите действие:" if lang == 'ru' else "🎤 Choose action:",
            reply_markup=voice_keyboard(lang)
        )
        
    else:
        bot.send_message(
            user_id,
            get_text('unknown_command', user_id),
            reply_markup=projects_keyboard(lang)
        )