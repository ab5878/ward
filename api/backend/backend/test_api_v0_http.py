"""
HTTP test script for API v0 endpoints
Tests endpoints against deployed API (requires authentication)
Usage: python3 test_api_v0_http.py [base_url]
"""

import requests
import sys
import json
from typing import Optional

class APIV0Tester:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.token: Optional[str] = None
        self.test_email = f"test_api_v0_{int(__import__('time').time())}@example.com"
        self.test_password = "TestPass123!"
        self.movement_id: Optional[str] = None
        self.facility_id: Optional[str] = None
        self.party_id: Optional[str] = None
        self.packet_id: Optional[str] = None
    
    def log(self, message: str, status: str = "INFO"):
        symbols = {
            "INFO": "🔍",
            "PASS": "✅",
            "FAIL": "❌",
            "WARN": "⚠️"
        }
        print(f"{symbols.get(status, '•')} {message}")
    
    def register_and_login(self) -> bool:
        """Register a test user and login"""
        try:
            # Register
            self.log("Registering test user...", "INFO")
            register_response = requests.post(
                f"{self.base_url}/api/auth/register",
                json={
                    "email": self.test_email,
                    "password": self.test_password
                },
                timeout=10
            )
            
            if register_response.status_code not in [200, 201]:
                # Try login in case user already exists
                self.log("Registration failed, trying login...", "WARN")
            else:
                self.log("User registered", "PASS")
            
            # Login
            self.log("Logging in...", "INFO")
            login_response = requests.post(
                f"{self.base_url}/api/auth/login",
                json={
                    "email": self.test_email,
                    "password": self.test_password
                },
                timeout=10
            )
            
            if login_response.status_code == 200:
                data = login_response.json()
                self.token = data.get("access_token")
                if self.token:
                    self.log("Login successful", "PASS")
                    return True
                else:
                    self.log("No token in response", "FAIL")
                    return False
            else:
                self.log(f"Login failed: {login_response.status_code}", "FAIL")
                return False
                
        except Exception as e:
            self.log(f"Auth failed: {e}", "FAIL")
            return False
    
    def get_headers(self) -> dict:
        """Get request headers with auth token"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def create_test_case(self) -> bool:
        """Create a test case/movement for testing dispute packets"""
        try:
            self.log("Creating test case...", "INFO")
            response = requests.post(
                f"{self.base_url}/api/cases",
                json={
                    "description": "Test case for API v0 testing",
                    "disruption_details": {
                        "disruption_type": "delay",
                        "identifier": "TEST-001"
                    },
                    "shipment_identifiers": {}
                },
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.movement_id = data.get("_id") or data.get("id")
                if self.movement_id:
                    self.log(f"Test case created: {self.movement_id}", "PASS")
                    return True
                else:
                    self.log("No case ID in response", "FAIL")
                    return False
            else:
                self.log(f"Failed to create case: {response.status_code}", "FAIL")
                return False
                
        except Exception as e:
            self.log(f"Create case failed: {e}", "FAIL")
            return False
    
    def test_facilities(self) -> bool:
        """Test Facility endpoints"""
        self.log("\n=== Testing Facilities ===", "INFO")
        
        try:
            # Create facility
            self.log("Creating facility...", "INFO")
            response = requests.post(
                f"{self.base_url}/api/v0/facilities",
                json={
                    "name": "Test Port JNPT",
                    "type": "port",
                    "code": "JNPT-TEST",
                    "address": {"city": "Mumbai", "state": "Maharashtra"},
                    "location": {"latitude": 18.9, "longitude": 72.8}
                },
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.facility_id = data.get("_id") or data.get("id")
                self.log(f"Facility created: {self.facility_id}", "PASS")
            else:
                self.log(f"Failed to create facility: {response.status_code} - {response.text[:200]}", "FAIL")
                return False
            
            # List facilities
            self.log("Listing facilities...", "INFO")
            response = requests.get(
                f"{self.base_url}/api/v0/facilities?type=port",
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                facilities = response.json()
                self.log(f"Listed {len(facilities)} facilities", "PASS")
            else:
                self.log(f"Failed to list facilities: {response.status_code}", "FAIL")
                return False
            
            # Get facility
            if self.facility_id:
                self.log("Getting facility...", "INFO")
                response = requests.get(
                    f"{self.base_url}/api/v0/facilities/{self.facility_id}",
                    headers=self.get_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.log("Facility retrieved", "PASS")
                    return True
                else:
                    self.log(f"Failed to get facility: {response.status_code}", "FAIL")
                    return False
            
            return True
            
        except Exception as e:
            self.log(f"Facilities test failed: {e}", "FAIL")
            return False
    
    def test_parties(self) -> bool:
        """Test Party endpoints"""
        self.log("\n=== Testing Parties ===", "INFO")
        
        try:
            # Create party
            self.log("Creating party...", "INFO")
            response = requests.post(
                f"{self.base_url}/api/v0/parties",
                json={
                    "name": "Test Forwarder Inc",
                    "type": "forwarder",
                    "code": "FWD-TEST",
                    "contact_info": {"email": "test@forwarder.com"}
                },
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.party_id = data.get("_id") or data.get("id")
                self.log(f"Party created: {self.party_id}", "PASS")
            else:
                self.log(f"Failed to create party: {response.status_code} - {response.text[:200]}", "FAIL")
                return False
            
            # List parties
            self.log("Listing parties...", "INFO")
            response = requests.get(
                f"{self.base_url}/api/v0/parties?type=forwarder",
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                parties = response.json()
                self.log(f"Listed {len(parties)} parties", "PASS")
            else:
                self.log(f"Failed to list parties: {response.status_code}", "FAIL")
                return False
            
            # Get party
            if self.party_id:
                self.log("Getting party...", "INFO")
                response = requests.get(
                    f"{self.base_url}/api/v0/parties/{self.party_id}",
                    headers=self.get_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.log("Party retrieved", "PASS")
                    return True
                else:
                    self.log(f"Failed to get party: {response.status_code}", "FAIL")
                    return False
            
            return True
            
        except Exception as e:
            self.log(f"Parties test failed: {e}", "FAIL")
            return False
    
    def test_dispute_packets(self) -> bool:
        """Test DisputePacket endpoints"""
        self.log("\n=== Testing DisputePackets ===", "INFO")
        
        if not self.movement_id:
            self.log("No movement ID available, skipping dispute packet tests", "WARN")
            return False
        
        try:
            # Create dispute packet
            self.log("Creating dispute packet...", "INFO")
            response = requests.post(
                f"{self.base_url}/api/v0/movements/{self.movement_id}/dispute-packets",
                json={
                    "invoice_id": "INV-TEST-001",
                    "template_type": "jnpt_demurrage",
                    "narrative": "Test dispute packet"
                },
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.packet_id = data.get("_id") or data.get("id")
                self.log(f"Dispute packet created: {self.packet_id}", "PASS")
            else:
                self.log(f"Failed to create dispute packet: {response.status_code} - {response.text[:200]}", "FAIL")
                return False
            
            # List dispute packets
            self.log("Listing dispute packets...", "INFO")
            response = requests.get(
                f"{self.base_url}/api/v0/movements/{self.movement_id}/dispute-packets",
                headers=self.get_headers(),
                timeout=10
            )
            
            if response.status_code == 200:
                packets = response.json()
                self.log(f"Listed {len(packets)} dispute packets", "PASS")
            else:
                self.log(f"Failed to list dispute packets: {response.status_code}", "FAIL")
                return False
            
            # Get dispute packet
            if self.packet_id:
                self.log("Getting dispute packet...", "INFO")
                response = requests.get(
                    f"{self.base_url}/api/v0/dispute-packets/{self.packet_id}",
                    headers=self.get_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.log("Dispute packet retrieved", "PASS")
                else:
                    self.log(f"Failed to get dispute packet: {response.status_code}", "FAIL")
                    return False
                
                # Update dispute packet
                self.log("Updating dispute packet...", "INFO")
                response = requests.patch(
                    f"{self.base_url}/api/v0/dispute-packets/{self.packet_id}",
                    json={"status": "generated"},
                    headers=self.get_headers(),
                    timeout=10
                )
                
                if response.status_code == 200:
                    self.log("Dispute packet updated", "PASS")
                else:
                    self.log(f"Failed to update dispute packet: {response.status_code}", "FAIL")
                    return False
            
            return True
            
        except Exception as e:
            self.log(f"DisputePackets test failed: {e}", "FAIL")
            return False
    
    def run_all_tests(self) -> bool:
        """Run all tests"""
        print("=" * 60)
        print("Ward API v0 HTTP Test")
        print("=" * 60)
        print(f"Base URL: {self.base_url}\n")
        
        # Auth
        if not self.register_and_login():
            self.log("Authentication failed, cannot continue", "FAIL")
            return False
        
        # Create test case
        if not self.create_test_case():
            self.log("Failed to create test case, some tests will be skipped", "WARN")
        
        # Run tests
        results = {
            "Facilities": self.test_facilities(),
            "Parties": self.test_parties(),
            "DisputePackets": self.test_dispute_packets(),
        }
        
        # Summary
        print("\n" + "=" * 60)
        print("Test Summary")
        print("=" * 60)
        
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{test_name}: {status}")
        
        print()
        print(f"Total: {passed}/{total} test suites passed")
        
        if passed == total:
            print("\n✅ All HTTP tests passed!")
            return True
        else:
            print("\n❌ Some HTTP tests failed.")
            return False

def main():
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    tester = APIV0Tester(base_url)
    success = tester.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())

