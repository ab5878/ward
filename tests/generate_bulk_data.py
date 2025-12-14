#!/usr/bin/env python3
"""
Bulk Data Generator for Ward v0
Generates 1000+ realistic Indian logistics disruption cases for analytics depth.
"""

import requests
import json
import random
from datetime import datetime, timedelta
import concurrent.futures
import time

BASE_URL = "http://localhost:8001/api"

# --- DEEP INDIAN CONTEXT DATA ---

LOCATIONS = [
    "JNPT (Nhava Sheva)", "Mundra Port", "Chennai Port", "Kolkata Port", "Cochin Port",
    "ICD Tughlakabad", "ICD Dadri", "ICD Whitefield", "ICD Sanathnagar", "ICD Pithampur",
    "Bhiwandi", "Manesar", "Sriperumbudur", "Chakan (Pune)", "Hosur",
    "Walayar Checkpost", "Vapi GIDC", "Ankleshwar", "Pantnagar", "Baddi"
]

ROUTES = [
    ("Delhi", "Mumbai"), ("Chennai", "Bangalore"), ("Mundra", "Delhi"),
    ("Kolkata", "Jamshedpur"), ("Mumbai", "Pune"), ("Hyderabad", "Bangalore"),
    ("Ahmedabad", "Surat"), ("Ludhiana", "Nhava Sheva"), ("Jaipur", "Mundra")
]

CARRIERS = [
    "Maersk Line", "MSC", "CMA CGM", "Hapag-Lloyd", "ONE",
    "VRL Logistics", "Gati KWE", "SafeExpress", "TCI Freight", "Mahindra Logistics",
    "Spoton", "Blue Dart", "Rivigo"
]

COMMODITIES = [
    "Automotive Components", "Pharmaceuticals", "Textiles & Garments", 
    "Consumer Electronics", "Rice (Basmati)", "Organic Chemicals", 
    "Steel Coils", "Solar Panels", "Mobile Accessories"
]

DISRUPTION_TEMPLATES = {
    "customs_hold": [
        "Bill of Entry mismatch for {commodity}. {carrier} container held at {location}.",
        "IGST refund issue flagging by system. Shipment stuck at {location}.",
        "Random spot check by SIIB. {commodity} consignment delayed at {location}.",
        "Valuation query raised by Appraising Officer. Invoice value questioned at {location}."
    ],
    "truck_breakdown": [
        "Axle breakdown near {location}. {carrier} truck carrying {commodity}.",
        "Engine overheating on highway near {location}. Backup requested.",
        "Tyre burst and spare unavailable near {location}. Delay expected for {commodity}.",
        "Clutch failure reported by driver at {location}."
    ],
    "port_congestion": [
        "Gate automation failure at {location}. 4km truck queue.",
        "Vessel berthing delayed by 48 hours due to draft issues at {location}.",
        "Crane breakdown at Terminal 2, {location}. Import clearance slow.",
        "Cyclonic weather warning suspended operations at {location}."
    ],
    "documentation_issue": [
        "E-Way bill expired at {location}. GST squad detained vehicle.",
        "Original BL not received from supplier. Cargo held at {location}.",
        "Incorrect HS Code filed for {commodity}. Amendment required at {location}.",
        "Packing list mismatch found during inspection at {location}."
    ],
    "labor_strike": [
        "Transport union strike declared at {location}. No movement of {commodity}.",
        "Mathadi worker dispute halted loading at {location} warehouse.",
        "Local political rally blocked access road to {location}."
    ]
}

def get_status_by_age(days_old):
    """Determine likely status based on age of disruption"""
    if days_old > 10:
        return "RESOLVED"
    elif days_old > 5:
        return random.choice(["RESOLVED", "RESOLVED", "IN_PROGRESS"])
    elif days_old > 2:
        return random.choice(["IN_PROGRESS", "DECIDED", "DECISION_REQUIRED"])
    else:
        return random.choice(["REPORTED", "CLARIFIED", "DECISION_REQUIRED"])

def generate_case_data(index):
    """Generate a single random case payload"""
    days_old = random.randint(0, 365)
    created_at = datetime.now() - timedelta(days=days_old)
    
    disruption_type = random.choice(list(DISRUPTION_TEMPLATES.keys()))
    template = random.choice(DISRUPTION_TEMPLATES[disruption_type])
    
    location = random.choice(LOCATIONS)
    carrier = random.choice(CARRIERS)
    commodity = random.choice(COMMODITIES)
    
    description = template.format(location=location, carrier=carrier, commodity=commodity)
    
    route = random.choice(ROUTES)
    route_str = f"{route[0]}-{route[1]}"
    
    return {
        "description": description,
        "disruption_details": {
            "disruption_type": disruption_type,
            "scope": random.choice(["container", "truck", "shipment"]),
            "identifier": f"{random.choice(['CNTR', 'TRK', 'SHP'])}-{random.randint(10000, 99999)}",
            "time_discovered_ist": created_at.strftime("%d/%m/%Y %H:%M IST"),
            "source": random.choice(["Driver Call", "CHA Email", "System Alert", "WhatsApp"])
        },
        "shipment_identifiers": {
            "ids": [f"ID-{random.randint(1000, 9999)}"],
            "routes": [route_str],
            "carriers": [carrier]
        },
        "status": get_status_by_age(days_old),
        "created_at_override": created_at.isoformat() # Used to force backend date if supported, else we simulate
    }

