# test_imports.py
print("Тестирование импортов...")

try:
    from bot_instance import bot
    print("✅ bot_instance импортирован")
except Exception as e:
    print(f"❌ Ошибка импорта bot_instance: {e}")

try:
    import handlers
    print("✅ handlers импортирован")
    print(f"   Содержит: {dir(handlers)}")
except Exception as e:
    print(f"❌ Ошибка импорта handlers: {e}")

try:
    from handlers import start
    print("✅ start импортирован")
except Exception as e:
    print(f"❌ Ошибка импорта start: {e}")

try:
    from handlers import main_handler
    print("✅ main_handler импортирован")
except Exception as e:
    print(f"❌ Ошибка импорта main_handler: {e}")