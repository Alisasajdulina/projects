import sys
import os
from dotenv import load_dotenv
from weatherapi_collector import WeatherAPIDataCollector

def main():
    """Быстрый поиск погоды для города"""
    
    load_dotenv()
    
    if len(sys.argv) < 2:
        print("🌤️  ПОИСК ПОГОДЫ ДЛЯ ГОРОДА")
        print("=" * 40)
        print("Использование: python search_city.py <название_города>")
        print("\nПримеры:")
        print("  python search_city.py Москва")
        print("  python search_city.py London")
        print("  python search_city.py \"New York\"")
        print("  python search_city.py Оренбург")
        return
    
    city_name = ' '.join(sys.argv[1:])
    
    print(f"🔍 Поиск погоды для: {city_name}")
    
    collector = WeatherAPIDataCollector()
    weather = collector.get_current_weather(city_name)
    
    if weather:
        print(f"\n✅ Погода в {city_name}:")
        print(f"   🌡️  Температура: {weather.get('temperature_c', 'N/A')}°C")
        print(f"   💨 Ветер: {weather.get('wind_kph', 'N/A')} км/ч")
        print(f"   💧 Влажность: {weather.get('humidity', 'N/A')}%")
        print(f"   ☁️  Состояние: {weather.get('condition_text', 'N/A')}")
        
        print(f"\n📊 Дополнительно:")
        print(f"   Ощущается как: {weather.get('feelslike_c', 'N/A')}°C")
        print(f"   Давление: {weather.get('pressure_mb', 'N/A')} гПа")
        print(f"   Облачность: {weather.get('cloud', 'N/A')}%")
        print(f"   Видимость: {weather.get('visibility_km', 'N/A')} км")
        
        save = input(f"\n💾 Сохранить данные? (да/нет): ")
        if save.lower() in ['да', 'yes', 'y', 'д']:
            os.makedirs('data/search_results', exist_ok=True)
            filename = f"data/search_results/{city_name.lower().replace(' ', '_')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Погода в {city_name}:\n")
                f.write(f"Температура: {weather.get('temperature_c', 'N/A')}°C\n")
                f.write(f"Ветер: {weather.get('wind_kph', 'N/A')} км/ч\n")
                f.write(f"Влажность: {weather.get('humidity', 'N/A')}%\n")
                f.write(f"Состояние: {weather.get('condition_text', 'N/A')}\n")
            print(f"✅ Данные сохранены в {filename}")
    else:
        print(f"❌ Не удалось получить данные для {city_name}")
        print("   Попробуйте:")
        print("   1. Проверить название города")
        print("   2. Использовать английское название")
        print("   3. Проверить подключение к интернету")

if __name__ == "__main__":
    main()