#!/bin/bash
cd /Users/tonylin/Projects/DataOne/macro-dashboard-v2

# Start Docker if not running
if ! docker info > /dev/null 2>&1; then
    echo "Starting Docker..."
    open -a Docker
    while ! docker info > /dev/null 2>&1; do
        sleep 2
    done
    echo "Docker is ready"
fi

# Start backend services
echo "Starting backend services..."
docker compose up -d

# Wait for API to be ready
echo "Waiting for API..."
until curl -s http://localhost:8000/health > /dev/null 2>&1; do
    sleep 1
done
echo "API is ready"

# Start dashboard
echo "Starting dashboard..."
sleep 1 && open http://localhost:8501 &
python3 -m streamlit run dashboard_ui.py --server.port 8501
