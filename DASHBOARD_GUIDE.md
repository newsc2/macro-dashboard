# Running the Streamlit Dashboard

## Quick Start

### 1. Make sure your API is running
```bash
# Check if containers are up
docker-compose ps

# Should show both postgres and api as "Up"
# If not running:
docker-compose up -d
```

### 2. Install Streamlit (if not already installed)
```bash
pip install streamlit plotly
```

### 3. Run the Dashboard
```bash
streamlit run dashboard_ui.py
```

The dashboard will open automatically in your browser at: http://localhost:8501

## What You Get

### 📊 Overview Page
- Health check status
- All key economic indicators at a glance
- All key market indicators
- S&P 500 year-to-date chart

### 🚨 Recession Watch
- Yield curve (10Y-2Y spread) with inversion warnings
- Unemployment rate trend
- Housing starts
- Industrial production
- Consumer sentiment
All with interactive charts!

### 📈 Market Overview
- S&P 500 performance
- VIX volatility index with warnings
- Federal Funds Rate
- 10-Year Treasury Rate
- Selectable time ranges (1 month to 5 years)
- 30-day change calculations

### 🔍 Custom Analysis
- Select ANY indicator from dropdown
- Choose years of history (1-10 years)
- Multiple chart types (Line, Area, Bar)
- Statistics: current, average, min, max
- Trend analysis: 30-day, 90-day, 1-year changes
- Download data as CSV

## Features

✅ **Interactive charts** - Hover for details, zoom, pan
✅ **Real-time data** - Pulls from your API
✅ **Smart warnings** - Yield curve inversions, high volatility alerts
✅ **Export data** - Download any indicator as CSV
✅ **Responsive layout** - Works on different screen sizes
✅ **Professional styling** - Clean, modern interface

## Troubleshooting

**Dashboard won't start?**
```bash
# Make sure API is running
curl http://localhost:8000/health

# Install dependencies
pip install -r requirements.txt
```

**"Connection refused" errors?**
- Check that your API container is running: `docker-compose ps`
- Make sure you're using port 8000 (not 8001 or other)

**No data showing?**
- Verify data was loaded: `docker-compose logs api | grep "records"`
- Try running setup again: `docker-compose exec api python setup.py`

## Customization

Want to add more pages or charts? Edit `dashboard_ui.py`:
- The code is well-commented
- Each page is a separate section
- Easy to add new indicators or charts

## Next Steps

1. **Use it daily** - Track your investment decisions
2. **Share with friends** - Get feedback
3. **Add features** - Correlation analysis, alerts, etc.
4. **Polish UI** - Custom colors, logos, branding

---

**Pro tip:** Run both the API docs (http://localhost:8000/docs) and the dashboard (http://localhost:8501) side-by-side!
