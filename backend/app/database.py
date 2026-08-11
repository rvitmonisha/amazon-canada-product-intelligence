import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[2] / "data" / "products.db"


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            price REAL,
            currency TEXT DEFAULT 'CAD',
            rating TEXT,
            url TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def add_product(
    product_id: str,
    title: str,
    price: float | None,
    currency: str,
    rating: str | None,
    url: str,
):
    connection = get_connection()

    connection.execute(
        """
        INSERT OR REPLACE INTO products
        (product_id, title, price, currency, rating, url)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (product_id, title, price, currency, rating, url),
    )

    connection.commit()
    connection.close()