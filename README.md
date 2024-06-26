# product_management_app
product_management_app - web-приложение для учета товара на складах, расположенных в разных локациях.

![скриншот страницы приложения](/images/main_page.png)

## Функционал
product_management_app позволяет:
- добавлять новые товары в список товаров. При добавлении нового товара необходимо указать:
    - наименование товара;
    - описание товара;
    - цену за единицу товара.
- добавлять новые локации (месторасположение складов);
- добавлять товар на склад с указанием количества добавляемого на склад товара;
- изменять количество товара, добавленного на склад;
- удалять товары со складов;
- доступен поиск по частичному совпадению с наименованием товара;
- доступна сортировка товара по возрастанию цены.

## Инструкция по запуску проекта 

**Важно!** Приложение работает с MySQL. Перед запуском убедитесь, что у вас есть доступ к MySQL Server (установлен локально или через Docker контейнер).

### Порядок действий

1. Склонируйте репозиторий проекта:

        git clone git@github.com:BKSLab/product_management_app.git

2. Перейдите в папку проекта:
    
        cd product_management_app

3. Установите виртуальное окружение:

        python -m venv venv

4. Активируйте виртуальное окружение:

    	venv/Scripts/activate

5. Обновите пакет pip:

    	python -m pip install --upgrade pip

6. Установите необходимые зависимости из файла requirements.txt:

    	pip install -r requirements.txt

7. Создайте файл .env с переменными, необходимыми для работы проекта (пример содержания файла .env смотрите в .env.example)
8. Создайте базу данных (для проверки работы приложения используйте имя базы product_management_db):
	
        python database_management.py create_database

9. Создайте необходимые таблицы:

    	python database_management.py create_tables

10. Добавьте информацию об используемых единицах измерения:
        
        python database_management.py add_units

11. Подгрузите данные в таблицы из файла dump-product_management_db-202404131337.sql

12. Запустите проект:

    	flask --app app run

13. После запуска проекта он будет доступен по адресу:
	
        http://127.0.0.1:5000/

## Стек технологий
- Python 3.12
- Flask 3.0.3
- Pydantic 2.7.0
- SQLAlchemy 2.0.29
- PyMySQL 1.1.0
- Bootsrap

Подробнее с используемыми зависимостями вы можете ознакомиться в файле requirements.txt

## Об авторе проекта
Меня зовут Барабанщиков Кирилл, я python backend разработчик.

## Мои контакты
Telegram: https://t.me/Kirill_Barabanshchikov
Почта: bks2408@mail.ru
