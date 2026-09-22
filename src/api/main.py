from fastapi import FastAPI
from aiokafka import AIOKafkaProducer
import json
from src.generators.ecommerce import generate_ecommerce_record

app = FastAPI(
    title="Messy Data Generator API",
    description="API to generate messy JSON data and push to Kafka.",
    version="2.0.0"
)

# Global variable for our Kafka producer
producer = None

@app.on_event("startup")
async def startup_event():
    """Connect to Kafka when the API starts."""
    global producer
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()

@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect from Kafka when the API stops."""
    global producer
    if producer:
        await producer.stop()

@app.get("/")
def read_root():
    return {"status": "API is running", "docs": "Visit /docs for Swagger UI"}

@app.get("/generate/ecommerce")
async def get_ecommerce():
    """Generates a messy record and pushes it to Kafka!"""
    # 1. Generate the messy data
    record = generate_ecommerce_record()
    
    # 2. Convert Python dict to JSON string, then to bytes (Kafka only understands bytes)
    record_bytes = json.dumps(record).encode("utf-8")
    
    # 3. Push to Kafka topic 'raw_ecommerce'
    if producer:
        await producer.send_and_wait("raw_ecommerce", record_bytes)
        return {"status": "Successfully pushed to Kafka!", "data": record}
    else:
        return {"error": "Kafka producer not ready yet."}