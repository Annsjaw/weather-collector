# Сборщик погоды 🌤

Приложение для сборки данных о погоде из 50 крупнейших городов мира.

Данное приложение собирает погоду из открытого API [openweathermap] и 
сохраняет ее в базу данных.

Технологии:
- [Python 3.10]
- [PostgreSQL 13.3]
- [SQLAlchemy]
- [alembic]
- [pydantic]
- [requests]

C помощью библиотеки requests и api_key полученного в личном кабинете 
[openweathermap] происходит сбор данных по 50 городам указанных в файле 
cities.txt. Данные проходят валидацию через pydantic и отправляются в базу 
данных postgresql через ORM SQLAlchemy. SQLAlchemy используется в связке с 
alembic для удобства отслеживания и создания миграций при расширении или 
изменении проекта.

На данный момент программа собирает только базовые метрики: 

- город
- температура
- влажность
- скорость ветра
- время обращения

При необходимости можно расширить сбор информации опираясь на данные, 
которые предоставляет сервис. 

Пример ответа для города New York вы можете увидеть ниже. 
```json
{
   "coord": {
      "lon": -74.006,
      "lat": 40.7143
   },
   "weather": [
      {
         "id": 701,
         "main": "Mist",
         "description": "mist",
         "icon": "50n"
      }
   ],
   "base": "stations",
   "main": {
      "temp": 295.08,
      "feels_like": 294.97,
      "temp_min": 292.56,
      "temp_max": 297.53,
      "pressure": 1012,
      "humidity": 63
   },
   "visibility": 10000,
   "wind": {
      "speed": 2.24,
      "deg": 181,
      "gust": 3.13
   },
   "clouds": {
      "all": 0
   },
   "dt": 1685755381,
   "sys": {
      "type": 2,
      "id": 2008101,
      "country": "US",
      "sunrise": 1685698017,
      "sunset": 1685751681
   },
   "timezone": -14400,
   "id": 5128581,
   "name": "New York",
   "cod": 200
}
```
___
## Запуск проекта
Клонируйте репозиторий
```
git clon git@github.com:Annsjaw/weather-collector.git
```
Перейдите в директорию weather_collector_infra
```
cd weather_collector_infra
```
Заполните файл **.env** своими секретами (или воспользуйтесь моими)
```python
# Секретный ключ для доступа к сервису openweathermap (получить можно в личном кабинете)
API_KEY = a2857b9b09c3fd61976e5a31c24fe180

# Данные для создания базы данных
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Данные для подключения к базе данных
DB_HOST=db
DB_PORT=5432
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
```
Выполните команду для развертывания Docker - контейнеров
```
docker-compose up -d --build
```

После развертывания проекта приложение сразу начнет работать и будет собирать 
информацию о погоде каждые 60 минут.
___
⚠️ **ВАЖНО!**

При использовании токена полученного бесплатно есть ограничение, **60** 
обращений в минуту. Для увеличения количества запросов необходимо разбить 
обращения по таймеру или приобрести одну из платных подписок.


[//]: #

   [SQLAlchemy]: <https://pypi.org/project/SQLAlchemy/>
   [PostgreSQL 13.3]: <https://www.postgresql.org/docs/13/release-13-3.html>
   [alembic]: <https://pypi.org/project/alembic/>
   [pydantic]: <https://pypi.org/project/pydantic/>
   [requests]: <https://pypi.org/project/requests/>
   [Python 3.10]: <https://www.python.org/downloads/release/python-3100/>
   [openweathermap]: <https://openweathermap.org>
