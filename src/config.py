from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

API_KEY = os.environ.get('API_KEY')

ENDPOINT = 'https://api.openweathermap.org/data/2.5/weather/'

cities = [
    'Tokyo',
    'Delhi',
    'Shanghai',
    'Sao Paulo',
    'Mumbai',
    'Beijing',
    'Cairo',
    'Dhaka',
    'Mexico City',
    'Osaka',
    'Karachi',
    'Chongqing',
    'Istanbul',
    'Buenos Aires',
    'Kolkata',
    'Lagos',
    'Kinshasa',
    'Manila',
    'Rio de Janeiro',
    'Guangzhou',
    'Lahore',
    'Shenzhen',
    'Bangalore',
    'Moscow',
    'Tianjin',
    'Jakarta',
    'London',
    'Lima',
    'Bangkok',
    'New York',
    'Chennai',
    'Bogota',
    'Ho Chi Minh',
    'Hyderabad',
    'Lima',
    'Hong Kong',
    'Hangzhou',
    'Rio de Janeiro',
    'Ahmedabad',
    'Kuala Lumpur',
    'Paris',
    'Shijiazhuang',
    'Changsha',
    'Bengaluru',
    'Chicago',
    'Chengdu',
    'Wuhan',
    'Nanjing',
    'Taipei',
    'Los Angeles',
    'Miami'
]
