from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.app.ai_insights import generate_product_insights
from backend.app.amazon_scraper import scrape_amazon_product
from backend.app.price_history import save_price
from backend.app.product_api import router as product_router
from backend.app.product_comparison import compare_products


app = FastAPI(
    title="Amazon Canada Product Intelligence API",
    description="Product intelligence and price tracking API for Amazon Canada.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(product_router)


@app.get("/")
def root():
    return {
        "message": "Amazon Canada Product Intelligence API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.post("/products/scrape")
def scrape_product(product: dict):
    url = product.get("url")

    if not url:
        raise HTTPException(
            status_code=400,
            detail="Amazon product URL is required",
        )

    try:
        scraped_product = scrape_amazon_product(url)

        save_price(scraped_product)

        return scraped_product

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


@app.post("/products/insights")
def product_insights(product: dict):
    return generate_product_insights(product)


@app.post("/products/compare")
def product_comparison(products: list[dict]):
    if len(products) < 2:
        raise HTTPException(
            status_code=400,
            detail="At least two Amazon product URLs are required",
        )

    scraped_products = []

    for item in products:
        url = item.get("url")

        if not url:
            raise HTTPException(
                status_code=400,
                detail="Each product must contain a URL",
            )

        try:
            product = scrape_amazon_product(url)
            scraped_products.append(product)

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

    try:
        return compare_products(scraped_products)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to compare products: {str(exc)}",
        ) from exc