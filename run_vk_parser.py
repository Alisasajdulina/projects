
from parsing.vk_parser import VKParser

def main():
    print("=" * 50)
    print("ПАРСИНГ ДАННЫХ С ВКОНТАКТЕ")
    print("=" * 50)
    
    # Создаем парсер (headless=False чтобы видеть браузер)
    parser = VKParser(headless=False)
    
    try:
        # 1. Ищем посты по запросу
        print("\n🔍 Ищем посты по запросу 'программирование'...")
        posts = parser.search_public_posts("программирование", max_posts=5)
        
        print(f"\n📊 Найдено {len(posts)} постов:")
        print("-" * 40)
        
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post.get('text', 'Нет текста')}")
            if 'likes' in post:
                print(f"   👍 {post['likes']} лайков")
            print()
        
        # 2. Ищем по другому запросу
        print("\n🔍 Ищем посты по запросу 'новости технологий'...")
        tech_posts = parser.search_public_posts("новости технологий", max_posts=3)
        
        print(f"\n📊 Найдено {len(tech_posts)} постов:")
        print("-" * 40)
        
        for i, post in enumerate(tech_posts, 1):
            print(f"{i}. {post.get('text', 'Нет текста')[:80]}...")
            if 'likes' in post:
                print(f"   👍 {post['likes']} лайков")
            print()
        
        # Сохраняем все посты в файл
        all_posts = posts + tech_posts
        
        if all_posts:
            # Создаем папку data если нет
            import os
            os.makedirs('data', exist_ok=True)
            
            # Сохраняем в CSV
            import pandas as pd
            df = pd.DataFrame(all_posts)
            df.to_csv('data/vk_posts.csv', index=False, encoding='utf-8-sig')
            
            print(f"\n💾 Данные сохранены в data/vk_posts.csv")
            print(f"   Всего записей: {len(df)}")
            print(f"   Колонки: {', '.join(df.columns.tolist())}")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
    
    finally:
        parser.close()
        print("\n✅ Парсинг завершен!")

if __name__ == "__main__":
    main()