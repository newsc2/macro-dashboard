#!/bin/bash

# This script automates starting the entire local environment for the Macro Dashboard.
# It can be run by double-clicking it in the Finder.

# Get the directory where this script is located to ensure all commands run in the correct project folder.
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# --- Step 1: Start Background Services ---
echo "▶️ Starting background services (PostgreSQL Database & FastAPI Backend)..."
# Starts the services defined in docker-compose.yml in detached (background) mode.
docker-compose up -d

# Check if docker-compose command was successful
if [ $? -ne 0 ]; then
    echo "❌ Error: docker-compose failed to start. Please ensure Docker Desktop is running and try again."
    # Pause to allow user to read the message before exiting.
    read -p "Press Enter to exit..."
    exit 1
fi
echo "✅ Background services are running."
echo ""


# --- Step 2: Start Streamlit Frontend ---
echo "▶️ Starting Streamlit frontend in a new Terminal window..."
# Use AppleScript to open a new Terminal window and run the Streamlit command.
# This allows the frontend to run as its own process.
osascript -e "tell app \"Terminal\" to do script \"cd '$DIR' && echo '--- Starting Streamlit ---' && python3 -m streamlit run dashboard_ui.py\""
echo "✅ Streamlit is starting up."
echo ""


# --- Step 3: Start ngrok Sharing ---
echo "▶️ Starting ngrok to create a public URL for your dashboard..."
# Use AppleScript to open another new Terminal window for ngrok.
# This provides the user with the public URL and live request logs.
osascript -e "tell app \"Terminal\" to do script \"cd '$DIR' && echo '--- Starting ngrok ---' && ngrok http 8501\""
echo "✅ ngrok is starting up. A new terminal will show your public URL."
echo ""

# --- Done ---
echo "🚀 All services are launching. You will have three terminal windows:"
echo "   1. This window (which you can close)."
echo "   2. The Streamlit server window."
echo "   3. The ngrok window with your public URL."

exit 0