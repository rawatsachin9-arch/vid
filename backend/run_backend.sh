#!/bin/bash

echo "🚀 Starting VideoAI Backend..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Activating virtual environment..."
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
else
    echo "Activating existing virtual environment..."
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found! Please create it with required environment variables."
    echo "See the .env template in the setup instructions."
    exit 1
fi

# Start the server
echo "Starting FastAPI server on http://localhost:8001"
echo "Press Ctrl+C to stop the server"
python server.py