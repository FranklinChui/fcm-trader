import requests
from sqlalchemy.orm import Session
from datetime import date, timedelta
from typing import List, Dict, Any

from . import repository, schemas
from app.core.config import settings

def fetch_data_from_source(symbol: str) -> List[Dict[str, Any]]:
    """
    Placeholder function to fetch data from an external API.
    In a real scenario, this would connect to a financial data provider.
    """
    # This is a mock implementation.
    # Replace with a real API call, e.g., to Alpha Vantage, Polygon.io, etc.
    print(f"Fetching data for {symbol} from external source...")
    # Returning dummy data for now
    return [
        {'date': date.today() - timedelta(days=1), 'open': 100, 'high': 110, 'low': 99, 'close': 105, 'volume': 10000},
        {'date': date.today(), 'open': 105, 'high': 115, 'low': 103, 'close': 110, 'volume': 12000},
    ]

def ingest_data_for_symbol(db: Session, symbol: str):
    """
    Orchestrates the data ingestion process for a given symbol.
    1. Fetches new data from the external source.
    2. Checks if the instrument exists, creates it if not.
    3. Saves the new market data to the database.
    """
    # 1. Fetch new data
    try:
        market_data_raw = fetch_data_from_source(symbol)
        if not market_data_raw:
            print(f"No new data found for {symbol}.")
            return
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        raise e

    # 2. Check for instrument
    instrument = repository.get_instrument_by_symbol(db, symbol=symbol)
    if not instrument:
        print(f"Instrument {symbol} not found, creating new one.")
        instrument_create = schemas.InstrumentCreate(
            symbol=symbol,
            name=f"{symbol} Name", # Placeholder name
            asset_class="Unknown" # Placeholder asset class
        )
        instrument = repository.create_instrument(db, instrument=instrument_create)

    # 3. Prepare and save market data
    market_data_to_create = [
        schemas.MarketDataCreate(
            instrument_id=instrument.id,
            **data
        ) for data in market_data_raw
    ]

    repository.bulk_create_market_data(db, market_data_list=market_data_to_create)
    print(f"Successfully ingested {len(market_data_to_create)} data points for {symbol}.")
