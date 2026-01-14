import os
import sys
from dotenv import load_dotenv
from weatherapi_collector import WeatherAPIDataCollector
from config import CITIES
from data_saver import DataSaver

def main():
    """Основная функция сбора данных через WeatherAPI"""
    
    # Загружаем переменные окружения
    load_dotenv()
    
    # Проверяем наличие API ключа
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
    
    # Определяем сколько городов собирать
    # Если передали аргумент командной строки
    if len(sys.argv) > 1:
        try:
            if sys.argv[1].lower() == 'all':
                num_cities = len(CITIES)
                print(f"📊 Собираем ВСЕ города из списка: {num_cities} городов")
            else:
                num_cities = int(sys.argv[1])
                print(f"📊 Собираем {num_cities} городов")
        except:
            num_cities = 10  # по умолчанию
            print(f"📊 Собираем {num_cities} городов (по умолчанию)")
    else:
        num_cities = len(CITIES)  # ← ВСЕ города!
        print(f"📊 Собираем ВСЕ города: {num_cities} городов")
    
    # Получаем список городов для сбора
    cities_to_collect = CITIES[:num_cities]
    
    # Проверяем, есть ли Оренбург в списке
    if 'Orenburg' not in cities_to_collect:
        print("➕ Добавляем Оренбург в список")
        cities_to_collect.append('Orenburg')
    
    # Показываем список городов
    print("\n📋 СПИСОК ГОРОДОВ:")
    print("-" * 40)
    for i, city in enumerate(cities_to_collect, 1):
        print(f"  {i:2d}. {city}")
    print("-" * 40)
    
    # Создаем коллектор
    collector = WeatherAPIDataCollector()
    
    # Собираем данные
    weather_data = collector.collect_multiple_cities(cities_to_collect)
    
    if weather_data:
        # Создаем папку data если её нет
        os.makedirs('data', exist_ok=True)
        
        # Сохраняем в CSV
        collector.save_to_csv(
            weather_data,
            'data/weatherapi_weather.csv'
        )
        
        # Сохраняем в JSON
        collector.save_to_json(
            weather_data,
            'data/weatherapi_weather.json'
        )
        
        print(f"\n{'='*70}")
        print("✅ СБОР ДАННЫХ УСПЕШНО ЗАВЕРШЕН!")
        print(f"{'='*70}")
        
        # Показать сводку
        DataSaver.print_data_summary(weather_data, "данных о погоде")
        
        # Показать статистику по температурам
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