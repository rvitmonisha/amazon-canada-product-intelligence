import pytest

from backend.app.amazon_scraper import (
    clean_amazon_url,
    extract_price,
    extract_rating,
    extract_reviews,
    validate_amazon_url,
)


def test_clean_amazon_url():
    url = "[Amazon Product](https://www.amazon.ca/dp/B0GSHQ525L)"

    result = clean_amazon_url(url)

    assert result == "https://www.amazon.ca/dp/B0GSHQ525L"


def test_clean_amazon_url_without_markdown():
    url = "https://www.amazon.ca/dp/B0GSHQ525L"

    result = clean_amazon_url(url)

    assert result == url


def test_validate_amazon_url():
    validate_amazon_url(
        "https://www.amazon.ca/dp/B0GSHQ525L"
    )


def test_invalid_amazon_url():
    with pytest.raises(ValueError):
        validate_amazon_url(
            "https://www.amazon.com/dp/B0GSHQ525L"
        )


def test_extract_price():
    from bs4 import BeautifulSoup

    html = """
    <span class="a-price">
        <span class="a-offscreen">$1,299.99</span>
    </span>
    """

    soup = BeautifulSoup(html, "html.parser")

    assert extract_price(soup) == 1299.99


def test_extract_rating():
    from bs4 import BeautifulSoup

    html = """
    <span class="a-icon-alt">
        4.6 out of 5 stars
    </span>
    """

    soup = BeautifulSoup(html, "html.parser")

    assert extract_rating(soup) == 4.6


def test_extract_reviews():
    from bs4 import BeautifulSoup

    html = """
    <span id="acrCustomerReviewText">
        1,234 ratings
    </span>
    """

    soup = BeautifulSoup(html, "html.parser")

    assert extract_reviews(soup) == 1234


def test_missing_price():
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(
        "<html></html>",
        "html.parser"
    )

    assert extract_price(soup) is None


def test_missing_rating():
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(
        "<html></html>",
        "html.parser"
    )

    assert extract_rating(soup) is None


def test_missing_reviews():
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(
        "<html></html>",
        "html.parser"
    )

    assert extract_reviews(soup) == 0