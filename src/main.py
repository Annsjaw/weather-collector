import datetime
import json
from http import HTTPStatus

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from pydantic import ValidationError

import exception
from config import CITIES_FILE, ENDPOINT, RETRY_TIME, settings
from database import Session
from logger import logger
from operations.models import weather
from operations.schemas import CityWeather


class WeatherData:

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
        self.url = f'{ENDPOINT}?q={city}&appid={settings.API_KEY}'
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


class WeatherCollector:

    def __init__(self):
        self.weather_data_list = []

    def collect_weather_data(self) -> None:
        for city in self.get_cities():
            api_weather = WeatherApi(city)
            weather_data = WeatherData(api_weather.api_response)
            self.get_weather_data(weather_data)
        self.insert_to_db()

    @staticmethod
    def get_cities() -> list:
        with CITIES_FILE.open() as file:
            return [city.strip() for city in file.readlines()]

    def insert_to_db(self) -> None:
        with Session() as session:
            logger.info('Открыл сессию для работы с БД')
            for data in self.weather_data_list:
                session.execute(weather.insert().values(**data))
            logger.info('Удачно записал данные о '
                        f'{len(self.weather_data_list)} городах в базу')
            session.commit()

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
    collector = WeatherCollector()
    collector.collect_weather_data()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(func=main,
                      trigger='interval',
                      seconds=RETRY_TIME,
                      next_run_time=datetime.datetime.now()
                      )
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info('Ой, работа прервана')
        exit()
