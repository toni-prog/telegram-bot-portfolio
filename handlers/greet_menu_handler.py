# handlers/greet_menu_handler.py

from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from utils import get_text
from keyboards import greet_keyboard, projects_keyboard, language_keyboard

def handle_greet(message):
    user_id = message.from_user.id
    text = message.text
    lang = user_lang.get(user_id, 'ru')

    # Кнопка "Назад" обрабатывается в main_handler.py
    if text == get_text('back', user_id):
        return

    if text == get_text('about_me', user_id):
        bot.send_message(
            user_id,
            get_text('about_me_text', user_id),
            parse_mode='Markdown'
        )
    elif text == get_text('skills', user_id):
        bot.send_message(
            user_id,
            get_text('skills_text', user_id),
            parse_mode='Markdown'
        )
    elif text == get_text('projects', user_id):
        # Переход в меню проектов
        user_states[user_id]['previous'] = State.GREET  # Запоминаем, откуда пришли
        user_states[user_id]['current'] = State.PROJECTS
        bot.send_message(
            user_id,
            get_text('projects_text', user_id),
            reply_markup=projects_keyboard(lang)
        )
    elif text == get_text('choose_lang', user_id):
        user_states[user_id]['previous'] = State.GREET  # Запоминаем, откуда пришли
        user_states[user_id]['current'] = State.LANGUAGE
        bot.send_message(
            user_id,
            get_text('choose_lang_prompt', user_id),
            reply_markup=language_keyboard(lang)
        )
    else:
        bot.send_message(
            user_id,
            get_text('unknown_command', user_id),
            reply_markup=greet_keyboard(lang)
        )