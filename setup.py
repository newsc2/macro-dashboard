#!/usr/bin/env python3
"""
Setup Script - Initialize database and load data
"""

import logging
from main import Base, engine
from ingest_fred import ingest_fred_data
from ingest_market import ingest_market_data

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Run setup"""
    print("\n" + "="*60)
    print("MACRO DASHBOARD SETUP")
    print("="*60 + "\n")
    
    try:
        # Create tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Tables created\n")
        
        # Load FRED data
        logger.info("Loading FRED data (this takes 5-10 minutes)...")
        ingest_fred_data(years_back=10)
        logger.info("✓ FRED data loaded\n")
        
        # Load market data
        logger.info("Loading market data...")
        ingest_market_data(years_back=10)
        logger.info("✓ Market data loaded\n")
        
        print("="*60)
        print("SETUP COMPLETE!")
        print("="*60)
        print("\nYour API is already running at:")
        print("  http://localhost:8000/docs")
        print("\nTry these endpoints:")
        print("  http://localhost:8000/api/dashboards/recession-watch")
        print("  http://localhost:8000/api/indicators")
        print("\n")
        
    except Exception as e:
        logger.error(f"Setup failed: {str(e)}")
        print("\n❌ Setup failed. Check the error above.")
        raise


if __name__ == "__main__":
    main()
