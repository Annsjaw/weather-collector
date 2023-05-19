import sys
import time
import logging
import requests
from operations.models import weather
from operations.schemas import WeatherData
import database
from config import API_KEY, ENDPOINT, cities, RETRY_TIME

logger = logging.getLogger()


def collect_weather_data():
    """
    Сбор данных о температуре, влажности и скорости ветра в городах из
    списка cities. Валидация и загрузка в базу данных.
    """

    for city in cities:
        url = f'{ENDPOINT}?q={city}&appid={API_KEY}'
        response = requests.get(url)
        data = response.json()
        logger.info(f'Забрал данные о {city}')

        weather_data = WeatherData(
            city=city,
            temperature=data['main']['temp'],
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed'],
        )
        logger.info(f'Прошел валидацию {city}')

        values = {
            'city': weather_data.city,
            'temperature': weather_data.temperature,
            'humidity': weather_data.humidity,
            'wind_speed': weather_data.wind_speed
        }
        insert_stmt = weather.insert().values(**values)
        database.session.execute(insert_stmt)
        logger.info(f'Записал в БД {values}')
    database.session.commit()


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(message)s - %(funcName)s - '
        'строка %(lineno)d'
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    while True:
        try:
            collect_weather_data()
            # Задержка в 1 час
            logger.info('Ушел в ожидание на 60 минут')
            time.sleep(RETRY_TIME)

        except KeyboardInterrupt:
            logger.info('Ой, работа прервана')
            exit()
