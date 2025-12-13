#!/usr/bin/env python3
"""
Create realistic demo data for Ward v0
Run this before tomorrow's demo
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8001/api"

def create_demo_users():
    """Create 3 demo users: driver, manager, warehouse"""
    users = [
        {"email": "driver@logistics.com", "password": "demo123", "role": "Driver"},
        {"email": "manager@logistics.com", "password": "demo123", "role": "Manager"},
        {"email": "warehouse@logistics.com", "password": "demo123", "role": "Warehouse Manager"}
    ]
    
    tokens = {}
    
    for user in users:
        print(f"\n📝 Creating user: {user['email']}")
        try:
            response = requests.post(f"{BASE_URL}/auth/register", json={
                "email": user["email"],
                "password": user["password"]
            })
            if response.status_code == 200:
                tokens[user['role']] = response.json()["access_token"]
                print(f"   ✓ {user['role']} created: {user['email']}")
            else:
                # User might exist, try login
                response = requests.post(f"{BASE_URL}/auth/login", json={
                    "email": user["email"],
                    "password": user["password"]
                })
                tokens[user['role']] = response.json()["access_token"]
                print(f"   ✓ {user['role']} logged in: {user['email']}")
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
    
    return tokens

def create_realistic_disruption_1(token):
    """Fresh disruption - Container stuck at JNPT (REPORTED)"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🚢 Creating Disruption 1: Container stuck at JNPT")
    
    # Create case
    response = requests.post(f"{BASE_URL}/cases", headers=headers, json={
        "description": "Container CMAU9876543 stuck at JNPT Mumbai - customs hold reported by CHA. Invoice-BL description mismatch suspected. Shipment contains electronic goods valued at ₹45 lakhs.",
        "disruption_details": {
            "disruption_type": "customs_hold",
            "scope": "container",
            "identifier": "CMAU9876543 at JNPT Gate 7",
            "time_discovered_ist": datetime.now().strftime("%d/%m/%Y %H:%M IST"),
            "source": "Call from CHA (Jagdish Customs Clearing)"
        },
        "shipment_identifiers": {
            "ids": ["SHP-2024-MUM-1234"],
            "routes": ["Shanghai-JNPT-Mumbai"],
            "carriers": ["Maersk Line"]
        }
    })
    
    if response.status_code == 200:
        case = response.json()
        case_id = case["_id"]
        print(f"   ✓ Case created: {case_id}")
        
        # Add initial timeline events
        events = [
            {
                "content": "Driver Ramesh called: Container reached JNPT at 08:30, but customs hold notice received at gate. Waiting for clearance.",
                "source_type": "voice",
                "reliability": "high"
            },
            {
                "content": "CHA Jagdish confirmed: Assessment pending with Customs Officer Sharma. Issue is invoice description doesn't match Bill of Lading. Says 'Electronics' but BL says 'Computer Parts'.",
                "source_type": "text",
                "reliability": "high"
            },
            {
                "content": "Customer (Raj Electronics) notified of delay. Requested urgent resolution as goods needed for upcoming festival sale.",
                "source_type": "text",
                "reliability": "medium"
            }
        ]
        
        for event in events:
            requests.post(f"{BASE_URL}/cases/{case_id}/timeline", headers=headers, json=event)
        
        print(f"   ✓ Added {len(events)} timeline events")
        print(f"   📊 Status: REPORTED")
        print(f"   📍 Location: JNPT Mumbai")
        print(f"   👤 Owner: Unassigned (perfect for demo)")
        
        return case_id
    else:
        print(f"   ✗ Failed to create case: {response.text}")
        return None

