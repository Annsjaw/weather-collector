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


class CityData:

    def __init__(self, city: str):
        self.city = city

    def get_api_response(self) -> dict:
        url = self._get_url()

        try:
            logger.info(f'Обращаюсь к эндпоинту {url}')
            api_response = requests.get(url)
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

    def _get_url(self) -> str:
        return f'{ENDPOINT}?q={self.city}&appid={settings.API_KEY}'

    def get_data(self) -> CityWeather:
        response = self.get_api_response()
        validate_data = self.validate(response)
        logger.info('Данные прошли валидацию')
        return validate_data

    @staticmethod
    def validate(api_response) -> CityWeather:
        try:
            logger.info('Отправил данные на валидацию')
            return CityWeather(**api_response)
        except ValidationError as error:
            logger.error(f"Ошибка валидации данных: {error.json()}")
            raise error


class Collector:

    def __init__(self):
        self.weather_data_list = []

    def collect_weather_data(self) -> None:
        for city in self.get_cities():
            citydata = CityData(city)
            self.weather_data_list.append(
                self.reformat_data(citydata.get_data()))
            logger.info(f'Добавил данные о городе {city} в список')
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

    @staticmethod
    def reformat_data(validate_data: CityWeather) -> dict:
        data = {
            'city': validate_data.name,
            'temperature': validate_data.basic_parameters.temperature,
            'humidity': validate_data.basic_parameters.humidity,
            'wind_speed': validate_data.wind.speed
        }
        logger.info('Преобразовал данные для вставки в БД')
        return data


def main():
    collector = Collector()
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