def create_case(session, token, data):
    """Send API request to create case"""
    headers = {"Authorization": f"Bearer {token}"}
    try:
        # Create Case
        resp = session.post(f"{BASE_URL}/cases", headers=headers, json=data)
        if resp.status_code == 200:
            case_id = resp.json()["_id"]
            
            # Hack: Manually update the date in DB to match historical simulation
            # Since the API sets "now", we rely on the large volume. 
            # Ideally we'd have a backfill API, but for this demo, 
            # we will just create them as "now" but with different "time_discovered" fields
            # OR we can hit a specialized endpoint if we added one. 
            # For "Analytics" to look good, we really need the `created_at` field in Mongo to differ.
            # I'll add a 'backfill' endpoint logic or just update the timestamp via a direct mongo update 
            # if I were in the shell. Since I am an API client, I'll assume the 
            # Analytics Dashboard uses `time_discovered_ist` text string or I accept 
            # that "Today" will have a massive spike.
            
            # WAIT: The `analytics_service.py` uses `created_at`.
            # If I create 1000 cases now, the chart will show 1000 cases today.
            # That looks bad.
            
            # SOLUTION: I will add a hidden "backfill" param to the create_case endpoint 
            # or simply use `mcp_execute_bash` to run a python script that interacts with Motor 
            # directly to insert data, bypassing the API for speed and date control.
            
            return case_id
    except Exception as e:
        pass
    return None

def get_manager_token():
    try:
        resp = requests.post(f"{BASE_URL}/auth/login", json={
            "email": "manager@logistics.com", "password": "demo123"
        })
        return resp.json()["access_token"]
    except:
        print("Creating manager first...")
        requests.post(f"{BASE_URL}/auth/register", json={
            "email": "manager@logistics.com", "password": "demo123"
        })
        return get_manager_token()

# ------------------------------------------------------------------
# DIRECT MONGO INSERTION (FAST & ACCURATE DATES)
# ------------------------------------------------------------------
# Since we are in the same environment, we can use Motor/PyMongo directly 
# to insert thousands of records with correct historical dates.
# This is much faster and cleaner for analytics demo data.

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "test_database" # Matches .env

async def bulk_insert_mongo():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Get user ID for manager
    user = await db.users.find_one({"email": "manager@logistics.com"})
    if not user:
        print("Manager user not found. Run basic setup first.")
        return

    user_id = str(user["_id"])
    email = user["email"]
    
    cases_to_insert = []
    events_to_insert = []
    
    print(f"Generating 1,500 historical cases...")
    
    for i in range(1500):
        data = generate_case_data(i)
        created_at_dt = datetime.fromisoformat(data["created_at_override"])
        updated_at_dt = created_at_dt + timedelta(hours=random.randint(4, 72))
        
        status = data["status"]
        
        # Case Document
        case_doc = {
            "operator_id": user_id,
            "operator_email": email,
            "decision_owner_id": user_id if status != "REPORTED" else None,
            "decision_owner_email": email if status != "REPORTED" else None,
            "description": data["description"],
            "disruption_details": data["disruption_details"],
            "shipment_identifiers": data["shipment_identifiers"],
            "status": status,
            "created_at": created_at_dt,
            "updated_at": updated_at_dt
        }
        
        # Add some RCA data for resolved cases
        if status == "RESOLVED":
            case_doc["rca"] = {
                "root_cause": f"Root cause for {data['disruption_details']['disruption_type']}",
                "confidence": "high",
                "preventive_measures": ["Preventive Step 1", "Preventive Step 2"]
            }
            
        cases_to_insert.append(case_doc)
    
    # Insert in batches
    if cases_to_insert:
        result = await db.cases.insert_many(cases_to_insert)
        print(f"✅ Successfully inserted {len(result.inserted_ids)} cases directly into MongoDB.")
        
        # Generate some events for these cases
        for idx, case_id in enumerate(result.inserted_ids):
            # Initial event
            events_to_insert.append({
                "case_id": str(case_id),
                "actor": email,
                "action": "DISRUPTION_REPORTED",
                "content": cases_to_insert[idx]["description"],
                "source_type": "text",
                "reliability": "high",
                "timestamp": cases_to_insert[idx]["created_at"]
            })
            
            # Resolution event if resolved
            if cases_to_insert[idx]["status"] == "RESOLVED":
                events_to_insert.append({
                    "case_id": str(case_id),
                    "actor": "system",
                    "action": "STATE_TRANSITION",
                    "content": "Case marked as RESOLVED",
                    "source_type": "system",
                    "reliability": "high",
                    "timestamp": cases_to_insert[idx]["updated_at"]
                })
    
    if events_to_insert:
        await db.timeline_events.insert_many(events_to_insert)
        print(f"✅ Successfully inserted {len(events_to_insert)} timeline events.")

    client.close()

if __name__ == "__main__":
    # Ensure manager exists via API first
    get_manager_token()
    
    # Run bulk insert
    asyncio.run(bulk_insert_mongo())
