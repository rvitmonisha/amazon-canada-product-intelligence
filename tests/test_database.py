from backend.app.database import (
    initialize_database,
    add_product,
    get_connection,
)


def test_database_and_product_creation():
    initialize_database()

    add_product(
        product_id="TEST001",
        title="Test Product",
        price=49.99,
        currency="CAD",
        rating="4.5 out of 5 stars",
        url="https://example.com/product",
    )

    connection = get_connection()

    result = connection.execute(
        "SELECT title, price, currency FROM products WHERE product_id = ?",
        ("TEST001",),
    ).fetchone()

    connection.close()

    assert result == ("Test Product", 49.99, "CAD")