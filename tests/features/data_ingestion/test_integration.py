import pytest
from unittest.mock import patch
from datetime import date, timedelta
from sqlalchemy.orm import Session

# Import the fixture for the database session
from .test_repository import db_session

from app.features.data_ingestion import repository
# We will import the script's main function later, once it's created
# from scripts import run_data_ingestion

@patch('app.features.data_ingestion.service.fetch_data_from_source')
def test_run_data_ingestion_integration(mock_fetch, db_session: Session):
    """
    Integration test for the data ingestion script.
    It verifies that running the script correctly fetches, processes,
    and saves data to the database.
    """
    # --- Arrange ---
    # This is the data we want our mocked API to return
    symbol = "INTEGTEST"
    mock_api_data = [
        {'date': date.today(), 'open': 500, 'high': 510, 'low': 490, 'close': 505, 'volume': 777},
    ]
    mock_fetch.return_value = mock_api_data

    # Dynamically import the script's main function to avoid import errors
    # if the script doesn't exist yet.
    from scripts import run_data_ingestion

    # --- Act ---
    # Run the main function of the script
    run_data_ingestion.main(symbols=[symbol], db_session=db_session)

    # --- Assert ---
    # Verify the data was written to the database correctly
    instrument = repository.get_instrument_by_symbol(db=db_session, symbol=symbol)
    assert instrument is not None
    assert instrument.symbol == symbol

    market_data = repository.get_market_data_for_instrument(db=db_session, instrument_id=instrument.id)
    assert len(market_data) == 1
    assert market_data[0].close == 505
    assert market_data[0].volume == 777
