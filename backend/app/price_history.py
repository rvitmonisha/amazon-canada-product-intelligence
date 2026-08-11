from datetime import datetime


def add_price_record(history: list[dict], price: float, currency: str = "CAD") -> list[dict]:
    """Add a timestamped price record."""

    record = {
        "price": price,
        "currency": currency,
        "timestamp": datetime.now().isoformat(),
    }

    history.append(record)
    return history


def calculate_price_trend(history: list[dict]) -> dict:
    """Calculate basic price trend information."""

    if len(history) < 2:
        return {
            "trend": "insufficient_data",
            "price_change": 0,
            "percentage_change": 0,
        }

    first_price = history[0]["price"]
    latest_price = history[-1]["price"]

    price_change = latest_price - first_price

    if first_price == 0:
        percentage_change = 0
    else:
        percentage_change = (price_change / first_price) * 100

    if price_change < 0:
        trend = "decreasing"
    elif price_change > 0:
        trend = "increasing"
    else:
        trend = "stable"

    return {
        "trend": trend,
        "price_change": round(price_change, 2),
        "percentage_change": round(percentage_change, 2),
    }