from backend.app.price_tracker import (
    create_price_record,
    calculate_price_change,
)


def test_create_price_record():
    record = create_price_record("TEST001", 49.99)

    assert record["product_id"] == "TEST001"
    assert record["price"] == 49.99
    assert record["currency"] == "CAD"
    assert "timestamp" in record


def test_price_change():
    change = calculate_price_change(100, 120)

    assert change == 20.0