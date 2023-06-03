from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    API_KEY: str

    class Config:
        env_file = BASE_DIR / '.env'


settings = Settings()

ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather/'
RETRY_TIME = 3600

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

CITIES_FILE = BASE_DIR / 'data/cities_test.txt'  # FIXME
