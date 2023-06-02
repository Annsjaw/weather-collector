from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

DB_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


metadata = MetaData()

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
