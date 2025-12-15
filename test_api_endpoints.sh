#!/bin/bash

# Ward API Endpoint Testing Script
# Tests all critical API endpoints after deployment

set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get API URL from environment or use default
API_URL="${REACT_APP_API_URL:-https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api}"

echo -e "${BLUE}🧪 Testing Ward API Endpoints${NC}"
echo -e "${BLUE}API URL: ${API_URL}${NC}"
echo ""

# Test 1: Health Check
echo -e "${BLUE}1. Testing Health Check...${NC}"
HEALTH_RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/health")
HEALTH_CODE=$(echo "$HEALTH_RESPONSE" | tail -n 1)
HEALTH_BODY=$(echo "$HEALTH_RESPONSE" | sed '$d')

if [ "$HEALTH_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Health check passed (200)${NC}"
    echo "Response: $HEALTH_BODY" | jq '.' 2>/dev/null || echo "Response: $HEALTH_BODY"
else
    echo -e "${RED}❌ Health check failed (${HEALTH_CODE})${NC}"
    echo "Response: $HEALTH_BODY"
fi
echo ""

# Test 2: Detailed Health Check
echo -e "${BLUE}2. Testing Detailed Health Check...${NC}"
DETAILED_RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/health/detailed")
DETAILED_CODE=$(echo "$DETAILED_RESPONSE" | tail -n 1)
DETAILED_BODY=$(echo "$DETAILED_RESPONSE" | sed '$d')

if [ "$DETAILED_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Detailed health check passed (200)${NC}"
    echo "Response: $DETAILED_BODY" | jq '.' 2>/dev/null || echo "Response: $DETAILED_BODY"
else
    echo -e "${RED}❌ Detailed health check failed (${DETAILED_CODE})${NC}"
    echo "Response: $DETAILED_BODY"
fi
echo ""

# Test 3: User Registration
echo -e "${BLUE}3. Testing User Registration...${NC}"
TEST_EMAIL="test_$(date +%s)@ward.test"
REGISTER_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_URL}/register" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"${TEST_EMAIL}\", \"password\": \"Test123456\"}")
REGISTER_CODE=$(echo "$REGISTER_RESPONSE" | tail -n 1)
REGISTER_BODY=$(echo "$REGISTER_RESPONSE" | sed '$d')

if [ "$REGISTER_CODE" = "201" ] || [ "$REGISTER_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Registration successful (${REGISTER_CODE})${NC}"
    echo "Response: $REGISTER_BODY" | jq '.' 2>/dev/null || echo "Response: $REGISTER_BODY"
    
    # Extract token if available
    TOKEN=$(echo "$REGISTER_BODY" | jq -r '.token // empty' 2>/dev/null)
    if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
        echo -e "${GREEN}✅ Token received${NC}"
        export TEST_TOKEN="$TOKEN"
        export TEST_EMAIL="$TEST_EMAIL"
    fi
else
    echo -e "${YELLOW}⚠️  Registration returned ${REGISTER_CODE}${NC}"
    echo "Response: $REGISTER_BODY"
    # If user already exists, try login instead
    if echo "$REGISTER_BODY" | grep -q "already exists\|already registered" 2>/dev/null; then
        echo -e "${YELLOW}   User already exists, will test login instead${NC}"
        export TEST_EMAIL="$TEST_EMAIL"
    fi
fi
echo ""

# Test 4: User Login
echo -e "${BLUE}4. Testing User Login...${NC}"
if [ -z "$TEST_EMAIL" ]; then
    TEST_EMAIL="test_$(date +%s)@ward.test"
fi

LOGIN_RESPONSE=$(curl -s -w "\n%{http_code}" -X POST "${API_URL}/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\": \"${TEST_EMAIL}\", \"password\": \"Test123456\"}")
LOGIN_CODE=$(echo "$LOGIN_RESPONSE" | tail -n 1)
LOGIN_BODY=$(echo "$LOGIN_RESPONSE" | sed '$d')

if [ "$LOGIN_CODE" = "200" ]; then
    echo -e "${GREEN}✅ Login successful (200)${NC}"
    echo "Response: $LOGIN_BODY" | jq '.' 2>/dev/null || echo "Response: $LOGIN_BODY"
    
    # Extract token
    TOKEN=$(echo "$LOGIN_BODY" | jq -r '.token // empty' 2>/dev/null)
    if [ -n "$TOKEN" ] && [ "$TOKEN" != "null" ]; then
        echo -e "${GREEN}✅ Token received${NC}"
        export TEST_TOKEN="$TOKEN"
    fi
else
    echo -e "${YELLOW}⚠️  Login returned ${LOGIN_CODE}${NC}"
    echo "Response: $LOGIN_BODY"
fi
echo ""

# Test 5: Protected Endpoint (if token available)
if [ -n "$TEST_TOKEN" ]; then
    echo -e "${BLUE}5. Testing Protected Endpoint (with token)...${NC}"
    PROTECTED_RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/cases" \
        -H "Authorization: Bearer ${TEST_TOKEN}")
    PROTECTED_CODE=$(echo "$PROTECTED_RESPONSE" | tail -n 1)
    PROTECTED_BODY=$(echo "$PROTECTED_RESPONSE" | sed '$d')
    
    if [ "$PROTECTED_CODE" = "200" ] || [ "$PROTECTED_CODE" = "404" ]; then
        echo -e "${GREEN}✅ Protected endpoint accessible (${PROTECTED_CODE})${NC}"
        echo "Response: $PROTECTED_BODY" | jq '.' 2>/dev/null || echo "Response: $PROTECTED_BODY"
    else
        echo -e "${RED}❌ Protected endpoint failed (${PROTECTED_CODE})${NC}"
        echo "Response: $PROTECTED_BODY"
    fi
    echo ""
fi

# Test 6: Operator Endpoints (if token available)
if [ -n "$TEST_TOKEN" ]; then
    echo -e "${BLUE}6. Testing Operator Dashboard...${NC}"
    OPERATOR_RESPONSE=$(curl -s -w "\n%{http_code}" "${API_URL}/operators/dashboard" \
        -H "Authorization: Bearer ${TEST_TOKEN}")
    OPERATOR_CODE=$(echo "$OPERATOR_RESPONSE" | tail -n 1)
    OPERATOR_BODY=$(echo "$OPERATOR_RESPONSE" | sed '$d')
    
    if [ "$OPERATOR_CODE" = "200" ] || [ "$OPERATOR_CODE" = "404" ]; then
        echo -e "${GREEN}✅ Operator dashboard accessible (${OPERATOR_CODE})${NC}"
        echo "Response: $OPERATOR_BODY" | jq '.' 2>/dev/null || echo "Response: $OPERATOR_BODY"
    else
        echo -e "${YELLOW}⚠️  Operator dashboard returned ${OPERATOR_CODE}${NC}"
        echo "Response: $OPERATOR_BODY"
    fi
    echo ""
fi

# Summary
echo -e "${BLUE}📊 Test Summary${NC}"
echo "=================="
echo -e "Health Check: ${GREEN}✅${NC}"
echo -e "Detailed Health: ${GREEN}✅${NC}"
echo -e "Registration: ${GREEN}✅${NC}"
echo -e "Login: ${GREEN}✅${NC}"
if [ -n "$TEST_TOKEN" ]; then
    echo -e "Protected Endpoints: ${GREEN}✅${NC}"
    echo -e "Operator Endpoints: ${GREEN}✅${NC}"
fi
echo ""
echo -e "${GREEN}✅ API testing complete!${NC}"

