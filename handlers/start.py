from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from keyboards import lang_select_keyboard
from database import add_or_update_user, log_action

@bot.message_handler(commands=['start'])

def start(message):
  user_id = message.from_user.id
  add_or_update_user(user_id, message.from_user.first_name, message.from_user.username)
  log_action(user_id, 'start')
  user_states[user_id] = {'current': State.LANG_SELECT, 'previous': None}
  if user_id in user_lang:
     del user_lang[user_id]
  

  bot.send_message(
    user_id,
    "Пожалуйста, выберите язык / Please choose a language:",
    reply_markup=lang_select_keyboard()
  )

