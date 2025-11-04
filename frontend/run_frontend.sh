#!/bin/bash

echo "🚀 Starting VideoAI Frontend..."

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found! Creating default .env file..."
    echo "REACT_APP_BACKEND_URL=http://localhost:8001" > .env
    echo "REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key_here" >> .env
fi

# Start the development server
echo "Starting React development server on http://localhost:3000"
echo "Press Ctrl+C to stop the server"
npm start