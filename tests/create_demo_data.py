#!/usr/bin/env python3
"""
Create realistic demo data for Ward v0 with Deep Indian Context
"""

import requests
import json
from datetime import datetime, timedelta
import random

BASE_URL = "http://localhost:8001/api"

# --- Indian Context Data Pools ---
INDIAN_PORTS = ["JNPT (Nhava Sheva)", "Mundra Port", "Chennai Port", "Visakhapatnam Port", "Kolkata Port"]
ICDS = ["ICD Tughlakabad", "ICD Dadri", "ICD Whitefield", "ICD Sanathnagar"]
WAREHOUSES = ["Bhiwandi Grade A Warehouse", "Sriperumbudur Logistics Park", "Manesar Warehousing Hub", "Nhava Sheva CFS"]
TRANSPORTERS = ["Gati KWE", "VRL Logistics", "SafeExpress", "TCI Freight", "Mahindra Logistics"]
CHAS = ["Jagdish Customs Clearing", "Seahorse Shipping", "Jeena & Company", "Robbins Maritime"]
DRIVERS = ["Ramesh Kumar", "Suresh Yadav", "Muthu Vel", "Gurpreet Singh", "Rajesh Patil"]

def create_demo_users():
    """Create demo users"""
    users = [
        {"email": "driver@logistics.com", "password": "demo123", "role": "Driver"},
        {"email": "manager@logistics.com", "password": "demo123", "role": "Manager"},
        {"email": "warehouse@logistics.com", "password": "demo123", "role": "Warehouse Manager"}
    ]
    tokens = {}
    for user in users:
        try:
            # Try login first
            response = requests.post(f"{BASE_URL}/auth/login", json={
                "email": user["email"], "password": user["password"]
            })
            if response.status_code == 200:
                tokens[user['role']] = response.json()["access_token"]
                continue
                
            # If login fails, register
            response = requests.post(f"{BASE_URL}/auth/register", json={
                "email": user["email"], "password": user["password"]
            })
            if response.status_code == 200:
                tokens[user['role']] = response.json()["access_token"]
        except Exception as e:
            print(f"Error user: {e}")
    return tokens

