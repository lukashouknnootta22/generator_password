from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from contextlib import contextmanager
from decouple import config
import logging

# Настройка логирования.
logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	)

logger = logging.getLogger(__name__)

def create_engine_url() -> str:
	"""
	Создание URL-аддреса для engine-sqlalchemy.
	:return: URL-аддрес sqlalchemy.
	"""
	try:
		db_type = config('DB_TYPE')
		if db_type == 'mysql':
			engine_url = f'mysql+mysqlconnector://{config("DB_USER")}:{config("DB_PASSWORD")}@{config("DB_HOST")}/{config("DB_NAME")}'
		elif db_type == 'postgresql':
			engine_url = f'postgresql+psycopg2://{config("DB_USER")}:{config("DB_PASSWORD")}@{config("DB_HOST")}/{config("DB_NAME")}'
		else:
			raise ValueError('Непподерживаемый тип базы данных')
		logger.info(f'Успешное подключение к базе данных - {db_type}')
		return engine_url
	except ValueError as e:
		logger.error(f'Ошибка: {e}')

@contextmanager
def get_session(sessionmake) -> Session:
	"""
	Получение сессии с базой данных.
	:param sessionmake: Класс для создания сессии с БД.
	:return: Сессия БД.
	"""
	session = sessionmake()
	try:
		yield session
	except Exception as e:
		logger.error(f'Ошибка при получении сессии с БД: {e}')
		session.rollback()
	else:
		session.commit()
	finally:
		session.close()

# Создание движка и сессии SQLAlchemy
engine = create_engine(create_engine_url())

sessionmake = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

if __name__ == '__main__':
	with get_session(sessionmake=sessionmake) as session:
		logger.info('База данных работает')
