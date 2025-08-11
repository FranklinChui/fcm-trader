import pytest
from unittest.mock import patch, MagicMock
from datetime import date, timedelta
from sqlalchemy.orm import Session

from app.features.data_ingestion import service, schemas, models

# Mock database session fixture from the repository tests
# This avoids redefining the same setup/teardown logic
from tests.features.data_ingestion.test_repository import db_session

@patch('app.features.data_ingestion.service.repository')
def test_ingest_data_for_new_instrument(mock_repo, db_session: Session):
    """
    Test ingesting data for a symbol that is not yet in the database.
    It should create the instrument and then save the market data.
    """
    # --- Arrange ---
    symbol = "NEWCOIN"
    mock_api_data = [
        {'date': date.today() - timedelta(days=1), 'open': 100, 'high': 110, 'low': 99, 'close': 105, 'volume': 10000},
        {'date': date.today(), 'open': 105, 'high': 115, 'low': 103, 'close': 110, 'volume': 12000},
    ]

    # Mock the external API call within the service
    with patch('app.features.data_ingestion.service.fetch_data_from_source', return_value=mock_api_data):
        # Mock repository responses
        mock_repo.get_instrument_by_symbol.return_value = None

        # Mock the instrument creation to return an object with an ID
        created_instrument = models.Instrument(id=1, symbol=symbol, name=f"{symbol} Name", asset_class="Crypto")
        mock_repo.create_instrument.return_value = created_instrument

        # --- Act ---
        service.ingest_data_for_symbol(db=db_session, symbol=symbol)

        # --- Assert ---
        # Verify that we checked if the instrument exists
        mock_repo.get_instrument_by_symbol.assert_called_once()
        assert mock_repo.get_instrument_by_symbol.call_args[1]['symbol'] == symbol

        # Verify that a new instrument was created
        mock_repo.create_instrument.assert_called_once()

        # Verify that the market data was saved
        mock_repo.bulk_create_market_data.assert_called_once()
        call_args = mock_repo.bulk_create_market_data.call_args[1]
        assert len(call_args['market_data_list']) == 2
        assert call_args['market_data_list'][0].close == 105

@patch('app.features.data_ingestion.service.repository')
def test_ingest_data_for_existing_instrument(mock_repo, db_session: Session):
    """
    Test ingesting data for an instrument that already exists.
    It should NOT create a new instrument.
    """
    # --- Arrange ---
    symbol = "OLDCOIN"
    existing_instrument = models.Instrument(id=2, symbol=symbol, name=f"{symbol} Name", asset_class="Crypto")
    mock_api_data = [
        {'date': date.today(), 'open': 200, 'high': 210, 'low': 199, 'close': 205, 'volume': 5000},
    ]

    with patch('app.features.data_ingestion.service.fetch_data_from_source', return_value=mock_api_data):
        mock_repo.get_instrument_by_symbol.return_value = existing_instrument

        # --- Act ---
        service.ingest_data_for_symbol(db=db_session, symbol=symbol)

        # --- Assert ---
        mock_repo.get_instrument_by_symbol.assert_called_once()
        assert mock_repo.get_instrument_by_symbol.call_args[1]['symbol'] == symbol

        # Ensure create_instrument was NOT called
        mock_repo.create_instrument.assert_not_called()

        # Verify market data was still saved
        mock_repo.bulk_create_market_data.assert_called_once()
        assert len(mock_repo.bulk_create_market_data.call_args[1]['market_data_list']) == 1

@patch('app.features.data_ingestion.service.repository')
def test_ingestion_fails_if_api_fails(mock_repo, db_session: Session):
    """
    Test that no data is written if the external API call fails.
    """
    # --- Arrange ---
    symbol = "FAILCOIN"
    with patch('app.features.data_ingestion.service.fetch_data_from_source', side_effect=Exception("API is down")):

        # --- Act & Assert ---
        with pytest.raises(Exception, match="API is down"):
            service.ingest_data_for_symbol(db=db_session, symbol=symbol)

        # Verify no database writes were attempted
        mock_repo.create_instrument.assert_not_called()
        mock_repo.bulk_create_market_data.assert_not_called()

@patch('app.features.data_ingestion.service.repository')
def test_ingestion_handles_no_new_data(mock_repo, db_session: Session):
    """
    Test that the service handles the case where the API returns no data.
    """
    # --- Arrange ---
    symbol = "NODATACOIN"
    with patch('app.features.data_ingestion.service.fetch_data_from_source', return_value=[]):

        # --- Act ---
        service.ingest_data_for_symbol(db=db_session, symbol=symbol)

        # --- Assert ---
        # Verify no database writes were attempted
        mock_repo.create_instrument.assert_not_called()
        mock_repo.bulk_create_market_data.assert_not_called()
