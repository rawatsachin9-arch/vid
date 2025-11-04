#!/bin/bash

echo "🚀 Starting VideoAI Development Environment"
echo "=========================================="

# Function to check if MongoDB is running
check_mongodb() {
    if ! pgrep -x "mongod" > /dev/null; then
        echo "⚠️  MongoDB is not running!"
        echo "Please start MongoDB first:"
        echo "  - macOS: brew services start mongodb-community"
        echo "  - Ubuntu: sudo systemctl start mongod"
        echo "  - Docker: docker run -d -p 27017:27017 --name mongodb mongo:latest"
        exit 1
    else
        echo "✅ MongoDB is running"
    fi
}

# Check MongoDB
check_mongodb

# Start backend in background
echo "🔧 Starting Backend (FastAPI)..."
cd backend
if [ ! -f ".env" ]; then
    echo "⚠️  Backend .env file not found! Please configure it first."
    exit 1
fi

# Start backend
./venv/bin/uvicorn server:app --reload --port 8001 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID) on http://localhost:8001"

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Starting Frontend (React)..."
cd ../frontend
if [ ! -f ".env" ]; then
    echo "Creating frontend .env file..."
    echo "REACT_APP_BACKEND_URL=http://localhost:8001" > .env
    echo "REACT_APP_STRIPE_PUBLISHABLE_KEY=pk_test_your_stripe_key_here" >> .env
fi

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "✅ Starting React development server on http://localhost:3000"
echo ""
echo "🎉 Development environment ready!"
echo "   - Backend API: http://localhost:8001"
echo "   - Frontend: http://localhost:3000"
echo "   - API Docs: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Start frontend (this will block)
npm start