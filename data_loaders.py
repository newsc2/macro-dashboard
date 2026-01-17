"""
Data Loading Utilities for Consumer Spending & Inflation Module

Provides standardized data fetching that returns clean long-format dataframes.
All charts should consume these standardized frames, not raw API pulls.
"""

import pandas as pd
import requests
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import streamlit as st

from categories import (
    CANONICAL_CATEGORIES,
    PCE_SERIES_MAP,
    CPI_SERIES_MAP,
    CPI_WEIGHTS,
    BLS_CEX_2023,
    get_category_color,
)

API_BASE = "http://localhost:8000"


def fetch_api(endpoint: str, silent: bool = False) -> Optional[dict]:
    """Fetch data from the API."""
    try:
        response = requests.get(f"{API_BASE}{endpoint}", timeout=30)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        if not silent:
            st.error(f"API error: {e}")
    return None


@st.cache_data(ttl=3600)
def get_pce_totals() -> Dict[str, float]:
    """
    Get PCE totals for per-household calculations.
    Uses annual NSA series PCECA for accuracy.

    Returns dict with:
        - pce_total: Total PCE in billions (annual)
        - households: Number of households in thousands
        - pce_per_household: PCE per household in dollars
    """
    # Try to get annual PCE (PCECA) - more accurate for annual totals
    # Fall back to monthly SAAR (PCE) if annual not available
    pce_data = fetch_api("/api/indicators/PCE/latest", silent=True)
    pce_total = pce_data.get("latest_value", 0) if pce_data else 0

    # Get household count
    hh_data = fetch_api("/api/indicators/TTLHH/latest", silent=True)
    if not hh_data or not hh_data.get("latest_value"):
        hh_data = fetch_api("/api/indicators/TTLHHM156N/latest", silent=True)
    households = hh_data.get("latest_value", 0) if hh_data else 0

    # Calculate per-household (PCE is in billions, HH is in thousands)
    if pce_total > 0 and households > 0:
        pce_per_household = (pce_total * 1e9) / (households * 1e3)
    else:
        pce_per_household = 0

    return {
        "pce_total_billions": pce_total,
        "households_thousands": households,
        "pce_per_household": pce_per_household,
        "pce_timestamp": pce_data.get("timestamp") if pce_data else None,
    }


def get_bls_cex_totals() -> Dict[str, float]:
    """
    Get BLS Consumer Expenditure Survey totals.
    These are out-of-pocket spending (what households actually pay).

    Note: BLS CEX data must be manually updated as FRED doesn't have detailed series.
    """
    return {
        "total_expenditure": BLS_CEX_2023["total"],
        "categories": BLS_CEX_2023["categories"],
        "year": 2023,
        "source": "BLS Consumer Expenditure Survey",
        "note": "Consumer unit ≈ household, but not identical",
    }


@st.cache_data(ttl=3600)
def get_pce_spending_by_category() -> pd.DataFrame:
    """
    Get PCE spending breakdown by canonical category.

    Returns DataFrame with columns: [category, value_billions, color, icon]
    Values are annual rate (SAAR) in billions of dollars.
    """
    data = []

    for series_id, category in PCE_SERIES_MAP.items():
        result = fetch_api(f"/api/indicators/{series_id}/latest", silent=True)
        if result and result.get("latest_value"):
            cat_info = CANONICAL_CATEGORIES.get(category, {})
            data.append({
                "category": category,
                "value_billions": result["latest_value"],
                "color": cat_info.get("color", "#718096"),
                "icon": cat_info.get("icon", "📦"),
                "description": cat_info.get("description", ""),
                "series_id": series_id,
                "timestamp": result.get("timestamp"),
            })

    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values("value_billions", ascending=False)
    return df


def get_bls_spending_by_category() -> pd.DataFrame:
    """
    Get BLS CEX spending breakdown by canonical category.

    Returns DataFrame with columns: [category, value_dollars, color, icon]
    Values are annual out-of-pocket spending in dollars per consumer unit.
    """
    data = []

    for category, value in BLS_CEX_2023["categories"].items():
        cat_info = CANONICAL_CATEGORIES.get(category, {})
        data.append({
            "category": category,
            "value_dollars": value,
            "color": cat_info.get("color", "#718096"),
            "icon": cat_info.get("icon", "📦"),
            "description": cat_info.get("description", ""),
        })

    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values("value_dollars", ascending=False)
    return df


