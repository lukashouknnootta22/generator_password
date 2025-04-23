from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

# Загрузка глобальных переменных
load_dotenv()
DB_TYPE = os.getenv('DB_TYPE')
DB_NAME= os.getenv('DB_NAME')
DB_USER= os.getenv('DB_USER')
DB_PASSWORD= os.getenv('DB_PASSWORD')
DB_HOST= os.getenv('DB_HOST')

def create_engine_url() -> str:
	"""
	Создание URL-аддреса для sqlalchemy
	:return: URL-аддрес sqlalchemy 
	"""
	try:
		if DB_TYPE == 'mysql':
			engine_url = f'mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
		elif DB_TYPE == 'postgresql':
			engine_url = f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
		else:
			raise ValueError('Непподерживаемый тип базы данных')
	except ValueError as e:
		print(f'Error: {e.text}')
	else:
		return engine_url


# Создание движка и сессии SQLAlchemy
engine = create_engine(create_engine_url())

local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()