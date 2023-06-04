from datetime import datetime

from sqlalchemy import Column, DateTime, Float, Integer, MetaData, String
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base()


class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    city = Column(String)
    temperature = Column(Float)
    humidity = Column(Float)
    wind_speed = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
