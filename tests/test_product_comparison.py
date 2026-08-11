from backend.app.product_comparison import compare_products


def test_compare_products():
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

    result = compare_products(products)

    assert result["lowest_price_product"]["product_id"] == "P002"
    assert result["highest_rated_product"]["product_id"] == "P002"


def test_empty_products():
    result = compare_products([])

    assert result["products"] == []
    assert result["lowest_price_product"] is None
    assert result["highest_rated_product"] is None