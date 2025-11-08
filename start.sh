#!/bin/bash
# Quick start script for ClaimEquity AI (React + Flask)

echo "🚀 Starting ClaimEquity AI..."
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Function to start backend
start_backend() {
    echo "📦 Starting Flask backend..."
    cd backend
    python3 app.py &
    BACKEND_PID=$!
    echo "Backend PID: $BACKEND_PID"
    cd ..
    sleep 2
}

# Function to start frontend
start_frontend() {
    echo "⚛️  Starting React frontend..."
    cd frontend
    
    # Check if node_modules exists
    if [ ! -d "node_modules" ]; then
        echo "📥 Installing frontend dependencies..."
        npm install
    fi
    
    npm run dev &
    FRONTEND_PID=$!
    echo "Frontend PID: $FRONTEND_PID"
    cd ..
}

# Start both servers
start_backend
start_frontend

echo ""
echo "✅ Both servers are starting..."
echo "📡 Backend API: http://localhost:5000"
echo "🌐 Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait

