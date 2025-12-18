#!/bin/bash

# Deploy Frontend to Vercel
# This script deploys only the frontend to Vercel

set -e

echo "🎨 Deploying Frontend to Vercel..."
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo -e "${YELLOW}⚠️  Vercel CLI not found. Installing...${NC}"
    npm install -g vercel
fi

# Check if logged in to Vercel
if ! vercel whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Vercel. Please login...${NC}"
    vercel login
fi

# Navigate to frontend directory
cd frontend

echo -e "${BLUE}📋 Pre-deployment checks...${NC}"

# Check if .npmrc exists
if [ ! -f ".npmrc" ]; then
    echo -e "${YELLOW}⚠️  .npmrc not found. Creating...${NC}"
    echo "legacy-peer-deps=true" > .npmrc
fi

# Install dependencies if needed
if [ ! -d "node_modules" ] || [ "$1" == "--clean" ]; then
    echo -e "${BLUE}📦 Installing dependencies...${NC}"
    rm -rf node_modules package-lock.json
    npm install --legacy-peer-deps
fi

# Build frontend
echo -e "${BLUE}🔨 Building frontend...${NC}"
npm run build

# Deploy to Vercel
echo -e "${BLUE}🚀 Deploying to Vercel...${NC}"
vercel deploy --prod --yes

cd ..

echo ""
echo -e "${GREEN}✅ Frontend deployment complete!${NC}"
echo ""
echo "📋 Next steps:"
echo "   1. Verify deployment at your Vercel URL"
echo "   2. Check that environment variables are set"
echo "   3. Test the frontend application"
echo ""

