from fastapi import FastAPI, Query
from src.generators.ecommerce import generate_ecommerce_record

# Initialize the FastAPI app
app = FastAPI(
    title="Messy Data Generator API",
    description="API to generate messy JSON data for ETL Pipeline testing.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"status": "API is running", "docs": "Visit /docs for Swagger UI"}

@app.get("/generate/ecommerce")
def get_ecommerce():
    """Returns a single messy e-commerce record"""
    return generate_ecommerce_record()

@app.get("/generate/batch")
def get_batch(count: int = Query(default=5, ge=1, le=100)):
    """Returns a batch of messy e-commerce records"""
    return [generate_ecommerce_record() for _ in range(count)]