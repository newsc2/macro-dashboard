"""
Market Data Ingestion - Multi-Source Version
Uses Yahoo Finance API directly + CoinGecko for crypto
More reliable than yfinance library
"""

import requests
from datetime import datetime, timedelta
import logging
import time

from main import (
    get_db_context,
    Indicator, IndicatorMetadata, RefreshLog
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Stock/ETF tickers (Yahoo Finance)
STOCK_INDICATORS = {
    "SPY": {
        "name": "S&P 500 ETF",
        "category": "market",
        "subcategory": "equity",
        "unit": "price",
        "description": "SPDR S&P 500 ETF Trust"
    },
    "QQQ": {
        "name": "Nasdaq 100 ETF",
        "category": "market",
        "subcategory": "equity",
        "unit": "price",
        "description": "Invesco QQQ Trust (Nasdaq 100)"
    },
    "VTI": {
        "name": "Total Stock Market ETF",
        "category": "market",
        "subcategory": "equity",
        "unit": "price",
        "description": "Vanguard Total Stock Market ETF (similar to VTSAX)"
    },
    "^VIX": {
        "name": "VIX",
        "category": "sentiment",
        "subcategory": "volatility",
        "unit": "index",
        "description": "CBOE Volatility Index"
    },
    "^GSPC": {
        "name": "S&P 500 Index",
        "category": "market",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Index"
    },
    "^DJI": {
        "name": "Dow Jones",
        "category": "market",
        "subcategory": "equity",
        "unit": "index",
        "description": "Dow Jones Industrial Average"
    },
    "^IXIC": {
        "name": "NASDAQ Composite",
        "category": "market",
        "subcategory": "equity",
        "unit": "index",
        "description": "NASDAQ Composite Index"
    },
    "GLD": {
        "name": "Gold ETF",
        "category": "market",
        "subcategory": "commodities",
        "unit": "price",
        "description": "SPDR Gold Shares"
    },
    "TLT": {
        "name": "20Y Treasury ETF",
        "category": "market",
        "subcategory": "bonds",
        "unit": "price",
        "description": "iShares 20+ Year Treasury Bond ETF"
    },

    # S&P 500 Sector ETFs (for sector rotation analysis)
    "XLK": {
        "name": "Technology",
        "category": "sector",
        "subcategory": "equity",
        "unit": "price",
        "description": "Technology Select Sector SPDR Fund"
    },
    "XLF": {
        "name": "Financials",
        "category": "sector",
        "subcategory": "equity",
        "unit": "price",
        "description": "Financial Select Sector SPDR Fund"
    },
    "XLE": {
        "name": "Energy",
        "category": "sector",
        "subcategory": "equity",
        "unit": "price",
        "description": "Energy Select Sector SPDR Fund"
    },
    "XLV": {
        "name": "Health Care",
        "category": "sector",
        "subcategory": "equity",
        "unit": "price",
        "description": "Health Care Select Sector SPDR Fund"
    },
    "XLY": {
        "name": "Consumer Discretionary",
        "category": "sector",
        "subcategory": "equity",
        "unit": "price",
        "description": "Consumer Discretionary Select Sector SPDR Fund"
    },
    "XLP": {
        "name": "Consumer Staples",
        "category": "sector",
        "subcategory": "equity",
        "unit": "price",
        "description": "Consumer Staples Select Sector SPDR Fund"
    },
    "XLI": {
        "name": "Industrials",
        "category": "sector",
        "subcategory": "equity",
        "unit": "price",
        "description": "Industrials Select Sector SPDR Fund"
    },
    "XLB": {
        "name": "Materials",
        "category": "sector",
        "subcategory": "equity",
        "unit": "price",
        "description": "Materials Select Sector SPDR Fund"
    },
    "XLU": {
        "name": "Utilities",
        "category": "sector",
        "subcategory": "equity",
        "unit": "price",
        "description": "Utilities Select Sector SPDR Fund"
    },
    "XLRE": {
        "name": "Real Estate",
        "category": "sector",
        "subcategory": "equity",
        "unit": "price",
        "description": "Real Estate Select Sector SPDR Fund"
    },
    "XLC": {
        "name": "Communication Services",
        "category": "sector",
        "subcategory": "equity",
        "unit": "price",
        "description": "Communication Services Select Sector SPDR Fund"
    },

    # S&P 500 Sector Indices (longer history than ETFs - back to 1993)
    "^SP500-45": {
        "name": "S&P 500 Technology Index",
        "category": "sector_index",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Information Technology Sector Index"
    },
    "^SP500-40": {
        "name": "S&P 500 Financials Index",
        "category": "sector_index",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Financials Sector Index"
    },
    "^SP500-35": {
        "name": "S&P 500 Health Care Index",
        "category": "sector_index",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Health Care Sector Index"
    },
    "^SP500-25": {
        "name": "S&P 500 Consumer Discretionary Index",
        "category": "sector_index",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Consumer Discretionary Sector Index"
    },
    "^SP500-20": {
        "name": "S&P 500 Industrials Index",
        "category": "sector_index",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Industrials Sector Index"
    },
    "^SP500-30": {
        "name": "S&P 500 Consumer Staples Index",
        "category": "sector_index",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Consumer Staples Sector Index"
    },
    "^SP500-55": {
        "name": "S&P 500 Utilities Index",
        "category": "sector_index",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Utilities Sector Index"
    },
    "^SP500-15": {
        "name": "S&P 500 Materials Index",
        "category": "sector_index",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Materials Sector Index"
    },
    "^SP500-60": {
        "name": "S&P 500 Real Estate Index",
        "category": "sector_index",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Real Estate Sector Index"
    },
    "^SP500-50": {
        "name": "S&P 500 Communication Services Index",
        "category": "sector_index",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Communication Services Sector Index"
    },

    # Style & Size ETFs (for market regime analysis)
    "IWM": {
        "name": "Russell 2000 (Small Cap)",
        "category": "market",
        "subcategory": "equity",
        "unit": "price",
        "description": "iShares Russell 2000 ETF"
    },
    "IWF": {
        "name": "Russell 1000 Growth",
        "category": "market",
        "subcategory": "equity",
        "unit": "price",
        "description": "iShares Russell 1000 Growth ETF"
    },
    "IWD": {
        "name": "Russell 1000 Value",
        "category": "market",
        "subcategory": "equity",
        "unit": "price",
        "description": "iShares Russell 1000 Value ETF"
    },
    "EEM": {
        "name": "Emerging Markets",
        "category": "market",
        "subcategory": "equity",
        "unit": "price",
        "description": "iShares MSCI Emerging Markets ETF"
    },
    "EFA": {
        "name": "Developed Markets ex-US",
        "category": "market",
        "subcategory": "equity",
        "unit": "price",
        "description": "iShares MSCI EAFE ETF"
    },

    # Fixed Income (for yield curve / liquidity)
    "SHY": {
        "name": "1-3Y Treasury ETF",
        "category": "market",
        "subcategory": "bonds",
        "unit": "price",
        "description": "iShares 1-3 Year Treasury Bond ETF"
    },
    "IEF": {
        "name": "7-10Y Treasury ETF",
        "category": "market",
        "subcategory": "bonds",
        "unit": "price",
        "description": "iShares 7-10 Year Treasury Bond ETF"
    },
    "HYG": {
        "name": "High Yield Corporate Bond",
        "category": "market",
        "subcategory": "bonds",
        "unit": "price",
        "description": "iShares iBoxx High Yield Corporate Bond ETF"
    },
    "LQD": {
        "name": "Investment Grade Corporate",
        "category": "market",
        "subcategory": "bonds",
        "unit": "price",
        "description": "iShares iBoxx Investment Grade Corporate Bond ETF"
    },

    # === Additional ETFs for Comprehensive Market Overview ===

    # Market Breadth - Equal Weight
    "RSP": {
        "name": "S&P 500 Equal Weight",
        "category": "market",
        "subcategory": "equity",
        "unit": "price",
        "description": "Invesco S&P 500 Equal Weight ETF - breadth indicator"
    },

    # Style & Factor ETFs
    "VUG": {
        "name": "Vanguard Growth",
        "category": "factor",
        "subcategory": "style",
        "unit": "price",
        "description": "Vanguard Growth ETF"
    },
    "VTV": {
        "name": "Vanguard Value",
        "category": "factor",
        "subcategory": "style",
        "unit": "price",
        "description": "Vanguard Value ETF"
    },
    "MTUM": {
        "name": "Momentum Factor",
        "category": "factor",
        "subcategory": "style",
        "unit": "price",
        "description": "iShares MSCI USA Momentum Factor ETF"
    },
    "QUAL": {
        "name": "Quality Factor",
        "category": "factor",
        "subcategory": "style",
        "unit": "price",
        "description": "iShares MSCI USA Quality Factor ETF"
    },
    "USMV": {
        "name": "Low Volatility",
        "category": "factor",
        "subcategory": "style",
        "unit": "price",
        "description": "iShares MSCI USA Min Vol Factor ETF"
    },
    "SIZE": {
        "name": "Size Factor",
        "category": "factor",
        "subcategory": "style",
        "unit": "price",
        "description": "iShares MSCI USA Size Factor ETF"
    },

    # International Markets
    "VGK": {
        "name": "Europe ETF",
        "category": "international",
        "subcategory": "developed",
        "unit": "price",
        "description": "Vanguard FTSE Europe ETF"
    },
    "EWJ": {
        "name": "Japan ETF",
        "category": "international",
        "subcategory": "developed",
        "unit": "price",
        "description": "iShares MSCI Japan ETF"
    },
    "EWU": {
        "name": "United Kingdom ETF",
        "category": "international",
        "subcategory": "developed",
        "unit": "price",
        "description": "iShares MSCI United Kingdom ETF"
    },
    "EWG": {
        "name": "Germany ETF",
        "category": "international",
        "subcategory": "developed",
        "unit": "price",
        "description": "iShares MSCI Germany ETF"
    },
    "FXI": {
        "name": "China Large Cap",
        "category": "international",
        "subcategory": "emerging",
        "unit": "price",
        "description": "iShares China Large-Cap ETF"
    },
    "MCHI": {
        "name": "China ETF",
        "category": "international",
        "subcategory": "emerging",
        "unit": "price",
        "description": "iShares MSCI China ETF"
    },
    "INDA": {
        "name": "India ETF",
        "category": "international",
        "subcategory": "emerging",
        "unit": "price",
        "description": "iShares MSCI India ETF"
    },
    "EWZ": {
        "name": "Brazil ETF",
        "category": "international",
        "subcategory": "emerging",
        "unit": "price",
        "description": "iShares MSCI Brazil ETF"
    },
    "VWO": {
        "name": "Vanguard Emerging Markets",
        "category": "international",
        "subcategory": "emerging",
        "unit": "price",
        "description": "Vanguard FTSE Emerging Markets ETF"
    },

    # Fixed Income - Additional
    "TIP": {
        "name": "TIPS ETF",
        "category": "market",
        "subcategory": "bonds",
        "unit": "price",
        "description": "iShares TIPS Bond ETF - inflation-protected"
    },
    "MUB": {
        "name": "Municipal Bonds",
        "category": "market",
        "subcategory": "bonds",
        "unit": "price",
        "description": "iShares National Muni Bond ETF"
    },
    "AGG": {
        "name": "US Aggregate Bond",
        "category": "market",
        "subcategory": "bonds",
        "unit": "price",
        "description": "iShares Core US Aggregate Bond ETF"
    },
    "BND": {
        "name": "Vanguard Total Bond",
        "category": "market",
        "subcategory": "bonds",
        "unit": "price",
        "description": "Vanguard Total Bond Market ETF"
    },
    "JNK": {
        "name": "High Yield Bond",
        "category": "market",
        "subcategory": "bonds",
        "unit": "price",
        "description": "SPDR Bloomberg High Yield Bond ETF"
    },
    "EMB": {
        "name": "Emerging Market Bonds",
        "category": "market",
        "subcategory": "bonds",
        "unit": "price",
        "description": "iShares JP Morgan USD Emerging Markets Bond ETF"
    },

    # Volatility
    "^VIX9D": {
        "name": "VIX 9-Day",
        "category": "sentiment",
        "subcategory": "volatility",
        "unit": "index",
        "description": "CBOE 9-Day Volatility Index"
    },
    "^VIX3M": {
        "name": "VIX 3-Month",
        "category": "sentiment",
        "subcategory": "volatility",
        "unit": "index",
        "description": "CBOE 3-Month Volatility Index"
    },
    "UVXY": {
        "name": "Ultra VIX Short-Term",
        "category": "sentiment",
        "subcategory": "volatility",
        "unit": "price",
        "description": "ProShares Ultra VIX Short-Term Futures ETF"
    },

    # Commodities
    "SLV": {
        "name": "Silver ETF",
        "category": "market",
        "subcategory": "commodities",
        "unit": "price",
        "description": "iShares Silver Trust"
    },
    "USO": {
        "name": "Oil ETF",
        "category": "market",
        "subcategory": "commodities",
        "unit": "price",
        "description": "United States Oil Fund"
    },
    "DBA": {
        "name": "Agriculture ETF",
        "category": "market",
        "subcategory": "commodities",
        "unit": "price",
        "description": "Invesco DB Agriculture Fund"
    },
    "DBC": {
        "name": "Commodities Broad",
        "category": "market",
        "subcategory": "commodities",
        "unit": "price",
        "description": "Invesco DB Commodity Index Tracking Fund"
    },
    "COPX": {
        "name": "Copper Miners",
        "category": "market",
        "subcategory": "commodities",
        "unit": "price",
        "description": "Global X Copper Miners ETF"
    },

    # Real Estate
    "VNQ": {
        "name": "Vanguard Real Estate",
        "category": "market",
        "subcategory": "real_estate",
        "unit": "price",
        "description": "Vanguard Real Estate ETF (REITs)"
    },
    "IYR": {
        "name": "iShares Real Estate",
        "category": "market",
        "subcategory": "real_estate",
        "unit": "price",
        "description": "iShares US Real Estate ETF"
    },

    # Dollar Index
    "UUP": {
        "name": "US Dollar Index ETF",
        "category": "market",
        "subcategory": "currency",
        "unit": "price",
        "description": "Invesco DB US Dollar Index Bullish Fund"
    },
    "DXY": {
        "name": "DXY Dollar Index",
        "category": "market",
        "subcategory": "currency",
        "unit": "index",
        "description": "US Dollar Index"
    },
}

# Crypto tickers (Yahoo Finance - more history than CoinGecko free tier)
CRYPTO_INDICATORS = {
    "BTC-USD": {
        "name": "Bitcoin",
        "category": "crypto",
        "subcategory": "cryptocurrency",
        "unit": "usd",
        "description": "Bitcoin price in USD"
    },
    "ETH-USD": {
        "name": "Ethereum",
        "category": "crypto",
        "subcategory": "cryptocurrency",
        "unit": "usd",
        "description": "Ethereum price in USD"
    },
}


def fetch_yahoo_data(symbol: str, days_back: int = 365 * 30) -> list:
    """
    Fetch historical data from Yahoo Finance API directly.
    More reliable than yfinance library.
    Uses period1=0 to get maximum available history.
    """
    end_time = int(datetime.now().timestamp())
    # Use 0 as start time to get all available history
    start_time = 0

    # Yahoo Finance chart API
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {
        "period1": start_time,
        "period2": end_time,
        "interval": "1d",
        "events": "history"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        result = data.get("chart", {}).get("result", [])
        if not result:
            return []

        chart_data = result[0]
        timestamps = chart_data.get("timestamp", [])
        quotes = chart_data.get("indicators", {}).get("quote", [{}])[0]
        closes = quotes.get("close", [])

        records = []
        for i, ts in enumerate(timestamps):
            if closes[i] is not None:
                records.append({
                    "timestamp": datetime.fromtimestamp(ts),
                    "value": closes[i]
                })

        return records

    except Exception as e:
        logger.warning(f"Yahoo Finance error for {symbol}: {str(e)}")
        return []


def fetch_coingecko_data(coin_id: str, days_back: int = 365 * 10) -> list:
    """
    Fetch historical data from CoinGecko API (free, no key needed).
    Free tier supports up to ~365 days with daily interval, or more with auto interval.
    We'll request a large number and let it return what it can.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"

    # CoinGecko free tier limits to ~365 days with daily granularity
    # For more history, would need paid API ($129/mo Demo plan)
    params = {
        "vs_currency": "usd",
        "days": 365,
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=60)
        response.raise_for_status()
        data = response.json()

        prices = data.get("prices", [])
        records = []

        for ts_ms, price in prices:
            records.append({
                "timestamp": datetime.fromtimestamp(ts_ms / 1000),
                "value": price
            })

        return records

    except Exception as e:
        logger.warning(f"CoinGecko error for {coin_id}: {str(e)}")
        return []


def ingest_market_data(years_back: int = 10):
    """
    Ingest market data from multiple sources.
    Default 10 years for stocks, max available for crypto.
    """
    days_back = years_back * 365
    success_count = 0
    error_count = 0

    logger.info("=" * 60)
    logger.info("MARKET DATA INGESTION")
    logger.info("Sources: Yahoo Finance (stocks/ETFs) + CoinGecko (crypto)")
    logger.info("=" * 60)

    with get_db_context() as db:
        # === STOCKS & ETFs from Yahoo Finance ===
        logger.info("\n--- Stocks & ETFs (Yahoo Finance) ---")

        for symbol, metadata in STOCK_INDICATORS.items():
            logger.info(f"Fetching {symbol}: {metadata['name']}")

            records = fetch_yahoo_data(symbol, days_back)

            if not records:
                logger.warning(f"  No data for {symbol}")
                error_count += 1

                # Log the error
                log = RefreshLog(
                    source="YAHOO_FINANCE",
                    indicator_id=symbol,
                    records_added=0,
                    status="error",
                    error_message="No data returned from Yahoo Finance"
                )
                db.add(log)
                db.commit()
                continue

            logger.info(f"  Fetched {len(records)} records")

            # Save metadata
            existing = db.query(IndicatorMetadata).filter(
                IndicatorMetadata.indicator_id == symbol
            ).first()

            if not existing:
                meta_obj = IndicatorMetadata(
                    indicator_id=symbol,
                    source="YAHOO_FINANCE",
                    typical_frequency="daily",
                    **metadata
                )
                db.add(meta_obj)
                db.commit()

            # Save time series
            records_added = 0
            for record in records:
                existing_data = db.query(Indicator).filter(
                    Indicator.indicator_id == symbol,
                    Indicator.timestamp == record["timestamp"]
                ).first()

                if not existing_data:
                    indicator = Indicator(
                        indicator_id=symbol,
                        timestamp=record["timestamp"],
                        value=float(record["value"]),
                        source="YAHOO_FINANCE",
                        frequency="daily"
                    )
                    db.add(indicator)
                    records_added += 1

            db.commit()

            # Log success
            log = RefreshLog(
                source="YAHOO_FINANCE",
                indicator_id=symbol,
                records_added=records_added,
                status="success"
            )
            db.add(log)
            db.commit()

            logger.info(f"  Added {records_added} new records")
            success_count += 1

            # Rate limiting - be nice to Yahoo
            time.sleep(0.5)

        # === CRYPTO from Yahoo Finance ===
        logger.info("\n--- Cryptocurrency (Yahoo Finance) ---")

        for symbol, metadata in CRYPTO_INDICATORS.items():
            logger.info(f"Fetching {symbol}: {metadata['name']}")

            records = fetch_yahoo_data(symbol, days_back)

            if not records:
                logger.warning(f"  No data for {symbol}")
                error_count += 1

                log = RefreshLog(
                    source="YAHOO_FINANCE",
                    indicator_id=symbol,
                    records_added=0,
                    status="error",
                    error_message="No data returned from Yahoo Finance"
                )
                db.add(log)
                db.commit()
                continue

            logger.info(f"  Fetched {len(records)} records")

            # Save metadata
            existing = db.query(IndicatorMetadata).filter(
                IndicatorMetadata.indicator_id == symbol
            ).first()

            if not existing:
                meta_obj = IndicatorMetadata(
                    indicator_id=symbol,
                    source="YAHOO_FINANCE",
                    typical_frequency="daily",
                    **metadata
                )
                db.add(meta_obj)
                db.commit()

            # Save time series
            records_added = 0
            for record in records:
                existing_data = db.query(Indicator).filter(
                    Indicator.indicator_id == symbol,
                    Indicator.timestamp == record["timestamp"]
                ).first()

                if not existing_data:
                    indicator = Indicator(
                        indicator_id=symbol,
                        timestamp=record["timestamp"],
                        value=float(record["value"]),
                        source="YAHOO_FINANCE",
                        frequency="daily"
                    )
                    db.add(indicator)
                    records_added += 1

            db.commit()

            # Log success
            log = RefreshLog(
                source="YAHOO_FINANCE",
                indicator_id=symbol,
                records_added=records_added,
                status="success"
            )
            db.add(log)
            db.commit()

            logger.info(f"  Added {records_added} new records")
            success_count += 1

            time.sleep(0.5)

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info(f"COMPLETE: {success_count} successful, {error_count} failed")
    logger.info("=" * 60)


if __name__ == "__main__":
    logger.info("Starting market data ingestion...")
    # Fetch maximum available history (most sector ETFs go back to 1998-1999)
    ingest_market_data(years_back=30)
    logger.info("Done!")
