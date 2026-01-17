"""
FRED Data Ingestion - Simplified Version
"""

from fredapi import Fred
from datetime import datetime, timedelta
import pandas as pd
import logging
import os

# Import from main.py
from main import (
    settings, get_db_context, 
    Indicator, IndicatorMetadata, RefreshLog
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FRED Indicators to track
FRED_INDICATORS = {
    # GDP & Growth
    "GDP": {
        "name": "Gross Domestic Product",
        "category": "economy",
        "subcategory": "growth",
        "unit": "billions_usd",
        "description": "Total value of goods and services"
    },
    "GDPC1": {
        "name": "Real GDP",
        "category": "economy",
        "subcategory": "growth",
        "unit": "billions_2017_usd",
        "description": "Inflation-adjusted GDP"
    },
    
    # Employment
    "UNRATE": {
        "name": "Unemployment Rate",
        "category": "economy",
        "subcategory": "employment",
        "unit": "percent",
        "description": "Civilian unemployment rate"
    },
    "PAYEMS": {
        "name": "Nonfarm Payrolls",
        "category": "economy",
        "subcategory": "employment",
        "unit": "thousands",
        "description": "Total nonfarm employment"
    },
    
    # Inflation
    "CPIAUCSL": {
        "name": "Consumer Price Index",
        "category": "economy",
        "subcategory": "inflation",
        "unit": "index",
        "description": "CPI measure"
    },
    "PCEPI": {
        "name": "PCE Price Index",
        "category": "economy",
        "subcategory": "inflation",
        "unit": "index",
        "description": "Fed's preferred inflation measure"
    },
    
    # Interest Rates
    "DFF": {
        "name": "Federal Funds Rate",
        "category": "economy",
        "subcategory": "monetary",
        "unit": "percent",
        "description": "Overnight lending rate"
    },
    "DGS10": {
        "name": "10-Year Treasury Rate",
        "category": "economy",
        "subcategory": "monetary",
        "unit": "percent",
        "description": "10-year rate"
    },
    "DGS2": {
        "name": "2-Year Treasury Rate",
        "category": "economy",
        "subcategory": "monetary",
        "unit": "percent",
        "description": "2-year rate"
    },
    "T10Y2Y": {
        "name": "10Y-2Y Yield Spread",
        "category": "economy",
        "subcategory": "monetary",
        "unit": "percent",
        "description": "Yield curve"
    },
    "M2SL": {
        "name": "M2 Money Supply",
        "category": "economy",
        "subcategory": "monetary",
        "unit": "billions_usd",
        "description": "Money supply"
    },
    
    # Housing
    "HOUST": {
        "name": "Housing Starts",
        "category": "economy",
        "subcategory": "housing",
        "unit": "thousands",
        "description": "New construction"
    },
    "MORTGAGE30US": {
        "name": "30-Year Mortgage Rate",
        "category": "economy",
        "subcategory": "housing",
        "unit": "percent",
        "description": "Average 30-year mortgage rate"
    },
    
    # Manufacturing & Sentiment
    "INDPRO": {
        "name": "Industrial Production",
        "category": "economy",
        "subcategory": "manufacturing",
        "unit": "index",
        "description": "Industrial output"
    },
    "UMCSENT": {
        "name": "Consumer Sentiment",
        "category": "sentiment",
        "subcategory": "consumer",
        "unit": "index",
        "description": "U Mich consumer sentiment"
    },
    "DCOILWTICO": {
        "name": "WTI Crude Oil",
        "category": "economy",
        "subcategory": "commodities",
        "unit": "dollars_per_barrel",
        "description": "Oil price"
    },

    # Recession Signals
    "ICSA": {
        "name": "Initial Jobless Claims",
        "category": "economy",
        "subcategory": "employment",
        "unit": "thousands",
        "description": "Weekly initial unemployment claims"
    },
    "CCSA": {
        "name": "Continued Jobless Claims",
        "category": "economy",
        "subcategory": "employment",
        "unit": "thousands",
        "description": "Continued unemployment claims"
    },
    "JTSJOL": {
        "name": "Job Openings (JOLTS)",
        "category": "economy",
        "subcategory": "employment",
        "unit": "thousands",
        "description": "Job openings from JOLTS survey"
    },

    # Consumer & Retail
    "RSAFS": {
        "name": "Retail Sales",
        "category": "economy",
        "subcategory": "consumer",
        "unit": "millions_usd",
        "description": "Total retail sales"
    },
    "PCE": {
        "name": "Personal Consumption Expenditures",
        "category": "economy",
        "subcategory": "consumer",
        "unit": "billions_usd",
        "description": "Total personal spending"
    },

    # Inflation
    "CPILFESL": {
        "name": "Core CPI",
        "category": "economy",
        "subcategory": "inflation",
        "unit": "index",
        "description": "CPI excluding food and energy"
    },
    "T10YIE": {
        "name": "10Y Breakeven Inflation",
        "category": "economy",
        "subcategory": "inflation",
        "unit": "percent",
        "description": "Market inflation expectations"
    },

    # Housing
    "PERMIT": {
        "name": "Building Permits",
        "category": "economy",
        "subcategory": "housing",
        "unit": "thousands",
        "description": "New housing permits issued"
    },

    # Credit & Risk
    "BAMLH0A0HYM2": {
        "name": "High Yield Spread",
        "category": "economy",
        "subcategory": "credit",
        "unit": "percent",
        "description": "High yield bond spread over treasury"
    },

    # Volatility
    "VIXCLS": {
        "name": "VIX (FRED)",
        "category": "sentiment",
        "subcategory": "volatility",
        "unit": "index",
        "description": "CBOE Volatility Index from FRED"
    },

    # Dollar & Trade
    "DTWEXBGS": {
        "name": "US Dollar Index",
        "category": "economy",
        "subcategory": "currency",
        "unit": "index",
        "description": "Trade-weighted dollar index"
    },
    "BOPGSTB": {
        "name": "Trade Balance",
        "category": "economy",
        "subcategory": "trade",
        "unit": "millions_usd",
        "description": "Trade balance goods and services"
    },

    # Federal Reserve
    "WALCL": {
        "name": "Fed Balance Sheet",
        "category": "economy",
        "subcategory": "monetary",
        "unit": "millions_usd",
        "description": "Total Fed assets"
    },
    "GFDEBTN": {
        "name": "Federal Debt",
        "category": "economy",
        "subcategory": "fiscal",
        "unit": "millions_usd",
        "description": "Total public debt"
    },

    # Full Yield Curve (for yield curve dashboard)
    "DGS1MO": {
        "name": "1-Month Treasury",
        "category": "economy",
        "subcategory": "yield_curve",
        "unit": "percent",
        "description": "1-Month Treasury Constant Maturity Rate"
    },
    "DGS3MO": {
        "name": "3-Month Treasury",
        "category": "economy",
        "subcategory": "yield_curve",
        "unit": "percent",
        "description": "3-Month Treasury Constant Maturity Rate"
    },
    "DGS6MO": {
        "name": "6-Month Treasury",
        "category": "economy",
        "subcategory": "yield_curve",
        "unit": "percent",
        "description": "6-Month Treasury Constant Maturity Rate"
    },
    "DGS1": {
        "name": "1-Year Treasury",
        "category": "economy",
        "subcategory": "yield_curve",
        "unit": "percent",
        "description": "1-Year Treasury Constant Maturity Rate"
    },
    "DGS5": {
        "name": "5-Year Treasury",
        "category": "economy",
        "subcategory": "yield_curve",
        "unit": "percent",
        "description": "5-Year Treasury Constant Maturity Rate"
    },
    "DGS7": {
        "name": "7-Year Treasury",
        "category": "economy",
        "subcategory": "yield_curve",
        "unit": "percent",
        "description": "7-Year Treasury Constant Maturity Rate"
    },
    "DGS20": {
        "name": "20-Year Treasury",
        "category": "economy",
        "subcategory": "yield_curve",
        "unit": "percent",
        "description": "20-Year Treasury Constant Maturity Rate"
    },
    "DGS30": {
        "name": "30-Year Treasury",
        "category": "economy",
        "subcategory": "yield_curve",
        "unit": "percent",
        "description": "30-Year Treasury Constant Maturity Rate"
    },

    # Liquidity & Credit Conditions
    "TOTRESNS": {
        "name": "Bank Reserves",
        "category": "economy",
        "subcategory": "liquidity",
        "unit": "billions_usd",
        "description": "Total Reserves of Depository Institutions"
    },
    "RRPONTSYD": {
        "name": "Reverse Repo",
        "category": "economy",
        "subcategory": "liquidity",
        "unit": "billions_usd",
        "description": "Overnight Reverse Repurchase Agreements"
    },
    "WTREGEN": {
        "name": "Treasury General Account",
        "category": "economy",
        "subcategory": "liquidity",
        "unit": "millions_usd",
        "description": "Treasury General Account at Fed"
    },
    "SOFR": {
        "name": "SOFR Rate",
        "category": "economy",
        "subcategory": "liquidity",
        "unit": "percent",
        "description": "Secured Overnight Financing Rate"
    },

    # CPI Components (Consumer Baskets)
    "CUSR0000SAF11": {
        "name": "CPI: Food at Home",
        "category": "inflation",
        "subcategory": "cpi_component",
        "unit": "index",
        "description": "CPI for food consumed at home (groceries)"
    },
    "CUSR0000SEFV": {
        "name": "CPI: Food Away from Home",
        "category": "inflation",
        "subcategory": "cpi_component",
        "unit": "index",
        "description": "CPI for restaurants and takeout"
    },
    "CUSR0000SAH1": {
        "name": "CPI: Shelter",
        "category": "inflation",
        "subcategory": "cpi_component",
        "unit": "index",
        "description": "CPI for housing/rent"
    },
    "CUSR0000SETA01": {
        "name": "CPI: New Vehicles",
        "category": "inflation",
        "subcategory": "cpi_component",
        "unit": "index",
        "description": "CPI for new cars and trucks"
    },
    "CUSR0000SETA02": {
        "name": "CPI: Used Vehicles",
        "category": "inflation",
        "subcategory": "cpi_component",
        "unit": "index",
        "description": "CPI for used cars and trucks"
    },
    "CUUR0000SETB01": {
        "name": "CPI: Gasoline",
        "category": "inflation",
        "subcategory": "cpi_component",
        "unit": "index",
        "description": "CPI for gasoline (all types)"
    },
    "CUSR0000SAM2": {
        "name": "CPI: Medical Care Services",
        "category": "inflation",
        "subcategory": "cpi_component",
        "unit": "index",
        "description": "CPI for medical care services"
    },
    "CUSR0000SEEB": {
        "name": "CPI: Electricity",
        "category": "inflation",
        "subcategory": "cpi_component",
        "unit": "index",
        "description": "CPI for electricity"
    },
    "CPIAPPSL": {
        "name": "CPI: Apparel",
        "category": "inflation",
        "subcategory": "cpi_component",
        "unit": "index",
        "description": "CPI for clothing and apparel"
    },
    "CUSR0000SEEE": {
        "name": "CPI: Utility Gas",
        "category": "inflation",
        "subcategory": "cpi_component",
        "unit": "index",
        "description": "CPI for utility (piped) gas service"
    },

    # PCE Categories (Personal Spending)
    "PCEDG": {
        "name": "PCE: Durable Goods",
        "category": "spending",
        "subcategory": "pce_component",
        "unit": "billions_usd",
        "description": "Personal spending on durable goods (cars, appliances)"
    },
    "PCEND": {
        "name": "PCE: Nondurable Goods",
        "category": "spending",
        "subcategory": "pce_component",
        "unit": "billions_usd",
        "description": "Personal spending on nondurable goods (food, clothing)"
    },
    "PCES": {
        "name": "PCE: Services",
        "category": "spending",
        "subcategory": "pce_component",
        "unit": "billions_usd",
        "description": "Personal spending on services (healthcare, rent)"
    },
    "A794RC0Q052SBEA": {
        "name": "PCE Per Capita",
        "category": "spending",
        "subcategory": "pce_component",
        "unit": "chained_2017_usd",
        "description": "Real personal consumption per capita"
    },

    # Detailed PCE Breakdown (Quarterly)
    "DHLCRC1Q027SBEA": {
        "name": "PCE: Healthcare",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal spending on healthcare services"
    },
    "DHUTRC1Q027SBEA": {
        "name": "PCE: Housing & Utilities",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal spending on housing and utilities"
    },
    "DTRSRC1Q027SBEA": {
        "name": "PCE: Transportation Services",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal spending on transportation services"
    },
    "DFSARC1Q027SBEA": {
        "name": "PCE: Food Services & Accommodation",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal spending on restaurants, hotels"
    },
    "DFDHRC1Q027SBEA": {
        "name": "PCE: Furnishings & Household",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal spending on furniture, appliances"
    },
    "DMOTRC1Q027SBEA": {
        "name": "PCE: Motor Vehicles",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal spending on cars, trucks, parts"
    },
    "DFXARC1Q027SBEA": {
        "name": "PCE: Food & Beverages (Off-Premises)",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal spending on groceries, alcohol"
    },
    "DGOERC1Q027SBEA": {
        "name": "PCE: Gasoline & Energy",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal spending on gas, fuel, energy goods"
    },
    "DIFSRC1Q027SBEA": {
        "name": "PCE: Financial & Insurance",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal spending on financial services and insurance"
    },
    "DRCARC1Q027SBEA": {
        "name": "PCE: Recreation Services",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal spending on recreation and entertainment"
    },
    "DCLORC1Q027SBEA": {
        "name": "PCE: Clothing & Footwear",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal spending on clothing and footwear"
    },
    "DOTSRC1Q027SBEA": {
        "name": "PCE: Personal & Social Services",
        "category": "spending",
        "subcategory": "pce_detail",
        "unit": "billions_usd",
        "description": "Personal care, social services, household maintenance"
    },

    # Population & Household Data (for per-capita/per-household calculations)
    "POPTHM": {
        "name": "US Population (Monthly)",
        "category": "demographics",
        "subcategory": "population",
        "unit": "thousands",
        "description": "Total US population, monthly, thousands"
    },
    "POP": {
        "name": "US Population (Annual)",
        "category": "demographics",
        "subcategory": "population",
        "unit": "thousands",
        "description": "Total US population, annual, thousands"
    },
    "TTLHH": {
        "name": "US Households (Annual)",
        "category": "demographics",
        "subcategory": "households",
        "unit": "thousands",
        "description": "Total US households, annual"
    },
    "TTLHHM156N": {
        "name": "US Households (Monthly)",
        "category": "demographics",
        "subcategory": "households",
        "unit": "thousands",
        "description": "Total US households, monthly"
    },

    # PCE Price Indexes (for inflation-adjusted spending analysis)
    "DSERRG3M086SBEA": {
        "name": "PCE Price Index: Services",
        "category": "inflation",
        "subcategory": "pce_prices",
        "unit": "index",
        "description": "Price index for personal consumption services"
    },
    "DGDSRG3M086SBEA": {
        "name": "PCE Price Index: Goods",
        "category": "inflation",
        "subcategory": "pce_prices",
        "unit": "index",
        "description": "Price index for personal consumption goods"
    },
    "DDURRG3M086SBEA": {
        "name": "PCE Price Index: Durable Goods",
        "category": "inflation",
        "subcategory": "pce_prices",
        "unit": "index",
        "description": "Price index for durable goods spending"
    },
    "DNDGRG3M086SBEA": {
        "name": "PCE Price Index: Nondurable Goods",
        "category": "inflation",
        "subcategory": "pce_prices",
        "unit": "index",
        "description": "Price index for nondurable goods spending"
    },

    # === Market Valuation & Sentiment Indicators ===

    # Note: Wilshire 5000 series (WILSHIRE5000PR, WILL5000INDFC) discontinued on FRED June 2024
    # Using SPY from Yahoo Finance as total market proxy instead

    "SP500": {
        "name": "S&P 500 (FRED)",
        "category": "market",
        "subcategory": "equity",
        "unit": "index",
        "description": "S&P 500 Index from FRED"
    },

    # Margin Debt (market participation)
    "BOGZ1FL663067003Q": {
        "name": "Margin Debt",
        "category": "market",
        "subcategory": "participation",
        "unit": "millions_usd",
        "description": "Margin accounts at broker-dealers"
    },

    # Equity Risk Premium components
    "AAA": {
        "name": "Moody's AAA Corporate Yield",
        "category": "market",
        "subcategory": "credit",
        "unit": "percent",
        "description": "Moody's Seasoned Aaa Corporate Bond Yield"
    },
    "BAA": {
        "name": "Moody's BAA Corporate Yield",
        "category": "market",
        "subcategory": "credit",
        "unit": "percent",
        "description": "Moody's Seasoned Baa Corporate Bond Yield"
    },

    # Stock Market Capitalization to GDP (Buffett Indicator components)
    "NCBEILQ027S": {
        "name": "Corporate Equities Market Value",
        "category": "market",
        "subcategory": "valuation",
        "unit": "billions_usd",
        "description": "Nonfinancial Corporate Business; Corporate Equities; Liability"
    },

    # Note: Put/Call Ratio (PCRATIOM) not available on FRED - using NFCI as sentiment proxy instead

    # ICE BofA Indices for credit spreads
    "BAMLC0A0CM": {
        "name": "US Corporate Master Index",
        "category": "market",
        "subcategory": "credit",
        "unit": "percent",
        "description": "ICE BofA US Corporate Index Option-Adjusted Spread"
    },
    "BAMLH0A0HYM2EY": {
        "name": "High Yield Master II",
        "category": "market",
        "subcategory": "credit",
        "unit": "percent",
        "description": "ICE BofA US High Yield Master II Effective Yield"
    },

    # Real Interest Rates
    "DFII10": {
        "name": "10Y Real Interest Rate",
        "category": "economy",
        "subcategory": "monetary",
        "unit": "percent",
        "description": "10-Year Treasury Inflation-Indexed Security"
    },
    "DFII5": {
        "name": "5Y Real Interest Rate",
        "category": "economy",
        "subcategory": "monetary",
        "unit": "percent",
        "description": "5-Year Treasury Inflation-Indexed Security"
    },

    # Financial Conditions
    "NFCI": {
        "name": "Financial Conditions Index",
        "category": "market",
        "subcategory": "conditions",
        "unit": "index",
        "description": "Chicago Fed National Financial Conditions Index"
    },
    "ANFCI": {
        "name": "Adjusted Financial Conditions",
        "category": "market",
        "subcategory": "conditions",
        "unit": "index",
        "description": "Chicago Fed Adjusted National Financial Conditions Index"
    },

    # Stock Market Volatility
    "VXVCLS": {
        "name": "VIX (CBOE via FRED)",
        "category": "sentiment",
        "subcategory": "volatility",
        "unit": "index",
        "description": "CBOE Volatility Index from FRED"
    },

    # Treasury Term Premium
    "THREEFYTP10": {
        "name": "10Y Term Premium",
        "category": "economy",
        "subcategory": "monetary",
        "unit": "percent",
        "description": "10-Year Treasury Term Premium"
    },

}


def ingest_fred_data(years_back=100):
    """Ingest FRED data - defaults to max available history"""
    fred = Fred(api_key=settings.fred_api_key)
    # Use 1900 as start to get all available history
    start_date = datetime(1900, 1, 1)
    
    with get_db_context() as db:
        for series_id, metadata in FRED_INDICATORS.items():
            try:
                logger.info(f"Fetching {series_id}: {metadata['name']}")
                
                # Fetch from FRED
                series = fred.get_series(series_id, observation_start=start_date)
                logger.info(f"  Fetched {len(series)} records")
                
                # Save metadata
                existing = db.query(IndicatorMetadata).filter(
                    IndicatorMetadata.indicator_id == series_id
                ).first()
                
                if not existing:
                    meta_obj = IndicatorMetadata(
                        indicator_id=series_id,
                        fred_series_id=series_id,
                        source="FRED",
                        **metadata
                    )
                    db.add(meta_obj)
                    db.commit()
                
                # Save time series
                records_added = 0
                for timestamp, value in series.items():
                    if pd.notna(value):
                        existing_data = db.query(Indicator).filter(
                            Indicator.indicator_id == series_id,
                            Indicator.timestamp == timestamp
                        ).first()
                        
                        if not existing_data:
                            indicator = Indicator(
                                indicator_id=series_id,
                                timestamp=timestamp,
                                value=float(value),
                                source="FRED",
                                frequency="daily"  # Simplified
                            )
                            db.add(indicator)
                            records_added += 1
                
                db.commit()
                
                # Log success
                log = RefreshLog(
                    source="FRED",
                    indicator_id=series_id,
                    records_added=records_added,
                    status="success"
                )
                db.add(log)
                db.commit()
                
                logger.info(f"  ✓ Added {records_added} new records")
                
            except Exception as e:
                logger.error(f"  ✗ Error: {str(e)}")
                log = RefreshLog(
                    source="FRED",
                    indicator_id=series_id,
                    records_added=0,
                    status="error",
                    error_message=str(e)
                )
                db.add(log)
                db.commit()


if __name__ == "__main__":
    logger.info("Starting FRED data ingestion...")
    ingest_fred_data()
    logger.info("Complete!")
