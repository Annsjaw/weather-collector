FROM python:3.10

RUN mkdir /weather_collector_app

WORKDIR /weather_collector_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN alembic upgrade head

WORKDIR src

CMD python main.py