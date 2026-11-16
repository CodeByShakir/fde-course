from enum import StrEnum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="NOOR FOOD API")


# Product categories
class Category(StrEnum):
    RICE = "rice"
    OIL = "oil"
    SPICES = "spices"
    FLOUR = "flour"


# Information received when creating a product
class NewProduct(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    price: int = Field(gt=0)
    category: Category
    in_stock: int = Field(default=0, ge=0)


# Complete product information returned by the API
class Product(BaseModel):
    id: str
    name: str
    price: int
    category: Category
    in_stock: int


# Information received when updating a product
class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=80)
    price: int | None = Field(default=None, gt=0)
    category: Category | None = None
    in_stock: int | None = Field(default=None, ge=0)


# Starting products
products = {
    "P101": {
        "name": "Basmati rice 5kg",
        "price": 2400,
        "category": "rice",
        "in_stock": 40,
    },
    "P102": {
        "name": "Cooking oil 1L",
        "price": 650,
        "category": "oil",
        "in_stock": 0,
    },
    "P103": {
        "name": "Red chilli powder 200g",
        "price": 320,
        "category": "spices",
        "in_stock": 120,
    },
    "P104": {
        "name": "Sella rice 10kg",
        "price": 4600,
        "category": "rice",
        "in_stock": 15,
    },
}


@app.get("/products")
def list_products(
    category: Category | None = None,
    max_price: int | None = None,
    limit: int = 10,
):
    result = []

    for product_id, product in products.items():
        result.append({"id": product_id, **product})

    return result[:limit]


@app.get("/products/{product_id}")
def get_product(product_id: str):
    if product_id not in products:
        raise HTTPException(
            status_code=404, detail=f"Product {product_id} not found"
        )

    return {"id": product_id, **products[product_id]}
