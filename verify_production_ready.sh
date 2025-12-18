#!/bin/bash

# Ward Production Readiness Verification Script
# Verifies all components are ready for production deployment

set -e

echo "🔍 Ward Production Readiness Verification"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

PASSED=0
FAILED=0
WARNINGS=0

check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
        ((PASSED++))
        return 0
    else
        echo -e "${RED}❌ $1${NC}"
        ((FAILED++))
        return 1
    fi
}

warn() {
    echo -e "${YELLOW}⚠️  $1${NC}"
    ((WARNINGS++))
}

info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# 1. Check required files
echo "📁 Checking Required Files..."
echo ""

[ -f "backend/server.py" ] && check "Backend server.py exists" || warn "Backend server.py missing"
[ -f "backend/operator_service.py" ] && check "Operator service exists" || warn "Operator service missing"
[ -f "backend/webhook_service.py" ] && check "Webhook service exists" || warn "Webhook service missing"
[ -f "backend/db_adapter.py" ] && check "Database adapter exists" || warn "Database adapter missing"
[ -f "backend/db_compat.py" ] && check "DB compat layer exists" || warn "DB compat layer missing"

[ -f "frontend/src/pages/OperatorOnboarding.jsx" ] && check "Operator onboarding UI exists" || warn "Operator onboarding UI missing"
[ -f "frontend/src/pages/OperatorDashboard.jsx" ] && check "Operator dashboard UI exists" || warn "Operator dashboard UI missing"
[ -f "frontend/src/pages/DriverApp.jsx" ] && check "Driver app UI exists" || warn "Driver app UI missing"

[ -f "supabase/migrations/003_operator_tables.sql" ] && check "Operator migration exists" || warn "Operator migration missing"

echo ""

# 2. Check Python dependencies
echo "🐍 Checking Python Dependencies..."
echo ""

if [ -f "backend/requirements.txt" ]; then
    check "requirements.txt exists"
    info "  Run: pip install -r backend/requirements.txt"
else
    warn "requirements.txt missing"
fi

echo ""

# 3. Check Node dependencies
echo "📦 Checking Node Dependencies..."
echo ""

if [ -f "frontend/package.json" ]; then
    check "package.json exists"
    info "  Run: cd frontend && npm install"
else
    warn "package.json missing"
fi

echo ""

# 4. Check environment variables
echo "🔐 Checking Environment Variables..."
echo ""

if [ -z "$SUPABASE_DB_URL" ]; then
    warn "SUPABASE_DB_URL not set"
else
    check "SUPABASE_DB_URL is set"
fi

if [ -z "$JWT_SECRET" ]; then
    warn "JWT_SECRET not set"
else
    check "JWT_SECRET is set"
fi

if [ -z "$OPENAI_API_KEY" ]; then
    warn "OPENAI_API_KEY not set (optional)"
else
    check "OPENAI_API_KEY is set"
fi

if [ -z "$SARVAM_API_KEY" ]; then
    warn "SARVAM_API_KEY not set (optional)"
else
    check "SARVAM_API_KEY is set"
fi

echo ""

# 5. Check API endpoints
echo "🔌 Checking API Endpoints..."
echo ""

ENDPOINTS=(
    "POST /api/operators/create"
    "POST /api/operators/fleet/add"
    "GET /api/operators/fleet"
    "GET /api/operators/dashboard"
    "GET /api/operators/settings"
    "PATCH /api/operators/settings"
    "POST /api/operators/drivers/generate-links"
    "GET /api/driver/verify/{token}"
    "POST /api/driver/report"
    "GET /api/health"
)

for endpoint in "${ENDPOINTS[@]}"; do
    if grep -q "$endpoint" backend/server.py 2>/dev/null; then
        check "Endpoint exists: $endpoint"
    else
        warn "Endpoint missing: $endpoint"
    fi
done

echo ""

# 6. Check database migrations
echo "🗄️  Checking Database Migrations..."
echo ""

if [ -f "supabase/migrations/001_initial_schema.sql" ]; then
    check "Initial schema migration exists"
fi

if [ -f "supabase/migrations/002_api_v0_tables.sql" ]; then
    check "API v0 migration exists"
fi

if [ -f "supabase/migrations/003_operator_tables.sql" ]; then
    check "Operator tables migration exists"
fi

echo ""

# 7. Check documentation
echo "📚 Checking Documentation..."
echo ""

DOCS=(
    "OPERATOR_QUICK_START.md"
    "OPERATOR_API_DOCS.md"
    "PRODUCTION_DEPLOYMENT_CHECKLIST.md"
    "INTEGRATION_EXAMPLES.md"
    "COMPLETE_IMPLEMENTATION_SUMMARY.md"
)

for doc in "${DOCS[@]}"; do
    if [ -f "$doc" ]; then
        check "Documentation exists: $doc"
    else
        warn "Documentation missing: $doc"
    fi
done

echo ""

# 8. Check deployment script
echo "🚀 Checking Deployment Scripts..."
echo ""

if [ -f "deploy_operator.sh" ]; then
    check "Deployment script exists"
    if [ -x "deploy_operator.sh" ]; then
        check "Deployment script is executable"
    else
        warn "Deployment script is not executable (run: chmod +x deploy_operator.sh)"
    fi
else
    warn "Deployment script missing"
fi

echo ""

# Summary
echo "=========================================="
echo "📊 Verification Summary"
echo "=========================================="
echo -e "${GREEN}✅ Passed: $PASSED${NC}"
echo -e "${RED}❌ Failed: $FAILED${NC}"
echo -e "${YELLOW}⚠️  Warnings: $WARNINGS${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    if [ $WARNINGS -eq 0 ]; then
        echo -e "${GREEN}🎉 All checks passed! Ready for production.${NC}"
        exit 0
    else
        echo -e "${YELLOW}⚠️  Ready for production with warnings.${NC}"
        exit 0
    fi
else
    echo -e "${RED}❌ Some checks failed. Please fix before deploying.${NC}"
    exit 1
fi

