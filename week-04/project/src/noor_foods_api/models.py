from datetime import UTC, date, datetime, time
from decimal import Decimal
from typing import Annotated, Any

from pydantic import StringConstraints
from sqlalchemy import DateTime, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field, SQLModel


def utc_now() -> datetime:
    return datetime.now(UTC)


class City(SQLModel, table=True):
    __tablename__ = "cities"

    city_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_type=Text, unique=True)
    province: str = Field(sa_type=Text)


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    category_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_type=Text, unique=True)


class Supplier(SQLModel, table=True):
    __tablename__ = "suppliers"

    supplier_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(sa_type=Text, unique=True)
    city_id: int = Field(foreign_key="cities.city_id")
    phone: str = Field(sa_type=Text)


ProductName = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=2),
]


class ProductBase(SQLModel):
    name: ProductName = Field(sa_type=Text)
    category_id: int = Field(foreign_key="categories.category_id")
    supplier_id: int = Field(foreign_key="suppliers.supplier_id")
    unit_price: Decimal = Field(max_digits=10, decimal_places=2, gt=0)
    stock_quantity: int = Field(default=0, ge=0)
    is_discontinued: bool = False
    attributes: dict[str, Any] = Field(default_factory=dict, sa_type=JSONB)


class Product(ProductBase, table=True):
    __tablename__ = "products"

    product_id: int | None = Field(default=None, primary_key=True)
    sku: str = Field(sa_type=Text, unique=True)
    added_on: date = Field(default_factory=date.today)


class ProductCreate(ProductBase):
    sku: str = Field(min_length=3)


class ProductUpdate(SQLModel):
    name: ProductName | None = None
    category_id: int | None = None
    supplier_id: int | None = None
    unit_price: Decimal | None = Field(
        default=None, max_digits=10, decimal_places=2, gt=0
    )
    stock_quantity: int | None = Field(default=None, ge=0)
    is_discontinued: bool | None = None
    attributes: dict[str, Any] | None = None


class ProductRead(ProductBase):
    product_id: int
    sku: str
    added_on: date


class Customer(SQLModel, table=True):
    __tablename__ = "customers"

    customer_id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field(sa_type=Text)
    email: str = Field(sa_type=Text, unique=True)
    phone: str | None = Field(default=None, sa_type=Text)
    city_id: int = Field(foreign_key="cities.city_id")
    referred_by: int | None = Field(
        default=None, foreign_key="customers.customer_id", ondelete="SET NULL"
    )
    signed_up_at: datetime = Field(sa_type=DateTime(timezone=True))
    is_active: bool = True


class Rider(SQLModel, table=True):
    __tablename__ = "riders"

    rider_id: int | None = Field(default=None, primary_key=True)
    full_name: str = Field(sa_type=Text)
    city_id: int = Field(foreign_key="cities.city_id")
    vehicle: str = Field(sa_type=Text)
    hired_on: date


class DiscountCode(SQLModel, table=True):
    __tablename__ = "discount_codes"

    code: str = Field(sa_type=Text, primary_key=True)
    percent_off: int
    valid_from: date
    valid_to: date


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    order_id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.customer_id")
    ordered_at: datetime = Field(
        default_factory=utc_now, sa_type=DateTime(timezone=True)
    )
    status: str = Field(default="pending", sa_type=Text)
    rider_id: int | None = Field(
        default=None, foreign_key="riders.rider_id", ondelete="SET NULL"
    )
    discount_code: str | None = Field(
        default=None, sa_type=Text, foreign_key="discount_codes.code"
    )
    delivery_fee: Decimal = Field(
        default=Decimal("0"), max_digits=10, decimal_places=2
    )
    delivered_at: datetime | None = Field(
        default=None, sa_type=DateTime(timezone=True)
    )


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    order_id: int | None = Field(
        default=None,
        foreign_key="orders.order_id",
        primary_key=True,
        ondelete="CASCADE",
    )
    product_id: int = Field(foreign_key="products.product_id", primary_key=True)
    quantity: int
    unit_price: Decimal = Field(max_digits=10, decimal_places=2)


class RiderShift(SQLModel, table=True):
    __tablename__ = "rider_shifts"

    shift_id: int | None = Field(default=None, primary_key=True)
    rider_id: int = Field(foreign_key="riders.rider_id")
    shift_date: date
    starts_at: time
    ends_at: time
    notes: str | None = Field(default=None, max_length=200)
