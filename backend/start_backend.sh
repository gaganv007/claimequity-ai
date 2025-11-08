#!/bin/bash
# Start Flask backend server

cd "$(dirname "$0")"
echo "🚀 Starting ClaimEquity AI Backend..."
echo ""

# Check if port 5000 is in use
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  Port 5000 is already in use"
    echo "   Stopping existing process..."
    lsof -ti:5000 | xargs kill -9 2>/dev/null
    sleep 2
fi

# Start the server
python3 app.py

