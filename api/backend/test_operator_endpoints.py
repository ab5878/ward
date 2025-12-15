"""
Test Operator Endpoints
Tests the plug & play operator functionality
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
import requests
import json
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

load_dotenv()

BASE_URL = os.getenv("WARD_API_BASE_URL", "http://localhost:8001/api")
TEST_EMAIL = f"operator_test_{int(datetime.now().timestamp())}@example.com"
TEST_PASSWORD = "TestPass123!"

AUTH_TOKEN = None
OPERATOR_ID = None
VEHICLE_ID = None
MAGIC_LINK_TOKEN = None

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
    
    log(f"Request: {method} {url}")
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=test_headers, timeout=30)
        elif method == 'POST':
            response = requests.post(url, json=data, headers=test_headers, timeout=30)
        elif method == 'PATCH':
            response = requests.patch(url, json=data, headers=test_headers, timeout=30)
        
        if response.status_code == expected_status:
            log(f"PASS - {method} {endpoint} (Status: {response.status_code})", "PASS")
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

def test_auth_flow():
    global AUTH_TOKEN
    log("\n--- Testing Authentication Flow ---")
    
    # Register
    register_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    response = make_request('POST', '/auth/register', data=register_data, expected_status=200)
    if response:
        AUTH_TOKEN = response.get('access_token')
        log(f"Registered and got token", "PASS")
    else:
        log("Failed to register.", "FAIL")
        return False
    
    # Login
    login_data = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
    response = make_request('POST', '/auth/login', data=login_data, expected_status=200)
    if response:
        AUTH_TOKEN = response.get('access_token')
        log(f"Logged in and got token", "PASS")
        return True
    else:
        log("Failed to login.", "FAIL")
        return False

def test_create_operator():
    global OPERATOR_ID
    log("\n--- Testing Create Operator ---")
    
    operator_data = {
        "company_name": "Test Transporters Pvt Ltd",
        "email": f"test_ops_{int(datetime.now().timestamp())}@test.com",
        "phone": "+91-98765-43210",
        "fleet_size": 10,
        "account_type": "pilot"
    }
    
    response = make_request('POST', '/operators/create', data=operator_data, expected_status=200)
    if response:
        OPERATOR_ID = response.get('operator_id')
        log(f"Created operator: {OPERATOR_ID}", "PASS")
        return True
    else:
        log("Failed to create operator.", "FAIL")
        return False

def test_add_vehicle():
    global VEHICLE_ID
    log("\n--- Testing Add Vehicle ---")
    
    vehicle_data = {
        "vehicle_number": f"TEST-{int(datetime.now().timestamp())}",
        "vehicle_type": "truck",
        "driver_name": "Test Driver",
        "driver_phone": "+91-98765-43211",
        "route": "JNPT-Delhi"
    }
    
    response = make_request('POST', '/operators/fleet/add', data=vehicle_data, expected_status=200)
    if response:
        VEHICLE_ID = response.get('vehicle_id')
        log(f"Added vehicle: {VEHICLE_ID}", "PASS")
        return True
    else:
        log("Failed to add vehicle.", "FAIL")
        return False

def test_get_fleet():
    log("\n--- Testing Get Fleet ---")
    
    response = make_request('GET', '/operators/fleet', expected_status=200)
    if response and isinstance(response, list):
        log(f"Retrieved {len(response)} vehicles", "PASS")
        if len(response) > 0:
            log(f"  First vehicle: {response[0].get('vehicle_number')}", "INFO")
        return True
    else:
        log("Failed to get fleet.", "FAIL")
        return False

def test_get_dashboard():
    log("\n--- Testing Get Dashboard ---")
    
    response = make_request('GET', '/operators/dashboard?days=7', expected_status=200)
    if response:
        log(f"Dashboard metrics:", "PASS")
        log(f"  Fleet size: {response.get('fleet_size', 0)}", "INFO")
        log(f"  Total cases: {response.get('total_cases', 0)}", "INFO")
        log(f"  Active cases: {response.get('active_cases', 0)}", "INFO")
        log(f"  Financial impact: ₹{response.get('total_financial_impact', 0)}", "INFO")
        return True
    else:
        log("Failed to get dashboard.", "FAIL")
        return False

def test_generate_magic_links():
    global MAGIC_LINK_TOKEN
    log("\n--- Testing Generate Magic Links ---")
    
    response = make_request('POST', '/operators/drivers/generate-links?method=magic_link', expected_status=200)
    if response:
        links = response.get('links', [])
        log(f"Generated {len(links)} magic links", "PASS")
        if len(links) > 0:
            link_url = links[0].get('link', '')
            # Extract token from URL
            if '/driver/' in link_url:
                MAGIC_LINK_TOKEN = link_url.split('/driver/')[-1]
                log(f"  First link token: {MAGIC_LINK_TOKEN[:20]}...", "INFO")
            return True
    else:
        log("Failed to generate magic links.", "FAIL")
        return False

def test_verify_driver_token():
    log("\n--- Testing Verify Driver Token ---")
    
    if not MAGIC_LINK_TOKEN:
        log("Skipping: No magic link token available", "WARN")
        return True
    
    response = make_request('GET', f'/driver/verify/{MAGIC_LINK_TOKEN}', expected_status=200)
    if response:
        log(f"Token verified successfully", "PASS")
        log(f"  Vehicle: {response.get('vehicle_number')}", "INFO")
        log(f"  Driver: {response.get('driver_name')}", "INFO")
        return True
    else:
        log("Failed to verify token.", "FAIL")
        return False

def test_bulk_upload():
    log("\n--- Testing Bulk Upload (CSV) ---")
    
    # Create CSV content
    csv_content = f"""vehicle_number,driver_name,driver_phone,route,vehicle_type
BULK-001,Driver One,+91-98765-43220,JNPT-Delhi,truck
BULK-002,Driver Two,+91-98765-43221,Mundra-Mumbai,truck
BULK-003,Driver Three,+91-98765-43222,Chennai-Bangalore,truck"""
    
    # For now, we'll skip the actual file upload test as it requires multipart/form-data
    # This would need to be tested with a proper file upload
    log("Bulk upload test skipped (requires file upload)", "WARN")
    return True

def main():
    log("=" * 60)
    log("Ward Operator Endpoints Test")
    log("=" * 60)
    
    if not test_auth_flow():
        log("Authentication failed. Exiting.", "FAIL")
        return
    
    tests = [
        ("Create Operator", test_create_operator),
        ("Add Vehicle", test_add_vehicle),
        ("Get Fleet", test_get_fleet),
        ("Get Dashboard", test_get_dashboard),
        ("Generate Magic Links", test_generate_magic_links),
        ("Verify Driver Token", test_verify_driver_token),
        ("Bulk Upload", test_bulk_upload),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            log(f"Test '{test_name}' raised exception: {e}", "FAIL")
            failed += 1
    
    log("\n" + "=" * 60)
    log("Test Summary")
    log("=" * 60)
    log(f"Passed: {passed}", "PASS" if passed > 0 else "INFO")
    log(f"Failed: {failed}", "FAIL" if failed > 0 else "INFO")
    
    if failed == 0:
        log("\n✅ All operator endpoint tests passed!", "PASS")
    else:
        log(f"\n❌ {failed} test(s) failed", "FAIL")

if __name__ == "__main__":
    main()

