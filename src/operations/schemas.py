from pydantic import BaseModel


class WeatherData(BaseModel):
    """
    Валидация типов данных поля WeatherData
    """
    city: str
    temperature: float
    humidity: float
    wind_speed: float
