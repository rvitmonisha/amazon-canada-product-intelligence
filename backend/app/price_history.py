from datetime import datetime


price_history = {}


def add_price_record(history: list, price: float, currency: str = "CAD") -> list:
    """
    Add a price record to an in-memory price history list.
    """

    history.append({
        "price": price,
        "currency": currency,
        "timestamp": datetime.now().isoformat(),
    })

    return history


def calculate_price_trend(history: list) -> dict:
    """
    Calculate price movement between the first and latest records.
    """

    if len(history) < 2:
        return {
            "trend": "stable",
            "price_change": 0.0,
            "percentage_change": 0.0,
        }

    first_price = history[0]["price"]
    latest_price = history[-1]["price"]

    price_change = latest_price - first_price

    if first_price == 0:
        percentage_change = 0.0
    else:
        percentage_change = (
            price_change / first_price
        ) * 100

    if price_change > 0:
        trend = "increasing"
    elif price_change < 0:
        trend = "decreasing"
    else:
        trend = "stable"

    return {
        "trend": trend,
        "price_change": round(price_change, 2),
        "percentage_change": round(percentage_change, 2),
    }


def save_price(product: dict):
    """
    Save a scraped product price using its Amazon URL.
    """

    url = product.get("url")

    if not url:
        return

    if url not in price_history:
        price_history[url] = []

    add_price_record(
        price_history[url],
        product.get("price"),
        product.get("currency", "CAD"),
    )


def get_price_history(url: str):
    """
    Return the stored price history for a product.
    """

    return price_history.get(url, [])