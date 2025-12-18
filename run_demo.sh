#!/bin/bash
# Run Demo Data Creation
# Usage: ./run_demo.sh
# Note: Server must be running on port 8001

echo "🧪 Running Ward Demo Data Creation..."
echo "⚠️  Make sure server is running: ./start_server.sh"
echo ""

cd "$(dirname "$0")"
python3 tests/create_demo_data.py

