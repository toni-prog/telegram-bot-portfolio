# handlers/game_guess_handler.py

import random
import time
from bot_instance import bot
from user_data import user_states, user_lang, user_game_data
from states import State
from utils import get_text
from keyboards import game_keyboard, projects_keyboard
from database import save_game_result, get_user_game_stats, log_action

def start_guess_game(user_id, lang):
    """Начинает новую игру"""
    secret = random.randint(1, 100)
    user_game_data[user_id] = {
        'secret': secret,
        'attempts': 0,
        'start_time': time.time()
    }
    bot.send_message(
        user_id,
        get_text('guess_game_start', user_id),
        reply_markup=game_keyboard(lang)
    )

def handle_guess_game(message):
    """Обработчик игры 'Угадай число'"""
    user_id = message.from_user.id
    text = message.text
    lang = user_lang.get(user_id, 'ru')

# Кнопка "Назад" обрабатывается в main_handler.py
    if text == get_text('back', user_id):
        # Эта часть не должна выполняться, так как "Назад" перехватывается в main_handler
        return

    # Проверяем, есть ли активная игра
    if user_id not in user_game_data:
        start_guess_game(user_id, lang)
        return

    try:
        guess = int(text)
    except ValueError:
        bot.send_message(
            user_id,
            get_text('guess_game_invalid', user_id)
        )
        return

    game_data = user_game_data[user_id]
    secret = game_data['secret']
    game_data['attempts'] += 1
    attempts = game_data['attempts']

    if guess == secret:
        # Победа!
        duration = int(time.time() - game_data['start_time'])
        
        # Сохраняем результат в БД
        save_game_result(
            user_id=user_id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            secret_number=secret,
            attempts=attempts,
            won=True,
            duration=duration
        )
        
        # Получаем статистику
        stats = get_user_game_stats(user_id)
        
        # Отправляем сообщение о победе
        win_message = get_text('guess_game_win', user_id).format(
            number=secret,
            attempts=attempts
        )
        
        # Добавляем статистику
        if stats and stats['total_games'] > 0:
            win_message += f"\n\n📊 Статистика:\n"
            win_message += f"Всего игр: {stats['total_games']}\n"
            win_message += f"Побед: {stats['wins']}\n"
            win_message += f"Среднее кол-во попыток: {stats['avg_attempts']:.1f}\n"
            if stats['best_attempts']:
                win_message += f"Лучший результат: {stats['best_attempts']} попыток"
        
        bot.send_message(user_id, win_message)
        
        # Логируем действие
        log_action(user_id, f'guess_game_win attempts={attempts}')
        
        # Удаляем данные игры
        del user_game_data[user_id]
        
        # ВОЗВРАТ В ПРОЕКТЫ через изменение состояния
        # Важно: мы не отправляем сообщение здесь, так как пользователь уже увидел результат
        # Но нужно вернуть состояние в PROJECTS для следующего действия
        user_states[user_id]['current'] = State.PROJECTS
        user_states[user_id]['previous'] = State.GREET
        
        # Отправляем сообщение о возврате в меню проектов
        bot.send_message(
            user_id,
            get_text('back_to_projects', user_id),
            reply_markup=projects_keyboard(lang)
        )
        
    elif guess < secret:
        bot.send_message(
            user_id,
            get_text('guess_game_hint_bigger', user_id)
        )
    else:
        bot.send_message(
            user_id,
            get_text('guess_game_hint_smaller', user_id)
        )