print("="*60)
print("МИНИМАЛЬНЫЙ ПАРСЕР ВКОНТАКТЕ")
print("="*60)

import sys
import os
sys.path.append(os.getcwd())

try:
    from parsing.vk_parser import VKParser
    print("✅ VKParser импортирован")
    
    parser = VKParser(headless=False)  # Видим браузер
    print("✅ Парсер создан")
    
    # Тестовый поиск
    print("\n🔍 Тестовый поиск...")
    posts = parser.search_public_posts("Python", 2)
    
    print(f"\n📊 Результат: {len(posts)} постов")
    
    if posts:
        # Просто выводим
        for i, post in enumerate(posts, 1):
            print(f"\n{i}. {post.get('text', 'Нет текста')}")
            print(f"   Автор: {post.get('author', 'N/A')}")
            print(f"   Лайки: {post.get('likes', 'N/A')}")
    
    parser.close()
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*60)
print("ЗАВЕРШЕНО")
input("Нажмите Enter...")
