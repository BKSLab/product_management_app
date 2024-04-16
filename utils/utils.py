from decimal import Decimal


def total_cost_calculation(price: Decimal, quantity: Decimal) -> Decimal:
    """
    Функция расчета общей стоимости товара, добавленного на склад
    """
    return round(price * quantity, 2)
