print("="*60)
print("ПРОСТОЙ ПАРСЕР ВКОНТАКТЕ")
print("="*60)

import pandas as pd
import os
from parsing.vk_parser import VKParser

parser = VKParser(headless=False)

try:
    print("\nИщем посты...")
    posts = parser.search_public_posts("технологии", 5)
    
    if not posts:
        print("Ищем другой запрос...")
        posts = parser.search_public_posts("новости", 5)
    
    print(f"\nНайдено: {len(posts)} постов")
    
    if posts:
        os.makedirs('data', exist_ok=True)
        df = pd.DataFrame(posts)
        df.to_csv('data/vk_simple.csv', index=False, encoding='utf-8')
        print(f"✅ Сохранено в data/vk_simple.csv")
        
        print("\nПервые 3 поста:")
        for i, (_, row) in enumerate(df.head(3).iterrows(), 1):
            print(f"{i}. {row.get('text', '')[:80]}...")
    
finally:
    parser.close()

print("\nГотово!")
