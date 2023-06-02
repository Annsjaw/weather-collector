import json
import logging
import sys
from dataclasses import dataclass
from http import HTTPStatus

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from pydantic import ValidationError

import exception
from config import API_KEY, CITIES_FILE, ENDPOINT, RETRY_TIME
from database import Session
from operations.models import weather
from operations.schemas import CityWeather

logger = logging.getLogger()


@dataclass
class WeatherData:
    validate_data: CityWeather

    def __init__(self, api_response: json):
        self.validate(api_response)
        self.city = self.validate_data.name
        self.temperature = self.validate_data.basic_parameters.temperature
        self.humidity = self.validate_data.basic_parameters.humidity
        self.wind_speed = self.validate_data.wind.speed

    def validate(self, api_response):
        try:
            self.validate_data = CityWeather(**api_response)
            logger.info('Валидация прошла успешно')
        except ValidationError as e:
            logger.error(f"Ошибка валидации данных: {e.json()}")


class WeatherApi:
    def __init__(self, city: str):
        self.city = city
        self.url = f'{ENDPOINT}?q={city}&appid={API_KEY}'
        self.api_response = self.get_api_response()

    def get_api_response(self) -> json:
        try:
            logger.info(f'Обращаюсь к эндпоинту {self.url}')
            api_response = requests.get(self.url)
        except Exception as error:
            raise Exception(f'Ошибка получения ответа от эндпоинта {error}')

        if api_response.status_code == HTTPStatus.OK:
            logger.info(f'Забрал данные о городе {self.city}')
            return api_response.json()
        elif api_response.status_code == HTTPStatus.UNAUTHORIZED:
            message = api_response.json()
            raise exception.UNAUTHORIZED(message)
        else:
            message = api_response.json()
            raise exception.EndpointError(message)


@dataclass
class WeatherCollector:
    weather_data_list: list

    def __init__(self):
        self.weather_data_list = []
        self.collect_weather_data()

    def collect_weather_data(self) -> None:
        for city in self.get_cities():
            api_weather = WeatherApi(city)
            weather_data = WeatherData(api_weather.api_response)
            self.get_weather_data(weather_data)
        self.insert_to_db()

    @staticmethod
    def get_cities():
        with CITIES_FILE.open() as file:
            return [city.strip() for city in file.readlines()]

    def insert_to_db(self) -> None:
        session = Session()
        logger.info('Открыл сессию для работы с БД')
        for data in self.weather_data_list:
            session.execute(weather.insert().values(**data))
        logger.info(f'Удачно записал данные о {len(self.weather_data_list)} '
                    'городах в базу')
        session.commit()
        session.close()

    def get_weather_data(self, weather_data: WeatherData) -> None:
        data = {
            'city': weather_data.city,
            'temperature': weather_data.temperature,
            'humidity': weather_data.humidity,
            'wind_speed': weather_data.wind_speed
        }
        self.weather_data_list.append(data)
        logger.info(f'Добавил данные о городе {weather_data.city} в список')


def main():
    WeatherCollector()


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - [%(levelname)s] - %(message)s - %(funcName)s - '
        'строка %(lineno)d'
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    scheduler = BlockingScheduler()
    scheduler.add_job(func=main, trigger='interval', seconds=RETRY_TIME)
    try:
        main()
        scheduler.start()
    except KeyboardInterrupt:
        logger.info('Ой, работа прервана')
        exit()
