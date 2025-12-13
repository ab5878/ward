"""
Comprehensive Backend API Testing for Ward v0
Tests all endpoints including authentication, case management, AI generation, approvals, and audit trails
"""

import requests
import sys
import time
from datetime import datetime
import json

class WardBackendTester:
    def __init__(self, base_url="https://disruption-hub.preview.emergentagent.com"):
        self.base_url = base_url
        self.token = None
        self.test_email = f"test_operator_{int(time.time())}@example.com"
        self.test_password = "TestPass123!"
        self.case_id = None
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        self.failed_tests = []

    def log(self, message, status="INFO"):
        symbols = {"PASS": "✅", "FAIL": "❌", "INFO": "🔍", "WARN": "⚠️"}
        print(f"{symbols.get(status, '•')} {message}")

    def run_test(self, name, method, endpoint, expected_status, data=None, headers=None):
        """Run a single API test"""
        url = f"{self.base_url}/api/{endpoint}"
        test_headers = {'Content-Type': 'application/json'}
        
        if self.token:
            test_headers['Authorization'] = f'Bearer {self.token}'
        
        if headers:
            test_headers.update(headers)

        self.tests_run += 1
        self.log(f"Testing {name}...", "INFO")
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=test_headers, timeout=30)
            elif method == 'POST':
                response = requests.post(url, json=data, headers=test_headers, timeout=30)
            elif method == 'PATCH':
                response = requests.patch(url, json=data, headers=test_headers, timeout=30)

            success = response.status_code == expected_status
            
            if success:
                self.tests_passed += 1
                self.log(f"PASSED - {name} (Status: {response.status_code})", "PASS")
                try:
                    return True, response.json()
                except:
                    return True, {}
            else:
                self.tests_failed += 1
                error_detail = ""
                try:
                    error_detail = response.json().get('detail', '')
                except:
                    error_detail = response.text[:100]
                
                self.log(f"FAILED - {name} (Expected {expected_status}, got {response.status_code})", "FAIL")
                self.log(f"  Error: {error_detail}", "FAIL")
                self.failed_tests.append({
                    "test": name,
                    "expected": expected_status,
                    "actual": response.status_code,
                    "error": error_detail
                })
                return False, {}

        except requests.exceptions.Timeout:
            self.tests_failed += 1
            self.log(f"FAILED - {name} (Timeout after 30s)", "FAIL")
            self.failed_tests.append({
                "test": name,
                "expected": expected_status,
                "actual": "TIMEOUT",
                "error": "Request timed out"
            })
            return False, {}
        except Exception as e:
            self.tests_failed += 1
            self.log(f"FAILED - {name} (Error: {str(e)})", "FAIL")
            self.failed_tests.append({
                "test": name,
                "expected": expected_status,
                "actual": "EXCEPTION",
                "error": str(e)
            })
            return False, {}

    def test_health(self):
        """Test health endpoint"""
        self.log("\n=== Testing Health Check ===", "INFO")
        success, response = self.run_test(
            "Health Check",
            "GET",
            "health",
            200
        )
        return success

    def test_register(self):
        """Test user registration"""
        self.log("\n=== Testing Authentication ===", "INFO")
        success, response = self.run_test(
            "User Registration",
            "POST",
            "auth/register",
            200,
            data={"email": self.test_email, "password": self.test_password}
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            self.log(f"  Token obtained: {self.token[:20]}...", "INFO")
            return True
        return False

    def test_login(self):
        """Test user login"""
        success, response = self.run_test(
            "User Login",
            "POST",
            "auth/login",
            200,
            data={"email": self.test_email, "password": self.test_password}
        )
        
        if success and 'access_token' in response:
            self.token = response['access_token']
            return True
        return False

    def test_get_me(self):
        """Test get current user"""
        success, response = self.run_test(
            "Get Current User",
            "GET",
            "auth/me",
            200
        )
        
        if success:
            self.log(f"  User email: {response.get('email')}", "INFO")
        return success

    def test_create_case(self):
        """Test case creation WITH MANDATORY disruption details"""
        self.log("\n=== Testing Case Management ===", "INFO")
        success, response = self.run_test(
            "Create Disruption Case (India Context)",
            "POST",
            "cases",
            200,
            data={
                "description": "Container CMAU1234567 held at JNPT customs for document verification. Discovered via call from CHA at 14:30 IST. Original documents submitted but customs officer requesting additional import license copy. Shipment contains electronics for urgent customer order. CHA says resolution can take 2-4 days normally.",
                "disruption_details": {
                    "disruption_type": "customs_hold",
                    "scope": "single container",
                    "identifier": "CMAU1234567",
                    "time_discovered_ist": "13/12/2024 14:30 IST",
                    "source": "Call from CHA (Jagdish Customs)"
                },
                "shipment_identifiers": {
                    "ids": ["SH-IND-2024-789"],
                    "routes": ["JNPT Port → Mumbai → Pune"],
                    "carriers": ["Maersk Line", "VRL Logistics"]
                }
            }
        )
        
        if success and '_id' in response:
            self.case_id = response['_id']
            self.log(f"  Case ID: {self.case_id}", "INFO")
            return True
        return False

    def test_list_cases(self):
        """Test listing cases"""
        success, response = self.run_test(
            "List Cases",
            "GET",
            "cases",
            200
        )
        
        if success:
            self.log(f"  Found {len(response)} case(s)", "INFO")
        return success

    def test_get_case(self):
        """Test getting case details"""
        if not self.case_id:
            self.log("Skipping Get Case - no case_id available", "WARN")
            return False
        
        success, response = self.run_test(
            "Get Case Details",
            "GET",
            f"cases/{self.case_id}",
            200
        )
        
        if success:
            self.log(f"  Case status: {response.get('case', {}).get('status')}", "INFO")
        return success

    def test_generate_ai_draft(self):
        """Test AI draft generation"""
        if not self.case_id:
            self.log("Skipping AI Draft - no case_id available", "WARN")
            return False
        
        self.log("\n=== Testing AI Decision Generation ===", "INFO")
        self.log("  This may take 10-15 seconds...", "INFO")
        
        success, response = self.run_test(
            "Generate AI Decision Structure",
            "POST",
            f"cases/{self.case_id}/ai_draft",
            200
        )
        
        if success:
            # Validate 6-step structure
            required_sections = [
                'decision_framing',
                'known_inputs',
                'declared_assumptions',
                'alternatives',
                'recommendation'
            ]
            
            missing_sections = [s for s in required_sections if s not in response]
            if missing_sections:
                self.log(f"  Missing sections: {missing_sections}", "WARN")
            else:
                self.log("  All 6 sections generated successfully", "PASS")
            
            # Check alternatives count (should be 2-3)
            alternatives = response.get('alternatives', [])
            self.log(f"  Alternatives count: {len(alternatives)}", "INFO")
            if len(alternatives) > 3:
                self.log(f"  WARNING: More than 3 alternatives ({len(alternatives)})", "WARN")
            
            # Check for evidence labeling
            facts = response.get('known_inputs', {}).get('facts', [])
            if facts:
                first_fact = facts[0]
                required_labels = ['source', 'freshness', 'reliability']
                has_labels = all(label in first_fact for label in required_labels)
                if has_labels:
                    self.log("  Evidence labeling present", "PASS")
                else:
                    self.log("  Evidence labeling incomplete", "WARN")
            
            # Check worst-case display
            if alternatives:
                has_worst_case = all('worst_case' in alt for alt in alternatives)
                if has_worst_case:
                    self.log("  Worst-case scenarios present for all alternatives", "PASS")
                else:
                    self.log("  Some alternatives missing worst-case", "WARN")
        
        return success

    def test_approve_sections(self):
        """Test section approval workflow"""
        if not self.case_id:
            self.log("Skipping Section Approval - no case_id available", "WARN")
            return False
        
        self.log("\n=== Testing Section Approval Workflow ===", "INFO")
        
        sections = [
            'decision_framing',
            'known_inputs',
            'declared_assumptions',
            'alternatives',
            'recommendation'
        ]
        
        all_success = True
        for section in sections:
            success, response = self.run_test(
                f"Approve Section: {section}",
                "POST",
                f"cases/{self.case_id}/sections/{section}/approve",
                200
            )
            if not success:
                all_success = False
        
        return all_success

    def test_finalize_decision_recommended(self):
        """Test finalizing with recommended choice"""
        if not self.case_id:
            self.log("Skipping Finalize Decision - no case_id available", "WARN")
            return False
        
        self.log("\n=== Testing Decision Finalization ===", "INFO")
        
        # First, get the draft to find recommended choice
        success, case_data = self.run_test(
            "Get Case for Finalization",
            "GET",
            f"cases/{self.case_id}",
            200
        )
        
        if not success:
            return False
        
        draft = case_data.get('draft', {})
        recommended = draft.get('recommendation', {}).get('choice', '')
        
        if not recommended:
            self.log("  No recommendation found in draft", "WARN")
            # Use first alternative as fallback
            alternatives = draft.get('alternatives', [])
            if alternatives:
                recommended = alternatives[0].get('name', '')
        
        if not recommended:
            self.log("  Cannot finalize - no alternatives available", "FAIL")
            return False
        
        self.log(f"  Finalizing with recommended choice: {recommended}", "INFO")
        
        success, response = self.run_test(
            "Finalize Decision (Recommended)",
            "POST",
            f"cases/{self.case_id}/finalize",
            200,
            data={
                "selected_alternative": recommended,
                "override_rationale": None
            }
        )
        
        if success:
            is_override = response.get('is_override', False)
            self.log(f"  Override: {is_override}", "INFO")
            if not is_override:
                self.log("  Decision finalized with recommended choice", "PASS")
            else:
                self.log("  WARNING: Expected non-override but got override", "WARN")
        
        return success

    def test_audit_trail(self):
        """Test audit trail endpoints"""
        self.log("\n=== Testing Audit Trail ===", "INFO")
        
        # Test global audit trail
        success1, response1 = self.run_test(
            "Get Global Audit Trail",
            "GET",
            "audit",
            200
        )
        
        if success1:
            self.log(f"  Found {len(response1)} audit entries", "INFO")
        
        # Test case-specific audit trail
        if self.case_id:
            success2, response2 = self.run_test(
                "Get Case Audit Trail",
                "GET",
                f"cases/{self.case_id}/audit",
                200
            )
            
            if success2:
                self.log(f"  Found {len(response2)} case-specific audit entries", "INFO")
                
                # Verify audit entries have required fields
                if response2:
                    first_entry = response2[0]
                    required_fields = ['case_id', 'actor', 'action', 'timestamp']
                    has_fields = all(field in first_entry for field in required_fields)
                    if has_fields:
                        self.log("  Audit entries have all required fields", "PASS")
                    else:
                        self.log("  Audit entries missing some fields", "WARN")
            
            return success1 and success2
        
        return success1

    def test_historical_disruptions(self):
        """Test historical disruptions (read-only)"""
        self.log("\n=== Testing Historical Disruptions ===", "INFO")
        
        success, response = self.run_test(
            "List Historical Disruptions",
            "GET",
            "historical",
            200
        )
        
        if success:
            self.log(f"  Found {len(response)} historical entries", "INFO")
        
        return success

    def test_disruption_validation(self):
        """Test that cases WITHOUT disruption details are rejected (DISRUPTION FIRST hard gate)"""
        self.log("\n=== Testing DISRUPTION FIRST Hard Gate ===", "INFO")
        
        # Try to create case WITHOUT disruption details - should fail with 422
        success, response = self.run_test(
            "Create Case WITHOUT Disruption Details (Should Fail)",
            "POST",
            "cases",
            422,  # Expecting validation error
            data={
                "description": "Some generic logistics issue without proper disruption context.",
                "shipment_identifiers": {
                    "ids": ["SH-2024-999"],
                    "routes": ["Mumbai → Delhi"],
                    "carriers": ["Generic Carrier"]
                }
            }
        )
        
        if success:
            self.log("  DISRUPTION FIRST gate working correctly - rejected case without disruption details", "PASS")
        else:
            self.log("  WARNING: Case without disruption details was not properly rejected", "FAIL")
        
        return success

    def test_override_scenario(self):
        """Test override handling with non-recommended choice"""
        self.log("\n=== Testing Override Scenario ===", "INFO")
        
        # Create a new case for override testing WITH disruption details
        success, response = self.run_test(
            "Create Case for Override Test",
            "POST",
            "cases",
            200,
            data={
                "description": "Truck MH-02-AB-5678 breakdown near Nashik. Shipment contains perishable goods. Driver called at 10:00 IST. Need immediate decision on alternative transport.",
                "disruption_details": {
                    "disruption_type": "truck_breakdown",
                    "scope": "single shipment",
                    "identifier": "MH-02-AB-5678",
                    "time_discovered_ist": "13/12/2024 10:00 IST",
                    "source": "Phone call from driver"
                },
                "shipment_identifiers": {
                    "ids": ["SH-IND-2024-100"],
                    "routes": ["Mumbai → Pune"],
                    "carriers": ["VRL Logistics"]
                }
            }
        )
        
        if not success or '_id' not in response:
            return False
        
        override_case_id = response['_id']
        self.log(f"  Override test case ID: {override_case_id}", "INFO")
        
        # Generate AI draft
        self.log("  Generating AI draft for override test...", "INFO")
        success, draft_response = self.run_test(
            "Generate AI Draft for Override",
            "POST",
            f"cases/{override_case_id}/ai_draft",
            200
        )
        
        if not success:
            return False
        
        # Get alternatives
        alternatives = draft_response.get('alternatives', [])
        recommended = draft_response.get('recommendation', {}).get('choice', '')
        
        if len(alternatives) < 2:
            self.log("  Not enough alternatives for override test", "WARN")
            return False
        
        # Select a non-recommended alternative
        non_recommended = None
        for alt in alternatives:
            if alt.get('name', '').lower() != recommended.lower():
                non_recommended = alt.get('name')
                break
        
        if not non_recommended:
            self.log("  Could not find non-recommended alternative", "WARN")
            return False
        
        self.log(f"  Recommended: {recommended}", "INFO")
        self.log(f"  Selecting: {non_recommended} (override)", "INFO")
        
        # Approve all sections first
        sections = ['decision_framing', 'known_inputs', 'declared_assumptions', 'alternatives', 'recommendation']
        for section in sections:
            self.run_test(
                f"Approve {section} for override test",
                "POST",
                f"cases/{override_case_id}/sections/{section}/approve",
                200
            )
        
        # Finalize with override
        success, finalize_response = self.run_test(
            "Finalize with Override",
            "POST",
            f"cases/{override_case_id}/finalize",
            200,
            data={
                "selected_alternative": non_recommended,
                "override_rationale": "Based on real-time traffic updates and customer priority, choosing alternative approach despite AI recommendation."
            }
        )
        
        if success:
            is_override = finalize_response.get('is_override', False)
            has_rationale = finalize_response.get('override_rationale') is not None
            
            if is_override and has_rationale:
                self.log("  Override correctly recorded with rationale", "PASS")
            else:
                self.log(f"  Override flag: {is_override}, Has rationale: {has_rationale}", "WARN")
        
        return success

    def run_all_tests(self):
        """Run all tests in sequence"""
        self.log("\n" + "="*60, "INFO")
        self.log("WARD V0 BACKEND API COMPREHENSIVE TEST SUITE", "INFO")
        self.log("="*60 + "\n", "INFO")
        
        start_time = time.time()
        
        # Test sequence
        tests = [
            ("Health Check", self.test_health),
            ("User Registration", self.test_register),
            ("User Login", self.test_login),
            ("Get Current User", self.test_get_me),
            ("DISRUPTION FIRST Validation", self.test_disruption_validation),
            ("Create Case", self.test_create_case),
            ("List Cases", self.test_list_cases),
            ("Get Case Details", self.test_get_case),
            ("Generate AI Draft", self.test_generate_ai_draft),
            ("Section Approval Workflow", self.test_approve_sections),
            ("Finalize Decision", self.test_finalize_decision_recommended),
            ("Audit Trail", self.test_audit_trail),
            ("Historical Disruptions", self.test_historical_disruptions),
            ("Override Scenario", self.test_override_scenario),
        ]
        
        for test_name, test_func in tests:
            try:
                test_func()
            except Exception as e:
                self.log(f"Exception in {test_name}: {str(e)}", "FAIL")
                self.tests_failed += 1
        
        # Print summary
        elapsed_time = time.time() - start_time
        self.log("\n" + "="*60, "INFO")
        self.log("TEST SUMMARY", "INFO")
        self.log("="*60, "INFO")
        self.log(f"Total Tests: {self.tests_run}", "INFO")
        self.log(f"Passed: {self.tests_passed}", "PASS")
        self.log(f"Failed: {self.tests_failed}", "FAIL")
        self.log(f"Success Rate: {(self.tests_passed/self.tests_run*100):.1f}%", "INFO")
        self.log(f"Time Elapsed: {elapsed_time:.2f}s", "INFO")
        
        if self.failed_tests:
            self.log("\n" + "="*60, "INFO")
            self.log("FAILED TESTS DETAILS", "FAIL")
            self.log("="*60, "INFO")
            for failed in self.failed_tests:
                self.log(f"\nTest: {failed['test']}", "FAIL")
                self.log(f"  Expected: {failed['expected']}", "INFO")
                self.log(f"  Actual: {failed['actual']}", "INFO")
                self.log(f"  Error: {failed['error']}", "INFO")
        
        return 0 if self.tests_failed == 0 else 1

def main():
    tester = WardBackendTester()
    return tester.run_all_tests()

if __name__ == "__main__":
    sys.exit(main())
