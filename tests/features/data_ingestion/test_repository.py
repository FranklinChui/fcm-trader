import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.database import Base
from app.features.data_ingestion import repository, schemas
from app.features.signal_generation.models import Signal  # Import to resolve relationship
from datetime import date

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pytest fixture to set up and tear down the database for each test function
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_instrument(db_session):
    """
    Tests the creation of a single instrument.
    """
    instrument_create = schemas.InstrumentCreate(
        symbol="AAPL",
        name="Apple Inc.",
        asset_class="Stock"
    )
    db_instrument = repository.create_instrument(db=db_session, instrument=instrument_create)
    assert db_instrument.id is not None
    assert db_instrument.symbol == "AAPL"
    assert db_instrument.name == "Apple Inc."

def test_get_instrument_by_symbol(db_session):
    """
    Tests retrieving an instrument by its symbol.
    """
    instrument_create = schemas.InstrumentCreate(symbol="GOOGL", name="Alphabet Inc.", asset_class="Stock")
    repository.create_instrument(db=db_session, instrument=instrument_create)

    db_instrument = repository.get_instrument_by_symbol(db=db_session, symbol="GOOGL")
    assert db_instrument is not None
    assert db_instrument.symbol == "GOOGL"

    db_instrument_none = repository.get_instrument_by_symbol(db=db_session, symbol="MSFT")
    assert db_instrument_none is None

def test_get_instruments(db_session):
    """
    Tests retrieving a list of all instruments.
    """
    repository.create_instrument(db=db_session, instrument=schemas.InstrumentCreate(symbol="TSLA", name="Tesla, Inc.", asset_class="Stock"))
    repository.create_instrument(db=db_session, instrument=schemas.InstrumentCreate(symbol="AMZN", name="Amazon.com, Inc.", asset_class="Stock"))

    instruments = repository.get_instruments(db=db_session)
    assert len(instruments) == 2
    assert instruments[0].symbol == "TSLA"
    assert instruments[1].symbol == "AMZN"

def test_bulk_create_market_data(db_session):
    """
    Tests the bulk creation of market data.
    """
    instrument = repository.create_instrument(db=db_session, instrument=schemas.InstrumentCreate(symbol="EURUSD", name="Euro/US Dollar", asset_class="FX"))

    market_data_list = [
        schemas.MarketDataCreate(instrument_id=instrument.id, date=date(2023, 1, 1), open=1.1, high=1.2, low=1.0, close=1.15, volume=1000),
        schemas.MarketDataCreate(instrument_id=instrument.id, date=date(2023, 1, 2), open=1.15, high=1.25, low=1.12, close=1.2, volume=1200),
    ]

    created_data = repository.bulk_create_market_data(db=db_session, market_data_list=market_data_list)
    assert len(created_data) == 2
    assert created_data[0].id is not None
    assert created_data[1].date == date(2023, 1, 2)

def test_get_market_data_for_instrument(db_session):
    """
    Tests retrieving market data for an instrument, including date filtering.
    """
    instrument = repository.create_instrument(db=db_session, instrument=schemas.InstrumentCreate(symbol="BTCUSD", name="Bitcoin/US Dollar", asset_class="Crypto"))

    market_data_list = [
        schemas.MarketDataCreate(instrument_id=instrument.id, date=date(2023, 1, 1), open=40000, high=42000, low=39000, close=41000, volume=500),
        schemas.MarketDataCreate(instrument_id=instrument.id, date=date(2023, 1, 2), open=41000, high=43000, low=40500, close=42500, volume=600),
        schemas.MarketDataCreate(instrument_id=instrument.id, date=date(2023, 1, 3), open=42500, high=44000, low=42000, close=43000, volume=700),
    ]
    repository.bulk_create_market_data(db=db_session, market_data_list=market_data_list)

    # Test getting all data
    all_data = repository.get_market_data_for_instrument(db=db_session, instrument_id=instrument.id)
    assert len(all_data) == 3

    # Test filtering by date range
    filtered_data = repository.get_market_data_for_instrument(db=db_session, instrument_id=instrument.id, start_date=date(2023, 1, 2), end_date=date(2023, 1, 2))
    assert len(filtered_data) == 1
    assert filtered_data[0].date == date(2023, 1, 2)
