from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

from backend.app.amazon_scraper import scrape_amazon_product
from backend.app.price_history import save_price


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


class ProductURLRequest(BaseModel):
    url: HttpUrl


@router.post("/analyze")
def analyze_product(request: ProductURLRequest):
    """
    Scrape and analyze an Amazon Canada product URL.
    """

    url = str(request.url)

    if "amazon.ca" not in url.lower():
        raise HTTPException(
            status_code=400,
            detail="Please provide a valid Amazon Canada product URL.",
        )

    try:
        product = scrape_amazon_product(url)

        save_price(product)

        return {
            "success": True,
            "product": product,
        }

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc