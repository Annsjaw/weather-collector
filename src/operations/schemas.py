from pydantic import BaseModel, Field


class Wind(BaseModel):
    """
    Валидация данных о ветре
    """
    speed: float


class BasicParameters(BaseModel):
    """
    Валидация базовых погодных данных
    """

    temperature: float = Field(alias='temp')
    humidity: float


class CityWeather(BaseModel):
    """
    Валидация типов данных поля City
    """

    name: str
    basic_parameters: BasicParameters = Field(alias='main')
    wind: Wind
