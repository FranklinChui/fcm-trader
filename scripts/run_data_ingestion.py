import argparse
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.features.data_ingestion import service

def main(symbols: list[str], db_session: Session):
    """
    Main function to run the data ingestion for a list of symbols.
    """
    for symbol in symbols:
        try:
            print(f"--- Ingesting data for {symbol} ---")
            service.ingest_data_for_symbol(db=db_session, symbol=symbol)
            print(f"--- Finished ingestion for {symbol} ---")
        except Exception as e:
            print(f"Failed to ingest data for {symbol}. Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run data ingestion for specified symbols.")
    parser.add_argument(
        "symbols",
        nargs="+",
        help="A list of symbols to ingest data for (e.g., AAPL GOOGL)."
    )
    args = parser.parse_args()

    db = SessionLocal()
    try:
        main(symbols=args.symbols, db_session=db)
    finally:
        db.close()
