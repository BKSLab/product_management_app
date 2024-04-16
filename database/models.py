from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.orm import DeclarativeBase, relationship

from config.config import configuration_data

user_db = configuration_data.user.get_secret_value()
password_db = configuration_data.password.get_secret_value()
host_db = configuration_data.host.get_secret_value()
name_db = configuration_data.db_name.get_secret_value()

engine = create_engine(
    f'mysql+pymysql://{user_db}:{password_db}@{host_db}/{name_db}'
)


class BaseModel(DeclarativeBase):
    """Определение базовой модели."""


class Unit(BaseModel):
    """Модель для хранения данных об единицах измерения товаров.."""

    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=5), comment='Единицы измерения', unique=True)
    products = relationship('Product', back_populates='units')

    def __repr__(self) -> str:
        return f'Единица измерения товара: {self.name}'


class Product(BaseModel):
    """Модель для хранения данных о товарах."""

    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(
        String(length=50),
        comment='Наименование продукции',
        unique=True,
    )
    description = Column(Text, comment='Описание продукции')
    price = Column(Numeric(precision=18, scale=2), comment='Цена продукции')
    unit_id = Column(Integer, ForeignKey('units.id'))
    units = relationship('Unit', back_populates='products', lazy='joined')
    inventories = relationship('Inventory', back_populates='products')

    def __repr__(self) -> str:
        return f'Товар: {self.name} по цене: {self.price}'


class Location(BaseModel):
    """Модель для хранения данных о локациях."""

    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True)
    name = Column(
        String(length=50), comment='Место хранения продукции', unique=True
    )
    inventories = relationship('Inventory', back_populates='locations')

    def __repr__(self) -> str:
        return f'Локация {self.name}'


class Inventory(BaseModel):
    """Модель для хранения данных о товарах, находящихся на складах."""

    __tablename__ = 'inventory'
    __table_args__ = (UniqueConstraint('product_id', 'location_id'),)

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    products = relationship(
        'Product', back_populates='inventories', lazy='joined'
    )
    location_id = Column(Integer, ForeignKey('locations.id'))
    locations = relationship(
        'Location', back_populates='inventories', lazy='joined'
    )
    quantity = Column(
        Numeric(precision=18, scale=3), comment='Количество товара'
    )

    def __repr__(self) -> str:
        return (
            f'Количество продукции {self.product_id}, расположенной '
            f'в  {self.location_id} составляет {self.quantity}'
        )
