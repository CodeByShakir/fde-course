from fastapi.testclient import TestClient

from products_api.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_list_products_default():
    res = client.get("/products")
    assert res.status_code == 200
    assert len(res.json()) >= 4


def test_list_products_filtered():
    res = client.get("/products?category=rice&max_price=3000")
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["id"] == "P101"


def test_list_products_invalid_category_422():
    res = client.get("/products?category=sugar")
    assert res.status_code == 422


def test_get_single_product():
    res = client.get("/products/P101")
    assert res.status_code == 200
    assert res.json()["name"] == "Basmati rice 5kg"


def test_get_missing_product_404():
    res = client.get("/products/P999")
    assert res.status_code == 404
    assert "P999" in res.json()["detail"]


def test_create_product_201():
    payload = {"name": "Chakki atta 10kg", "price": 1800, "category": "flour"}
    res = client.post("/products", json=payload)
    assert res.status_code == 201
    body = res.json()
    assert body["id"].startswith("P")
    assert body["in_stock"] == 0


def test_create_product_invalid_price_422():
    payload = {"name": "Bad Oil", "price": -10, "category": "oil"}
    res = client.post("/products", json=payload)
    assert res.status_code == 422


def test_patch_product():
    # Create a fresh product first so other tests aren't affected
    created = client.post(
        "/products",
        json={"name": "Test Spice", "price": 100, "category": "spices"},
    ).json()
    pid = created["id"]

    res = client.patch(f"/products/{pid}", json={"price": 250})
    assert res.status_code == 200
    assert res.json()["price"] == 250
    assert res.json()["name"] == "Test Spice"


def test_patch_invalid_stock_422():
    res = client.patch("/products/P103", json={"in_stock": -5})
    assert res.status_code == 422


def test_patch_missing_product_404():
    res = client.patch("/products/P999", json={"price": 500})
    assert res.status_code == 404
    assert "P999" in res.json()["detail"]


def test_delete_in_stock_conflict_409():
    res = client.delete("/products/P101")
    assert res.status_code == 409


def test_delete_zero_stock_204():
    # Create a fresh product with 0 stock to delete cleanly
    created = client.post(
        "/products",
        json={
            "name": "Temp Item",
            "price": 50,
            "category": "oil",
            "in_stock": 0,
        },
    ).json()
    pid = created["id"]

    res = client.delete(f"/products/{pid}")
    assert res.status_code == 204
    assert client.get(f"/products/{pid}").status_code == 404


def test_delete_missing_product_404():
    res = client.delete("/products/P999")
    assert res.status_code == 404
    assert "P999" in res.json()["detail"]


def test_summary():
    res = client.get("/summary")
    assert res.status_code == 200
    data = res.json()
    assert "product_count" in data
    assert "stock_value" in data
    assert "by_category" in data
