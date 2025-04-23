from bcrypt import hashpw, gensalt
from random import choices
from database import Base, local_session, engine
from sqlalchemy.orm import Session
from models import Password
from sqlalchemy.exc import SQLAlchemyError
import logging

# Логирование
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")

Base.metadata.create_all(bind=engine)

def get_session() -> Session:
	"""
	Получение сессии с базой данных
	:return: Сессия БД
	"""
	session = local_session()
	try:
		yield session
	except Exception as e:
		logging.error(f'Error with DB: {e.text}')
		session.rollback()
	else:
		session.commit()
	finally:
		session.close()

SPECIAL_CHARACTERS = '+-/*!&$#?=@<>'
LETTERS = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
NUMBERS = '1234567890'

def gen_pw(length_password: int, symbols: str) -> str:
	"""
	Генерация пароля с выбранными символами
	:param length_password: Длина пароля
	:param symbols: Строка символов для генерации
	:return: Сгенерированный пароль
	"""
	return ''.join(choices(symbols, k=length_password))

def gen_hash_pw(password: str) -> str:
	"""
	Хэширование сгенерированного пароля
	:param password: Оригинальный пароль
	:return: Хешированный пароль
	"""
	return hashpw(password.encode('utf-8'), gensalt(rounds=14)).decode('utf-8')

def save_to_file(password: str, hashed_password: str = None, service_name: str = None):
	"""
	Cохранение пароля в текстовый файл
	:param password: Оригинальный пароль
	:param hashed_password: Хэшированный пароль (опционально)
	:param service_name: Имя сервиса
	"""
	with open('Your_password', mode='a') as file:
		file.write(f'Пароль: {password}')
		if hashed_password is not None:
			file.write(f'\nХэшированный пароль: {hashed_password}')
		if service_name is not None:
			file.write(f'\nИмя сервиса: {service_name}\n')

def save_to_db(password: str, hashed_password: str = None, service_name: str = None):
	"""
	Сохранение пароля в Базу Данных
	:param password: Оригинальный пароль
	:param hashed_password: Хэшированный пароль (опционально)
	:param service_name: Имя сервиса (опционально)
	"""
	try:
		db_pass = Password(password=password, hashed_password=hashed_password, service_name=service_name)
		session = next(get_session())
		session.add(db_pass)
	except SQLAlchemyError as e:
		logging.error(f'Error with save_to_db: {e.text}')

if __name__ == '__main__':

	pos_answer = ('y', 'yes')

	while True:
		try:
			# Запрос длины пароля
			length_password = int(input('Введите желаемую длину пароля: '))
			if length_password <= 0:
				print('Длина пароля не может быть меньше или равна нулю.')
				continue

			# Выбор символов для генерации
			symbols = ''
			print(f'Выбор символов для пароля: (y/n)\n')
			is_special = input('Специальные символы: ')
			is_letters = input('Буквы: ')
			is_numbers = input('Цифры: ')

			if is_special.lower() in pos_answer:
				symbols += SPECIAL_CHARACTERS
			if is_letters.lower() in pos_answer:
				symbols += LETTERS
			if is_numbers.lower() in pos_answer:
				symbols += NUMBERS
			else:
				raise ValueError('Пароль должен содержать одну из предложенных групп символов')

			# Запрос необходимости хеширования
			hashed_password = None
			is_hash_pw = input('Вам нужен хешированный пароль? (y/n) ')

			# Запрос имени сервиса
			service_name = input('Введите название сервиса для сгенерированого пароля:\n(Оставьте поле пустым, если необходимо) ')

			# Запрос на сохранение в файл.
			is_save_file = input('Сохранить пароль в файле? (y/n) ')

			# Запрос на сохранение в базе данных.
			is_save_db = input('Сохранить пароль в базу данных? (y/n) ')

		except ValueError as e:
			print(f"Error: {e.text}")
			continue

		else:
			# Генерация пароля с выбранными значениями
			password = gen_pw(length_password, symbols)

			# Получить хэш, если он был выбран
			if is_hash_pw.lower() in pos_answer:
				hashed_password = gen_hash_pw(password)

			# Вывод результатов
			print(f'\nПароль: {password}\nХэшированный пароль: {hashed_password}')
			
			# Сохранить в базе данных и/или в файле, если один из вариантов был выбран
			if is_save_file.lower() in pos_answer:
				save_to_file(password, hashed_password, service_name)
				print("Успешное сохранение в файл")
			if is_save_db.lower() in pos_answer:
				save_to_db(password, hashed_password, service_name)
				print("Данные успешно записаны в БД")

			# Запрос на продолжение
			again = input("\nХотите создать еще один пароль? (y/n)")
			if again not in pos_answer:
				print("\nСпасибо за использование генератора паролей")
				break
