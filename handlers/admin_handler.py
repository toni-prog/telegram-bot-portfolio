# handlers/admin_handler.py

from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from utils import get_text
from keyboards import admin_keyboard, admin_action_keyboard, main_keyboard
from database import get_all_users, get_user_stats, set_user_role, get_user_role
from decorators import admin_only, moderator_plus

# ID главного админа (ваш Telegram ID)
MAIN_ADMIN_ID = 679790991  # ЗАМЕНИТЕ НА СВОЙ ID

def is_main_admin(user_id):
    """Проверка, является ли пользователь главным админом"""
    return user_id == MAIN_ADMIN_ID

@admin_only
def handle_admin(message):
    """Обработчик админ-панели (только для админов)"""
    user_id = message.from_user.id
    text = message.text
    lang = user_lang.get(user_id, 'ru')

    if text == get_text('back', user_id):
        # Возврат в главное меню
        user_states[user_id]['current'] = State.MAIN
        user_states[user_id]['previous'] = None
        bot.send_message(
            user_id,
            get_text('back_to_main', user_id),
            reply_markup=main_keyboard(lang)
        )
        return

    if text == get_text('admin_users', user_id):
        # Просмотр пользователей
        show_users_list(user_id, lang)
        
    elif text == get_text('admin_stats', user_id):
        # Просмотр статистики
        show_stats(user_id, lang)
        
    elif text == get_text('admin_set_role', user_id) and is_main_admin(user_id):
        # Изменение роли (только для главного админа)
        user_states[user_id]['previous'] = State.ADMIN
        user_states[user_id]['current'] = State.ADMIN_ROLE
        bot.send_message(
            user_id,
            "👤 Введите ID пользователя и новую роль через пробел.\nПример: `123456789 moderator`" if lang == 'ru' else "👤 Enter user ID and new role separated by space.\nExample: `123456789 moderator`",
            parse_mode='Markdown',
            reply_markup=admin_action_keyboard(lang)
        )
        
    else:
        bot.send_message(
            user_id,
            get_text('unknown_command', user_id),
            reply_markup=admin_keyboard(lang)
        )

def show_users_list(user_id, lang):
    """Показывает список пользователей"""
    users = get_all_users(limit=20)
    
    if not users:
        bot.send_message(
            user_id,
            "📭 Нет пользователей." if lang == 'ru' else "📭 No users."
        )
        return
    
    message = "👥 **Последние пользователи:**\n\n" if lang == 'ru' else "👥 **Recent users:**\n\n"
    
    for user in users:
        role_emoji = {
            'admin': '👑',
            'moderator': '🛡️',
            'user': '👤'
        }.get(user['role'], '👤')
        
        message += f"{role_emoji} **{user['first_name']}** (@{user['username'] or 'no_username'})\n"
        message += f"   ID: `{user['user_id']}`\n"
        message += f"   Роль: {user['role']}\n" if lang == 'ru' else f"   Role: {user['role']}\n"
        message += f"   Последний визит: {user['last_active'][:10]}\n\n" if lang == 'ru' else f"   Last active: {user['last_active'][:10]}\n\n"
    
    bot.send_message(user_id, message, parse_mode='Markdown')

def show_stats(user_id, lang):
    """Показывает статистику бота"""
    stats = get_user_stats()
    
    message = "📊 **Статистика бота:**\n\n" if lang == 'ru' else "📊 **Bot Statistics:**\n\n"
    message += f"👥 Всего пользователей: {stats['total_users']}\n" if lang == 'ru' else f"👥 Total users: {stats['total_users']}\n"
    message += f"📝 Всего действий: {stats['total_actions']}\n" if lang == 'ru' else f"📝 Total actions: {stats['total_actions']}\n"
    message += f"🎮 Всего игр: {stats['total_games']}\n" if lang == 'ru' else f"🎮 Total games: {stats['total_games']}\n"
    
    bot.send_message(user_id, message, parse_mode='Markdown')

@admin_only
def handle_admin_role(message):
    """Обработчик изменения роли"""
    user_id = message.from_user.id
    text = message.text
    lang = user_lang.get(user_id, 'ru')

    if text == get_text('back', user_id):
        user_states[user_id]['current'] = State.ADMIN
        bot.send_message(
            user_id,
            "🔄 Возврат в админ-панель.",
            reply_markup=admin_keyboard(lang)
        )
        return

    # Парсим ввод: "ID роль"
    parts = text.split()
    if len(parts) != 2:
        bot.send_message(
            user_id,
            "❌ Неверный формат. Используйте: `ID роль`\nНапример: `123456789 moderator`" if lang == 'ru' else "❌ Invalid format. Use: `ID role`\nExample: `123456789 moderator`",
            parse_mode='Markdown'
        )
        return
    
    try:
        target_id = int(parts[0])
        new_role = parts[1].lower()
        
        if new_role not in ['user', 'moderator', 'admin']:
            bot.send_message(
                user_id,
                "❌ Роль должна быть: `user`, `moderator` или `admin`" if lang == 'ru' else "❌ Role must be: `user`, `moderator` or `admin`",
                parse_mode='Markdown'
            )
            return
        
        # Изменяем роль
        if set_user_role(target_id, new_role):
            bot.send_message(
                user_id,
                f"✅ Роль пользователя {target_id} изменена на `{new_role}`" if lang == 'ru' else f"✅ User {target_id} role changed to `{new_role}`",
                parse_mode='Markdown'
            )
            
            # Уведомляем пользователя об изменении роли
            try:
                role_names = {
                    'user': 'пользователь' if lang == 'ru' else 'user',
                    'moderator': 'модератор' if lang == 'ru' else 'moderator',
                    'admin': 'администратор' if lang == 'ru' else 'admin'
                }
                bot.send_message(
                    target_id,
                    f"🔔 Ваша роль изменена на: **{role_names[new_role]}**" if lang == 'ru' else f"🔔 Your role has been changed to: **{role_names[new_role]}**",
                    parse_mode='Markdown'
                )
            except:
                pass  # Пользователь мог заблокировать бота
        else:
            bot.send_message(
                user_id,
                "❌ Пользователь не найден." if lang == 'ru' else "❌ User not found."
            )
            
    except ValueError:
        bot.send_message(
            user_id,
            "❌ ID должен быть числом." if lang == 'ru' else "❌ ID must be a number."
        )