# Генератор пароля на python
## Описание
Генератор паролей с возможностью хеширования через bcrypt. Возможно сохранения пароля и его хэша, как в текстовый файл, так и в БД (postgresql/mysql)

## Установка
1) Клонируйте репозиторий или скачайте его zip ( git clone https://github.com/lukashouknnootta22/generator_password.git )
2) Установите и активируйте виртуальное окружение ( python3 -m venv {your_name_venv} & source {your_name_venv}/bin/activate)
3) Установите все зависимости ( pip install -r requirements.txt )
4) Создайте env-файл с настройками вашей базы данных ( DB_TYPE (postgresql/mysql); DB_NAME ; DB_PASSWORD ; DB_HOST ; DB_USER )
5) Запустите main-файл ( python main.py )
