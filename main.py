"""
Macro Dashboard - Simplified Single-File Version
All code in one place to avoid import issues
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine, Column, String, Numeric, DateTime, Integer, Boolean, Text, func, and_, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
from datetime import datetime, timedelta
from contextlib import contextmanager
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

class Settings(BaseSettings):
    """Application settings from environment"""
    database_url: str = "postgresql://postgres:postgres@postgres:5432/macro_dashboard"
    fred_api_key: str = ""  # Optional - only needed for FRED data refresh
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()

# Fix Render's postgres:// URL format (SQLAlchemy needs postgresql://)
if settings.database_url.startswith("postgres://"):
    settings.database_url = settings.database_url.replace("postgres://", "postgresql://", 1)

# ============================================================================
# DATABASE SETUP
# ============================================================================

Base = declarative_base()
engine = create_engine(settings.database_url, pool_pre_ping=True, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def get_db_context():
    """Database context manager for scripts"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# ============================================================================
# DATABASE MODELS
# ============================================================================

class Indicator(Base):
    """Time series data"""
    __tablename__ = 'indicators'
    
    indicator_id = Column(String(100), primary_key=True)
    timestamp = Column(DateTime, primary_key=True)
    value = Column(Numeric)
    source = Column(String(50), nullable=False)
    frequency = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class IndicatorMetadata(Base):
    """Indicator metadata"""
    __tablename__ = 'indicator_metadata'
    
    indicator_id = Column(String(100), primary_key=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    category = Column(String(50), nullable=False)
    subcategory = Column(String(50))
    unit = Column(String(50))
    source = Column(String(50), nullable=False)
    fred_series_id = Column(String(100))
    typical_frequency = Column(String(20))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class RefreshLog(Base):
    """Data refresh log"""
    __tablename__ = 'refresh_log'
    
    refresh_id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), nullable=False)
    indicator_id = Column(String(100))
    refresh_timestamp = Column(DateTime, server_default=func.now())
    records_added = Column(Integer)
    status = Column(String(20), nullable=False)
    error_message = Column(Text)

# ============================================================================
# PYDANTIC MODELS (API)
# ============================================================================

class IndicatorMetadataResponse(BaseModel):
    indicator_id: str
    name: str
    description: Optional[str] = None
    category: str
    subcategory: Optional[str] = None
    unit: Optional[str] = None
    source: str
    
    class Config:
        from_attributes = True


class TimeSeriesPoint(BaseModel):
    timestamp: datetime
    value: float


