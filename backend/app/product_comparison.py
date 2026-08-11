def compare_products(products: list[dict]) -> dict:
    """Compare products by price and rating."""

    if not products:
        return {
            "products": [],
            "lowest_price_product": None,
            "highest_rated_product": None,
        }

    lowest_price = min(
        products,
        key=lambda product: product.get("price", float("inf"))
    )

    highest_rated = max(
        products,
        key=lambda product: float(product.get("rating", 0) or 0)
    )

    return {
        "products": products,
        "lowest_price_product": lowest_price,
        "highest_rated_product": highest_rated,
    }