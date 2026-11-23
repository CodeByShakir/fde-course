from fastapi import APIRouter

from .. import crud
from ..dependencies import SessionDep
from ..models import Category

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
def list_categories(session: SessionDep) -> list[Category]:
    return crud.list_categories(session)
