from fastapi import APIRouter, HTTPException, status

from .. import crud
from ..dependencies import SessionDep
from ..models import Category

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
def list_categories(session: SessionDep) -> list[Category]:
    return crud.list_categories(session)


@router.get("/{category_id}")
def get_category(category_id: int, session: SessionDep) -> Category:
    category = session.get(Category, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
        )
    return category
