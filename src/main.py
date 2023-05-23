import json
import logging
import sys
import time
from http import HTTPStatus

import requests

import database
import exception
from config import API_KEY, ENDPOINT, RETRY_TIME, cities
from operations.models import weather
from operations.schemas import CityWeather
from pydantic import ValidationError

logger = logging.getLogger()


def insert_to_db(city_weather: CityWeather) -> None:
    """
    Запись в базу данных валидированных данных.
    """

    values = {
        'city': city_weather.name,
        'temperature': city_weather.basic_parameters.temperature,
        'humidity': city_weather.basic_parameters.humidity,
        'wind_speed': city_weather.wind.speed
    }
    insert_stmt = weather.insert().values(**values)
    database.session.execute(insert_stmt)
    logger.info(f'Записал в БД {values}')


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
        logger.info(f'Забрал данные о {city}')
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
        api_response = get_api_answer(city)
        try:
            city_weather = CityWeather(**api_response)

        except ValidationError as e:
            logger.error(e.json())

        else:
            insert_to_db(city_weather)
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
            logger.info('Ушел в ожидание на 60 минут')
            time.sleep(RETRY_TIME)

        except KeyboardInterrupt:
            logger.info('Ой, работа прервана')
            exit()
