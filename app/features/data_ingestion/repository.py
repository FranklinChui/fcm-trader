from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from . import models, schemas

# --- Instrument Repository ---

def create_instrument(db: Session, instrument: schemas.InstrumentCreate) -> models.Instrument:
    """
    Creates a new instrument in the database.
    """
    db_instrument = models.Instrument(**instrument.model_dump())
    db.add(db_instrument)
    db.commit()
    db.refresh(db_instrument)
    return db_instrument

def get_instrument_by_symbol(db: Session, symbol: str) -> Optional[models.Instrument]:
    """
    Retrieves an instrument by its symbol.
    """
    return db.query(models.Instrument).filter(models.Instrument.symbol == symbol).first()

def get_instruments(db: Session, skip: int = 0, limit: int = 100) -> List[models.Instrument]:
    """
    Retrieves a list of all instruments.
    """
    return db.query(models.Instrument).offset(skip).limit(limit).all()


# --- Market Data Repository ---

def bulk_create_market_data(db: Session, market_data_list: List[schemas.MarketDataCreate]) -> List[models.MarketData]:
    """
    Bulk creates market data records.
    """
    db_market_data_list = [models.MarketData(**md.model_dump()) for md in market_data_list]
    db.add_all(db_market_data_list)
    db.commit()
    # The objects in db_market_data_list will have their IDs populated after the commit.
    return db_market_data_list


def get_market_data_for_instrument(
    db: Session, instrument_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None
) -> List[models.MarketData]:
    """
    Retrieves market data for a specific instrument, optionally filtered by a date range.
    """
    query = db.query(models.MarketData).filter(models.MarketData.instrument_id == instrument_id)
    if start_date:
        query = query.filter(models.MarketData.date >= start_date)
    if end_date:
        query = query.filter(models.MarketData.date <= end_date)
    return query.order_by(models.MarketData.date.asc()).all()
