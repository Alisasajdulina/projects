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
    
    # Международные города
    'London', 'New York', 'Tokyo', 'Berlin',
    'Paris', 'Rome', 'Madrid', 'Beijing',
    'Istanbul', 'Sydney', 'Dubai', 'Singapore',
    'Seoul', 'Toronto', 'Mumbai', 'Cairo'
]

# Дополнительные настройки
MAX_CITIES_TO_COLLECT = 15  # Сколько городов собирать за один запуск
RUSSIAN_CITIES_ONLY = False  # Только российские города

# Можно создать отдельные списки
RUSSIAN_CITIES = [
    'Moscow', 'Saint Petersburg', 'Novosibirsk',
    'Yekaterinburg', 'Kazan', 'Nizhny Novgorod',
    'Chelyabinsk', 'Samara', 'Omsk', 'Rostov-on-Don',
    'Ufa', 'Krasnoyarsk', 'Voronezh', 'Perm',
    'Volgograd', 'Krasnodar', 'Saratov', 'Tyumen',
    'Izhevsk', 'Barnaul', 'Vladivostok', 'Irkutsk',
    'Khabarovsk', 'Orenburg', 'Novokuznetsk',
    'Tolyatti', 'Kemerovo', 'Astrakhan', 'Tula',
    'Sochi', 'Ryazan', 'Penza', 'Lipetsk',
    'Naberezhnye Chelny', 'Kaliningrad', 'Stavropol'
]

EUROPEAN_CITIES = [
    'London', 'Berlin', 'Paris', 'Rome',
    'Madrid', 'Vienna', 'Prague', 'Warsaw',
    'Budapest', 'Athens', 'Lisbon', 'Stockholm',
    'Oslo', 'Copenhagen', 'Helsinki', 'Dublin'
]

ASIAN_CITIES = [
    'Tokyo', 'Beijing', 'Seoul', 'Singapore',
    'Bangkok', 'Hong Kong', 'Taipei', 'Manila',
    'Jakarta', 'Kuala Lumpur', 'Hanoi', 'Mumbai',
    'Delhi', 'Bangalore', 'Karachi', 'Dhaka'
]

# Функция для получения списка городов
def get_cities_list(region='all', limit=10):
    """
    Получить список городов по региону
    
    Args:
        region: 'all', 'russia', 'europe', 'asia'
        limit: максимальное количество городов
    
    Returns:
        Список городов
    """
    if region == 'russia':
        return RUSSIAN_CITIES[:limit]
    elif region == 'europe':
        return EUROPEAN_CITIES[:limit]
    elif region == 'asia':
        return ASIAN_CITIES[:limit]
    else:  # all
        return CITIES[:limit]