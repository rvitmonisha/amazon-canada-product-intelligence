from backend.app.ai_insights import generate_product_insights


def test_generate_product_insights():
    product = {
        "title": "Wireless Headphones",
        "price": 79.99,
        "rating": "4.7",
    }

    result = generate_product_insights(product)

    assert result["product_title"] == "Wireless Headphones"
    assert result["price_assessment"] == "Mid-range price"
    assert result["rating_assessment"] == "Excellent customer rating"
    assert result["recommendation"] == "Strong value for money"


def test_missing_price():
    product = {
        "title": "Test Product",
        "price": None,
        "rating": "3.5",
    }

    result = generate_product_insights(product)

    assert result["price_assessment"] == "Price information unavailable"