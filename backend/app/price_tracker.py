from datetime import datetime


def create_price_record(
    product_id: str,
    price: float,
    currency: str = "CAD"
) -> dict:
    """Create a timestamped price record for a product."""

    return {
        "product_id": product_id,
        "price": price,
        "currency": currency,
        "timestamp": datetime.utcnow().isoformat()
    }


def calculate_price_change(old_price: float, new_price: float) -> float:
    """Calculate percentage change between two prices."""

    if old_price == 0:
        return 0.0

    return round(((new_price - old_price) / old_price) * 100, 2)