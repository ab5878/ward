"""
Test Full Operator Flow
Tests the complete operator onboarding → fleet → driver → reporting flow
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

load_dotenv()

BASE_URL = os.getenv("WARD_API_BASE_URL", "http://localhost:8001/api")
TEST_EMAIL = f"operator_flow_{int(datetime.now().timestamp())}@test.com"
TEST_PASSWORD = "TestPass123!"

AUTH_TOKEN = None
OPERATOR_ID = None
VEHICLE_ID = None
MAGIC_LINK_TOKEN = None
CASE_ID = None

def log(message, status="INFO"):
    symbols = {"INFO": "•", "PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}
    print(f"{symbols.get(status, '•')} {message}")

def make_request(method, endpoint, data=None, headers=None, expected_status=200):
    url = f"{BASE_URL}{endpoint}"
    test_headers = {'Content-Type': 'application/json'}
    if AUTH_TOKEN:
        test_headers['Authorization'] = f'Bearer {AUTH_TOKEN}'
    if headers:
        test_headers.update(headers)
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=test_headers, timeout=30)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=test_headers, timeout=30)
        
        if response.status_code == expected_status:
            log(f"PASS - {method} {endpoint}", "PASS")
            try:
                return response.json()
            except:
                return response.text
        else:
            log(f"FAIL - {method} {endpoint} (Expected {expected_status}, got {response.status_code})", "FAIL")
            try:
                log(f"  Response: {response.json()}", "FAIL")
            except:
                log(f"  Response: {response.text[:200]}", "FAIL")
            return None
    except requests.exceptions.RequestException as e:
        log(f"FAIL - {method} {endpoint} (Request failed: {e})", "FAIL")
        return None

def test_full_flow():
    global AUTH_TOKEN, OPERATOR_ID, VEHICLE_ID, MAGIC_LINK_TOKEN, CASE_ID
    
    log("=" * 60)
    log("Ward Operator Full Flow Test")
    log("=" * 60)
    
    # Step 1: Register & Login
    log("\n--- Step 1: Authentication ---")
    register_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    response = make_request('POST', '/auth/register', data=register_data, expected_status=200)
    if not response:
        log("Failed to register. Exiting.", "FAIL")
        return False
    
    AUTH_TOKEN = response.get('access_token')
    log("Registered successfully", "PASS")
    
    login_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    response = make_request('POST', '/auth/login', data=login_data, expected_status=200)
    if not response:
        log("Failed to login. Exiting.", "FAIL")
        return False
    
    AUTH_TOKEN = response.get('access_token')
    log("Logged in successfully", "PASS")
    
    # Step 2: Create Operator Account
    log("\n--- Step 2: Create Operator Account ---")
    operator_data = {
        "company_name": "Test Transporters Pvt Ltd",
        "email": TEST_EMAIL,  # Use same email as user
        "phone": "+91-98765-43210",
        "fleet_size": 5,
        "account_type": "pilot"
    }
    response = make_request('POST', '/operators/create', data=operator_data, expected_status=200)
    if not response:
        log("Failed to create operator. Exiting.", "FAIL")
        return False
    
    OPERATOR_ID = response.get('operator_id')
    log(f"Created operator: {OPERATOR_ID}", "PASS")
    
    # Step 3: Add Vehicle
    log("\n--- Step 3: Add Vehicle to Fleet ---")
    vehicle_data = {
        "vehicle_number": f"FLOW-TEST-{int(datetime.now().timestamp())}",
        "vehicle_type": "truck",
        "driver_name": "Test Driver",
        "driver_phone": "+91-98765-43211",
        "route": "JNPT-Delhi"
    }
    response = make_request('POST', '/operators/fleet/add', data=vehicle_data, expected_status=200)
    if not response:
        log("Failed to add vehicle. Exiting.", "FAIL")
        return False
    
    VEHICLE_ID = response.get('vehicle_id')
    log(f"Added vehicle: {VEHICLE_ID}", "PASS")
    
    # Step 4: Get Fleet
    log("\n--- Step 4: Verify Fleet ---")
    response = make_request('GET', '/operators/fleet', expected_status=200)
    if response and isinstance(response, list) and len(response) > 0:
        log(f"Fleet verified: {len(response)} vehicle(s)", "PASS")
    else:
        log("Fleet verification failed", "FAIL")
        return False
    
    # Step 5: Get Dashboard
    log("\n--- Step 5: Check Dashboard ---")
    response = make_request('GET', '/operators/dashboard?days=7', expected_status=200)
    if response:
        log(f"Dashboard loaded: Fleet size = {response.get('fleet_size', 0)}", "PASS")
    else:
        log("Dashboard check failed", "FAIL")
        return False
    
    # Step 6: Generate Magic Links
    log("\n--- Step 6: Generate Magic Links ---")
    response = make_request('POST', '/operators/drivers/generate-links?method=magic_link', expected_status=200)
    if not response:
        log("Failed to generate magic links. Exiting.", "FAIL")
        return False
    
    links = response.get('links', [])
    if len(links) == 0:
        log("No magic links generated", "FAIL")
        return False
    
    link_url = links[0].get('link', '')
    if '/driver/' in link_url:
        MAGIC_LINK_TOKEN = link_url.split('/driver/')[-1]
        log(f"Generated magic link: {MAGIC_LINK_TOKEN[:30]}...", "PASS")
    else:
        log("Invalid magic link format", "FAIL")
        return False
    
    # Step 7: Verify Driver Token
    log("\n--- Step 7: Verify Driver Token ---")
    response = make_request('GET', f'/driver/verify/{MAGIC_LINK_TOKEN}', expected_status=200)
    if not response:
        log("Failed to verify driver token. Exiting.", "FAIL")
        return False
    
    if response.get('valid'):
        log(f"Token verified: Vehicle {response.get('vehicle_number')}", "PASS")
    else:
        log("Token verification failed", "FAIL")
        return False
    
    # Step 8: Driver Report (without audio for now)
    log("\n--- Step 8: Driver Report Disruption ---")
    report_data = {
        "token": MAGIC_LINK_TOKEN,
        "audio_base64": "",  # Empty for now
        "audio_format": "webm",
        "language_code": "hi-IN"
    }
    response = make_request('POST', '/driver/report', data=report_data, expected_status=200)
    if not response:
        log("Failed to report disruption. Exiting.", "FAIL")
        return False
    
    CASE_ID = response.get('case_id')
    log(f"Disruption reported: Case {CASE_ID}", "PASS")
    
    # Step 9: Verify Case Created
    log("\n--- Step 9: Verify Case in Dashboard ---")
    response = make_request('GET', '/operators/dashboard?days=7', expected_status=200)
    if response:
        total_cases = response.get('total_cases', 0)
        if total_cases > 0:
            log(f"Case verified in dashboard: {total_cases} case(s)", "PASS")
        else:
            log("Case not found in dashboard", "WARN")
    else:
        log("Dashboard check failed", "WARN")
    
    log("\n" + "=" * 60)
    log("Full Flow Test Complete!")
    log("=" * 60)
    log(f"Operator ID: {OPERATOR_ID}", "INFO")
    log(f"Vehicle ID: {VEHICLE_ID}", "INFO")
    log(f"Magic Link Token: {MAGIC_LINK_TOKEN[:30]}...", "INFO")
    log(f"Case ID: {CASE_ID}", "INFO")
    log("\n✅ All steps completed successfully!", "PASS")
    
    return True

if __name__ == "__main__":
    success = test_full_flow()
    sys.exit(0 if success else 1)

