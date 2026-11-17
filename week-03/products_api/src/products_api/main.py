from itertools import count

from fastapi import FastAPI, HTTPException, Query, Response

from products_api.models import (
    Category,
    NewProduct,
    Product,
    ProductUpdate,
    Summary,
)

app = FastAPI(title="Noor Foods Products API")

# 1. In-memory storage seeded with the 4 starting products
products: dict[str, Product] = {
    "P101": Product(
        id="P101",
        name="Basmati rice 5kg",
        price=2400,
        category=Category.rice,
        in_stock=40,
    ),
    "P102": Product(
        id="P102",
        name="Cooking oil 1L",
        price=650,
        category=Category.oil,
        in_stock=0,
    ),
    "P103": Product(
        id="P103",
        name="Red chilli powder 200g",
        price=320,
        category=Category.spices,
        in_stock=120,
    ),
    "P104": Product(
        id="P104",
        name="Sella rice 10kg",
        price=4600,
        category=Category.rice,
        in_stock=15,
    ),
}

# 2. Infinite counter starting at 105 so deleted IDs are never reused
id_counter = count(105)


# 3. Shared 404 helper function
def find_product(product_id: str) -> Product:
    if product_id not in products:
        raise HTTPException(
            status_code=404, detail=f"Product {product_id} not found"
        )
    return products[product_id]


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/products")
def list_products(
    category: Category | None = None,
    max_price: int | None = None,
    limit: int = Query(default=10, ge=1),
) -> list[Product]:
    results: list[Product] = []
    for product in products.values():
        if category is not None and product.category != category:
            continue
        if max_price is not None and product.price > max_price:
            continue
        results.append(product)
    return results[:limit]


@app.get("/products/{product_id}")
def get_product(product_id: str) -> Product:
    return find_product(product_id)


@app.post("/products", status_code=201)
def create_product(new_product: NewProduct) -> Product:
    new_id = f"P{next(id_counter)}"
    product = Product(id=new_id, **new_product.model_dump())
    products[new_id] = product
    return product


@app.patch("/products/{product_id}")
def update_product(product_id: str, updates: ProductUpdate) -> Product:
    existing = find_product(product_id)
    update_data = updates.model_dump(exclude_unset=True)
    updated_product = existing.model_copy(update=update_data)
    products[product_id] = updated_product
    return updated_product


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: str) -> Response:
    product = find_product(product_id)
    if product.in_stock > 0:
        raise HTTPException(
            status_code=409,
            detail=f"Cannot delete {product_id}: {product.in_stock} items still in stock",
        )
    del products[product_id]
    return Response(status_code=204)


@app.get("/summary")
def get_summary() -> Summary:
    total_value = 0
    by_category: dict[str, int] = {}

    for product in products.values():
        total_value += product.price * product.in_stock
        cat_name = product.category.value
        by_category[cat_name] = by_category.get(cat_name, 0) + 1

    return Summary(
        product_count=len(products),
        stock_value=total_value,
        by_category=by_category,
    )
