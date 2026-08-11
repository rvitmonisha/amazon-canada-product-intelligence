def generate_product_insights(product: dict) -> dict:
    """Generate rule-based product insights."""

    price = product.get("price")
    rating = float(product.get("rating", 0) or 0)

    if price is None:
        price_assessment = "Price information unavailable"
    elif price < 50:
        price_assessment = "Budget-friendly price"
    elif price < 150:
        price_assessment = "Mid-range price"
    else:
        price_assessment = "Premium price"

    if rating >= 4.5:
        rating_assessment = "Excellent customer rating"
    elif rating >= 4.0:
        rating_assessment = "Good customer rating"
    elif rating > 0:
        rating_assessment = "Average customer rating"
    else:
        rating_assessment = "Rating unavailable"

    if rating >= 4.5 and price is not None and price < 100:
        recommendation = "Strong value for money"
    elif rating >= 4.0:
        recommendation = "Worth considering"
    else:
        recommendation = "Review carefully before purchasing"

    return {
        "product_title": product.get("title"),
        "price_assessment": price_assessment,
        "rating_assessment": rating_assessment,
        "recommendation": recommendation,
    }