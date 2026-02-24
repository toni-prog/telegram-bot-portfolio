import os
import speech_recognition as sr
from pydub import AudioSegment
from bot_instance import bot
from user_data import user_states, user_lang
from states import State
from utils import get_text
from keyboards import voice_keyboard, voice_action_keyboard, projects_keyboard
from database import save_voice_query, log_action

# Путь к папке для временных файлов
TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

def handle_voice(message):
    """Обработчик для раздела голосовых сообщений"""
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

    if text == get_text('voice_recognize', user_id):
        # Начинаем распознавание
        user_states[user_id]['previous'] = State.VOICE
        user_states[user_id]['current'] = State.VOICE_WAIT
        bot.send_message(
            user_id,
            "🎤 Отправьте мне голосовое сообщение, и я распознаю текст:" if lang == 'ru' else "🎤 Send me a voice message and I'll recognize the text:",
            reply_markup=voice_action_keyboard(lang)
        )
        
    else:
        bot.send_message(
            user_id,
            get_text('unknown_command', user_id),
            reply_markup=voice_keyboard(lang)
        )

def handle_voice_wait(message):
    """Обработчик ожидания голосового сообщения"""
    user_id = message.from_user.id
    lang = user_lang.get(user_id, 'ru')

    if message.voice:
        # Отправляем уведомление о начале обработки
        bot.send_chat_action(user_id, 'typing')
        
        try:
            # Скачиваем голосовое сообщение
            file_info = bot.get_file(message.voice.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            
            # Сохраняем временный файл
            ogg_path = os.path.join(TEMP_DIR, f"voice_{user_id}_{message.voice.file_id}.ogg")
            with open(ogg_path, 'wb') as f:
                f.write(downloaded_file)
            
            # Конвертируем OGG в WAV
            wav_path = ogg_path.replace('.ogg', '.wav')
            audio = AudioSegment.from_ogg(ogg_path)
            audio.export(wav_path, format="wav")
            
            # Распознаем речь
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_path) as source:
                audio_data = recognizer.record(source)
                
                try:
                    # Пробуем распознать на выбранном языке
                    lang_code = 'ru-RU' if lang == 'ru' else 'en-US'
                    recognized_text = recognizer.recognize_google(audio_data, language=lang_code)
                    
                    # Сохраняем результат
                    save_voice_query(
                        user_id=user_id,
                        username=message.from_user.username,
                        recognized_text=recognized_text
                    )
                    
                    # Отправляем результат
                    result_message = f"📝 Распознанный текст:\n\n_{recognized_text}_" if lang == 'ru' else f"📝 Recognized text:\n\n_{recognized_text}_"
                    bot.send_message(user_id, result_message, parse_mode='Markdown')
                    
                    log_action(user_id, 'voice_recognition_success')
                    
                except sr.UnknownValueError:
                    bot.send_message(
                        user_id,
                        "😕 Не удалось распознать речь. Попробуйте говорить четче." if lang == 'ru' else "😕 Could not understand audio. Please speak more clearly."
                    )
                except sr.RequestError as e:
                    bot.send_message(
                        user_id,
                        "🌐 Ошибка сервиса распознавания. Попробуйте позже." if lang == 'ru' else "🌐 Recognition service error. Try again later."
                    )
            
            # Удаляем временные файлы
            os.remove(ogg_path)
            if os.path.exists(wav_path):
                os.remove(wav_path)
                
        except Exception as e:
            print(f"Ошибка обработки голоса: {e}")
            bot.send_message(
                user_id,
                "❌ Ошибка при обработке голосового сообщения.",
                reply_markup=voice_keyboard(lang)
            )
        
        # Возвращаемся в меню голосовых
        user_states[user_id]['current'] = State.VOICE
        bot.send_message(
            user_id,
            "🔄 Выберите действие:" if lang == 'ru' else "🔄 Choose action:",
            reply_markup=voice_keyboard(lang)
        )
        
    else:
        bot.send_message(
            user_id,
            "❌ Пожалуйста, отправьте именно голосовое сообщение!" if lang == 'ru' else "❌ Please send a voice message!",
            reply_markup=voice_action_keyboard(lang)
        )