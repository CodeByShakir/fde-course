from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from . import crud
from .database import get_session
from .models import Order, Product

SessionDep = Annotated[Session, Depends(get_session)]


def get_product_or_404(product_id: int, session: SessionDep) -> Product:
    product = crud.get_product(session, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


ProductDep = Annotated[Product, Depends(get_product_or_404)]


def get_order_or_404(order_id: int, session: SessionDep) -> Order:
    order = crud.get_order(session, order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )
    return order


OrderDep = Annotated[Order, Depends(get_order_or_404)]
