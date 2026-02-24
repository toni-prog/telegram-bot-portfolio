from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from utils import get_text
from keyboards import (
    lang_select_keyboard, main_keyboard, greet_keyboard, 
    language_keyboard, projects_keyboard, game_keyboard, weather_keyboard, parsing_keyboard,
    admin_keyboard, voice_keyboard, meme_keyboard
)
from handlers.lang_select_handler import handle_lang_select
from handlers.main_menu_handler import handle_main
from handlers.greet_menu_handler import handle_greet
from handlers.language_menu_handler import handle_language
from handlers.projects_handler import handle_projects
from handlers.game_guess_handler import handle_guess_game
from handlers.weather_handler import handle_weather
from handlers.parsing_handler import handle_parsing, get_currency_rates, get_random_quote, get_random_joke
from handlers.meme_handler import handle_meme, handle_meme_wait_photo, handle_meme_wait_text
from handlers.voice_handler import handle_voice, handle_voice_wait
from handlers.admin_handler import handle_admin, handle_admin_role
from decorators import admin_only

def go_back(user_id, current_state, lang):
    """Универсальная функция для возврата на предыдущий уровень"""
    prev_state = user_states[user_id].get('previous')
    
    # Для отладки
    print(f"go_back: user_id={user_id}, current_state={current_state}, prev_state={prev_state}")
    
    if prev_state is None:
        # Если предыдущего состояния нет, отправляем в главное меню
        user_states[user_id]['current'] = State.MAIN
        user_states[user_id]['previous'] = None
        bot.send_message(
            user_id,
            get_text('back_to_main', user_id),
            reply_markup=main_keyboard(lang)
        )
        return
    
    # Переходим в предыдущее состояние
    user_states[user_id]['current'] = prev_state
    
    # Устанавливаем new_previous в зависимости от того, куда возвращаемся
    if prev_state == State.MAIN:
        user_states[user_id]['previous'] = None
        bot.send_message(
            user_id,
            get_text('back_to_main', user_id),
            reply_markup=main_keyboard(lang)
        )
    elif prev_state == State.GREET:
        # Для GREET предыдущим должно быть MAIN
        user_states[user_id]['previous'] = State.MAIN
        bot.send_message(
            user_id,
            get_text('back_to_greet', user_id),
            reply_markup=greet_keyboard(lang)
        )
    elif prev_state == State.PROJECTS:
        # Для PROJECTS предыдущим должно быть GREET
        user_states[user_id]['previous'] = State.GREET
        bot.send_message(
            user_id,
            get_text('back_to_projects', user_id),
            reply_markup=projects_keyboard(lang)
        )

    elif prev_state == State.PARSING:
        user_states[user_id]['previous'] = State.PROJECTS
        bot.send_message(
            user_id,
            get_text('back_to_parsing', user_id),
            reply_markup=parsing_keyboard(lang)
        )

    elif prev_state == State.LANGUAGE:
        user_states[user_id]['previous'] = State.GREET
        bot.send_message(
            user_id,
            get_text('back', user_id),
            reply_markup=language_keyboard(lang)
        )

    elif prev_state in [State.PARSING_CURRENCY, State.PARSING_QUOTE, State.PARSING_JOKE]:
        # Возврат из действий парсинга в меню парсинга
        user_states[user_id]['current'] = State.PARSING
        user_states[user_id]['previous'] = State.PROJECTS
        bot.send_message(
            user_id,
            get_text('back_to_parsing', user_id),
            reply_markup=parsing_keyboard(lang)
        )

    elif prev_state == State.GUESS_GAME:
        user_states[user_id]['previous'] = State.PROJECTS
        bot.send_message(
            user_id,
            get_text('back', user_id),
            reply_markup=game_keyboard(lang)
        )
    elif prev_state == State.WEATHER:
        user_states[user_id]['previous'] = State.PROJECTS
        bot.send_message(
            user_id,
            get_text('back', user_id),
            reply_markup=weather_keyboard(lang)
        )

    elif prev_state == State.MEME:
        user_states[user_id]['previous'] = State.PROJECTS
        bot.send_message(
            user_id,
            get_text('back_to_projects', user_id),
            reply_markup=meme_keyboard(lang)
        )
    elif prev_state == State.VOICE:
        user_states[user_id]['previous'] = State.PROJECTS
        bot.send_message(
            user_id,
            get_text('back_to_projects', user_id),
            reply_markup=voice_keyboard(lang)
        )
    elif prev_state == State.ADMIN:
        user_states[user_id]['previous'] = State.MAIN
        bot.send_message(
            user_id,
            get_text('back_to_main', user_id),
            reply_markup=admin_keyboard(lang)
            )

    else:
        # На всякий случай
        user_states[user_id]['previous'] = None
        bot.send_message(
            user_id,
            get_text('back_to_main', user_id),
            reply_markup=main_keyboard(lang)
        )

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    text = message.text

    # Если пользователя нет в хранилище
    if user_id not in user_states:
        user_states[user_id] = {'current': State.LANG_SELECT, 'previous': None}
        bot.send_message(
            user_id,
            "Пожалуйста, выберите язык / Please choose a language:",
            reply_markup=lang_select_keyboard()
        )
        return

    current_state = user_states[user_id]['current']
    lang = user_lang.get(user_id, 'ru')

    # Универсальная обработка кнопки "Назад"
    if text == "Назад" or text == "Back" or text == get_text('back', user_id):
        if current_state == State.LANG_SELECT:
            # В выборе языка кнопка "Назад" не работает
            bot.send_message(
                user_id,
                "Пожалуйста, выберите язык / Please choose a language:",
                reply_markup=lang_select_keyboard()
            )
            return
        
        # Используем универсальную функцию возврата
        go_back(user_id, current_state, lang)
        return

    # Диспетчеризация по состояниям
    if current_state == State.LANG_SELECT:
        handle_lang_select(message)
    elif current_state == State.MAIN:
        handle_main(message)
    elif current_state == State.GREET:
        handle_greet(message)
    elif current_state == State.LANGUAGE:
        handle_language(message)
    elif current_state == State.PROJECTS:
        handle_projects(message)
    elif current_state == State.GUESS_GAME:
        handle_guess_game(message)
    elif current_state == State.WEATHER:
        handle_weather(message)
    elif current_state == State.PARSING:
        handle_parsing(message)
    elif current_state == State.PARSING_CURRENCY:
        get_currency_rates(message)
    elif current_state == State.PARSING_QUOTE:
        get_random_quote(message)
    elif current_state == State.PARSING_JOKE:
        get_random_joke(message)
    elif current_state == State.MEME:
        handle_meme(message)
    elif current_state == State.MEME_WAIT_PHOTO:
        handle_meme_wait_photo(message)
    elif current_state == State.MEME_WAIT_TEXT:
        handle_meme_wait_text(message)
    elif current_state == State.VOICE:
        handle_voice(message)
    elif current_state == State.VOICE_WAIT:
        handle_voice_wait(message)
    elif current_state == State.ADMIN:
        handle_admin(message)
    elif current_state == State.ADMIN_ROLE:
        handle_admin_role(message)
        
    else:
        # Неизвестное состояние - сброс
        user_states[user_id] = {'current': State.MAIN, 'previous': None}
        bot.send_message(
            user_id,
            get_text('error_return', user_id),
            reply_markup=main_keyboard(lang)
        )