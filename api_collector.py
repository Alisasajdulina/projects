import requests
import pandas as pd
import time
import json
from typing import Dict, List
from datetime import datetime
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

class APIDataCollector:
    """Базовый класс для сбора данных через API"""
    
    def __init__(self, api_name: str):
        """
        Инициализация коллектора данных
        
        Args:
            api_name: Название API
        """
        self.api_name = api_name
        self.demo_mode = False
        self.session = requests.Session()
        self.setup_session()
        self.request_delay = 1.0
    
    def setup_session(self):
        """Настройка HTTP сессии"""
        self.session.headers.update({
            'User-Agent': 'DataScienceStudent/1.0',
            'Accept': 'application/json'
        })
        
        # Проверяем API ключ
        api_key = os.getenv('WEATHERAPI_API_KEY')
        if not api_key or api_key == 'ваш_api_ключ_здесь':
            print("⚠️  API ключ не найден, используем демо-режим")
            self.demo_mode = True
    
    def make_request(self, endpoint: str, params: Dict = None) -> Dict:
        """
        Выполнение API запроса
        
        Args:
            endpoint: API endpoint
            params: Параметры запроса
            
        Returns:
            Словарь с данными ответа
        """
        # Демо-режим с тестовыми данными
        if self.demo_mode:
            print(f"   [ДЕМО] Запрос к {endpoint}")
            return self._get_mock_data(params)
        
        try:
            # Для WeatherAPI
            base_url = "http://api.weatherapi.com/v1"
            url = f"{base_url}{endpoint}"
            
            # Добавляем параметры
            request_params = params or {}
            
            # Добавляем API ключ
            api_key = os.getenv('WEATHERAPI_API_KEY')
            if api_key:
                request_params['key'] = api_key
            
            # Для WeatherAPI добавляем язык
            request_params['lang'] = 'ru'
            
            # Выполняем запрос
            print(f"   Запрос: {url}")
            
            response = self.session.get(url, params=request_params, timeout=15)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            print(f"   ❌ HTTP ошибка {e.response.status_code}: {e.response.text[:100]}")
            return {}
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Ошибка при запросе: {e}")
            return {}
        except json.JSONDecodeError as e:
            print(f"   ❌ Ошибка декодирования JSON: {e}")
            return {}
    
    def _get_mock_data(self, params: Dict = None) -> Dict:
        """Возвращает тестовые данные для демо-режима"""
        import random
        from datetime import datetime
        
        city_name = params.get('q', 'Test City') if params else 'Test City'
        
        return {
            "location": {
                "name": city_name,
                "country": "Russia",
                "lat": random.uniform(50, 60),
                "lon": random.uniform(30, 40),
                "localtime": datetime.now().isoformat()
            },
            "current": {
                "temp_c": random.randint(-10, 25),
                "feelslike_c": random.randint(-15, 20),
                "humidity": random.randint(30, 90),
                "pressure_mb": random.randint(980, 1030),
                "wind_kph": random.uniform(0, 20),
                "wind_dir": random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
                "cloud": random.randint(0, 100),
                "condition": {
                    "text": random.choice(['Sunny', 'Cloudy', 'Rainy', 'Snowy']),
                    "icon": "//cdn.weatherapi.com/weather/64x64/day/113.png"
                }
            }
        }
    
    def safe_request_with_delay(self, endpoint: str, params: Dict = None) -> Dict:
        """Безопасный запрос с задержкой"""
        result = self.make_request(endpoint, params)
        if not self.demo_mode:
            time.sleep(self.request_delay)
        return result
    
    def save_to_csv(self, data: List[Dict], filename: str):
        """
        Сохранение данных в CSV
        
        Args:
            data: Список словарей с данными
            filename: Имя файла для сохранения
        """
        if not data:
            print("❌ Нет данных для сохранения")
            return
        
        df = pd.DataFrame(data)
        
        # Создаем папку если нет
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        # Сохраняем
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ Данные сохранены в {filename}")
        print(f"   Всего записей: {len(df)}")
        
        # Показываем первые 3 строки
        print("\nПервые 3 записи:")
        print(df.head(3).to_string())
    
    def save_to_json(self, data: List[Dict], filename: str):
        """Сохранение данных в JSON"""
        if not data:
            print("❌ Нет данных для сохранения")
            return
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON сохранен в {filename}")