from fastapi import FastAPI

app = FastAPI(title="Noor Foods products API")

PRODUCTS = {
    {
        "id": "P101",
        "name": "Basmati rice 5kg",
        "price": 2400,
        "category": "rice",
        "in_stock": 40,
    },
    {
        "id": "P102",
        "name": "Cooking oil 1L",
        "price": 650,
        "category": "oil",
        "in_stock": 0,
    },
    {
        "id": "P103",
        "name": "Red chilli powder 200g",
        "price": 320,
        "category": "spices",
        "in_stock": 120,
    },
    {
        "id": "P104",
        "name": "Sella rice 10kg",
        "price": 4600,
        "category": "rice",
        "in_stock": 15,
    },
}
