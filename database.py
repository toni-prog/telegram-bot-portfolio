import sqlite3
import os

DB_NAME = 'bot_database.db'


def get_connection():
  conn = sqlite3.connect(DB_NAME)
  conn.row_factory = sqlite3.Row
  return conn

def init_db():
  """Создаёт таблицы, если их нет."""
  with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
                   user_id INTEGER PRIMARY KEY,
                   first_name TEXT,
                   username TEXT,
                   language TEXT DEFAULT 'ru',
                   role TEXT DEFAULT 'user', -- 'user', 'moderator', 'admin'
                   first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
                   ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_actions (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER,
                   action TEXT,
                   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                   FOREIGN KEY (user_id) REFERENCES users(user_id)
                   )
                   ''')
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS guess_game_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                first_name TEXT,
                secret_number INTEGER,
                attempts INTEGER,
                won BOOLEAN,
                game_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                game_duration_seconds INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                first_name TEXT,
                city TEXT,
                temperature REAL,
                description TEXT,
                query_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
    # Таблица для курсов валют
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS currency_rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                usd_rate REAL,
                eur_rate REAL,
                cny_rate REAL,
                gbp_rate REAL,
                jpy_rate REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
     # Таблица для запросов цитат
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS quote_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                first_name TEXT,
                quote_text TEXT,
                quote_author TEXT,
                query_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
        
        # Таблица для запросов анекдотов
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS joke_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                first_name TEXT,
                joke_text TEXT,
                query_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)
    
        #Таблица для голосовых запросов
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS voice_queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                recognized_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        """)

    conn.commit()
    print("База данных успешно инициализирована")

def add_or_update_user(user_id, first_name, username, language='ru'):
    """Добавляет или обновляет пользователя в БД"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (user_id, first_name, username, language, last_active)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
                first_name=excluded.first_name,
                username=excluded.username,
                language=excluded.language,
                last_active=CURRENT_TIMESTAMP
        """, (user_id, first_name, username, language))
        conn.commit()

def log_action(user_id, action):
  with get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute('INSERT INTO user_actions (user_id, action) VALUES (?, ?)', (user_id, action))
    conn.commit()

def save_game_result(user_id, username, first_name, secret_number, attempts, won, duration):
    """Сохраняет результат игры в БД"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO guess_game_results 
            (user_id, username, first_name, secret_number, attempts, won, game_duration_seconds)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, username, first_name, secret_number, attempts, won, duration))
        conn.commit()

def get_user_game_stats(user_id):
    """Получает статистику игр пользователя"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_games,
                SUM(CASE WHEN won = 1 THEN 1 ELSE 0 END) as wins,
                AVG(attempts) as avg_attempts,
                MIN(attempts) as best_attempts
            FROM guess_game_results 
            WHERE user_id = ? AND won = 1
        """, (user_id,))
        result = cursor.fetchone()
        return dict(result) if result else None
    
def save_weather_query(user_id, username, first_name, city, temperature, description):
    """Сохраняет запрос погоды в БД"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO weather_queries 
            (user_id, username, first_name, city, temperature, description)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, username, first_name, city, temperature, description))
        conn.commit()

def get_user_weather_history(user_id, limit=5):
    """Получает историю запросов погоды пользователя"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT city, temperature, description, query_date
            FROM weather_queries
            WHERE user_id = ?
            ORDER BY query_date DESC
            LIMIT ?
        """, (user_id, limit))
        results = []
        for row in cursor.fetchall():
            results.append({
                'city': row['city'],
                'temperature': row['temperature'],  # ← ключ temperature
                'description': row['description'],
                'query_date': row['query_date']
            })
        return results
    
def save_currency_rates(usd, eur, cny, gbp, jpy, date):
    """Сохраняет курсы валют в БД"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO currency_rates (date, usd_rate, eur_rate, cny_rate, gbp_rate, jpy_rate)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (date, usd, eur, cny, gbp, jpy))
        conn.commit()

def save_quote_query(user_id, username, first_name, quote_text, quote_author):
    """Сохраняет запрос цитаты в БД"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO quote_queries (user_id, username, first_name, quote_text, quote_author)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, username, first_name, quote_text, quote_author))
        conn.commit()

def save_joke_query(user_id, username, first_name, joke_text):
    """Сохраняет запрос анекдота в БД"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO joke_queries (user_id, username, first_name, joke_text)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, first_name, joke_text))
        conn.commit()

def get_user_role(user_id):
    """Получает роль пользователя"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE user_id = ?", (user_id,))
        result = cursor.fetchone()
        return result['role'] if result else 'user'

def set_user_role(user_id, role):
    """Устанавливает роль пользователя (только для админов)"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET role = ? WHERE user_id = ?", (role, user_id))
        conn.commit()
        return cursor.rowcount > 0

def get_all_users(limit=100):
    """Получает список всех пользователей"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id, first_name, username, language, role, last_active
            FROM users
            ORDER BY last_active DESC
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]

def get_user_stats():
    """Получает общую статистику"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total_users = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM user_actions")
        total_actions = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM guess_game_results")
        total_games = cursor.fetchone()['total']
        
        return {
            'total_users': total_users,
            'total_actions': total_actions,
            'total_games': total_games
        }
    
def save_meme(user_id, username, meme_path, text_used):
    """Сохраняет информацию о созданном меме"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO memes (user_id, username, meme_path, text_used)
            VALUES (?, ?, ?, ?)
        """, (user_id, username, meme_path, text_used))
        conn.commit()

def save_voice_query(user_id, username, recognized_text):
    """Сохраняет результат распознавания голоса"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO voice_queries (user_id, username, recognized_text)
            VALUES (?, ?, ?)
        """, (user_id, username, recognized_text))
        conn.commit()

