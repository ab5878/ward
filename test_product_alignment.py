#!/usr/bin/env python3
"""
Product Alignment Test Script
Tests all functionality to ensure alignment with Ward's problem statement and solution.
"""

import requests
import json
import time
import sys
from datetime import datetime

BASE_URL = "http://localhost:8001/api"
TEST_EMAIL = f"test_alignment_{int(time.time())}@ward.com"
TEST_PASSWORD = "Test123!"

# Test results
results = {
    "passed": [],
    "failed": [],
    "warnings": []
}

def log_test(name, passed, message=""):
    """Log test result"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}: {name}")
    if message:
        print(f"   {message}")
    
    if passed:
        results["passed"].append(name)
    else:
        results["failed"].append(name)

def log_warning(name, message):
    """Log warning"""
    print(f"⚠️  WARN: {name}")
    print(f"   {message}")
    results["warnings"].append(f"{name}: {message}")

# Global token
auth_token = None
test_case_id = None

print("=" * 70)
print("WARD PRODUCT ALIGNMENT TEST")
print("=" * 70)
print(f"Testing against: {BASE_URL}")
print(f"Test user: {TEST_EMAIL}")
print()

# ============================================================================
# 1. SIGNIN & ACCESS (Foundation)
# ============================================================================
print("=" * 70)
print("1. SIGNIN & ACCESS")
print("=" * 70)

# Register
print("\n1.1 Testing user registration...")
try:
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
        timeout=10
    )
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        auth_token = response.json().get("access_token")
        log_test("User Registration", True, f"Token received in {elapsed:.2f}s")
    else:
        # Maybe user already exists, try login
        log_warning("User Registration", f"Status {response.status_code}, trying login...")
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
            timeout=10
        )
        if response.status_code == 200:
            auth_token = response.json().get("access_token")
            log_test("User Login (fallback)", True, f"Token received in {elapsed:.2f}s")
        else:
            log_test("User Registration/Login", False, f"Status {response.status_code}: {response.text}")
            sys.exit(1)
except Exception as e:
    log_test("User Registration", False, str(e))
    sys.exit(1)

# Login
print("\n1.2 Testing user login...")
try:
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
        timeout=10
    )
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        auth_token = response.json().get("access_token")
        log_test("User Login", True, f"Token received in {elapsed:.2f}s")
    else:
        log_test("User Login", False, f"Status {response.status_code}: {response.text}")
except Exception as e:
    log_test("User Login", False, str(e))

# Get /me
print("\n1.3 Testing /me endpoint...")
try:
    response = requests.get(
        f"{BASE_URL}/auth/me",
        headers={"Authorization": f"Bearer {auth_token}"},
        timeout=10
    )
    if response.status_code == 200:
        user_data = response.json()
        log_test("Get User Info", True, f"Email: {user_data.get('email')}")
    else:
        log_test("Get User Info", False, f"Status {response.status_code}")
except Exception as e:
    log_test("Get User Info", False, str(e))

# Dashboard (cases list)
print("\n1.4 Testing dashboard (cases list)...")
try:
    start_time = time.time()
    response = requests.get(
        f"{BASE_URL}/cases",
        headers={"Authorization": f"Bearer {auth_token}"},
        timeout=10
    )
    elapsed = time.time() - start_time
    
    if response.status_code == 200:
        cases = response.json()
        log_test("Dashboard Load", True, f"Found {len(cases)} cases in {elapsed:.2f}s")
    else:
        log_test("Dashboard Load", False, f"Status {response.status_code}")
except Exception as e:
    log_test("Dashboard Load", False, str(e))

# ============================================================================
# 2. CASE CREATION (Problem: Capture Disruption)
# Requirement: ≤5 seconds from incident to log
# ============================================================================
print("\n" + "=" * 70)
print("2. CASE CREATION (Fast Capture)")
print("=" * 70)

print("\n2.1 Testing case creation speed...")
try:
    start_time = time.time()
    response = requests.post(
        f"{BASE_URL}/cases",
        headers={"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"},
        json={
            "description": "Container stuck at JNPT gate. Driver reports customs hold.",
            "disruption_details": {
                "disruption_type": "customs_hold",
                "scope": "container",
                "identifier": "JNPT-GATE-4",
                "time_discovered_ist": datetime.now().strftime("%H:%M IST"),
                "source": "Driver Call"
            },
            "shipment_identifiers": {
                "ids": ["CON-12345"],
                "routes": ["Mundra-Delhi"],
                "carriers": ["Maersk"]
            },
            "financial_impact": {
                "currency": "INR",
                "amount": 5000,
                "category": "demurrage"
            }
        },
        timeout=10
    )
    elapsed = time.time() - start_time
    
    if response.status_code in [200, 201]:
        case_data = response.json()
        test_case_id = case_data.get("_id")
        log_test("Case Creation", True, f"Created in {elapsed:.2f}s (ID: {test_case_id})")
        
        # Check if it's fast enough (≤5 seconds)
        if elapsed <= 5.0:
            log_test("Case Creation Speed", True, f"✅ Meets requirement (≤5s)")
        else:
            log_warning("Case Creation Speed", f"⚠️  Takes {elapsed:.2f}s (target: ≤5s)")
    else:
        log_test("Case Creation", False, f"Status {response.status_code}: {response.text}")
except Exception as e:
    log_test("Case Creation", False, str(e))

# ============================================================================
# 3. TIMELINE/EVENT LOGGING (Solution: Evidence Capture)
# Requirement: Capture 100% of field data, timestamped
# ============================================================================
print("\n" + "=" * 70)
print("3. TIMELINE/EVENT LOGGING (Evidence Capture)")
print("=" * 70)

if not test_case_id:
    log_warning("Timeline Tests", "Skipping - no test case ID")
else:
    # Add voice event
    print("\n3.1 Testing voice event addition...")
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/cases/{test_case_id}/timeline",
            headers={"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"},
            json={
                "content": "Driver called: Container stuck at gate 4. Customs officer says HS code mismatch.",
                "source_type": "voice",
                "reliability": "high"
            },
            timeout=10
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            log_test("Add Voice Event", True, f"Added in {elapsed:.2f}s")
        else:
            log_test("Add Voice Event", False, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        log_test("Add Voice Event", False, str(e))
    
    # Add text event
    print("\n3.2 Testing text event addition...")
    try:
        response = requests.post(
            f"{BASE_URL}/cases/{test_case_id}/timeline",
            headers={"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"},
            json={
                "content": "CHA confirmed: Invoice shows 'Electronics', BL shows 'Computer Parts'. Need correction.",
                "source_type": "text",
                "reliability": "high"
            },
            timeout=10
        )
        if response.status_code == 200:
            log_test("Add Text Event", True)
        else:
            log_test("Add Text Event", False, f"Status {response.status_code}")
    except Exception as e:
        log_test("Add Text Event", False, str(e))
    
    # Get timeline
    print("\n3.3 Testing timeline retrieval...")
    try:
        response = requests.get(
            f"{BASE_URL}/cases/{test_case_id}",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=10
        )
        if response.status_code == 200:
            case_data = response.json()
            timeline = case_data.get("timeline", [])
            log_test("Get Timeline", True, f"Found {len(timeline)} events")
            
            # Check if events are timestamped
            if timeline:
                has_timestamps = all("timestamp" in event for event in timeline)
                log_test("Events Timestamped", has_timestamps, "All events have timestamps" if has_timestamps else "Some events missing timestamps")
        else:
            log_test("Get Timeline", False, f"Status {response.status_code}")
    except Exception as e:
        log_test("Get Timeline", False, str(e))

# ============================================================================
# 4. EVIDENCE SCORING (Solution: Audit-Grade Evidence)
# Requirement: Real-time 0-100% score, turns green at 70%
# ============================================================================
print("\n" + "=" * 70)
print("4. EVIDENCE SCORING (Audit-Grade Evidence)")
print("=" * 70)

if not test_case_id:
    log_warning("Evidence Scoring Tests", "Skipping - no test case ID")
else:
    # Check evidence score
    print("\n4.1 Testing evidence score retrieval...")
    try:
        response = requests.get(
            f"{BASE_URL}/cases/{test_case_id}/evidence",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=10
        )
        if response.status_code == 200:
            evidence_data = response.json()
            score = evidence_data.get("score", 0)
            breakdown = evidence_data.get("breakdown", [])
            missing = evidence_data.get("missing_actions", [])
            
            log_test("Get Evidence Score", True, f"Score: {score}%")
            log_test("Score Breakdown Available", len(breakdown) > 0, f"Breakdown: {len(breakdown)} items")
            log_test("Missing Actions Listed", len(missing) > 0, f"Missing: {len(missing)} actions")
            
            # Check if score is audit-grade (≥70%)
            if score >= 70:
                log_test("Audit-Grade Score", True, f"✅ Score {score}% ≥ 70% (audit-grade)")
            else:
                log_warning("Audit-Grade Score", f"⚠️  Score {score}% < 70% (not audit-grade yet)")
        else:
            log_test("Get Evidence Score", False, f"Status {response.status_code}")
    except Exception as e:
        log_test("Get Evidence Score", False, str(e))
    
    # Recalculate evidence score
    print("\n4.2 Testing evidence score recalculation...")
    try:
        response = requests.post(
            f"{BASE_URL}/cases/{test_case_id}/evidence/recalc",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=10
        )
        if response.status_code == 200:
            evidence_data = response.json()
            score = evidence_data.get("score", 0)
            log_test("Recalculate Evidence Score", True, f"Recalculated: {score}%")
        else:
            log_test("Recalculate Evidence Score", False, f"Status {response.status_code}")
    except Exception as e:
        log_test("Recalculate Evidence Score", False, str(e))

# ============================================================================
# 5. RESPONSIBILITY ATTRIBUTION (Solution: Clear Attribution)
# Requirement: AI analyzes timeline/docs to assign primary responsible party
# ============================================================================
print("\n" + "=" * 70)
print("5. RESPONSIBILITY ATTRIBUTION (Clear Attribution)")
print("=" * 70)

if not test_case_id:
    log_warning("Responsibility Tests", "Skipping - no test case ID")
else:
    # Analyze responsibility
    print("\n5.1 Testing responsibility analysis...")
    try:
        start_time = time.time()
        response = requests.post(
            f"{BASE_URL}/cases/{test_case_id}/responsibility/analyze",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=30  # AI analysis may take longer
        )
        elapsed = time.time() - start_time
        
        if response.status_code == 200:
            resp_data = response.json()
            primary_party = resp_data.get("primary_party", "Unknown")
            confidence = resp_data.get("confidence", "Low")
            reasoning = resp_data.get("reasoning", "")
            
            log_test("Analyze Responsibility", True, f"Completed in {elapsed:.2f}s")
            log_test("Primary Party Assigned", primary_party != "Unknown", f"Party: {primary_party}")
            log_test("Confidence Level", confidence in ["High", "Medium", "Low"], f"Confidence: {confidence}")
            log_test("Reasoning Provided", len(reasoning) > 0, f"Reasoning: {reasoning[:50]}...")
        else:
            log_test("Analyze Responsibility", False, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        log_test("Analyze Responsibility", False, str(e))
    
    # Get responsibility
    print("\n5.2 Testing responsibility retrieval...")
    try:
        response = requests.get(
            f"{BASE_URL}/cases/{test_case_id}/responsibility",
            headers={"Authorization": f"Bearer {auth_token}"},
            timeout=10
        )
        if response.status_code == 200:
            resp_data = response.json()
            log_test("Get Responsibility", True, f"Party: {resp_data.get('primary_party', 'N/A')}")
        else:
            log_test("Get Responsibility", False, f"Status {response.status_code}")
    except Exception as e:
        log_test("Get Responsibility", False, str(e))

# ============================================================================
# 6. DISPUTE PACKET GENERATION (Solution: Stop the Meter)
# Requirement: One-click export, includes audio/transcript/timeline/docs
# ============================================================================
print("\n" + "=" * 70)
print("6. DISPUTE PACKET GENERATION (Stop the Meter)")
print("=" * 70)

if not test_case_id:
    log_warning("Dispute Packet Tests", "Skipping - no test case ID")
else:
    # First create a dispute packet
    print("\n6.1 Testing dispute packet creation...")
    test_packet_id = None
    try:
        response = requests.post(
            f"{BASE_URL}/v0/movements/{test_case_id}/dispute-packets",
            headers={"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"},
            json={
                "invoice_id": "INV-TEST-001",
                "template_type": "jnpt_demurrage",
                "narrative": "Test dispute packet for alignment testing"
            },
            timeout=10
        )
        if response.status_code in [200, 201]:
            packet_data = response.json()
            test_packet_id = packet_data.get("_id")
            log_test("Create Dispute Packet", True, f"Created packet: {test_packet_id}")
        else:
            log_test("Create Dispute Packet", False, f"Status {response.status_code}: {response.text}")
    except Exception as e:
        log_test("Create Dispute Packet", False, str(e))
    
    # Then export it
    if test_packet_id:
        print("\n6.2 Testing dispute packet export...")
        try:
            start_time = time.time()
            response = requests.post(
                f"{BASE_URL}/v0/dispute-packets/{test_packet_id}/export",
                headers={"Authorization": f"Bearer {auth_token}"},
                timeout=60  # Export may take time
            )
            elapsed = time.time() - start_time
            
            if response.status_code == 200:
                # Check if it's a file download
                content_type = response.headers.get("Content-Type", "")
                if "zip" in content_type or "application/octet-stream" in content_type:
                    file_size = len(response.content)
                    log_test("Export Dispute Packet", True, f"Exported in {elapsed:.2f}s ({file_size} bytes)")
                else:
                    log_test("Export Dispute Packet", True, f"Exported in {elapsed:.2f}s")
            else:
                log_test("Export Dispute Packet", False, f"Status {response.status_code}: {response.text}")
        except Exception as e:
            log_test("Export Dispute Packet", False, str(e))
    else:
        log_warning("Export Dispute Packet", "Skipping - no packet ID")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"✅ Passed: {len(results['passed'])}")
print(f"❌ Failed: {len(results['failed'])}")
print(f"⚠️  Warnings: {len(results['warnings'])}")
print()

if results['failed']:
    print("FAILED TESTS:")
    for test in results['failed']:
        print(f"  ❌ {test}")
    print()

if results['warnings']:
    print("WARNINGS:")
    for warning in results['warnings']:
        print(f"  ⚠️  {warning}")
    print()

# Overall result
if len(results['failed']) == 0:
    print("✅ ALL TESTS PASSED!")
    sys.exit(0)
else:
    print(f"❌ {len(results['failed'])} TEST(S) FAILED")
    sys.exit(1)

