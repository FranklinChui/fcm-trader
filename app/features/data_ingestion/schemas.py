from pydantic import BaseModel
from datetime import date

# Pydantic schema for Instrument
class InstrumentBase(BaseModel):
    symbol: str
    name: str
    asset_class: str

class InstrumentCreate(InstrumentBase):
    pass

class Instrument(InstrumentBase):
    id: int

    class Config:
        from_attributes = True

# Pydantic schema for MarketData
class MarketDataBase(BaseModel):
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int

class MarketDataCreate(MarketDataBase):
    instrument_id: int

class MarketData(MarketDataBase):
    id: int
    instrument_id: int

    class Config:
        from_attributes = True
