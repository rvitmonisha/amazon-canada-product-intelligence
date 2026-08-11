from backend.app.price_history import (
    add_price_record,
    calculate_price_trend,
)


def test_add_price_record():
    history = []

    result = add_price_record(history, 99.99)

    assert len(result) == 1
    assert result[0]["price"] == 99.99
    assert result[0]["currency"] == "CAD"
    assert "timestamp" in result[0]


def test_decreasing_price_trend():
    history = [
        {"price": 100.00},
        {"price": 80.00},
    ]

    result = calculate_price_trend(history)

    assert result["trend"] == "decreasing"
    assert result["price_change"] == -20.00
    assert result["percentage_change"] == -20.00


def test_increasing_price_trend():
    history = [
        {"price": 100.00},
        {"price": 120.00},
    ]

    result = calculate_price_trend(history)

    assert result["trend"] == "increasing"
    assert result["price_change"] == 20.00
    assert result["percentage_change"] == 20.00