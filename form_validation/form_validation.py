def validation_location(location: str) -> bool:
    """Функция валидации данных о новой локации."""
    return isinstance(location, str) and len(location) <= 50


def validation_product(name: str, description: str, unit_id: str) -> bool:
    """Функция валидации данных о новом товаре."""
    return (
        isinstance(name, str)
        and len(name) <= 50
        and isinstance(description, str)
        and unit_id.isdigit()
    )


def validation_inventory(
    location_id: str, quantity: str, product_id: str
) -> bool:
    """Функция валидации данных о новом товаре при добавлении на склад."""
    return (
        isinstance(location_id, str)
        and isinstance(quantity, str)
        and isinstance(product_id, str)
        and location_id.isdigit()
        and product_id.isdigit()
        and float(quantity) > 0
    )


def validation_inventory_id(inventory_id: str) -> bool:
    """
    Функция валидации id записи о товаре,
    добавленном на склад при его удалении.
    """
    return isinstance(inventory_id, str) and inventory_id.isdigit()


def validation_quantity(quantity: str) -> bool:
    """Функция валидации количества товара на складе при его изменении."""
    return (
        isinstance(quantity, str) and quantity.isdigit() and int(quantity) >= 0
    )
