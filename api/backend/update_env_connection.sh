#!/bin/bash
# Update SUPABASE_DB_URL in .env file with correct password

PASSWORD="Mridulahemant1*"
ENCODED_PASSWORD="Mridulahemant1%2A"

echo "🔧 Updating SUPABASE_DB_URL in backend/.env"
echo ""

# Try Session Pooler format (recommended)
SESSION_POOLER_URL="postgresql://postgres.gjwzaylkzknsykjvtpcd:${PASSWORD}@aws-0-ap-south-1.pooler.supabase.com:6543/postgres"

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    touch .env
fi

# Backup existing .env
if [ -f .env ]; then
    cp .env .env.backup
    echo "✅ Backed up existing .env to .env.backup"
fi

# Update or add SUPABASE_DB_URL
if grep -q "SUPABASE_DB_URL" .env; then
    # Update existing
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|SUPABASE_DB_URL=.*|SUPABASE_DB_URL=${SESSION_POOLER_URL}|" .env
    else
        # Linux
        sed -i "s|SUPABASE_DB_URL=.*|SUPABASE_DB_URL=${SESSION_POOLER_URL}|" .env
    fi
    echo "✅ Updated SUPABASE_DB_URL in .env"
else
    # Add new
    echo "" >> .env
    echo "SUPABASE_DB_URL=${SESSION_POOLER_URL}" >> .env
    echo "✅ Added SUPABASE_DB_URL to .env"
fi

echo ""
echo "📋 Updated connection string:"
echo "   SUPABASE_DB_URL=${SESSION_POOLER_URL}"
echo ""
echo "🧪 Test connection:"
echo "   python3 test_db_connection.py"
echo ""
echo "⚠️  If connection fails, you may need to:"
echo "   1. Get the exact connection string from Supabase Dashboard"
echo "   2. Verify the project is active"
echo "   3. Check if password needs URL encoding"

