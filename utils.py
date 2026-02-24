from user_data import user_lang
from translations import translations

def get_text(key, user_id):
  lang = user_lang.get(user_id, 'ru')
  return translations[lang].get(key, key)