def create_realistic_disruption_2(token):
    """In-progress disruption - Truck breakdown (CLARIFIED with RCA)"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🚛 Creating Disruption 2: Truck breakdown on NH-8")
    
    # Create case
    response = requests.post(f"{BASE_URL}/cases", headers=headers, json={
        "description": "Truck GJ-06-AB-1234 broke down on NH-8 near Vapi toll plaza. Engine overheating. Carrying 3 containers from Mundra to Mumbai. Estimated 4-hour delay if backup truck arranged immediately.",
        "disruption_details": {
            "disruption_type": "truck_breakdown",
            "scope": "truck",
            "identifier": "GJ-06-AB-1234 at NH-8 KM 245",
            "time_discovered_ist": (datetime.now() - timedelta(hours=2)).strftime("%d/%m/%Y %H:%M IST"),
            "source": "Driver WhatsApp message with photo"
        },
        "shipment_identifiers": {
            "ids": ["SHP-2024-MUN-567", "SHP-2024-MUN-568", "SHP-2024-MUN-569"],
            "routes": ["Mundra-Mumbai"],
            "carriers": ["Safexpress"]
        }
    })
    
    if response.status_code == 200:
        case = response.json()
        case_id = case["_id"]
        print(f"   ✓ Case created: {case_id}")
        
        # Assign owner
        requests.post(f"{BASE_URL}/cases/{case_id}/assign-owner", headers=headers, json={
            "owner_email": "manager@logistics.com"
        })
        
        # Transition to CLARIFIED
        requests.post(f"{BASE_URL}/cases/{case_id}/transition", headers=headers, json={
            "next_state": "CLARIFIED",
            "reason": "Spoke with driver and mechanic. Engine coolant leak. Repair will take 6 hours. Backup truck is faster option."
        })
        
        # Add timeline events
        events = [
            {
                "content": "Driver Suresh reported via WhatsApp: Engine temperature gauge showing red, pulled over safely. Sent photo of smoke from engine.",
                "source_type": "voice",
                "reliability": "high"
            },
            {
                "content": "Local mechanic inspected: Coolant leak from radiator. Needs replacement part. Estimated repair time: 5-6 hours.",
                "source_type": "text",
                "reliability": "medium"
            },
            {
                "content": "Checked nearest depot: Vapi depot has backup truck available. Can reach location in 45 minutes.",
                "source_type": "text",
                "reliability": "high"
            },
            {
                "content": "Decision: Arrange backup truck from Vapi depot. Transfer containers. Send broken truck to depot for repair. ETA to Mumbai: +4 hours from original plan.",
                "source_type": "text",
                "reliability": "high"
            }
        ]
        
        for event in events:
            requests.post(f"{BASE_URL}/cases/{case_id}/timeline", headers=headers, json=event)
        
        print(f"   ✓ Added {len(events)} timeline events")
        print(f"   📊 Status: CLARIFIED")
        print(f"   📍 Location: NH-8 near Vapi")
        print(f"   👤 Owner: manager@logistics.com")
        print(f"   🔍 RCA ready to perform")
        
        return case_id
    else:
        print(f"   ✗ Failed to create case: {response.text}")
        return None

def create_realistic_disruption_3(token):
    """Resolved disruption - Customs hold cleared (RESOLVED)"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n✅ Creating Disruption 3: Customs hold resolved")
    
    # Create case
    response = requests.post(f"{BASE_URL}/cases", headers=headers, json={
        "description": "Container TEMU1234567 held at Mundra Port - Assessment complete but duty payment pending. Total duty: ₹2.3 lakhs. Customer approved payment. Cleared within 4 hours.",
        "disruption_details": {
            "disruption_type": "customs_hold",
            "scope": "container",
            "identifier": "TEMU1234567 at Mundra Port",
            "time_discovered_ist": (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y %H:%M IST"),
            "source": "CHA email with ICEGATE screenshot"
        },
        "shipment_identifiers": {
            "ids": ["SHP-2024-MUN-890"],
            "routes": ["Dubai-Mundra-Ahmedabad"],
            "carriers": ["MSC"]
        }
    })
    
    if response.status_code == 200:
        case = response.json()
        case_id = case["_id"]
        print(f"   ✓ Case created: {case_id}")
        
        # Assign owner
        requests.post(f"{BASE_URL}/cases/{case_id}/assign-owner", headers=headers, json={
            "owner_email": "manager@logistics.com"
        })
        
        # Progress through all states
        states = [
            ("CLARIFIED", "CHA confirmed duty amount. Waiting for customer payment approval."),
            ("DECISION_REQUIRED", "Customer needs to approve ₹2.3L duty payment."),
            ("DECIDED", "Customer approved payment. CHA will process payment at customs."),
            ("IN_PROGRESS", "CHA paid duty. Waiting for Out of Charge certificate."),
            ("RESOLVED", "Out of Charge received. Container released at 16:45 IST. Total resolution time: 4 hours.")
        ]
        
        for state, reason in states:
            requests.post(f"{BASE_URL}/cases/{case_id}/transition", headers=headers, json={
                "next_state": state,
                "reason": reason
            })
        
        # Add timeline events
        events = [
            {
                "content": "CHA sent ICEGATE screenshot: Assessment completed. Duty payable: ₹2,30,450. Payment deadline: 24 hours.",
                "source_type": "text",
                "reliability": "high"
            },
            {
                "content": "Called customer (Mehta Traders): Explained duty amount and urgency. Customer approved payment immediately.",
                "source_type": "voice",
                "reliability": "high"
            },
            {
                "content": "CHA processed payment at customs online portal. Payment receipt #: ICEGATE/2024/12345.",
                "source_type": "text",
                "reliability": "high"
            },
            {
                "content": "Out of Charge (OOC) certificate received from customs. Container ready for delivery.",
                "source_type": "system",
                "reliability": "high"
            },
            {
                "content": "Driver assigned: Amit (GJ-12-CD-5678). ETA to customer warehouse: Tomorrow 10:00 AM.",
                "source_type": "text",
                "reliability": "high"
            }
        ]
        
        for event in events:
            requests.post(f"{BASE_URL}/cases/{case_id}/timeline", headers=headers, json=event)
        
        print(f"   ✓ Added {len(events)} timeline events")
        print(f"   📊 Status: RESOLVED ✅")
        print(f"   📍 Location: Mundra Port")
        print(f"   👤 Owner: manager@logistics.com")
        print(f"   ⏱️  Resolution time: 4 hours (vs usual 24h)")
        print(f"   💰 Cost impact: Prevented ₹50K demurrage")
        
        return case_id
    else:
        print(f"   ✗ Failed to create case: {response.text}")
        return None

def main():
    print("=" * 80)
    print("WARD v0 - DEMO DATA SETUP")
    print("=" * 80)
    
    # Create users
    tokens = create_demo_users()
    
    if not tokens.get("Manager"):
        print("\n❌ Failed to create users. Exiting.")
        return
    
    manager_token = tokens["Manager"]
    
    # Create disruptions
    case1 = create_realistic_disruption_1(manager_token)
    case2 = create_realistic_disruption_2(manager_token)
    case3 = create_realistic_disruption_3(manager_token)
    
    print("\n" + "=" * 80)
    print("✅ DEMO DATA SETUP COMPLETE")
    print("=" * 80)
    
    print("\n📋 DEMO USERS:")
    print("   • driver@logistics.com / demo123")
    print("   • manager@logistics.com / demo123")
    print("   • warehouse@logistics.com / demo123")
    
    print("\n📊 DEMO DISRUPTIONS CREATED:")
    print(f"   1. Fresh Report (REPORTED): {case1 or 'Failed'}")
    print("      → Container at JNPT, customs hold, unassigned")
    print("      → Perfect for showing ownership assignment + voice demo")
    
    print(f"\n   2. In Progress (CLARIFIED): {case2 or 'Failed'}")
    print("      → Truck breakdown on NH-8, clear situation")
    print("      → Perfect for showing RCA + decision making")
    
    print(f"\n   3. Resolved (RESOLVED): {case3 or 'Failed'}")
    print("      → Customs cleared at Mundra, full lifecycle")
    print("      → Perfect for showing complete audit trail + outcome")
    
    print("\n🎬 READY FOR DEMO!")
    print("   Open: https://logistics-ward.preview.emergentagent.com")
    print("   Login: manager@logistics.com / demo123")
    print("   See: /app/DEMO_SCRIPT.md for full script")
    
    print("\n💡 PRO TIPS:")
    print("   • Open 3 browser tabs: Dashboard, Voice Case, Case Detail")
    print("   • Have phone ready for voice demo (or explain it)")
    print("   • Emphasize: Multilingual voice, RCA, 4h vs 24h resolution")
    print("   • Close with: '30-day pilot, 5 managers, 20 drivers, free'")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
