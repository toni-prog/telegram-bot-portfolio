from telebot import types
from translations import translations

def main_keyboard(lang):
  """Клавиатура главного меню"""
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn_greet = types.KeyboardButton(translations[lang]['greet_button'])
  markup.add(btn_greet)
  return markup

def greet_keyboard(lang):
  """Клавиатура подменю (после приветствия)"""
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  btn1 = types.KeyboardButton(translations[lang]['about_me'])
  btn2 = types.KeyboardButton(translations[lang]['skills'])
  btn3 = types.KeyboardButton(translations[lang]['projects'])
  btn4 = types.KeyboardButton(translations[lang]['choose_lang'])
  btn_back = types.KeyboardButton(translations[lang]['back'])
  markup.add(btn1, btn2)
  markup.add(btn3, btn4)
  markup.add(btn_back)
  return markup

def projects_keyboard(lang):
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
   markup.add(
      types.KeyboardButton(translations[lang]['guess_game']),
      types.KeyboardButton(translations[lang]['weather'])
   )
   markup.add(
      types.KeyboardButton(translations[lang]['parsing']),
      types.KeyboardButton(translations[lang]['meme'])
      
   )
   markup.add(
      types.KeyboardButton(translations[lang]['voice']),
      types.KeyboardButton(translations[lang]['back'])
   )
   return markup

def game_keyboard(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(translations[lang]['back']))
    return markup

def weather_keyboard(lang):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(translations[lang]['back']))
    return markup

def language_keyboard(lang):
   markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
   btn_ru = types.KeyboardButton(translations[lang]['lang_ru'])
   btn_en = types.KeyboardButton(translations[lang]['lang_en'])
   btn_back = types.KeyboardButton(translations[lang]['back'])
   markup.add(btn_ru, btn_en)
   markup.add(btn_back)
   return markup

def lang_select_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('Русский'), types.KeyboardButton('English'))
    return markup

def parsing_keyboard(lang):
    """Клавиатура для раздела парсинга"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(translations[lang]['currency']),
        types.KeyboardButton(translations[lang]['quote'])
    )
    markup.add(
        types.KeyboardButton(translations[lang]['joke']),
        types.KeyboardButton(translations[lang]['back'])
    )
    return markup

def parsing_action_keyboard(lang):
    """Клавиатура для действий внутри парсинга (только назад)"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(translations[lang]['back']))
    return markup

def meme_keyboard(lang):
    """Клавиатура для раздела мемов"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(translations[lang]['meme_create']),
        types.KeyboardButton(translations[lang]['meme_random'])
    )
    markup.add(types.KeyboardButton(translations[lang]['back']))
    return markup

def meme_action_keyboard(lang):
    """Клавиатура для действий внутри мемов (только назад)"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(translations[lang]['back']))
    return markup

def voice_keyboard(lang):
    """Клавиатура для раздела голосовых"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(translations[lang]['voice_recognize']))
    markup.add(types.KeyboardButton(translations[lang]['back']))
    return markup

def voice_action_keyboard(lang):
    """Клавиатура для действий внутри голосовых (только назад)"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(translations[lang]['back']))
    return markup

def admin_keyboard(lang):
    """Клавиатура для админ-панели"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(translations[lang]['admin_users']),
        types.KeyboardButton(translations[lang]['admin_stats'])
    )
    # Кнопка изменения роли только для главного админа (проверка в хэндлере)
    markup.add(types.KeyboardButton(translations[lang]['admin_set_role']))
    markup.add(types.KeyboardButton(translations[lang]['back']))
    return markup

def admin_action_keyboard(lang):
    """Клавиатура для действий внутри админки (только назад)"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(translations[lang]['back']))
    return markup