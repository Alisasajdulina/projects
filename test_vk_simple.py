
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from parsing.vk_parser import VKParser
    
    print("✅ Модуль VKParser успешно импортирован!")
    
    parser = VKParser(headless=False)  
    try:
        print("\n🧪 Запускаем тест...")
        result = parser.get_simple_test()
        print(f"Результат теста: {result}")
        
        print("\n🔍 Ищем посты...")
        posts = parser.search_public_posts("технологии", max_posts=3)
        
        print(f"\n📊 Найдено {len(posts)} постов:")
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post.get('text', 'Нет текста')[:100]}...")
        
    finally:
        parser.close()
        
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("\nПроверьте что файл vk_parser.py существует и содержит класс VKParser")
except Exception as e:
    print(f"❌ Другая ошибка: {e}")