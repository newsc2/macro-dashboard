"""
Canonical Category Definitions for Consumer Spending & Inflation

This module defines a unified category schema used across all spending and inflation charts.
All charts must use these exact category names for consistency.
"""

# =============================================================================
# CANONICAL CATEGORIES - Use these names everywhere
# =============================================================================

CANONICAL_CATEGORIES = {
    "Shelter": {
        "description": "Housing, rent, owners' equivalent rent",
        "color": "#F6AD55",
        "icon": "🏠",
        "pce_series": ["DHUTRC1Q027SBEA"],  # Housing & Utilities (includes shelter)
        "cpi_series": ["CUSR0000SAH1"],  # CPI: Shelter
        "cpi_weight": 0.348,  # Approximate CPI relative importance weight
    },
    "Food at home": {
        "description": "Groceries, food purchased for home consumption",
        "color": "#00D4AA",
        "icon": "🛒",
        "pce_series": ["DFXARC1Q027SBEA"],  # Food & beverages off-premises
        "cpi_series": ["CUSR0000SAF11"],  # CPI: Food at home
        "cpi_weight": 0.084,
    },
    "Food away from home": {
        "description": "Restaurants, takeout, cafeterias, hotels",
        "color": "#48BB78",
        "icon": "🍽️",
        "pce_series": ["DFSARC1Q027SBEA"],  # Food services & accommodations
        "cpi_series": ["CUSR0000SEFV"],  # CPI: Food away from home
        "cpi_weight": 0.056,
    },
    "Gasoline & fuel": {
        "description": "Motor fuel, gasoline",
        "color": "#ED64A6",
        "icon": "⛽",
        "pce_series": ["DGOERC1Q027SBEA"],  # Gasoline & energy goods
        "cpi_series": ["CUUR0000SETB01"],  # CPI: Gasoline
        "cpi_weight": 0.034,
    },
    "Household energy": {
        "description": "Electricity, natural gas, heating oil",
        "color": "#9F7AEA",
        "icon": "💡",
        "pce_series": [],  # Part of Housing & Utilities, hard to separate
        "cpi_series": ["CUSR0000SEEB", "CUSR0000SEEE"],  # Electricity + Utility gas
        "cpi_weight": 0.033,
    },
    "Medical care": {
        "description": "Healthcare services, drugs, medical equipment",
        "color": "#FC8181",
        "icon": "🏥",
        "pce_series": ["DHLCRC1Q027SBEA"],  # Healthcare
        "cpi_series": ["CUSR0000SAM2"],  # CPI: Medical care services
        "cpi_weight": 0.066,
    },
    "Vehicles": {
        "description": "New and used cars, trucks, parts",
        "color": "#00A3FF",
        "icon": "🚗",
        "pce_series": ["DMOTRC1Q027SBEA"],  # Motor vehicles & parts
        "cpi_series": ["CUSR0000SETA01", "CUSR0000SETA02"],  # New + Used vehicles
        "cpi_weight": 0.076,
    },
    "Transportation services": {
        "description": "Airfare, public transit, vehicle insurance, maintenance",
        "color": "#B794F4",
        "icon": "✈️",
        "pce_series": ["DTRSRC1Q027SBEA"],  # Transportation services
        "cpi_series": [],  # No clean single CPI series
        "cpi_weight": 0.057,
    },
    "Apparel": {
        "description": "Clothing, footwear, accessories",
        "color": "#38B2AC",
        "icon": "👕",
        "pce_series": ["DCLORC1Q027SBEA"],  # Clothing & footwear
        "cpi_series": ["CPIAPPSL"],  # CPI: Apparel
        "cpi_weight": 0.025,
    },
    "Recreation": {
        "description": "Entertainment, hobbies, sports, pets",
        "color": "#667EEA",
        "icon": "🎮",
        "pce_series": ["DRCARC1Q027SBEA"],  # Recreation services
        "cpi_series": [],  # No clean single CPI series
        "cpi_weight": 0.057,
    },
    "Education & communication": {
        "description": "Tuition, telecom, internet, phone",
        "color": "#4FD1C5",
        "icon": "📚",
        "pce_series": [],  # Not available as clean series
        "cpi_series": [],  # Would need CUSR0000SAE + CUSR0000SAR
        "cpi_weight": 0.065,
    },
    "Financial services & insurance": {
        "description": "Banking fees, insurance premiums, financial advice",
        "color": "#F687B3",
        "icon": "💳",
        "pce_series": ["DIFSRC1Q027SBEA"],  # Financial services & insurance
        "cpi_series": [],  # CPI doesn't cover this well
        "cpi_weight": 0.0,  # Not in CPI
    },
    "Furnishings & household": {
        "description": "Furniture, appliances, housekeeping supplies",
        "color": "#A0AEC0",
        "icon": "🛋️",
        "pce_series": ["DFDHRC1Q027SBEA"],  # Furnishings & durable household
        "cpi_series": [],
        "cpi_weight": 0.044,
    },
    "Personal care & other": {
        "description": "Personal care services, social services, misc",
        "color": "#718096",
        "icon": "💇",
        "pce_series": ["DOTSRC1Q027SBEA"],  # Other services
        "cpi_series": [],
        "cpi_weight": 0.027,
    },
}

