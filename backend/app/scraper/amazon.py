import requests
from bs4 import BeautifulSoup


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def scrape_product(url: str) -> dict:
    """Extract basic product information from a publicly accessible page."""

    response = requests.get(url, headers=HEADERS, timeout=15)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.select_one("#productTitle")
    price = soup.select_one(".a-price .a-offscreen")
    rating = soup.select_one(".a-icon-alt")

    return {
        "url": url,
        "title": title.get_text(strip=True) if title else None,
        "price": price.get_text(strip=True) if price else None,
        "rating": rating.get_text(strip=True) if rating else None,
    }