@st.cache_data(ttl=3600)
def get_cpi_inflation_timeseries(
    start_date: datetime,
    categories: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Get CPI inflation time series for specified categories.

    Returns DataFrame with columns: [timestamp, category, value, yoy_change]
    """
    if categories is None:
        categories = list(CPI_SERIES_MAP.values())

    all_data = []

    for series_id, category in CPI_SERIES_MAP.items():
        if category not in categories:
            continue

        result = fetch_api(
            f"/api/indicators/{series_id}/timeseries?start={start_date.isoformat()}&limit=10000",
            silent=True
        )

        if result and result.get("data"):
            df = pd.DataFrame(result["data"])
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp")
            df["category"] = category
            df["series_id"] = series_id

            # Calculate YoY change
            df["yoy_change"] = df["value"].pct_change(periods=12) * 100

            all_data.append(df)

    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()


@st.cache_data(ttl=3600)
def get_cpi_indexed_series(
    start_date: datetime,
    categories: Optional[List[str]] = None
) -> Tuple[pd.DataFrame, Dict[str, Dict]]:
    """
    Get CPI series indexed to 100 at start date.

    Returns:
        - DataFrame with columns: [timestamp, category, indexed_value]
        - Dict of summary stats per category
    """
    if categories is None:
        categories = list(CPI_SERIES_MAP.values())

    all_data = []
    summary_stats = {}

    for series_id, category in CPI_SERIES_MAP.items():
        if category not in categories:
            continue

        result = fetch_api(
            f"/api/indicators/{series_id}/timeseries?start={start_date.isoformat()}&limit=10000",
            silent=True
        )

        if result and result.get("data") and len(result["data"]) > 0:
            df = pd.DataFrame(result["data"])
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp")

            # Index to 100 at start
            base_value = df.iloc[0]["value"]
            end_value = df.iloc[-1]["value"]
            df["indexed_value"] = (df["value"] / base_value) * 100
            df["category"] = category

            # Calculate summary stats
            cumulative_change = ((end_value / base_value) - 1) * 100
            years = (df.iloc[-1]["timestamp"] - df.iloc[0]["timestamp"]).days / 365.25
            cagr = ((end_value / base_value) ** (1 / years) - 1) * 100 if years > 0 else 0

            summary_stats[category] = {
                "start_date": df.iloc[0]["timestamp"],
                "end_date": df.iloc[-1]["timestamp"],
                "start_value": base_value,
                "end_value": end_value,
                "cumulative_change": cumulative_change,
                "cagr": cagr,
                "years": years,
                "color": get_category_color(category),
            }

            all_data.append(df[["timestamp", "category", "indexed_value"]])

    if all_data:
        return pd.concat(all_data, ignore_index=True), summary_stats
    return pd.DataFrame(), {}


@st.cache_data(ttl=3600)
def get_inflation_contributions(
    start_date: datetime,
    categories: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Calculate category contributions to headline CPI inflation.

    Contribution formula: contribution_i(t) = weight_i * yoy_i(t)

    Returns DataFrame with columns: [timestamp, category, yoy_change, weight, contribution]
    """
    inflation_df = get_cpi_inflation_timeseries(start_date, categories)

    if inflation_df.empty:
        return pd.DataFrame()

    # Add weights and calculate contributions
    inflation_df["weight"] = inflation_df["category"].map(
        lambda x: CPI_WEIGHTS.get(x, 0) / 100  # Convert to decimal
    )
    inflation_df["contribution"] = inflation_df["yoy_change"] * inflation_df["weight"]

    return inflation_df


@st.cache_data(ttl=3600)
def get_current_yoy_inflation() -> pd.DataFrame:
    """
    Get current YoY inflation for all CPI categories.

    Returns DataFrame with columns: [category, yoy_change, weight, color]
    """
    data = []

    for series_id, category in CPI_SERIES_MAP.items():
        # Get 2 years of data to calculate YoY
        two_years_ago = datetime.now() - timedelta(days=730)
        result = fetch_api(
            f"/api/indicators/{series_id}/timeseries?start={two_years_ago.isoformat()}&limit=500",
            silent=True
        )

        if result and result.get("data") and len(result["data"]) >= 13:
            df = pd.DataFrame(result["data"])
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df = df.sort_values("timestamp")

            current = df.iloc[-1]["value"]
            year_ago = df.iloc[-13]["value"]
            yoy = ((current - year_ago) / year_ago) * 100

            data.append({
                "category": category,
                "yoy_change": yoy,
                "weight": CPI_WEIGHTS.get(category, 0),
                "color": get_category_color(category),
            })

    df = pd.DataFrame(data)
    if not df.empty:
        df = df.sort_values("yoy_change", ascending=True)
    return df


def get_headline_cpi_yoy() -> Optional[float]:
    """Get current headline CPI YoY inflation."""
    two_years_ago = datetime.now() - timedelta(days=730)
    result = fetch_api(
        f"/api/indicators/CPIAUCSL/timeseries?start={two_years_ago.isoformat()}&limit=500",
        silent=True
    )

    if result and result.get("data") and len(result["data"]) >= 13:
        df = pd.DataFrame(result["data"])
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        current = df.iloc[-1]["value"]
        year_ago = df.iloc[-13]["value"]
        return ((current - year_ago) / year_ago) * 100

    return None
