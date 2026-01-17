# Macro Dashboard v2 - Simplified Version

A streamlined economic and market indicators dashboard. **Everything in one place - no complex folder structures.**

## ✅ What's Included

- **30+ Economic Indicators** from FRED (GDP, unemployment, inflation, rates, housing, etc.)
- **6 Market Indicators** from Yahoo Finance (S&P 500, VIX, NASDAQ, Gold, etc.)
- **RESTful API** with automatic documentation
- **Docker-ready** - works immediately
- **Pre-built Dashboards** (Recession Watch, Market Overview)

## 🚀 Quick Start (3 Steps)

### Step 1: Get Your FRED API Key
1. Go to: https://fred.stlouisfed.org/docs/api/api_key.html
2. Sign up (it's free)
3. Copy your API key

### Step 2: Setup
```bash
# Make sure Docker Desktop is running

# Navigate to this folder in Terminal
cd /path/to/macro-dashboard-v2

# Create .env file with your FRED API key
echo "FRED_API_KEY=your_actual_key_here" > .env

# Start Docker containers
docker-compose up -d
```

### Step 3: Load Data
```bash
# Run setup (takes 5-10 minutes)
docker-compose exec api python setup.py
```

## 🎉 You're Done!

Open your browser to:
- **API Docs:** http://localhost:8000/docs
- **Recession Watch:** http://localhost:8000/api/dashboards/recession-watch
- **Market Overview:** http://localhost:8000/api/dashboards/market-overview

## 📊 Available Indicators

### Economic Indicators (FRED)
- **GDP & Growth:** GDP, Real GDP
- **Employment:** Unemployment Rate, Nonfarm Payrolls
- **Inflation:** CPI, PCE Price Index
- **Interest Rates:** Fed Funds Rate, 10Y Treasury, 2Y Treasury, Yield Curve
- **Money Supply:** M2
- **Housing:** Housing Starts, 30Y Mortgage Rate
- **Manufacturing:** Industrial Production
- **Sentiment:** Consumer Sentiment
- **Commodities:** WTI Crude Oil

### Market Indicators (Yahoo Finance)
- S&P 500
- VIX (Volatility Index)
- Dow Jones
- NASDAQ
- Gold ETF
- 20Y Treasury Bond ETF

## 🔧 Useful Commands

```bash
# Check container status
docker-compose ps

# View logs
docker-compose logs api

# Stop everything
docker-compose down

# Restart
docker-compose down && docker-compose up -d

# Run daily update
docker-compose exec api python ingest_fred.py
docker-compose exec api python ingest_market.py
```

## 🌐 API Endpoints

### Core Endpoints
```
GET /                                        # API info
GET /health                                  # Health check
GET /api/indicators                          # List all indicators
GET /api/indicators/{id}/timeseries          # Get time series data
GET /api/indicators/{id}/latest              # Get latest value
GET /api/categories                          # List categories
GET /api/dashboards/recession-watch          # Recession dashboard
GET /api/dashboards/market-overview          # Market dashboard
```

### Example Queries
```bash
# Get S&P 500 data for last year
curl "http://localhost:8000/api/indicators/^GSPC/timeseries"

# Get latest unemployment rate
curl "http://localhost:8000/api/indicators/UNRATE/latest"

# Get all economy indicators
curl "http://localhost:8000/api/indicators?category=economy"
```

## 📱 Python Client Example

```python
import requests

# Get recession watch dashboard
response = requests.get("http://localhost:8000/api/dashboards/recession-watch")
data = response.json()

# Access indicators
for indicator_id, info in data['indicators'].items():
    print(f"{info['name']}: {info['latest_value']}")
```

## 🐛 Troubleshooting

**Container won't start?**
- Make sure Docker Desktop is running (whale icon in menu bar)
- Check your .env file has FRED_API_KEY set
- Run: `docker-compose logs api`

**No data loading?**
- Verify FRED API key is correct in .env
- Check network connection
- Run: `docker-compose logs api`

**Port 8000 in use?**
Edit `docker-compose.yml` and change:
```yaml
ports:
  - "8001:8000"  # Use port 8001 instead
```

## 📈 What's Next?

This MVP gives you everything you need to:
1. **Track macro trends daily**
2. **Build your own analysis**
3. **Test investment strategies**
4. **Validate the business idea**

### Future Enhancements (if you decide to continue):
- React frontend with charts
- Correlation tracking & alerts
- Backtesting engine
- User authentication
- Subscription payments
- Mobile app

## 📝 Files Overview

- `main.py` - Complete FastAPI application (all-in-one)
- `ingest_fred.py` - FRED data fetcher
- `ingest_market.py` - Market data fetcher
- `setup.py` - One-time setup script
- `docker-compose.yml` - Docker configuration
- `requirements.txt` - Python dependencies

**Everything is in this one folder. No subdirectories. No import issues.**

## 💡 Tips

1. **Use it yourself first** - Track your portfolio decisions against the data
2. **Set up daily updates** - Add a cron job to run the ingest scripts
3. **Share with friends** - Get 5-10 beta users for feedback
4. **Track engagement** - See if people actually use it regularly

## 🎯 Success Metrics

- Can you improve your returns by 1-2%?
- Do you check it daily?
- Would you pay $100/year for this?

If yes to all three → you have product-market fit

---

**Questions?** Everything is documented above. If stuck, check:
1. Docker Desktop is running
2. .env has correct FRED_API_KEY
3. `docker-compose ps` shows both containers "Up"
4. `docker-compose logs api` for errors

Good luck! 🚀
