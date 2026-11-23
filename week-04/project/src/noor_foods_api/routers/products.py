from typing import Annotated, Any

from fastapi import APIRouter, Query, Response, status

from .. import crud
from ..dependencies import ProductDep, SessionDep
from ..models import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(
    session: SessionDep,
    category_id: int | None = None,
    search: str | None = None,
    in_stock: bool | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Any:
    return crud.list_products(
        session,
        category_id=category_id,
        search=search,
        in_stock=in_stock,
        limit=limit,
        offset=offset,
    )


@router.get("/{product_id}", response_model=ProductRead)
def get_product(product: ProductDep) -> Any:
    return product


@router.post(
    "", response_model=ProductRead, status_code=status.HTTP_201_CREATED
)
def create_product(payload: ProductCreate, session: SessionDep) -> Any:
    return crud.create_product(session, payload)


@router.patch("/{product_id}", response_model=ProductRead)
def update_product(
    product: ProductDep, payload: ProductUpdate, session: SessionDep
) -> Any:
    return crud.update_product(session, product, payload)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product: ProductDep, session: SessionDep) -> Response:
    crud.delete_product(session, product)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
