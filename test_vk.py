# test_vk.py
import sys
import os

# Добавляем текущую директорию в путь Python
sys.path.append(os.getcwd())

try:
    # Пробуем импортировать
    from parsing.vk_parser import VKParser
    print("✅ VKParser успешно импортирован!")
    
    # Создаем парсер
    print("\nСоздаем парсер...")
    parser = VKParser(headless=False)  # headless=False чтобы видеть браузер
    
    try:
        # Тестируем
        print("\nТестируем...")
        result = parser.hello() if hasattr(parser, 'hello') else parser.test()
        print(f"Результат: {result}")
        
        # Ищем посты
        print("\nИщем посты...")
        posts = parser.search("новости", 3)
        
        print(f"\nНайдено {len(posts)} постов:")
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post.get('title', post.get('text', 'Нет текста'))}")
            
    finally:
        parser.close()
        print("\n✅ Готово!")
        
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("\nСоздайте файл parsing/vk_parser.py с классом VKParser")
except Exception as e:
    print(f"❌ Другая ошибка: {e}")
    import traceback
    traceback.print_exc()