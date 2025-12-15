#!/bin/bash
# Prepare deployment by copying backend files into api directory

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKEND_DIR="$PROJECT_ROOT/backend"
API_BACKEND_DIR="$SCRIPT_DIR/backend"

echo "📦 Preparing deployment..."

# Remove old backend copy if exists
if [ -d "$API_BACKEND_DIR" ]; then
    echo "  Removing old backend copy..."
    rm -rf "$API_BACKEND_DIR"
fi

# Copy backend directory
echo "  Copying backend files..."
cp -r "$BACKEND_DIR" "$API_BACKEND_DIR"

# Remove unnecessary files
echo "  Cleaning up..."
find "$API_BACKEND_DIR" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find "$API_BACKEND_DIR" -type f -name "*.pyc" -delete 2>/dev/null || true
find "$API_BACKEND_DIR" -type f -name ".env*" -delete 2>/dev/null || true

echo "✅ Deployment prepared!"

