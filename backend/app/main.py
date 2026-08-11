from fastapi import FastAPI

app = FastAPI(
    title="Amazon Canada Product Intelligence API",
    description="Backend API for product intelligence and price tracking.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Amazon Canada Product Intelligence API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}