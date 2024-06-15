import os

# Установка переменных окружения непосредственно в коде
SECRET_KEY = 'b3baa1cb519a5651c472d1afa1b3f4e04f1adf6909dae88a4cd39adc0ddd9732'
MYSQL_USER = 'std_2419_zhak_project'
MYSQL_PASSWORD = 'zhakaris'
MYSQL_HOST = 'std-mysql.ist.mospolytech.ru'
MYSQL_DATABASE = 'std_2419_zhak_project'

# Вывод переменных окружения для диагностики
print(f"SECRET_KEY={SECRET_KEY}")
print(f"MYSQL_USER={MYSQL_USER}")
print(f"MYSQL_PASSWORD={MYSQL_PASSWORD}")
print(f"MYSQL_HOST={MYSQL_HOST}")
print(f"MYSQL_DATABASE={MYSQL_DATABASE}")

SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = 'static/uploads'
