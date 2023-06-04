import datetime
from http import HTTPStatus

import requests
from apscheduler.schedulers.blocking import BlockingScheduler
from pydantic import ValidationError

import exception
from config import CITIES_FILE, ENDPOINT, RETRY_TIME, settings
from database import Session
from logger import logger
from operations.models import Weather
from operations.schemas import CityWeather


class CityData:
    """
    Получение данных о погоде переданного города.
    После успешного запроса к эндпоинту, полученные данные проходят валидацию
    и возвращаются если все прошло успешно.
    """

    def __init__(self, city: str):
        self.city = city

    def get_api_response(self) -> dict:
        """
        Получение ответа с данными о погоде от эндпоинта.
        """
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
        """
        Формирование эндпоинта.
        """
        return f'{ENDPOINT}?q={self.city}&appid={settings.API_KEY}'

    def get_data(self) -> CityWeather:
        """
        Запускающий метод, получает данные от эндпоинта и возвращает
        валидные данные.
        """
        response = self.get_api_response()
        validate_data = self.validate(response)
        logger.info('Данные прошли валидацию')
        return validate_data

    @staticmethod
    def validate(api_response) -> CityWeather:
        """
        Валидация данных с помощью pydantic
        """
        try:
            logger.info('Отправил данные на валидацию')
            return CityWeather(**api_response)
        except ValidationError as error:
            logger.error(f"Ошибка валидации данных: {error.json()}")
            raise error


class Collector:
    """
    Сборщик данных о погоде в городе.
    """

    def __init__(self):
        self.weather_objects = []

    def collect_weather_data(self) -> None:
        """
        Получение данных о погоде, добавление в один список
        и запись списка данных в БД
        """
        for city in self.get_cities():
            citydata = CityData(city)
            data = self.reformat_data(citydata.get_data())
            self.weather_objects.append(Weather(**data))
            logger.info(f'Добавил данные о городе {city} в список')
        self.insert_to_db()

    @staticmethod
    def get_cities() -> list:
        """
        Получение списка городов из файла.
        """
        with CITIES_FILE.open() as file:
            return [city.strip() for city in file.readlines()]

    def insert_to_db(self) -> None:
        """
        Запись данных о погоде в городах в базу данных.
        """
        with Session() as session:
            logger.info('Открыл сессию для работы с БД')
            session.bulk_save_objects(self.weather_objects)
            logger.info('Удачно записал данные о '
                        f'{len(self.weather_objects)} городах в базу')
            session.commit()

    @staticmethod
    def reformat_data(validate_data: CityWeather) -> dict:
        """
        Преобразование валидных данных в удобный для записи в БД формат.
        """
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
