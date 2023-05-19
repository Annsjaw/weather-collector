import json
import sys
from http import HTTPStatus
import time
import logging
import requests
from operations.models import weather
from operations.schemas import WeatherData
import database
from config import API_KEY, ENDPOINT, cities, RETRY_TIME
import exception

logger = logging.getLogger()


def insert_to_db(weather_data: WeatherData) -> None:
    """
    Запись в базу данных валидированных данных.
    """

    values = {
        'city': weather_data.city,
        'temperature': weather_data.temperature,
        'humidity': weather_data.humidity,
        'wind_speed': weather_data.wind_speed
    }
    insert_stmt = weather.insert().values(**values)
    database.session.execute(insert_stmt)
    logger.info(f'Записал в БД {values}')


def validate_data(city: str, data: json) -> WeatherData:
    """
    Валидация данных с помощью pydantic
    """

    weather_data = WeatherData(
        city=city,
        temperature=data['main']['temp'],
        humidity=data['main']['humidity'],
        wind_speed=data['wind']['speed'],
    )
    logger.info(f'Прошел валидацию {city}')
    return weather_data


def get_api_answer(city: str) -> json:
    """
    Проверяем ответ от запроса на эндпоинт.
    """

    try:
        url = f'{ENDPOINT}?q={city}&appid={API_KEY}'
        logger.info(f'Обращаюсь к эндпоинту {url}')

        api_response = requests.get(url)
        api_status = api_response.status_code
    except Exception as error:
        raise Exception(f'Ошибка получения ответа от эндпоинта {error}')

    if api_status == HTTPStatus.OK:
        return api_response.json()
    elif api_status == HTTPStatus.UNAUTHORIZED:
        message = api_response.json()
        raise exception.UNAUTHORIZED(message)
    else:
        message = api_response.json()
        raise exception.EndpointErrore(message)


def main():
    """
    Сбор данных о температуре, влажности и скорости ветра в городах из
    списка cities. Валидация и загрузка в базу данных.
    """

    for city in cities:
        data = get_api_answer(city)
        logger.info(f'Забрал данные о {city}')
        weather_data = validate_data(city, data)
        insert_to_db(weather_data)
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
            main()
            # Задержка в 1 час
            logger.info('Ушел в ожидание на 60 минут')
            time.sleep(RETRY_TIME)

        except KeyboardInterrupt:
            logger.info('Ой, работа прервана')
            exit()
