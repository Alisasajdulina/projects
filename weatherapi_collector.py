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
                'region': location.get('region', ''),
                'latitude': location.get('lat', None),
                'longitude': location.get('lon', None),
                'local_time': location.get('localtime', ''),
                
                'temperature_c': current.get('temp_c', None),
                'feelslike_c': current.get('feelslike_c', None),
                'temperature_f': current.get('temp_f', None),
                'feelslike_f': current.get('feelslike_f', None),
                
                'humidity': current.get('humidity', None),
                'pressure_mb': current.get('pressure_mb', None),
                'pressure_in': current.get('pressure_in', None),
                
                'wind_kph': current.get('wind_kph', None),
                'wind_mph': current.get('wind_mph', None),
                'wind_dir': current.get('wind_dir', ''),
                'wind_degree': current.get('wind_degree', None),
                'gust_kph': current.get('gust_kph', None),
                'gust_mph': current.get('gust_mph', None),
                
                'cloud': current.get('cloud', None),
                'visibility_km': current.get('vis_km', None),
                'visibility_miles': current.get('vis_miles', None),
                
                'condition_text': condition.get('text', ''),
                'condition_icon': condition.get('icon', ''),
                'condition_code': condition.get('code', None),
                
                'uv_index': current.get('uv', None),
                
                'last_updated': current.get('last_updated', ''),
                'scraped_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            return result
            
        except Exception as e:
            print(f"   ❌ Ошибка парсинга данных погоды: {e}")
            return {}
    
    def get_detailed_weather(self, city: str) -> Dict:
        """
        Получить подробные данные о погоде с красивым выводом
        
        Args:
            city: Название города
            
        Returns:
            Словарь с данными о погоде
        """
        weather_data = self.get_current_weather(city)
        
        if weather_data:
            print(f"\n{'='*60}")
            print(f"🌤️  ДЕТАЛЬНАЯ ПОГОДА ДЛЯ {city.upper()}")
            print(f"{'='*60}")
            
            details = [
                ("🌡️  Температура", f"{weather_data.get('temperature_c', 'N/A')}°C"),
                ("🤔 Ощущается как", f"{weather_data.get('feelslike_c', 'N/A')}°C"),
                ("💨 Ветер", f"{weather_data.get('wind_kph', 'N/A')} км/ч, {weather_data.get('wind_dir', 'N/A')}"),
                ("💧 Влажность", f"{weather_data.get('humidity', 'N/A')}%"),
                ("📊 Давление", f"{weather_data.get('pressure_mb', 'N/A')} гПа"),
                ("☁️  Облачность", f"{weather_data.get('cloud', 'N/A')}%"),
                ("👁️  Видимость", f"{weather_data.get('visibility_km', 'N/A')} км"),
                ("🌈 Состояние", weather_data.get('condition_text', 'N/A'))
            ]
            
            for label, value in details:
                print(f"   {label:15} : {value}")
            
            print(f"{'='*60}")
        
        return weather_data
    
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
    
    def get_forecast(self, city: str, days: int = 3) -> List[Dict]:
        """
        Получение прогноза погоды
        
        Args:
            city: Название города
            days: Количество дней прогноза (макс 3 для бесплатного тарифа)
            
        Returns:
            Список прогнозов по дням
        """
        params = {
            'q': city,
            'days': min(days, 3),  
            'aqi': 'no',
            'alerts': 'no'
        }
        
        data = self.safe_request_with_delay('/forecast.json', params)
        forecasts = []
        
        if data and 'forecast' in data:
            forecast_days = data['forecast'].get('forecastday', [])
            
            for day_data in forecast_days:
                day_info = day_data.get('day', {})
                forecast = {
                    'date': day_data.get('date', ''),
                    'max_temp_c': day_info.get('maxtemp_c', None),
                    'min_temp_c': day_info.get('mintemp_c', None),
                    'avg_temp_c': day_info.get('avgtemp_c', None),
                    'max_wind_kph': day_info.get('maxwind_kph', None),
                    'total_precip_mm': day_info.get('totalprecip_mm', None),
                    'avg_humidity': day_info.get('avghumidity', None),
                    'condition': day_info.get('condition', {}).get('text', ''),
                    'uv_index': day_info.get('uv', None),
                    'sunrise': day_data.get('astro', {}).get('sunrise', ''),
                    'sunset': day_data.get('astro', {}).get('sunset', '')
                }
                forecasts.append(forecast)
        
        return forecasts