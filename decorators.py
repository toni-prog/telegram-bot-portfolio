from functools import wraps
from bot_instance import bot
from user_data import user_lang
from database import get_user_role
from utils import get_text

def role_required(allowed_roles):
  # Декоратор для проверки роли пользователя allowed_roles: список разрешенных ролей, например ['admin', 'moderator']

  def decorator(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
      user_id = message.from_user.id
      user_role = get_user_role(user_id)

      if user_role in allowed_roles:
        return func(message, *args, **kwargs)
      else:
        lang = user_lang.get(user_id, 'ru')
        bot.send_message(
          user_id,
          "⛔ У вас нет прав для выполнения этой команды." if lang == 'ru' else "⛔ You don't have permission to use this command."
        )
        return None
    return wrapper
  return decorator

def admin_only(func):
  # Декоратор только для админов
  return role_required(['admin'])(func)

def moderator_plus(func):
  # Декоратор для модераторов и админов
  return role_required(['admin', 'moderator'])(func)