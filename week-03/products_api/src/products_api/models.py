from enum import Enum

from pydantic import BaseModel, Field


class Category(str, Enum):
    rice = "rice"
    oil = "oil"
    spices = "spices"
    flour = "flour"


class NewProduct(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    price: int = Field(gt=0)
    category: Category
    in_stock: int = Field(default=0, ge=0)


class Product(NewProduct):
    id: str


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    price: int | None = Field(default=None, gt=0)
    category: Category | None = None
    in_stock: int | None = Field(default=None, ge=0)


class Summary(BaseModel):
    product_count: int
    stock_value: int
    by_category: dict[str, int]
