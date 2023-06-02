import os

from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

API_KEY = os.environ.get('API_KEY')

ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather/'
RETRY_TIME = 3600

CITIES_FILE = BASE_DIR / 'data/cities.txt'

# class Settings(BaseSettings):
#     db_host: str
#     db_port: str
#     db_name: str
#     db_user: str
#     db_pass: str
#     api_key: str