# Categories with reliable CPI data for inflation charts
CPI_INFLATION_CATEGORIES = [
    "Shelter",
    "Food at home",
    "Food away from home",
    "Gasoline & fuel",
    "Medical care",
    "Vehicles",
    "Apparel",
]

# Categories with PCE spending data
PCE_SPENDING_CATEGORIES = [
    "Shelter",  # Note: PCE series is Housing & Utilities combined
    "Food at home",
    "Food away from home",
    "Gasoline & fuel",
    "Medical care",
    "Vehicles",
    "Transportation services",
    "Apparel",
    "Recreation",
    "Financial services & insurance",
    "Furnishings & household",
    "Personal care & other",
]

# CPI Series mapping for inflation tracking
CPI_SERIES_MAP = {
    "CUSR0000SAH1": "Shelter",
    "CUSR0000SAF11": "Food at home",
    "CUSR0000SEFV": "Food away from home",
    "CUUR0000SETB01": "Gasoline & fuel",
    "CUSR0000SEEB": "Household energy",  # Electricity
    "CUSR0000SAM2": "Medical care",
    "CUSR0000SETA02": "Vehicles",  # Used vehicles (more volatile)
    "CPIAPPSL": "Apparel",
}

# PCE Series mapping for spending
PCE_SERIES_MAP = {
    "DHUTRC1Q027SBEA": "Shelter",  # Housing & Utilities
    "DFXARC1Q027SBEA": "Food at home",
    "DFSARC1Q027SBEA": "Food away from home",
    "DGOERC1Q027SBEA": "Gasoline & fuel",
    "DHLCRC1Q027SBEA": "Medical care",
    "DMOTRC1Q027SBEA": "Vehicles",
    "DTRSRC1Q027SBEA": "Transportation services",
    "DCLORC1Q027SBEA": "Apparel",
    "DRCARC1Q027SBEA": "Recreation",
    "DIFSRC1Q027SBEA": "Financial services & insurance",
    "DFDHRC1Q027SBEA": "Furnishings & household",
    "DOTSRC1Q027SBEA": "Personal care & other",
}

# BLS Consumer Expenditure Survey approximate values (2023)
# Source: https://www.bls.gov/cex/
BLS_CEX_2023 = {
    "total": 77280,  # Average annual expenditures per consumer unit
    "categories": {
        "Shelter": 24298,  # Housing (includes utilities, but we separate)
        "Food at home": 5703,
        "Food away from home": 3862,
        "Gasoline & fuel": 2510,
        "Household energy": 2149,  # Utilities, fuels, public services minus phone
        "Medical care": 5953,  # Healthcare
        "Vehicles": 5683,  # Vehicle purchases
        "Transportation services": 4036,  # Other transport (maintenance, insurance, etc)
        "Apparel": 1945,
        "Recreation": 3458,  # Entertainment
        "Education & communication": 3537,  # Education + phone/internet
        "Financial services & insurance": 855,  # Personal insurance & pensions (partial)
        "Furnishings & household": 2387,  # Household furnishings & equipment
        "Personal care & other": 2904,  # Personal care + misc
    }
}

# CPI Relative Importance Weights (December 2024, approximate)
# These sum to ~100 for All Items
CPI_WEIGHTS = {
    "Shelter": 36.2,
    "Food at home": 8.2,
    "Food away from home": 5.4,
    "Gasoline & fuel": 3.2,
    "Household energy": 3.1,
    "Medical care": 6.4,
    "Vehicles": 7.3,
    "Transportation services": 5.5,
    "Apparel": 2.4,
    "Recreation": 5.5,
    "Education & communication": 6.3,
    "Other": 10.5,  # Remaining items
}


def get_category_color(category: str) -> str:
    """Get the color for a canonical category."""
    return CANONICAL_CATEGORIES.get(category, {}).get("color", "#718096")


def get_category_icon(category: str) -> str:
    """Get the icon for a canonical category."""
    return CANONICAL_CATEGORIES.get(category, {}).get("icon", "📦")


def get_cpi_weight(category: str) -> float:
    """Get the CPI weight for a canonical category."""
    return CPI_WEIGHTS.get(category, 0.0)
