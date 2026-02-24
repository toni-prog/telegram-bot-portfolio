from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from keyboards import lang_select_keyboard, main_keyboard
from translations import translations
from database import add_or_update_user


def handle_lang_select(message):
  user_id = message.from_user.id
  text = message.text

  if text == 'Русский':
    user_lang[user_id] = 'ru'
    add_or_update_user(user_id, message.from_user.first_name, message.from_user.username, language='ru')
    user_states[user_id]['current'] = State.MAIN
    user_states[user_id]['previous'] = None
    bot.send_message(user_id, translations['ru']['start_message'],
                     reply_markup=main_keyboard('ru'))
  elif text == 'English':
    user_lang[user_id] = 'en'
    add_or_update_user(user_id, message.from_user.first_name, message.from_user.username, language='en')
    user_states[user_id]['current'] = State.MAIN
    user_states[user_id]['previous'] = None
    bot.send_message(
      user_id, translations['en']['start_message'],
                     reply_markup=main_keyboard('en'))
  
  else:
    bot.send_message(user_id, "Пожалуйста, выберите язык / Please choose a language:", reply_markup=lang_select_keyboard())
