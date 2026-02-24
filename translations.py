# translations.py

translations = {
    'ru': {
        # Существующие ключи...
        'greet_button': '👋 Поздороваться',
        'about_me': 'О себе',
        'skills': 'Навыки и опыт работы',
        'projects': 'Мои проекты',
        'choose_lang': 'Выбор языка',
        'back': 'Назад',
        'lang_ru': 'Русский',
        'lang_en': 'English',
        'start_message': '👋 Привет! Добро пожаловать в мой бот-портфолио 🤖\n\n' '📌 Здесь ты сможешь узнать обо мне, моих навыках и проектах.\n' '🔽 Используй кнопки ниже для навигации',
        'choose_question': '❓ Выберите интересующий вопрос',
        'choose_lang_prompt': '🌐 Выберите язык:',
        'language_selected_ru': 'Язык изменён на русский.',
        'language_selected_en': 'Language changed to English.',
        'unknown_command': 'Незнакомая команда. Пожалуйста, используйте кнопки меню.',
        'error_return': 'Произошла ошибка. Возвращаем в главное меню.',
        'back_to_main': 'Главное меню',
        'back_to_greet': 'Вы вернулись в меню информации',
        'already_main': 'Вы уже в главном меню.',
        
        # Тексты разделов
        'about_me_text': '👨‍💻 *Возраст:* 26 лет\n\n🎓 *Образование:* Техник-программист, КПЭУ (Колледж права, экономики и управления)\n\n📚 *Дополнительное обучение:* Прошёл множество бесплатных онлайн-курсов и самостоятельно изучал различные языки программирования и технологии. Имею хорошую теоретическую базу, активно применяю знания на практике.\n\n💡 *О себе:* Я увлечён миром IT, постоянно учусь новому и стремлюсь создавать полезные продукты. Легко осваиваю новые инструменты, ответственно подхожу к задачам и умею работать в команде.\n\n🚀 *Цель:* Стать востребованным разработчиком и внести вклад в интересные проекты.',
        'skills_text': '💼 *Опыт работы по специальности:* отсутствует (начинающий специалист).\n\n📚 *Текущее обучение:* углублённо изучаю Python и связанные с ним библиотеки. Планирую освоить Django/Flask для веб-разработки, а также библиотеки для анализа данных и автоматизации.\n\n🛠️ *Технологии, с которыми знаком:*\n• *Языки программирования:* Python, C#, PHP, JavaScript (базово)\n• *Базы данных:* SQL (запросы, проектирование), MySQL, MS Access\n• *Веб-разработка:* HTML, CSS, WordPress (основы создания и настройки сайтов)\n• *Системы управления предприятием:* 1С (базовые знания конфигураций и программирования)\n• *Инструменты:* Git (основы), VS Code, PyCharm, работа с командной строкой\n\n💪 *Личные качества:* усидчивость, внимательность, аналитический склад ума, умение искать и структурировать информацию, стремление к качественному результату.',
        'projects_text': '📁 *Портфолио:* раздел находится в стадии наполнения.\n\n🛠️ В ближайшее время здесь появятся примеры моих работ: консольные приложения на Python, небольшие веб-сайты, учебные проекты по базам данных и автоматизации.\n\n📌 *Планирую опубликовать:*\n• Парсер данных с веб-сайтов (Python + BeautifulSoup/Scrapy)\n• Простой веб-сайт на Django с использованием базы данных\n• Скрипты для работы с Excel и автоматизации отчётов\n',
    
        
        # ключи для проектов
        'guess_game': '🎮 Угадай число',
        'weather': '🌤 Погода',
        'back_to_projects': 'Возврат в меню проектов',
        
        # Для игры "Угадай число"
        'guess_game_start': 'Я загадал число от 1 до 100. Попробуй угадать!',
        'guess_game_hint_bigger': 'Больше!',
        'guess_game_hint_smaller': 'Меньше!',
        'guess_game_win': 'Поздравляю! Ты угадал число {number} с {attempts} попытки(ок)!',
        'guess_game_invalid': 'Пожалуйста, введите число.',
        'guess_game_error': 'Ошибка игры. Начните заново.',
        
        # Для погоды
        'weather_enter_city': 'Введите название города:',
        'weather_result': 'Погода в {city}: {description}, температура {temp}°C',
        'weather_not_found': 'Город не найден. Попробуйте ещё раз.',
        'weather_error': 'Ошибка при получении данных о погоде.',

        # Для раздела парсинга
        'parsing': '🕷 Парсинг данных',
        'currency': '💵 Курсы валют',
        'quote': '💬 Случайная цитата',
        'joke': '😄 Случайный анекдот',
        'back_to_parsing': 'Возврат в меню парсинга',
    
        # Для курсов валют
        'currency_rates': '📊 Курсы валют ЦБ РФ на {date}:',
        'currency_usd': '🇺🇸 Доллар США (USD): {rate} ₽',
        'currency_eur': '🇪🇺 Евро (EUR): {rate} ₽',
        'currency_cny': '🇨🇳 Юань (CNY): {rate} ₽',
        'currency_gbp': '🇬🇧 Фунт стерлингов (GBP): {rate} ₽',
        'currency_jpy': '🇯🇵 Японская йена (JPY): {rate} ₽',
        'currency_error': '❌ Не удалось получить курсы валют. Попробуйте позже.',
    
        # Для цитат
        'quote_title': '💭 Случайная цитата:',
        'quote_author': '— {author}',
        'quote_error': '❌ Не удалось получить цитату. Попробуйте позже.',
    
        # Для анекдотов
        'joke_title': '😂 Случайный анекдот:',
        'joke_error': '❌ Не удалось получить анекдот. Попробуйте позже.',

        'currency_prompt': '🔄 Нажмите кнопку "Назад" для выхода или отправьте любой город для нового запроса курсов',
        'quote_prompt': '🔄 Нажмите кнопку "Назад" для выхода или отправьте любое сообщение для новой цитаты',
        'joke_prompt': '🔄 Нажмите кнопку "Назад" для выхода или отправьте любое сообщение для нового анекдота',

        # Для мемов
        'meme': '🎭 Генератор мемов',
        'meme_create': '✨ Создать мем',
        'meme_random': '🎲 Случайный мем',
    
        # Для голосовых
        'voice': '🎤 Голосовые сообщения',
        'voice_recognize': '🔊 Распознать речь',
    
        # Для админки
        'admin_panel': '👑 Админ-панель',
        'admin_users': '👥 Пользователи',
        'admin_stats': '📊 Статистика',
        'admin_set_role': '🔐 Изменить роль',

    },
    
    'en': {
        # Существующие ключи...
        'greet_button': '👋 Greet',
        'about_me': 'About me',
        'skills': 'Skills and experience',
        'projects': 'My projects',
        'choose_lang': 'Choose language',
        'back': 'Back',
        'lang_ru': 'Russian',
        'lang_en': 'English',
        'start_message': '👋 Hello! Welcome to my portfolio bot 🤖\n\n' '📌 Here you can learn about me, my skills, and projects.\n' '🔽 Use the buttons below to navigate',
        'choose_question': '❓ Choose a question',
        'choose_lang_prompt': '🌐 Choose language:',
        'language_selected_ru': 'Language changed to Russian.',
        'language_selected_en': 'Language changed to English.',
        'unknown_command': 'Unknown command. Please use the menu buttons.',
        'error_return': 'An error occurred. Returning to main menu.',
        'back_to_main': 'Main menu',
        'back_to_greet': 'You are back to info menu',
        'already_main': 'You are already in the main menu.',
        
        # Section texts
        'about_me_text': '👨‍💻 *Age:* 26 years\n\n🎓 *Education:* Technician-programmer, KPEU (College of Law, Economics and Management)\n\n📚 *Additional training:* Completed many free online courses and independently studied various programming languages and technologies. I have a good theoretical background and actively apply knowledge in practice.\n\n💡 *About me:* I am passionate about the IT world, constantly learning new things and striving to create useful products. I easily master new tools, take a responsible approach to tasks, and can work in a team.\n\n🚀 *Goal:* To become a sought-after developer and contribute to interesting projects.',
        'skills_text': '💼 *Work experience in the field:* none (entry-level specialist).\n\n📚 *Current study:* in-depth study of Python and related libraries. I plan to master Django/Flask for web development, as well as libraries for data analysis and automation.\n\n🛠️ *Technologies I am familiar with:*\n• *Programming languages:* Python, C#, PHP, JavaScript (basic)\n• *Databases:* SQL (queries, design), MySQL, MS Access\n• *Web development:* HTML, CSS, WordPress (basics of creating and configuring sites)\n• *Enterprise management systems:* 1C (basic knowledge of configurations and programming)\n• *Tools:* Git (basics), VS Code, PyCharm, command line work\n\n💪 *Personal qualities:* perseverance, attentiveness, analytical mind, ability to search and structure information, desire for a quality result.',
        'projects_text': '📁 *Portfolio:* section is being populated.\n\n🛠️ In the near future, examples of my work will appear here: console applications in Python, small websites, educational projects on databases and automation.\n\n📌 *I plan to publish:*\n• Web scraper (Python + BeautifulSoup/Scrapy)\n• Simple Django website with database\n• Scripts for working with Excel and report automation\n',
        
        # New keys for projects
        'guess_game': '🎮 Guess the number',
        'weather': '🌤 Weather',
        'back_to_projects': 'Back to projects menu',
        
        # For "Guess the number" game
        'guess_game_start': 'I have guessed a number from 1 to 100. Try to guess!',
        'guess_game_hint_bigger': 'Bigger!',
        'guess_game_hint_smaller': 'Smaller!',
        'guess_game_win': 'Congratulations! You guessed the number {number} in {attempts} attempts!',
        'guess_game_invalid': 'Please enter a number.',
        'guess_game_error': 'Game error. Please start over.',
        
        # For weather
        'weather_enter_city': 'Enter city name:',
        'weather_result': 'Weather in {city}: {description}, temperature {temp}°C',
        'weather_not_found': 'City not found. Please try again.',
        'weather_error': 'Error getting weather data.',

        # For parsing section
        'parsing': '🕷 Data parsing',
        'currency': '💵 Currency rates',
        'quote': '💬 Random quote',
        'joke': '😄 Random joke',
        'back_to_parsing': 'Back to parsing menu',
    
        # For currency rates
        'currency_rates': '📊 Central Bank rates for {date}:',
        'currency_usd': '🇺🇸 US Dollar (USD): {rate} RUB',
        'currency_eur': '🇪🇺 Euro (EUR): {rate} RUB',
        'currency_cny': '🇨🇳 Chinese Yuan (CNY): {rate} RUB',
        'currency_gbp': '🇬🇧 British Pound (GBP): {rate} RUB',
        'currency_jpy': '🇯🇵 Japanese Yen (JPY): {rate} RUB',
        'currency_error': '❌ Failed to get currency rates. Try again later.',
    
        # For quotes
        'quote_title': '💭 Random quote:',
        'quote_author': '— {author}',
        'quote_error': '❌ Failed to get quote. Try again later.',
    
        # For jokes
        'joke_title': '😂 Random joke:',
        'joke_error': '❌ Failed to get joke. Try again later.',

        'currency_prompt': '🔄 Press "Back" to exit or send any city for new currency rates',
        'quote_prompt': '🔄 Press "Back" to exit or send any message for a new quote',
        'joke_prompt': '🔄 Press "Back" to exit or send any message for a new joke',

        # For memes
        'meme': '🎭 Meme generator',
        'meme_create': '✨ Create meme',
        'meme_random': '🎲 Random meme',

        # For voice
        'voice': '🎤 Voice messages',
        'voice_recognize': '🔊 Recognize speech',
    
        # For admin
        'admin_panel': '👑 Admin panel',
        'admin_users': '👥 Users',
        'admin_stats': '📊 Statistics',
        'admin_set_role': '🔐 Change role',

    }
}