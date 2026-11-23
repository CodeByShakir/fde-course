from typing import Annotated, Any

from fastapi import APIRouter, Query

from .. import crud
from ..dependencies import OrderDep, SessionDep
from ..models import OrderDetail, OrderRead, OrderStatus

router = APIRouter(tags=["orders"])


@router.get("/orders", response_model=list[OrderRead])
def list_orders(
    session: SessionDep,
    customer_id: int | None = None,
    order_status: Annotated[OrderStatus | None, Query(alias="status")] = None,
    city: str | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Any:
    return crud.list_orders(
        session,
        customer_id=customer_id,
        order_status=order_status,
        city=city,
        limit=limit,
        offset=offset,
    )


@router.get("/orders/{order_id}", response_model=OrderDetail)
def get_order(order: OrderDep) -> Any:
    return order
