import time
import requests
from operations.models import weather
from operations.schemas import WeatherData
import database
from config import API_KEY, ENDPOINT, cities


def collect_weather_data():

    for city in cities:
        url = f'{ENDPOINT}?q={city}&appid={API_KEY}'
        response = requests.get(url)
        data = response.json()

        weather_data = WeatherData(
            city=city,
            temperature=data['main']['temp'],
            humidity=data['main']['humidity'],
            wind_speed=data['wind']['speed'],
        )

        values = {
            'city': weather_data.city,
            'temperature': weather_data.temperature,
            'humidity': weather_data.humidity,
            'wind_speed': weather_data.wind_speed
        }
        insert_stmt = weather.insert().values(**values)
        database.session.execute(insert_stmt)
    database.session.commit()


while True:
    collect_weather_data()
    # Задержка в 1 час
    time.sleep(3600)
