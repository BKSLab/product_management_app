import sys

from pymysql import connect
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from config.config import configuration_data
from database.models import BaseModel, Unit, engine


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


def add_units():
    """Функция добавления новой локации."""
    units = [
        'кг',
        'шт',
        'м',
        'м\u00B2',
        'м\u00B3',
        'л',
    ]
    with Session(autoflush=False, bind=engine) as session:
        try:
            for unit in units:
                instance = Unit(name=unit)
                session.add(instance)
                session.commit()
        except SQLAlchemyError as error:
            print(
                'Придобавлении данных об единицах измерения '
                f'произошла ошибка: {error}'
            )
        print('Данные в таблицу units успешно добавлены')


name = sys.argv[1]
func = globals().get(name)
if func:
    func()
