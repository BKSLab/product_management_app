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
    price = Column(Numeric(precision=10, scale=2), comment='Цена продукции')
    inventories = relationship(
        'Inventory', back_populates='product', lazy='joined'
    )

    def __repr__(self) -> str:
        return f'Товар: {self.name} по цене: {self.price}'


class Location(BaseModel):
    """Модель для хранения данных о локациях."""

    __tablename__ = 'location'

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
    product = relationship('Product', back_populates='inventories')
    location_id = Column(Integer, ForeignKey('location.id'))
    locations = relationship(
        'Location', back_populates='inventories', lazy='joined'
    )
    quantity = Column(
        Integer, comment='Количество продукции в месте ее хранения'
    )

    def __repr__(self) -> str:
        return (
            f'Количество продукции {self.product_id}, расположенной '
            f'в  {self.location_id} составляет {self.quantity}'
        )
