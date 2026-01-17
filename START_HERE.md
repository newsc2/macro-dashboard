# START HERE - 3 Simple Steps

## Step 1: Get FRED API Key (2 minutes)
Go to: https://fred.stlouisfed.org/docs/api/api_key.html
Sign up and copy your key.

## Step 2: Setup (1 minute)
Open Terminal and run:
```bash
cd /path/to/macro-dashboard-v2

echo "FRED_API_KEY=paste_your_key_here" > .env

docker-compose up -d
```

## Step 3: Load Data (5-10 minutes)
```bash
docker-compose exec api python setup.py
```

## Done!
Open: http://localhost:8000/docs

---

**Everything works now!**
- All files in one folder
- No subdirectories
- No import errors
- Just works™

See README.md for full details.
