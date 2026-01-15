import os
import sys
from dotenv import load_dotenv
from weatherapi_collector import WeatherAPIDataCollector
from config import find_city, CITIES
import json
import pandas as pd

class WeatherCLI:
    """Интерактивная командная строка для поиска погоды"""
    
    def __init__(self):
        load_dotenv()
        self.collector = WeatherAPIDataCollector()
        
    def run(self):
        """Запуск интерактивного режима"""
        
        print("\n" + "="*60)
        print("🌤️  WEATHER DATA COLLECTOR - ИНТЕРАКТИВНЫЙ РЕЖИМ")
        print("="*60)
        
        while True:
            print("\nДоступные команды:")
            print("  1. search <город>   - Найти погоду для города")
            print("  2. list             - Показать все города")
            print("  3. forecast <город> - Прогноз на 3 дня")
            print("  4. save <город>     - Сохранить данные")
            print("  5. exit             - Выход")
            print("  6. help             - Помощь")
            
            command = input("\n👉 Введите команду: ").strip().lower()
            
            if command.startswith('search '):
                city = command[7:].strip()
                if city:
                    self.search_weather(city)
                else:
                    print("❌ Укажите название города")
            
            elif command == 'list':
                self.list_cities()
            
            elif command.startswith('forecast '):
                city = command[9:].strip()
                if city:
                    self.get_forecast(city)
                else:
                    print("❌ Укажите название города")
            
            elif command.startswith('save '):
                city = command[5:].strip()
                if city:
                    self.save_weather(city)
                else:
                    print("❌ Укажите название города")
            
            elif command == 'exit':
                print("👋 До свидания!")
                break
            
            elif command == 'help':
                self.show_help()
            
            else:
                print("❌ Неизвестная команда. Введите 'help' для помощи.")
    
    def search_weather(self, city):
        """Поиск погоды для города"""
        print(f"\n🔍 Поиск погоды для: {city}")
        
        # Сначала ищем в базе
        found_cities = find_city(city)
        if found_cities:
            if len(found_cities) == 1:
                city = found_cities[0]
            else:
                print(f"\nНайдено несколько городов:")
                for i, c in enumerate(found_cities, 1):
                    print(f"  {i}. {c}")
                try:
                    choice = int(input("\nВыберите номер: "))
                    city = found_cities[choice - 1]
                except:
                    print("❌ Неверный выбор")
                    return
        
        weather = self.collector.get_current_weather(city)
        
        if weather:
            self.display_weather(weather)
        else:
            print(f"❌ Не удалось найти погоду для '{city}'")
    
    def display_weather(self, weather_data):
        """Отобразить данные о погоде"""
        city = weather_data.get('city_name', weather_data.get('city', 'Неизвестно'))
        
        print(f"\n✅ Погода в {city}:")
        print(f"   🌡️  Температура: {weather_data.get('temperature_c', 'N/A')}°C")
        print(f"   🤔 Ощущается как: {weather_data.get('feelslike_c', 'N/A')}°C")
        print(f"   💨 Ветер: {weather_data.get('wind_kph', 'N/A')} км/ч, {weather_data.get('wind_dir', 'N/A')}")
        print(f"   💧 Влажность: {weather_data.get('humidity', 'N/A')}%")
        print(f"   📊 Давление: {weather_data.get('pressure_mb', 'N/A')} гПа")
        print(f"   ☁️  Облачность: {weather_data.get('cloud', 'N/A')}%")
        print(f"   👁️  Видимость: {weather_data.get('visibility_km', 'N/A')} км")
        print(f"   🌈 Состояние: {weather_data.get('condition_text', 'N/A')}")
    
    def list_cities(self):
        """Показать список городов"""
        print(f"\n📋 Всего городов в базе: {len(CITIES)}")
        
        # Разбиваем на страницы
        page_size = 20
        total_pages = (len(CITIES) + page_size - 1) // page_size
        
        page = 1
        while True:
            start_idx = (page - 1) * page_size
            end_idx = min(start_idx + page_size, len(CITIES))
            
            print(f"\n📄 Страница {page}/{total_pages}:")
            print("-" * 40)
            
            for i in range(start_idx, end_idx):
                print(f"  {i+1:3d}. {CITIES[i]}")
            
            print("-" * 40)
            
            if page < total_pages:
                command = input("\n↵ Enter - следующая, q - выход: ").strip().lower()
                if command == 'q':
                    break
                page += 1
            else:
                input("\n↵ Конец списка. Нажмите Enter...")
                break
    
    def get_forecast(self, city):
        """Получить прогноз погоды"""
        print(f"\n📅 Прогноз погды для: {city}")
        
        forecast = self.collector.get_forecast(city, days=3)
        
        if forecast:
            for day in forecast:
                print(f"\n  {day['date']}:")
                print(f"    Температура: ↑{day['max_temp_c']}°C / ↓{day['min_temp_c']}°C")
                print(f"    Погода: {day['condition']}")
                print(f"    Осадки: {day['total_precip_mm']} mm")
                print(f"    Влажность: {day['avg_humidity']}%")
                print(f"    Ветер: {day['max_wind_kph']} км/ч")
        else:
            print(f"❌ Не удалось получить прогноз для '{city}'")
    
    def save_weather(self, city):
        """Сохранить данные о погоде"""
        weather = self.collector.get_current_weather(city)
        
        if weather:
            # Создаем папку если нет
            os.makedirs('data/saved', exist_ok=True)
            
            # Генерируем имя файла
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"data/saved/{city.lower().replace(' ', '_')}_{timestamp}"
            
            # Сохраняем в CSV
            df = pd.DataFrame([weather])
            df.to_csv(f"{filename}.csv", index=False, encoding='utf-8-sig')
            
            # Сохраняем в JSON
            with open(f"{filename}.json", 'w', encoding='utf-8') as f:
                json.dump(weather, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Данные сохранены в {filename}.csv и {filename}.json")
        else:
            print(f"❌ Не удалось получить данные для '{city}'")
    
    def show_help(self):
        """Показать справку"""
        print("\n📖 СПРАВКА ПО КОМАНДАМ:")
        print("  search <город>   - Найти погоду для указанного города")
        print("  list             - Показать список всех доступных городов")
        print("  forecast <город> - Показать прогноз на 3 дня для города")
        print("  save <город>     - Сохранить данные о погоде в файл")
        print("  exit             - Выйти из программы")
        print("  help             - Показать эту справку")
        
        print("\n💡 Примеры использования:")
        print("  search Moscow")
        print("  search Москва")
        print("  forecast London")
        print("  save Paris")

def main():
    """Главная функция"""
    cli = WeatherCLI()
    cli.run()

if __name__ == "__main__":
    main()