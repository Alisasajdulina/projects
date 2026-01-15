print("=" * 50)
print("ТЕСТОВЫЙ СКРИПТ")
print("=" * 50)
print("Если вы видите этот текст, значит Python работает")
print(f"Текущая папка: {__file__}")

import sys
print(f"\nPython версия: {sys.version}")
print(f"Python путь: {sys.executable}")

try:
    from parsing.vk_parser import VKParser
    print("✅ VKParser импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта VKParser: {e}")

try:
    from utils.data_saver import DataSaver
    print("✅ DataSaver импортирован успешно")
except ImportError as e:
    print(f"❌ Ошибка импорта DataSaver: {e}")

input("\nНажмите Enter для выхода...")