def create_case(token, data, timeline_events=[]):
    """Helper to create a case and add timeline events"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Create Case
        resp = requests.post(f"{BASE_URL}/cases", headers=headers, json=data)
        if resp.status_code != 200:
            print(f"Failed to create case: {resp.text}")
            return None
        
        case_id = resp.json()["_id"]
        print(f"   ✓ Created: {data['disruption_details']['identifier']}")

        # Add Timeline Events
        for event in timeline_events:
            requests.post(f"{BASE_URL}/cases/{case_id}/timeline", headers=headers, json=event)
            
        return case_id
    except Exception as e:
        print(f"Error creating case: {e}")
        return None

def create_indian_scenarios(token):
    """Generate specific Indian logistics scenarios"""
    print("\n🇮🇳 Generating Indian Logistics Scenarios...")

    # Scenario 1: E-Way Bill Expiry (South India)
    create_case(token, {
        "description": "E-Way Bill expired for Shipment #BLR-889 at Walayar Checkpost (Kerala-TN border). Truck detained by GST squad. Penalty demanded ₹50,000.",
        "disruption_details": {
            "disruption_type": "documentation_issue",
            "scope": "shipment",
            "identifier": "Truck TN-04-AK-9988 at Walayar",
            "time_discovered_ist": (datetime.now() - timedelta(hours=3)).strftime("%d/%m/%Y %H:%M IST"),
            "source": "Driver Call (Muthu Vel)"
        },
        "shipment_identifiers": {
            "ids": ["EWB-123456789012"],
            "routes": ["Bangalore-Kochi"],
            "carriers": ["VRL Logistics"]
        }
    }, timeline_events=[
        {"content": "Driver Muthu called: 'Sir, GST officer stopped vehicle. Says E-Way bill time over by 2 hours due to traffic. Asking for penalty.'", "source_type": "voice", "reliability": "high"},
        {"content": "Verified E-Way Bill portal: Validity expired at 14:00 today. Extension not applied.", "source_type": "system", "reliability": "high"},
        {"content": "Action Required: Pay penalty or file appeal. Goods are urgent (Auto parts for assembly line).", "source_type": "text", "reliability": "medium"}
    ])

    # Scenario 2: Bhiwandi Warehouse Flooding (West India)
    create_case(token, {
        "description": "Heavy monsoon rains caused waterlogging at Bhiwandi Grade A Warehouse approach road. 12 trucks stuck outside. Loading operations suspended for 4 hours.",
        "disruption_details": {
            "disruption_type": "port_congestion", # Using closest type
            "scope": "warehouse",
            "identifier": "Bhiwandi Warehouse Zone 5",
            "time_discovered_ist": (datetime.now() - timedelta(hours=1)).strftime("%d/%m/%Y %H:%M IST"),
            "source": "Warehouse Manager WhatsApp"
        },
        "shipment_identifiers": {
            "ids": ["Multiple Shipments"],
            "routes": ["Mumbai-Pune", "Mumbai-Nashik"],
            "carriers": ["Mahindra Logistics"]
        }
    }, timeline_events=[
        {"content": "Warehouse Manager sent video: Knee-deep water at Gate 1 & 2. Trucks cannot enter safely.", "source_type": "text", "reliability": "high"},
        {"content": "Alert sent to all inbound drivers: 'Divert to waiting area at Mankoli Naka. Do not enter warehouse lane.'", "source_type": "system", "reliability": "high"}
    ])

    # Scenario 3: ICEGATE Downtime (Pan India)
    create_case(token, {
        "description": "ICEGATE Portal is down/slow. Unable to file Bill of Entry for 15 air shipments at Delhi Air Cargo. Demurrage risk if not cleared by midnight.",
        "disruption_details": {
            "disruption_type": "system_outage",
            "scope": "customs",
            "identifier": "ICEGATE Portal",
            "time_discovered_ist": datetime.now().strftime("%d/%m/%Y %H:%M IST"),
            "source": "CHA Alert"
        },
        "shipment_identifiers": {
            "ids": ["BOE-PENDING-001...015"],
            "routes": ["DEL-Import"],
            "carriers": ["Multiple"]
        }
    }, timeline_events=[
        {"content": "CHA Jeena & Co reported: 'ICEGATE server not responding since 10 AM. Cannot upload checklist.'", "source_type": "text", "reliability": "high"},
        {"content": "Twitter Check: Multiple users reporting ICEGATE issues.", "source_type": "system", "reliability": "medium"}
    ])

    # Scenario 4: Rail Rake Delay (North India)
    create_case(token, {
        "description": "Export container rake from ICD Tughlakabad to Mundra delayed by 24 hours due to fog/track maintenance near Kota. Vessel cutoff missed.",
        "disruption_details": {
            "disruption_type": "transit_delay",
            "scope": "rake",
            "identifier": "Rake #CONCOR-776",
            "time_discovered_ist": (datetime.now() - timedelta(hours=5)).strftime("%d/%m/%Y %H:%M IST"),
            "source": "CONCOR Tracker"
        },
        "shipment_identifiers": {
            "ids": ["EXP-DEL-MUN-556"],
            "routes": ["Tughlakabad-Mundra"],
            "carriers": ["CONCOR"]
        }
    }, timeline_events=[
        {"content": "CONCOR Status Update: Train held at Kota Junction. Expected delay 18-24 hours.", "source_type": "system", "reliability": "high"},
        {"content": "Impact: 40 containers will miss vessel 'MSC ALICIA'. Need to roll over to next vessel.", "source_type": "text", "reliability": "high"}
    ])

def main():
    print("=" * 60)
    print("WARD v0 - INDIAN CONTEXT DATA INJECTION")
    print("=" * 60)
    
    tokens = create_demo_users()
    if not tokens.get("Manager"):
        print("Failed to get manager token")
        return

    create_indian_scenarios(tokens["Manager"])
    print("\n✅ Data injection complete!")

if __name__ == "__main__":
    main()
