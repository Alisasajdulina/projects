import os
import sys
from dotenv import load_dotenv
from weatherapi_collector import WeatherAPIDataCollector
from config import CITIES
from data_saver import DataSaver

def search_single_city(city_name):
    """Поиск погоды для одного города"""
    print(f"🔍 Поиск погоды для: {city_name}")
    
    collector = WeatherAPIDataCollector()
    weather = collector.get_current_weather(city_name)
    
    if weather:
        print(f"\n✅ Погода в {city_name}:")
        print(f"   Температура: {weather.get('temperature_c', 'N/A')}°C")
        print(f"   Ветер: {weather.get('wind_kph', 'N/A')} км/ч")
        print(f"   Влажность: {weather.get('humidity', 'N/A')}%")
        print(f"   Состояние: {weather.get('condition_text', 'N/A')}")
        
        os.makedirs('data/single', exist_ok=True)
        filename = f"data/single/{city_name.lower().replace(' ', '_')}.csv"
        collector.save_to_csv([weather], filename)
        
        return True
    else:
        print(f"❌ Не удалось получить данные для {city_name}")
        return False

def main():
    """Основная функция сбора данных через WeatherAPI"""

    if len(sys.argv) > 1 and sys.argv[1] == 'search':
        if len(sys.argv) > 2:
            city = ' '.join(sys.argv[2:])
            search_single_city(city)
        else:
            print("Использование: python run_api_weatherapi.py search <город>")
        return
    
    load_dotenv()
    
    api_key = os.getenv('WEATHERAPI_API_KEY')
    
    print("=" * 70)
    print("СБОР ДАННЫХ О ПОГОДЕ ЧЕРЕЗ WEATHERAPI.COM")
    print("=" * 70)
    
    if api_key and api_key != 'ваш_api_ключ_здесь':
        print(f"✅ API ключ найден: {api_key[:8]}...{api_key[-4:]}")
    else:
        print("⚠️  API ключ не найден, используем демо-режим")
        print("   Получите ключ на: https://www.weatherapi.com/")
        print("   Добавьте в .env: WEATHERAPI_API_KEY=ваш_ключ")
    
    if len(sys.argv) > 1:
        try:
            if sys.argv[1].lower() == 'all':
                num_cities = len(CITIES)
                print(f"📊 Собираем ВСЕ города из списка: {num_cities} городов")
            else:
                num_cities = int(sys.argv[1])
                print(f"📊 Собираем {num_cities} городов")
        except:
            num_cities = 10  
            print(f"📊 Собираем {num_cities} городов (по умолчанию)")
    else:
        num_cities = len(CITIES) 
        print(f"📊 Собираем ВСЕ города: {num_cities} городов")
    
    cities_to_collect = CITIES[:num_cities]
    
    if 'Orenburg' not in cities_to_collect:
        print("➕ Добавляем Оренбург в список")
        cities_to_collect.append('Orenburg')
    
    print("\n📋 СПИСОК ГОРОДОВ:")
    print("-" * 40)
    for i, city in enumerate(cities_to_collect, 1):
        print(f"  {i:2d}. {city}")
    print("-" * 40)
    
    collector = WeatherAPIDataCollector()
    
    weather_data = collector.collect_multiple_cities(cities_to_collect)
    
    if weather_data:
        os.makedirs('data', exist_ok=True)
        collector.save_to_csv(
            weather_data,
            'data/weatherapi_weather.csv'
        )
        
        collector.save_to_json(
            weather_data,
            'data/weatherapi_weather.json'
        )
        
        print(f"\n{'='*70}")
        print("✅ СБОР ДАННЫХ УСПЕШНО ЗАВЕРШЕН!")
        print(f"{'='*70}")
        
        DataSaver.print_data_summary(weather_data, "данных о погоде")
        
        temperatures = [d.get('temperature_c') for d in weather_data if d.get('temperature_c') is not None]
        if temperatures:
            print(f"\n📈 СТАТИСТИКА ПО ТЕМПЕРАТУРАМ:")
            print(f"   Средняя: {sum(temperatures)/len(temperatures):.1f}°C")
            print(f"   Минимальная: {min(temperatures)}°C")
            print(f"   Максимальная: {max(temperatures)}°C")
            print(f"   Разница: {max(temperatures) - min(temperatures):.1f}°C")
        
    else:
        print("❌ Не удалось собрать данные")

if __name__ == "__main__":
    main()