# weather-collector
# Сборщик погоды

Приложение для сборки данных о погоде из 50 крупнейших городов мира.
Данное приложение собирает погоду из открытого API [openweathermap].

Технологии:
- [Python 3.10]
- [SQLAlchemy]
- [alembic]
- [pydantic]
- [requests]

C помощью библиотеки requests и api_key полученного у [openweathermap] происходит сбор данных по 50 городам указанных в переменной cities. данные проходят валидацию через pydantic и отправляются в базу данных postgresql через ORM SQLAlchemy. SQLAlchemy используется в связке с  alembiс для удобства отслеживания и создания миграци при расширении или изменении проекта.

Для запуска проекта клонируйте репозиторий
```
git clon git@github.com:Annsjaw/weather-collector.git
```
Перейдите в директорию weather_collector_infra
```
cd weather_collector_infra
```
Заполните файл .env своими секретами (или воспользуйтесь моими)
```
# Секретный ключ для доступа к сервису openweathermap (получит можно в личном кабинете)
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

После развертывания проекта приложение сразу начнет работать и будет собирать информацию о погоде каждые 60 минут.


[//]: #

   [SQLAlchemy]: <https://pypi.org/project/SQLAlchemy/>
   [alembic]: <https://pypi.org/project/alembic/>
   [pydantic]: <https://pypi.org/project/pydantic/>
   [requests]: <https://pypi.org/project/requests/>
   [Python 3.10]: <https://www.python.org/downloads/release/python-3100/>
   [openweathermap]: <https://openweathermap.org>
