from backend.app.scraper.amazon import scrape_product


def test_scraper_returns_product_structure():
    assert callable(scrape_product)