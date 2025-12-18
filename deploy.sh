#!/bin/bash

# Ward Deployment Script
# This script helps deploy Ward to Vercel

set -e

echo "🚀 Ward Deployment to Vercel"
echo "=============================="
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Install it with: npm i -g vercel"
    exit 1
fi

# Check if logged in
if ! vercel whoami &> /dev/null; then
    echo "❌ Not logged in to Vercel. Run: vercel login"
    exit 1
fi

echo "✅ Vercel CLI found and logged in"
echo ""

# Ask about backend URL
echo "📋 Before deploying, we need your backend URL."
echo "   If you haven't deployed the backend yet, you can:"
echo "   1. Deploy to Railway (recommended): https://railway.app"
echo "   2. Deploy to Render: https://render.com"
echo "   3. Set it later in Vercel dashboard"
echo ""
read -p "Enter your backend URL (or press Enter to skip for now): " BACKEND_URL

if [ -z "$BACKEND_URL" ]; then
    echo "⚠️  Skipping backend URL. You'll need to set REACT_APP_BACKEND_URL in Vercel dashboard later."
    echo ""
    read -p "Continue with deployment? (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ]; then
        echo "Deployment cancelled."
        exit 0
    fi
else
    echo "✅ Backend URL set: $BACKEND_URL"
    echo ""
fi

# Deploy to Vercel
echo "📦 Deploying to Vercel..."
echo ""

if [ -n "$BACKEND_URL" ]; then
    # Deploy with environment variable
    vercel --prod --env REACT_APP_BACKEND_URL="$BACKEND_URL"
else
    # Deploy without environment variable (user will set it later)
    vercel --prod
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
if [ -z "$BACKEND_URL" ]; then
    echo "   1. Go to your Vercel project dashboard"
    echo "   2. Navigate to Settings → Environment Variables"
    echo "   3. Add REACT_APP_BACKEND_URL with your backend URL"
    echo "   4. Redeploy the project"
fi
echo "   5. Visit your deployment URL to test the app"
echo ""
echo "🔗 Useful links:"
echo "   - Vercel Dashboard: https://vercel.com/dashboard"
echo "   - Deployment Guide: See QUICK_DEPLOY.md"
echo ""

