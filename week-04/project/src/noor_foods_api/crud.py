from sqlmodel import Session, col, select

from .models import Category, Product, ProductCreate, ProductUpdate


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
