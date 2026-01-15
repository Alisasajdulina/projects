import pandas as pd
import json
import os
from typing import List, Dict

class DataSaver:
    """Класс для сохранения данных в различные форматы"""
    
    @staticmethod
    def save_to_csv(data: List[Dict], filename: str, encoding: str = 'utf-8-sig'):
        """
        Сохранение данных в CSV
        
        Args:
            data: Список словарей с данными
            filename: Путь к файлу
            encoding: Кодировка файла
        """
        if not data:
            print("Нет данных для сохранения")
            return False
        
        try:
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            
            df = pd.DataFrame(data)
            df.to_csv(filename, index=False, encoding=encoding)
            
            print(f"✅ Данные сохранены: {filename}")
            print(f"   Записей: {len(df)} | Колонок: {len(df.columns)}")
            
            file_size = os.path.getsize(filename) / 1024  
            print(f"   Размер файла: {file_size:.2f} KB")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при сохранении CSV: {e}")
            return False
    
    @staticmethod
    def save_to_json(data: List[Dict], filename: str):
        """Сохранение данных в JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"✅ JSON сохранен: {filename}")
            return True
        except Exception as e:
            print(f"❌ Ошибка при сохранении JSON: {e}")
            return False
    
    @staticmethod
    def print_data_summary(data: List[Dict], name: str = "данных"):
        """Печать сводки по данным"""
        if not data:
            print(f"Нет {name} для анализа")
            return
        
        df = pd.DataFrame(data)
        
        print(f"\n{'='*50}")
        print(f"СВОДКА ПО {name.upper()}:")
        print(f"{'='*50}")
        print(f"Всего записей: {len(df)}")
        print(f"Колонки: {', '.join(df.columns.tolist())}")
        
        print("\nПервые 3 записи:")
        print(df.head(3).to_string())