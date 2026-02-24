
from database import get_user_role
from decorators import admin_only
from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from utils import get_text
from keyboards import greet_keyboard, main_keyboard, admin_keyboard

@bot.message_handler(commands=['admin'])
@admin_only
def admin_command(message):
    """Команда для входа в админ-панель"""
    user_id = message.from_user.id
    lang = user_lang.get(user_id, 'ru')
    
    user_states[user_id]['previous'] = State.MAIN
    user_states[user_id]['current'] = State.ADMIN
    
    bot.send_message(
        user_id,
        "👑 Добро пожаловать в админ-панель!" if lang == 'ru' else "👑 Welcome to admin panel!",
        reply_markup=admin_keyboard(lang)
    )

def handle_main(message):
    user_id = message.from_user.id
    text = message.text
    lang = user_lang.get(user_id, 'ru')

    # Кнопка "Назад" обрабатывается в main_handler.py
    if text == get_text('back', user_id):
        return

    if text == get_text('greet_button', user_id):
        user_states[user_id]['previous'] = State.MAIN  # Запоминаем, откуда пришли
        user_states[user_id]['current'] = State.GREET
        bot.send_message(
            user_id,
            get_text('choose_question', user_id),
            reply_markup=greet_keyboard(lang)
        )
    else:
        bot.send_message(
            user_id,
            get_text('unknown_command', user_id),
            reply_markup=main_keyboard(lang)
        )