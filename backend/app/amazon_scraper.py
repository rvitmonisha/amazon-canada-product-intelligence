import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup


AMAZON_DOMAIN = "www.amazon.ca"


def clean_amazon_url(url: str) -> str:
    """Clean whitespace and Markdown-wrapped Amazon URLs."""

    url = url.strip()

    markdown_match = re.match(
        r"^\[.*?\]\((https?://[^)]+)\)$",
        url
    )

    if markdown_match:
        url = markdown_match.group(1)

    return url


def validate_amazon_url(url: str) -> None:
    """Validate that the URL belongs to Amazon Canada."""

    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        raise ValueError("Invalid URL scheme.")

    if parsed.netloc.lower() != AMAZON_DOMAIN:
        raise ValueError("Only Amazon Canada URLs are supported.")


def extract_price(soup: BeautifulSoup):
    """Extract product price from Amazon page."""

    price_selectors = [
        ".a-price .a-offscreen",
        "#corePrice_feature_div .a-offscreen",
        "#corePriceDisplay_desktop_feature_div .a-offscreen",
        "#priceblock_ourprice",
        "#priceblock_dealprice",
        "#price_inside_buybox",
    ]

    for selector in price_selectors:
        element = soup.select_one(selector)

        if not element:
            continue

        text = element.get_text(" ", strip=True)

        match = re.search(
            r"[\d,]+(?:\.\d{2})?",
            text
        )

        if match:
            return float(
                match.group().replace(",", "")
            )

    return None


def extract_rating(soup: BeautifulSoup):
    """Extract product rating."""

    rating_element = soup.select_one(
        "#acrPopover, "
        "[data-hook='rating-out-of-text'], "
        ".a-icon-alt"
    )

    if not rating_element:
        return None

    rating_text = (
        rating_element.get("title", "")
        or rating_element.get_text(" ", strip=True)
    )

    match = re.search(
        r"([0-5](?:\.\d+)?)",
        rating_text
    )

    if match:
        return float(match.group(1))

    return None


def extract_reviews(soup: BeautifulSoup) -> int:
    """Extract total customer review count."""

    review_element = soup.select_one(
        "#acrCustomerReviewText, "
        "[data-hook='total-review-count']"
    )

    if not review_element:
        return 0

    review_text = review_element.get_text(
        " ",
        strip=True
    )

    match = re.search(
        r"[\d,]+",
        review_text
    )

    if match:
        return int(
            match.group().replace(",", "")
        )

    return 0


def scrape_amazon_product(url: str) -> dict:
    """Scrape product information from an Amazon Canada product page."""

    url = clean_amazon_url(url)

    validate_amazon_url(url)

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/151.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-CA,en;q=0.9",
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/avif,image/webp,"
            "*/*;q=0.8"
        ),
        "Referer": "https://www.amazon.ca/",
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=20,
            allow_redirects=True,
        )

        response.raise_for_status()

    except requests.Timeout as exc:
        raise RuntimeError(
            "Amazon request timed out."
        ) from exc

    except requests.ConnectionError as exc:
        raise RuntimeError(
            "Unable to connect to Amazon."
        ) from exc

    except requests.HTTPError as exc:
        raise RuntimeError(
            f"Amazon returned HTTP {response.status_code}."
        ) from exc

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    title = "Unknown Product"

    title_element = soup.select_one(
        "#productTitle"
    )

    if title_element:
        title = title_element.get_text(
            " ",
            strip=True
        )

    return {
        "title": title,
        "price": extract_price(soup),
        "currency": "CAD",
        "rating": extract_rating(soup),
        "reviews": extract_reviews(soup),
        "url": url,
    }