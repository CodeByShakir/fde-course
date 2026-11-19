from typing import Annotated

from fastapi import Depends, FastAPI
from sqlmodel import Session, col, select

from .database import get_session
from .models import Category

app = FastAPI(
    title="Noor Foods API",
    description="Products, orders and stock for Noor Foods.",
)


@app.get("/")
def read_root() -> dict[str, str]:
    return {"app": "Noor Foods API", "docs": "/docs"}


@app.get("/categories")
def list_categories(
    session: Annotated[Session, Depends(get_session)],
) -> list[Category]:
    statement = select(Category).order_by(col(Category.category_id))
    return list(session.exec(statement).all())
