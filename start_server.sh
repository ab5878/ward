#!/bin/bash
# Start Ward Backend Server
# Usage: ./start_server.sh

cd "$(dirname "$0")/backend"
echo "🚀 Starting Ward backend server..."
echo "📍 Directory: $(pwd)"
echo "🌐 Server will be available at: http://localhost:8001"
echo "📊 Health check: http://localhost:8001/api/health"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 -m uvicorn server:app --port 8001 --host 0.0.0.0 --reload

