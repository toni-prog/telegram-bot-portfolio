class State:
  LANG_SELECT = 'lang_select'
  MAIN = 'main'
  GREET = 'greet'
  LANGUAGE = 'language'
  WEATHER = "weather"
  PROJECTS = "projects"
  GUESS_GAME = "guess_game"
  WEATHER_CITY = "weather_city"
  PARSING = "parsing"
  PARSING_CURRENCY = "parsing_currency"
  PARSING_QUOTE = "parsing_quote"
  PARSING_JOKE = "parsing_joke"

  MEME = "meme"   # Главное меню мемов
  MEME_WAIT_PHOTO = "meme_wait_photo"    # Ожидание фото
  MEME_WAIT_TEXT = "meme_wait_text"    # Ожидание текста

  VOICE = "voice"    # Главное меню голосовых
  VOICE_WAIT = "voice_wait"    # Ожидание голосового сообщения

  ADMIN = "admin"    # Админ-панель
  ADMIN_USERS = "admin_users"    # Управление пользователями
  ADMIN_STATS = "admin_stats"    # Просмотр статистики
  ADMIN_ROLE = "admin_role"    # Изменение ролей