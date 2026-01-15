
import sys
import os

print("="*60)
print("ПАРСИНГ ВКОНТАКТЕ С ВИДИМЫМ БРАУЗЕРОМ")
print("="*60)

sys.path.append(os.getcwd())

try:
    from parsing.vk_parser import VKParser
    print("✅ VKParser импортирован")
except ImportError as e:
    print(f"❌ Ошибка: {e}")
    sys.exit(1)

print("\n🚀 Запускаем парсер с ВИДИМЫМ браузером...")
parser = VKParser(headless=False)  

try:
    print("\n🔍 Ищем посты 'программирование'...")
    posts = parser.search_public_posts("программирование", max_posts=5)
    
    print(f"\n📊 Найдено постов: {len(posts)}")
    
    if posts:
        os.makedirs('parsing/data', exist_ok=True)
        
        import pandas as pd
        df = pd.DataFrame(posts)
        filename = 'parsing/data/vk_visible_results.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        
        print(f"💾 Сохранено в: {filename}")
        print("\n📝 Результаты:")
        for i, post in enumerate(posts[:3], 1):
            text = post.get('text', '')[:100] + '...' if len(post.get('text', '')) > 100 else post.get('text', '')
            print(f"{i}. {text}")
            print(f"   👤 Автор: {post.get('author', 'N/A')}")
            print(f"   👍 Лайки: {post.get('likes', 'N/A')}")
            print()
    
    print("\n⏳ Ждем 10 секунд чтобы вы могли увидеть браузер...")
    import time
    time.sleep(10)
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    import traceback
    traceback.print_exc()
    
    print("\n⏳ Ждем 10 секунд...")
    import time
    time.sleep(10)
    
finally:
    parser.close()

print("\n" + "="*60)
print("✅ ЗАВЕРШЕНО!")
print("="*60)
input("Нажмите Enter для выхода...")