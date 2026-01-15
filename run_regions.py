import os
from dotenv import load_dotenv
from weatherapi_collector import WeatherAPIDataCollector
from config import get_cities_list, RUSSIAN_CITIES, EUROPEAN_CITIES, ASIAN_CITIES
from data_saver import DataSaver

def collect_region(region_name, cities, collector):
    """Сбор данных для региона"""
    print(f"\n{'='*60}")
    print(f"🌍 РЕГИОН: {region_name.upper()}")
    print(f"{'='*60}")
    
    weather_data = collector.collect_multiple_cities(cities)
    
    if weather_data:
        filename = f"data/weather_{region_name.lower()}.csv"
        DataSaver.save_to_csv(weather_data, filename)
        
        print(f"\n📊 Статистика для {region_name}:")
        temperatures = [d.get('temperature_c') for d in weather_data if d.get('temperature_c')]
        if temperatures:
            avg_temp = sum(temperatures) / len(temperatures)
            min_temp = min(temperatures)
            max_temp = max(temperatures)
            print(f"   Средняя температура: {avg_temp:.1f}°C")
            print(f"   Минимальная: {min_temp}°C")
            print(f"   Максимальная: {max_temp}°C")
    
    return weather_data

def main():
    """Сбор данных по разным регионам"""
    
    load_dotenv()
    
    api_key = os.getenv('WEATHERAPI_API_KEY')
    if not api_key or api_key == 'ваш_api_ключ_здесь':
        print("⚠️  Используем демо-режим")
    
    collector = WeatherAPIDataCollector()
    
    os.makedirs('data', exist_ok=True)
    all_data = []
    
    russian_cities = RUSSIAN_CITIES[:10]
    if 'Orenburg' not in russian_cities:
        russian_cities.append('Orenburg')
    
    russia_data = collect_region('Россия', russian_cities, collector)
    all_data.extend(russia_data)
    europe_data = collect_region('Европа', EUROPEAN_CITIES[:5], collector)
    all_data.extend(europe_data)
    
    asia_data = collect_region('Азия', ASIAN_CITIES[:5], collector)
    all_data.extend(asia_data)
    
    if all_data:
        DataSaver.save_to_csv(all_data, 'data/weather_all_regions.csv')
        DataSaver.save_to_json(all_data, 'data/weather_all_regions.json')
        
        print(f"\n{'='*60}")
        print("✅ ВСЕ ДАННЫХ СОБРАНЫ!")
        print(f"{'='*60}")
        
        DataSaver.print_data_summary(all_data, "всех данных")

if __name__ == "__main__":
    main()