from fastapi import FastAPI
from app.core.logging import setup_logging
from app.core.database import engine, Base
from app.features.data_ingestion.models import Instrument, MarketData
from app.features.signal_generation.models import Signal

# Create all tables
# In a real application, you would use Alembic for migrations
Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    setup_logging()

@app.get("/")
def read_root():
    return {"message": "FCM Trader API is running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
