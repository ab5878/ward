#!/bin/bash

# Ward Supabase Setup Script
# This script helps you set up Supabase for Ward

set -e

echo "🚀 Ward Supabase Setup"
echo "======================"
echo ""

# Supabase project details
SUPABASE_URL="https://gjwzaylkzknsykjvtpcd.supabase.co"
SUPABASE_ANON_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imdqd3pheWxremtuc3lranZ0cGNkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU3MDYwOTQsImV4cCI6MjA4MTI4MjA5NH0.6eEmujnFLD6Lo4vsh_gOV_HKRL34cPgbbRZ4HFUFzJM"

echo "📋 Supabase Project Details:"
echo "   URL: $SUPABASE_URL"
echo "   Project ID: gjwzaylkzknsykjvtpcd"
echo ""

echo "⚠️  IMPORTANT: You need your database password to continue."
echo "   This is the password you set when creating the Supabase project."
echo ""

read -p "Enter your Supabase database password: " -s DB_PASSWORD
echo ""

if [ -z "$DB_PASSWORD" ]; then
    echo "❌ Password cannot be empty"
    exit 1
fi

# Build connection string
DB_URL="postgresql://postgres:${DB_PASSWORD}@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres"

echo ""
echo "✅ Connection string generated"
echo ""

# Test connection
echo "🔌 Testing database connection..."
cd backend

# Check if asyncpg is installed
if ! python -c "import asyncpg" 2>/dev/null; then
    echo "📦 Installing asyncpg..."
    pip install asyncpg > /dev/null 2>&1
fi

# Test connection
python3 << EOF
import asyncio
import asyncpg
import sys

async def test():
    try:
        conn = await asyncpg.connect("$DB_URL")
        print("✅ Successfully connected to Supabase!")
        await conn.close()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print("")
        print("Please check:")
        print("1. Your database password is correct")
        print("2. Your IP is whitelisted in Supabase (Settings → Database → Connection pooling)")
        sys.exit(1)

asyncio.run(test())
EOF

if [ $? -ne 0 ]; then
    exit 1
fi

echo ""
echo "📝 Next steps:"
echo ""
echo "1. Run the database migration:"
echo "   - Go to: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd/sql"
echo "   - Click 'New query'"
echo "   - Copy contents of: supabase/migrations/001_initial_schema.sql"
echo "   - Paste and click 'Run'"
echo ""
echo "2. Set environment variables:"
echo "   Add to backend/.env:"
echo "   SUPABASE_DB_URL=$DB_URL"
echo ""
echo "3. Or export for current session:"
echo "   export SUPABASE_DB_URL=\"$DB_URL\""
echo ""
echo "4. Start the backend:"
echo "   cd backend"
echo "   uvicorn server:app --reload"
echo ""

