# Список городов для сбора данных
CITIES = [
    # Российские города
    'Moscow', 'Saint Petersburg', 'Novosibirsk',
    'Yekaterinburg', 'Kazan', 'Nizhny Novgorod',
    'Chelyabinsk', 'Samara', 'Omsk', 'Rostov-on-Don',
    'Ufa', 'Krasnoyarsk', 'Voronezh', 'Perm',
    'Volgograd', 'Krasnodar', 'Saratov', 'Tyumen',
    'Izhevsk', 'Barnaul', 'Vladivostok', 'Irkutsk',
    'Khabarovsk', 'Orenburg', 'Novokuznetsk', 
    'Tolyatti', 'Kemerovo', 'Astrakhan', 'Tula',
    'Sochi', 'Ryazan', 'Penza', 'Lipetsk',
    'Naberezhnye Chelny', 'Kaliningrad', 'Stavropol',
    
    # Международные города
    'London', 'New York', 'Tokyo', 'Berlin',
    'Paris', 'Rome', 'Madrid', 'Beijing',
    'Istanbul', 'Sydney', 'Dubai', 'Singapore',
    'Seoul', 'Toronto', 'Mumbai', 'Cairo',
    'Bangkok', 'Hong Kong', 'Vienna', 'Prague',
    'Warsaw', 'Budapest', 'Athens', 'Lisbon',
    'Stockholm', 'Oslo', 'Copenhagen', 'Helsinki'
]

# Города с русскими названиями для поиска
CITIES_RU = {
    'Москва': 'Moscow',
    'Санкт-Петербург': 'Saint Petersburg',
    'Новосибирск': 'Novosibirsk',
    'Екатеринбург': 'Yekaterinburg',
    'Казань': 'Kazan',
    'Нижний Новгород': 'Nizhny Novgorod',
    'Челябинск': 'Chelyabinsk',
    'Самара': 'Samara',
    'Омск': 'Omsk',
    'Ростов-на-Дону': 'Rostov-on-Don',
    'Уфа': 'Ufa',
    'Красноярск': 'Krasnoyarsk',
    'Воронеж': 'Voronezh',
    'Пермь': 'Perm',
    'Волгоград': 'Volgograd',
    'Краснодар': 'Krasnodar',
    'Саратов': 'Saratov',
    'Тюмень': 'Tyumen',
    'Ижевск': 'Izhevsk',
    'Барнаул': 'Barnaul',
    'Владивосток': 'Vladivostok',
    'Иркутск': 'Irkutsk',
    'Хабаровск': 'Khabarovsk',
    'Оренбург': 'Orenburg',
    'Новокузнецк': 'Novokuznetsk',
    'Тольятти': 'Tolyatti',
    'Кемерово': 'Kemerovo',
    'Астрахань': 'Astrakhan',
    'Тула': 'Tula',
    'Сочи': 'Sochi',
    'Рязань': 'Ryazan',
    'Пенза': 'Penza',
    'Липецк': 'Lipetsk',
    'Набережные Челны': 'Naberezhnye Chelny',
    'Калининград': 'Kaliningrad',
    'Ставрополь': 'Stavropol',
    'Лондон': 'London',
    'Нью-Йорк': 'New York',
    'Токио': 'Tokyo',
    'Берлин': 'Berlin',
    'Париж': 'Paris',
    'Рим': 'Rome',
    'Мадрид': 'Madrid',
    'Пекин': 'Beijing',
    'Стамбул': 'Istanbul',
    'Сидней': 'Sydney',
    'Дубай': 'Dubai',
    'Сингапур': 'Singapore',
    'Сеул': 'Seoul',
    'Торонто': 'Toronto',
    'Мумбаи': 'Mumbai',
    'Каир': 'Cairo'
}

def find_city(search_term):
    """
    Найти город по названию (частичному совпадению)
    
    Args:
        search_term: название города или его часть
        
    Returns:
        Список найденных городов
    """
    search_term = search_term.lower().strip()
    results = []
    
    # Ищем в английских названиях
    for city in CITIES:
        if search_term in city.lower():
            results.append(city)
    
    # Ищем в русских названиях
    for ru_name, en_name in CITIES_RU.items():
        if search_term in ru_name.lower():
            if en_name not in results:
                results.append(en_name)
    
    return results

def get_city_info(city_name):
    """
    Получить информацию о городе
    
    Args:
        city_name: название города
        
    Returns:
        Словарь с информацией о городе
    """
    # Проверяем, есть ли город в списке
    if city_name in CITIES:
        return {
            'name': city_name,
            'in_list': True,
            'russian_name': get_russian_name(city_name)
        }
    else:
        # Город не в списке, но может существовать
        return {
            'name': city_name,
            'in_list': False,
            'russian_name': None
        }

def get_russian_name(english_name):
    """
    Получить русское название города
    
    Args:
        english_name: английское название
        
    Returns:
        Русское название или None
    """
    for ru_name, en_name in CITIES_RU.items():
        if en_name == english_name:
            return ru_name
    return None

def get_english_name(russian_name):
    """
    Получить английское название города
    
    Args:
        russian_name: русское название
        
    Returns:
        Английское название или None
    """
    return CITIES_RU.get(russian_name)