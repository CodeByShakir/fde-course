from sqlalchemy.orm import selectinload
from sqlmodel import Session, col, select

from .models import (
    Category,
    City,
    Customer,
    Order,
    OrderItem,
    OrderStatus,
    Product,
    ProductCreate,
    ProductUpdate,
)


def list_categories(session: Session) -> list[Category]:
    statement = select(Category).order_by(col(Category.category_id))
    return list(session.exec(statement).all())


def list_products(
    session: Session,
    *,
    category_id: int | None = None,
    search: str | None = None,
    in_stock: bool | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Product]:
    statement = select(Product)

    if category_id is not None:
        statement = statement.where(Product.category_id == category_id)
    if search is not None:
        statement = statement.where(col(Product.name).ilike(f"%{search}%"))
    if in_stock is True:
        statement = statement.where(Product.stock_quantity > 0)
    if in_stock is False:
        statement = statement.where(Product.stock_quantity == 0)

    statement = (
        statement.order_by(col(Product.product_id)).offset(offset).limit(limit)
    )
    return list(session.exec(statement).all())


def get_product(session: Session, product_id: int) -> Product | None:
    return session.get(Product, product_id)


def create_product(session: Session, payload: ProductCreate) -> Product:
    product = Product.model_validate(payload)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def update_product(
    session: Session, product: Product, payload: ProductUpdate
) -> Product:
    product.sqlmodel_update(payload.model_dump(exclude_unset=True))
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


def delete_product(session: Session, product: Product) -> None:
    session.delete(product)
    session.commit()


def list_orders(
    session: Session,
    *,
    customer_id: int | None = None,
    order_status: OrderStatus | None = None,
    city: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Order]:
    statement = select(Order).options(selectinload(Order.customer))  # type: ignore[arg-type]

    if customer_id is not None:
        statement = statement.where(Order.customer_id == customer_id)
    if order_status is not None:
        statement = statement.where(Order.status == order_status)
    if city is not None:
        statement = statement.join(Customer).join(City).where(City.name == city)

    statement = (
        statement.order_by(col(Order.order_id).desc())
        .offset(offset)
        .limit(limit)
    )
    return list(session.exec(statement).all())


def get_order(session: Session, order_id: int) -> Order | None:
    statement = (
        select(Order)
        .options(
            selectinload(Order.customer),  # type: ignore[arg-type]
            selectinload(Order.items).selectinload(OrderItem.product),  # type: ignore[arg-type]
        )
        .where(Order.order_id == order_id)
    )
    return session.exec(statement).first()
