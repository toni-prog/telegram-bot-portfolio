import os
import io
import random
from PIL import Image, ImageDraw, ImageFont
from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from utils import get_text
from keyboards import meme_keyboard, meme_action_keyboard, projects_keyboard
from database import save_meme, log_action

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

FONT_PATH = "fonts/arial.ttf"

def handle_meme(message):
  """Обработчик для раздела мемов"""
  user_id = message.from_user.id
  text = message.text
  lang = user_lang.get(user_id, 'ru')

  if text == get_text('back', user_id):
    # Возврат в меню проектов
    user_states[user_id]['current'] = State.PROJECTS
    user_states[user_id]['previous'] = State.GREET
    bot.send_message(
      user_id,
      get_text('back_to_projects', user_id),
      reply_markup=projects_keyboard(lang)
    )
    return
  
  if text == get_text('meme_create', user_id):
    # Начинаем создание мема
    user_states[user_id]['previous'] = State.MEME
    user_states[user_id]['current'] = State.MEME_WAIT_PHOTO
    bot.send_message(
      user_id,
      "📸 Отправьте мне фотографию для мема:" if lang == 'ru' else "📸 Send me a photo for the meme:",
      reply_markup=meme_action_keyboard(lang)
    )
  elif text == get_text('meme_random', user_id):
    # Случайный мем из шаблонов
    send_random_meme(user_id, lang)

  else:
    bot.send_message(
      user_id,
      get_text('unknown_command', user_id),
      reply_markup=meme_keyboard(lang)
    )

def handle_meme_wait_photo(message):
  """Обработчик ожидания фото для мема"""
  user_id = message.from_user.id
  lang = user_lang.get(user_id, 'ru')

  # Проверяем, что прислали фото
  if message.photo:
    # Сохраняем file_id фото в user_data
    from user_data import user_meme_data
    user_meme_data[user_id] = {
      'photo_file_id': message.photo[-1].file_id    # Берем самое большое фото
    }

    # Переходим в состояние ожидания текста
    user_states[user_id]['current'] = State.MEME_WAIT_TEXT
    bot.send_message(
      user_id,
      "✏️ Теперь напишите текст, который хотите разместить на меме:",
      reply_markup=meme_action_keyboard(lang)
    )
  else:
    bot.send_message(
      user_id,
      "❌ Пожалуйста, отправьте именно фотографию!" if lang == 'ru' else "❌ Please send a photo!",
      reply_markup=meme_action_keyboard(lang)
    )

def handle_meme_wait_text(message):
    """Обработчик ожидания текста для мема"""
    user_id = message.from_user.id
    text = message.text
    lang = user_lang.get(user_id, 'ru')
    
    from user_data import user_meme_data
    
    if user_id not in user_meme_data or 'photo_file_id' not in user_meme_data[user_id]:
        bot.send_message(
            user_id,
            "❌ Что-то пошло не так. Начните заново.",
            reply_markup=meme_keyboard(lang)
        )
        user_states[user_id]['current'] = State.MEME
        return
    
    # Отправляем уведомление о начале генерации
    bot.send_chat_action(user_id, 'upload_photo')
    
    try:
        # Получаем фото
        photo_file_id = user_meme_data[user_id]['photo_file_id']
        file_info = bot.get_file(photo_file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Создаем мем
        meme_bytes = create_meme_from_bytes(downloaded_file, text)
        
        if meme_bytes:
            # Сохраняем информацию о меме
            meme_filename = f"meme_{user_id}_{random.randint(1000, 9999)}.jpg"
            meme_path = os.path.join(TEMP_DIR, meme_filename)
            with open(meme_path, 'wb') as f:
                f.write(meme_bytes)
            
            save_meme(user_id, message.from_user.username, meme_path, text)
            
            # Отправляем мем пользователю
            bot.send_photo(
                user_id,
                meme_bytes,
                caption="✅ Ваш мем готов!" if lang == 'ru' else "✅ Your meme is ready!"
            )
            
            log_action(user_id, 'meme_created')
        else:
            bot.send_message(
                user_id,
                "❌ Не удалось создать мем. Попробуйте другое фото.",
                reply_markup=meme_keyboard(lang)
            )
            
    except Exception as e:
        print(f"Ошибка создания мема: {e}")
        bot.send_message(
            user_id,
            "❌ Ошибка при создании мема.",
            reply_markup=meme_keyboard(lang)
        )
    
    # Очищаем временные данные
    if user_id in user_meme_data:
        del user_meme_data[user_id]
    
    # Возвращаемся в меню мемов
    user_states[user_id]['current'] = State.MEME
    bot.send_message(
        user_id,
        "🔄 Выберите действие:" if lang == 'ru' else "🔄 Choose action:",
        reply_markup=meme_keyboard(lang)
    )

def create_meme_from_bytes(image_bytes, text):
    """Создает мем из байтов изображения и текста"""
    try:
        # Открываем изображение
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        draw = ImageDraw.Draw(image)
        
        # Определяем размер шрифта (10% от ширины изображения)
        font_size = int(image.width / 15)
        
        # Загружаем шрифт
        try:
            font = ImageFont.truetype(FONT_PATH, size=font_size)
        except:
            # Если шрифт не найден, используем стандартный
            font = ImageFont.load_default()
            font_size = 20
        
        # Разбиваем текст на строки, если он длинный
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            # Используем getbbox для измерения ширины текста
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]
            
            if text_width < image.width * 0.9:  # 90% ширины изображения
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Рисуем текст в нижней части изображения
        y = image.height - (font_size + 10) * len(lines) - 20
        
        for i, line in enumerate(lines):
            # Вычисляем ширину строки
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (image.width - text_width) // 2
            
            # Рисуем черный контур для читаемости
            for dx, dy in [(1,1), (-1,-1), (1,-1), (-1,1), (2,0), (-2,0), (0,2), (0,-2)]:
                draw.text((x+dx, y+dy + i*(font_size+5)), line, fill="black", font=font)
            
            # Рисуем белый текст поверх
            draw.text((x, y + i*(font_size+5)), line, fill="white", font=font)
        
        # Сохраняем в байты
        output = io.BytesIO()
        image.save(output, format='JPEG', quality=90)
        output.seek(0)
        
        return output.getvalue()
        
    except Exception as e:
        print(f"Ошибка в create_meme_from_bytes: {e}")
        return None

def send_random_meme(user_id, lang):
    """Отправляет случайный мем из готовых шаблонов"""
    # Здесь можно использовать API случайных мемов
    # Например, https://api.imgflip.com/popular_meme_ids
    
    bot.send_message(
        user_id,
        "🔄 Функция случайных мемов в разработке. Пока попробуйте создать свой мем!",
        reply_markup=meme_keyboard(lang)
    )