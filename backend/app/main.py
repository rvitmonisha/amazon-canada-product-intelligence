from fastapi import FastAPI, HTTPException

from backend.app.ai_insights import generate_product_insights
from backend.app.product_comparison import compare_products

app = FastAPI(
    title="Amazon Canada Product Intelligence API",
    description="Product intelligence and price tracking API for Amazon Canada.",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Amazon Canada Product Intelligence API",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/products/insights")
def product_insights(product: dict):
    return generate_product_insights(product)


@app.post("/products/compare")
def product_comparison(products: list[dict]):
    if not products:
        raise HTTPException(
            status_code=400,
            detail="At least one product is required",
        )

    return compare_products(products)