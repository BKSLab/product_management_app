from decimal import Decimal

from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from database.models import (
    BaseModel,
    Inventory,
    Location,
    Product,
    Unit,
    engine,
)


def add_product(
    product_name: str,
    product_description: str,
    product_price: Decimal,
    unit: Unit,
) -> dict:
    """Добавление товара"""
    with Session(autoflush=False, bind=engine) as session:
        try:
            new_product = Product(
                name=product_name,
                description=product_description,
                price=product_price,
                unit_id=unit.id,
            )
            session.add(new_product)
            session.commit()
        except SQLAlchemyError as error:
            return {
                'status': False,
                'error': error,
            }
        instance = session.get(Product, new_product.id)
    return {
        'status': True,
        'product': instance,
    }


def add_location(name_location: str) -> dict:
    """Функция добавления новой локации."""
    with Session(autoflush=False, bind=engine) as session:
        try:
            location = Location(name=name_location)
            session.add(location)
            session.commit()
        except IntegrityError as error:
            return {
                'status': False,
                'error_message': error,
            }
        instance = session.get(Location, location.id)
    return {
        'status': True,
        'location': instance,
    }


def get_objects(model: BaseModel):
    """Получение всех добавленных продуктов."""
    with Session(autoflush=False, bind=engine) as session:
        instance = session.query(model).all()
    return instance


def get_object_by_id(model: BaseModel, id: int):
    """Получение объекта по его id."""
    with Session(autoflush=False, bind=engine) as session:
        instance = session.get(model, id)
    return instance


def add_product_to_inventory(
    product: Product,
    location: Location,
    quantity: Decimal,
):
    """Функция добавления товара на склад."""
    with Session(autoflush=False, bind=engine) as session:
        try:
            inventory_record = Inventory(
                product_id=product.id,
                location_id=location.id,
                quantity=quantity,
            )
            session.add(inventory_record)
            session.commit()
        except IntegrityError as error:
            return {
                'status': False,
                'error_message': error,
            }
        instance = session.get(Inventory, inventory_record.id)
    return {
        'status': True,
        'instance': instance,
    }


def del_product_from_inventory(inventory_id: str):
    """Функция удаления товара со склада."""
    with Session(autoflush=False, bind=engine) as session:
        try:
            instance = session.get(Inventory, inventory_id)
            session.delete(instance)
            session.commit()
        except IntegrityError as error:
            return {
                'status': False,
                'error_message': error,
            }
    return {
        'status': True,
    }


def change_quantity_product_in_inventory(
    new_quantity: int,
    inventory_id: int,
):
    """Изменение количества товара на складе."""
    with Session(autoflush=False, bind=engine) as session:
        try:
            instance = session.get(Inventory, inventory_id)
            instance.quantity = new_quantity
            session.commit()
        except IntegrityError as error:
            return {
                'status': False,
                'error_message': error,
            }
    return {
        'status': True,
    }