class TimeSeriesResponse(BaseModel):
    indicator_id: str
    name: str
    data: List[TimeSeriesPoint]
    frequency: str

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Macro Dashboard API",
    description="Economic and market indicators dashboard",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Macro Dashboard API v2.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check"""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        indicator_count = db.query(IndicatorMetadata).count()
        db.close()

        return {
            "status": "healthy",
            "database": "connected",
            "total_indicators": indicator_count
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Unhealthy: {str(e)}")


@app.get("/api/indicators", response_model=List[IndicatorMetadataResponse])
async def get_indicators(
    category: Optional[str] = None,
    source: Optional[str] = None
):
    """Get all indicators"""
    db = SessionLocal()
    query = db.query(IndicatorMetadata).filter(IndicatorMetadata.is_active == True)
    
    if category:
        query = query.filter(IndicatorMetadata.category == category)
    if source:
        query = query.filter(IndicatorMetadata.source == source)
    
    indicators = query.all()
    db.close()
    return indicators


@app.get("/api/indicators/{indicator_id}", response_model=IndicatorMetadataResponse)
async def get_indicator_metadata(indicator_id: str):
    """Get indicator metadata"""
    db = SessionLocal()
    metadata = db.query(IndicatorMetadata).filter(
        IndicatorMetadata.indicator_id == indicator_id
    ).first()
    db.close()
    
    if not metadata:
        raise HTTPException(status_code=404, detail="Indicator not found")
    
    return metadata


@app.get("/api/indicators/{indicator_id}/timeseries", response_model=TimeSeriesResponse)
async def get_timeseries(
    indicator_id: str,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    limit: int = Query(20000, le=50000)
):
    """Get time series data"""
    db = SessionLocal()
    
    # Get metadata
    metadata = db.query(IndicatorMetadata).filter(
        IndicatorMetadata.indicator_id == indicator_id
    ).first()
    
    if not metadata:
        db.close()
        raise HTTPException(status_code=404, detail="Indicator not found")
    
    # Set defaults
    if end is None:
        end = datetime.now()
    if start is None:
        start = end - timedelta(days=365)
    
    # Query data - order ascending so limit cuts off newest, not oldest
    query = db.query(Indicator).filter(
        and_(
            Indicator.indicator_id == indicator_id,
            Indicator.timestamp >= start,
            Indicator.timestamp <= end
        )
    ).order_by(Indicator.timestamp.asc()).limit(limit)
    
    data = query.all()
    db.close()

    # Return empty array instead of 404 when no data in range
    time_series_points = [
        TimeSeriesPoint(timestamp=d.timestamp, value=float(d.value))
        for d in data  # Already sorted ascending
    ]

    return TimeSeriesResponse(
        indicator_id=indicator_id,
        name=metadata.name,
        data=time_series_points,
        frequency=data[0].frequency if data else "unknown"
    )


@app.get("/api/indicators/{indicator_id}/latest")
async def get_latest_value(indicator_id: str):
    """Get latest value. Returns null values if no data available."""
    db = SessionLocal()

    latest = db.query(Indicator).filter(
        Indicator.indicator_id == indicator_id
    ).order_by(Indicator.timestamp.desc()).first()

    metadata = db.query(IndicatorMetadata).filter(
        IndicatorMetadata.indicator_id == indicator_id
    ).first()

    db.close()

    # Return null values instead of 404 when no data
    if not latest:
        return {
            "indicator_id": indicator_id,
            "name": metadata.name if metadata else indicator_id,
            "latest_value": None,
            "timestamp": None,
            "unit": metadata.unit if metadata else None
        }

    return {
        "indicator_id": indicator_id,
        "name": metadata.name if metadata else indicator_id,
        "latest_value": float(latest.value),
        "timestamp": latest.timestamp,
        "unit": metadata.unit if metadata else None
    }


@app.get("/api/categories")
async def get_categories():
    """Get all categories"""
    db = SessionLocal()
    categories = db.query(
        IndicatorMetadata.category,
        func.count(IndicatorMetadata.indicator_id).label('count')
    ).filter(
        IndicatorMetadata.is_active == True
    ).group_by(
        IndicatorMetadata.category
    ).all()
    db.close()
    
    return [{"category": cat, "count": count} for cat, count in categories]


@app.get("/api/dashboards/recession-watch")
async def recession_watch_dashboard():
    """Recession watch dashboard"""
    key_indicators = ["T10Y2Y", "UNRATE", "INDPRO", "HOUST", "UMCSENT"]
    
    db = SessionLocal()
    dashboard_data = {}
    
    for indicator_id in key_indicators:
        latest = db.query(Indicator).filter(
            Indicator.indicator_id == indicator_id
        ).order_by(Indicator.timestamp.desc()).first()
        
        if latest:
            metadata = db.query(IndicatorMetadata).filter(
                IndicatorMetadata.indicator_id == indicator_id
            ).first()
            
            dashboard_data[indicator_id] = {
                "name": metadata.name if metadata else indicator_id,
                "latest_value": float(latest.value),
                "timestamp": latest.timestamp,
                "unit": metadata.unit if metadata else None
            }
    
    db.close()
    
    return {
        "dashboard": "recession_watch",
        "description": "Key recession indicators",
        "indicators": dashboard_data
    }


@app.get("/api/dashboards/market-overview")
async def market_overview_dashboard():
    """Market overview dashboard"""
    key_indicators = ["SPY", "QQQ", "^VIX", "BTC-USD", "ETH-USD"]
    
    db = SessionLocal()
    dashboard_data = {}
    
    for indicator_id in key_indicators:
        latest = db.query(Indicator).filter(
            Indicator.indicator_id == indicator_id
        ).order_by(Indicator.timestamp.desc()).first()
        
        if latest:
            metadata = db.query(IndicatorMetadata).filter(
                IndicatorMetadata.indicator_id == indicator_id
            ).first()
            
            dashboard_data[indicator_id] = {
                "name": metadata.name if metadata else indicator_id,
                "latest_value": float(latest.value),
                "timestamp": latest.timestamp,
                "unit": metadata.unit if metadata else None
            }
    
    db.close()
    
    return {
        "dashboard": "market_overview",
        "description": "Key market indicators",
        "indicators": dashboard_data
    }


# ============================================================================
# DATA REFRESH ENDPOINT
# ============================================================================

@app.post("/api/refresh")
async def refresh_data(source: Optional[str] = None):
    """
    Trigger data refresh from external sources.
    source: 'fred', 'market', or None for both
    """
    import subprocess
    import sys

    results = {"status": "success", "refreshed": []}

    try:
        if source is None or source == "fred":
            subprocess.run([sys.executable, "ingest_fred.py"], check=True, timeout=300)
            results["refreshed"].append("fred")

        if source is None or source == "market":
            subprocess.run([sys.executable, "ingest_market.py"], check=True, timeout=300)
            results["refreshed"].append("market")

        return results

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=504, detail="Refresh timed out")
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Refresh failed: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Refresh error: {str(e)}")


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
