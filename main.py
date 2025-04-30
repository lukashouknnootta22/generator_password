from bcrypt import hashpw, gensalt
from random import choices
from database import Base, get_session, engine, sessionmake
from models import Password
from sqlalchemy.exc import SQLAlchemyError
import logging

# Настройка логирования.
logging.basicConfig(
		level=logging.INFO,
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	)

logger = logging.getLogger(__name__)

# Создание БД.
Base.metadata.create_all(bind=engine)

class Generator:
	# Объявление констант.
	SPECIAL_CHARACTERS = '+-/*!&$#?=@<>'
	LETTERS = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
	NUMBERS = '1234567890'

	def __init__(self, symbols: str):
		"""
		Инициализация класса.
		:param symbols: Строка символов для генерации.
		"""
		self.symbols = symbols

	def gen_pw(self, length_password: int) -> str:
		"""
		Генерация пароля с выбранными символами.
		:param length_password: Длина пароля.
		:return: Сгенерированный пароль.
		"""
		return ''.join(choices(self.symbols, k=length_password))

	@staticmethod
	def gen_hash_pw(password: str) -> str:
		"""
		Хэширование сгенерированного пароля.
		:param password: Оригинальный пароль.
		:return: Хешированный пароль.
		"""
		return hashpw(password.encode('utf-8'), gensalt(rounds=14)).decode('utf-8')

	@staticmethod	
	def save_to_file(password: str, hashed_password: str = None, service_name: str = None):
	"""
	Cохранение пароля в текстовый файл.
	:param password: Оригинальный пароль.
	:param hashed_password: Хэшированный пароль (опционально).
	:param service_name: Имя сервиса (опционально).
	"""
	with open('passwords', mode='a') as file:
		file.write(f'Пароль: {password}')
		if hashed_password is not None:
			file.write(f'\nХэшированный пароль: {hashed_password}')
		if service_name is not None:
			file.write(f'\nИмя сервиса: {service_name}\n')

	@staticmethod
	def save_to_db(password: str, hashed_password: str = None, service_name: str = None):
		"""
		Сохранение пароля в Базу Данных.
		:param password: Оригинальный пароль.
		:param hashed_password: Хэшированный пароль (опционально).
		:param service_name: Имя сервиса (опционально).
		"""
		try:
			with get_session(sessionmake) as session:
				db_pass = Password(password=password, hashed_password=hashed_password, service_name=service_name)
				session.add(db_pass)
				logger.info(f'Пароль успешно сохранён в БД')
		except SQLAlchemyError as e:
			logging.error(f'Ошибка с сохранением пароля в БД: {e}')

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
				symbols += Generator.SPECIAL_CHARACTERS
			if is_letters.lower() in pos_answer:
				symbols += Generator.LETTERS
			if is_numbers.lower() in pos_answer:
				symbols += Generator.NUMBERS
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

			generator = Generator(symbols=symbols)

		except ValueError as e:
			print(f"Ошибка: {e}")
			continue

		else:
			# Генерация пароля с выбранными значениями
			password = generator.gen_pw(length_password=length_password)

			# Получить хэш, если он был выбран
			if is_hash_pw.lower() in pos_answer:
				hashed_password = generator.gen_hash_pw(password=password)

			# Вывод результатов
			print(f'\nПароль: {password}\nХэшированный пароль: {hashed_password}')
			
			# Сохранить в базе данных и/или в файле, если один из вариантов был выбран
			if is_save_file.lower() in pos_answer:
				generator.save_to_file(password, hashed_password, service_name)
				print("Успешное сохранение в файл")
			if is_save_db.lower() in pos_answer:
				generator.save_to_db(password, hashed_password, service_name)
				print("Данные успешно записаны в БД")

			# Запрос на продолжение
			again = input("\nХотите создать еще один пароль? (y/n)")
			if again not in pos_answer:
				print("\nСпасибо за использование генератора паролей")
				break
