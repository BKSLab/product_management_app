from decimal import Decimal

from flask import flash, request
from werkzeug.datastructures.structures import ImmutableMultiDict

from database.data_operations import (
    add_location,
    add_product,
    add_product_to_inventory,
    change_quantity_product_in_inventory,
    del_product_from_inventory,
    get_object_by_id,
)
from database.models import Location, Product, Unit
from form_validation.form_validation import (
    validation_inventory,
    validation_inventory_id,
    validation_location,
    validation_product,
    validation_quantity,
)


def processing_request_add_location(form_data: ImmutableMultiDict) -> None:
    """
    Обработка запроса пользователя на добавление
    информации о новой локации.
    """
    location = form_data.get('location')
    result = validation_location(location)
    if result:
        query_result = add_location(location)
        if query_result.get('status'):
            flash(f'{query_result.get("location")} успешно добавлена')
        else:
            flash(f'Локация: {location} ранее уже была добавлена')
    else:
        flash(
            f'Локация: {location} не может быть добавлена, '
            'проверьте корректность ввода'
        )


def processing_request_add_product(form_data: ImmutableMultiDict) -> None:
    """
    Обработка запроса пользователя на добавление
    информации о новом товаре.
    """
    name = form_data.get('product_name')
    description = form_data.get('product_description')
    price = form_data.get('product_price')
    unit_id = form_data.get('unit_id')
    result = validation_product(name, description, unit_id)
    if result:
        unit_instance = get_object_by_id(model=Unit, id=int(unit_id))
        query_result = add_product(
            name, description, Decimal(price.replace(',', '.')), unit_instance
        )
        if query_result.get('status'):
            flash(f'{query_result.get("product")} успешно добавлен')
        else:
            query_result.get('error')
            flash(
                f'При добавлении товара: {name} произошла '
                f'ошибка: {query_result.get("error")}'
            )
    else:
        flash(
            f'Товар: {name} не может быть добавлен, '
            'проверьте корректность ввода данных'
        )


def processing_request_add_product_to_inventory(
    form_data: ImmutableMultiDict,
) -> None:
    """
    Обработка запроса пользователя на добавление
    товара на склад в конкретной локации.
    """
    location_id = form_data.get('location_id')
    quantity = request.form.get('quantity')
    product_id = request.form.get('product_id')
    result = validation_inventory(location_id, quantity, product_id)
    if result:
        product_instance = get_object_by_id(model=Product, id=int(product_id))
        location_instance = get_object_by_id(
            model=Location, id=int(location_id)
        )
        if product_instance and location_instance:
            query_result = add_product_to_inventory(
                product_instance,
                location_instance,
                Decimal(quantity.replace(',', '.')),
            )
            if query_result.get('status'):
                inventory_instance = query_result.get('instance')
                flash(
                    f'Товар {inventory_instance.products.name} '
                    'успешно добавлен!'
                )
            else:
                flash(
                    f'Товар: {product_instance.name} ранее уже '
                    'был добавлен на склад'
                )
        else:
            flash(
                'При обработке данных произошла ошибка, '
                'проверьте правильность указания товара или локации.'
            )
    else:
        flash(
            'При валидации введенных данных произошла ошибка, '
            'проверьте корректность указания товара или локации.'
        )


def processing_request_del_product_from_inventory(
    form_data: ImmutableMultiDict,
) -> None:
    """
    Обработка запроса пользователя на удаление товара со
    склада в конкретной локации.
    """
    inventory_id = form_data.get('inventory_id')
    result = validation_inventory_id(inventory_id)
    if result:
        query_result = del_product_from_inventory(inventory_id)
        if query_result.get('status'):
            flash('Товар успешно удален со склада')
        else:
            flash(
                'При удалении товара произошла ошибка, свяжитесь '
                'с администратором базы'
            )
    else:
        flash(
            'Товар не может быть удален со склада, '
            'проверьте корректность ввода данных'
        )


def processing_request_change_quantity(form_data: ImmutableMultiDict) -> None:
    """
    Обработка запроса пользователя на внесение информации о количестве
    товара на складе в конкретной локации.
    """
    new_quantity = form_data.get('new_quantity')
    if int(new_quantity) == 0:
        processing_request_del_product_from_inventory(form_data)
    else:
        result = validation_quantity(new_quantity)
        if result:
            inventory_id = form_data.get('inventory_id')
            query_result = change_quantity_product_in_inventory(
                int(new_quantity), inventory_id
            )
            if query_result.get('status'):
                flash('Количество товара на складе успешно изменено')
            else:
                flash(
                    'При изменении количества товара произошла '
                    'ошибка, свяжитесь с администратором базы'
                )
        else:
            flash(
                'Количество товара не может быть изменено, '
                'проверьте корректность ввода данных'
            )
