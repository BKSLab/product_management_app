import sys

from pymysql import connect

from config.config import configuration_data
from database.models import BaseModel, engine


def create_database():
    """Функция создания базы данных."""
    try:
        connection = connect(
            host=configuration_data.host.get_secret_value(),
            port=configuration_data.port,
            user=configuration_data.user.get_secret_value(),
            password=configuration_data.password.get_secret_value(),
        )
        db_name = configuration_data.db_name.get_secret_value()
        connection.cursor().execute(
            f'CREATE DATABASE IF NOT EXISTS {db_name};'
        )
        print(f'База данных с именем {db_name} успешно создана.')
    except Exception as error:
        print(f'При создании базы данных произошла ошибка: {error}')


def create_tables() -> None:
    """Функция для создания таблиц"""
    try:
        BaseModel.metadata.create_all(bind=engine)
        print('Таблицы успешно созданы!')
    except Exception as error:
        print(f'При создании таблиц произошла ошибка: {error}')


name = sys.argv[1]
func = globals().get(name)
if func:
    func()
