from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from . import crud
from .database import get_session
from .models import Product

SessionDep = Annotated[Session, Depends(get_session)]


def get_product_or_404(product_id: int, session: SessionDep) -> Product:
    product = crud.get_product(session, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product


ProductDep = Annotated[Product, Depends(get_product_or_404)]
