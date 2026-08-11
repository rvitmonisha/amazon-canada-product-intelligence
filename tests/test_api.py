from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "running"


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_product_insights():
    product = {
        "title": "Wireless Headphones",
        "price": 79.99,
        "rating": "4.7",
    }

    response = client.post("/products/insights", json=product)

    assert response.status_code == 200
    assert response.json()["recommendation"] == "Strong value for money"


def test_product_comparison():
    products = [
        {
            "product_id": "P001",
            "title": "Product A",
            "price": 49.99,
            "rating": "4.2",
        },
        {
            "product_id": "P002",
            "title": "Product B",
            "price": 39.99,
            "rating": "4.7",
        },
    ]

    response = client.post("/products/compare", json=products)

    assert response.status_code == 200
    assert response.json()["lowest_price_product"]["product_id"] == "P002"