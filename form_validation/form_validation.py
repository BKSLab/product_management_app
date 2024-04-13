def validation_location(location: str) -> bool:
    """Функция валидации данных о новой локации."""
    return isinstance(location, str) and len(location) <= 50


def validation_product(name: str, description: str, price: str) -> bool:
    """Функция валидации данных о новом товаре."""
    return (
        isinstance(name, str)
        and len(name) <= 50
        and isinstance(description, str)
    )


def validation_inventory(
    location_info: str, quantity: str, product_id: str
) -> bool:
    """Функция валидации данных о новом товаре при добавлении на склад."""
    location_id = location_info.split()[0]
    return (
        isinstance(location_id, str)
        and isinstance(quantity, str)
        and isinstance(product_id, str)
        and location_id.isdigit()
        and quantity.isdigit()
        and product_id.isdigit()
        and int(quantity) > 0
    )


def validation_product_and_location_id(product_info: str) -> bool:
    """
    Функция валидации id товара и локации нахождения товара при его удалении.
    """
    product_id = product_info[0]
    location_id = product_info[1]
    return (
        isinstance(product_id, str)
        and product_id.isdigit()
        and isinstance(location_id, str)
        and location_id.isdigit()
    )


def validation_quantity(quantity: str) -> bool:
    """Функция валидации количества товара на складе при его изменении."""
    return (
        isinstance(quantity, str) and quantity.isdigit() and int(quantity) >= 0
    )
