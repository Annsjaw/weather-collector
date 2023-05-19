from datetime import datetime

from sqlalchemy import (Column, DateTime, Float, Integer, MetaData, String,
                        Table)

metadata = MetaData()

weather = Table(
    'weather',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('city', String),
    Column('temperature', Float),
    Column('humidity', Float),
    Column('wind_speed', Float),
    Column('timestamp', DateTime, default=datetime.utcnow),
)
