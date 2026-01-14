from api_collector import APIDataCollector
from typing import Dict, List
from datetime import datetime
import random

class WeatherAPIDataCollector(APIDataCollector):
    """Сборщик данных о погоде с WeatherAPI.com"""
    
    def __init__(self):
        super().__init__('weatherapi')
    
    def get_current_weather(self, city: str) -> Dict:
        """
        Получение текущей погоды для города
        
        Args:
            city: Название города
            
        Returns:
            Словарь с данными о погоде
        """
        params = {
            'q': city,
            'aqi': 'no'
        }
        
        data = self.safe_request_with_delay('/current.json', params)
        
        if data and 'current' in data:
            return self._parse_weather_data(data, city)
        else:
            print(f"   ❌ Не удалось получить данные для {city}")
            return {}
    
    def _parse_weather_data(self, data: Dict, city: str) -> Dict:
        """Парсинг данных о погоде из ответа WeatherAPI"""
        try:
            location = data.get('location', {})
            current = data.get('current', {})
            condition = current.get('condition', {})
            
            result = {
                'city': city,
                'city_name': location.get('name', city),
                'country': location.get('country', ''),
                'latitude': location.get('lat', None),
                'longitude': location.get('lon', None),
                'local_time': location.get('localtime', ''),
                
                # Температура
                'temperature_c': current.get('temp_c', None),
                'feelslike_c': current.get('feelslike_c', None),
                
                # Атмосферные условия
                'humidity': current.get('humidity', None),
                'pressure_mb': current.get('pressure_mb', None),
                
                # Ветер
                'wind_kph': current.get('wind_kph', None),
                'wind_dir': current.get('wind_dir', ''),
                
                # Облачность
                'cloud': current.get('cloud', None),
                
                # Состояние погоды
                'condition_text': condition.get('text', ''),
                'condition_icon': condition.get('icon', ''),
                
                # Метаданные
                'last_updated': current.get('last_updated', ''),
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result
            
        except Exception as e:
            print(f"   ❌ Ошибка парсинга данных погоды: {e}")
            return {}
    
    def collect_multiple_cities(self, cities: List[str]) -> List[Dict]:
        """
        Сбор погоды для нескольких городов
        
        Args:
            cities: Список названий городов
            
        Returns:
            Список с данными о погоде
        """
        all_weather = []
        
        print(f"📊 Начинаем сбор данных для {len(cities)} городов...")
        
        for i, city in enumerate(cities, 1):
            print(f"\n[{i}/{len(cities)}] Город: {city}")
            
            weather_data = self.get_current_weather(city)
            
            if weather_data:
                all_weather.append(weather_data)
                print(f"   ✅ Данные получены")
                print(f"   🌡  {weather_data.get('temperature_c', 'N/A')}°C, "
                      f"💨 {weather_data.get('wind_kph', 'N/A')} км/ч, "
                      f"💧 {weather_data.get('humidity', 'N/A')}%")
            else:
                # В демо-режиме создаем тестовые данные
                if self.demo_mode:
                    mock_data = self._create_mock_data(city)
                    all_weather.append(mock_data)
                    print(f"   📝 Созданы тестовые данные")
        
        print(f"\n{'='*50}")
        print(f"✅ Собраны данные для {len(all_weather)} из {len(cities)} городов")
        return all_weather
    
    def _create_mock_data(self, city: str) -> Dict:
        """Создание тестовых данных для демо-режима"""
        conditions = [
            "Sunny", "Partly cloudy", "Cloudy", "Overcast", 
            "Light rain", "Moderate rain", "Light snow"
        ]
        
        return {
            'city': city,
            'city_name': city,
            'country': random.choice(['Russia', 'USA', 'UK', 'Japan']),
            'temperature_c': random.randint(-10, 35),
            'feelslike_c': random.randint(-15, 30),
            'humidity': random.randint(30, 95),
            'pressure_mb': random.randint(980, 1030),
            'wind_kph': round(random.uniform(0, 30), 1),
            'wind_dir': random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']),
            'cloud': random.randint(0, 100),
            'condition_text': random.choice(conditions),
            'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'demo_mode': True
        }