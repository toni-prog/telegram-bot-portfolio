# handlers/language_menu_handler.py

from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from utils import get_text
from keyboards import greet_keyboard, language_keyboard

def handle_language(message):
    user_id = message.from_user.id
    text = message.text
    lang = user_lang.get(user_id, 'ru')

    # Кнопка "Назад" обрабатывается в main_handler.py
    if text == get_text('back', user_id):
        return

    if text == get_text('lang_ru', user_id):
        user_lang[user_id] = 'ru'
        bot.send_message(
            user_id,
            get_text('language_selected_ru', user_id),
            reply_markup=greet_keyboard('ru')
        )
        # Возвращаемся в GREET
        user_states[user_id]['current'] = State.GREET
        user_states[user_id]['previous'] = State.MAIN
        
    elif text == get_text('lang_en', user_id):
        user_lang[user_id] = 'en'
        bot.send_message(
            user_id,
            get_text('language_selected_en', user_id),
            reply_markup=greet_keyboard('en')
        )
        # Возвращаемся в GREET
        user_states[user_id]['current'] = State.GREET
        user_states[user_id]['previous'] = State.MAIN
        
    else:
        bot.send_message(
            user_id,
            get_text('unknown_command', user_id),
            reply_markup=language_keyboard(lang)
        )