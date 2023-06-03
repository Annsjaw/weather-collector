from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from config import settings

# from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DB_URL = f'postgresql://{settings.DB_USER}:{settings.DB_PASS}@' \
         f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'


metadata = MetaData()

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
