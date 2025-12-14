#!/usr/bin/env python3
"""
Bulk Data Generator for Ward v0 (Enterprise Edition)
Generates 1000+ realistic Indian logistics disruption cases with Financial & Master Data.
"""

import requests
import json
import random
from datetime import datetime, timedelta
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "test_database" # Matches .env

# --- MASTER DATA MAPPINGS ---
LOCATIONS = [
    {"code": "INNSA", "name": "JNPT (Nhava Sheva)"},
    {"code": "INMUN", "name": "Mundra Port"},
    {"code": "INMAA", "name": "Chennai Port"},
    {"code": "INTKD", "name": "ICD Tughlakabad"},
    {"code": "INCCU", "name": "Kolkata Port"},
]

CARRIERS = [
    {"code": "MAEU", "name": "Maersk Line"},
    {"code": "MSCU", "name": "MSC"},
    {"code": "CMDU", "name": "CMA CGM"},
    {"code": "VRL", "name": "VRL Logistics"},
    {"code": "GATI", "name": "Gati KWE"},
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
    ],
    "truck_breakdown": [
        "Axle breakdown near {location}. {carrier} truck carrying {commodity}.",
        "Engine overheating on highway near {location}. Backup requested.",
    ],
    "port_congestion": [
        "Gate automation failure at {location}. 4km truck queue.",
        "Vessel berthing delayed by 48 hours due to draft issues at {location}.",
    ],
    "documentation_issue": [
        "E-Way bill expired at {location}. GST squad detained vehicle.",
        "Original BL not received from supplier. Cargo held at {location}.",
    ]
}

def get_status_by_age(days_old):
    if days_old > 10: return "RESOLVED"
    elif days_old > 5: return random.choice(["RESOLVED", "RESOLVED", "IN_PROGRESS"])
    elif days_old > 2: return random.choice(["IN_PROGRESS", "DECIDED", "DECISION_REQUIRED"])
    else: return random.choice(["REPORTED", "CLARIFIED", "DECISION_REQUIRED"])

def generate_financial_impact(disruption_type):
    """Generate realistic financial risk based on disruption"""
    if disruption_type == "customs_hold":
        return {
            "amount": random.randint(50000, 500000),
            "currency": "INR",
            "category": "demurrage",
            "estimated_daily_increase": random.randint(5000, 20000)
        }
    elif disruption_type == "port_congestion":
        return {
            "amount": random.randint(20000, 100000),
            "currency": "INR",
            "category": "detention",
            "estimated_daily_increase": random.randint(2000, 8000)
        }
    elif disruption_type == "truck_breakdown":
        return {
            "amount": random.randint(10000, 50000),
            "currency": "INR",
            "category": "penalty",
            "estimated_daily_increase": 0
        }
    return None

def generate_case_data(index):
    days_old = random.randint(0, 365)
    created_at = datetime.now() - timedelta(days=days_old)
    
    disruption_type = random.choice(list(DISRUPTION_TEMPLATES.keys()))
    template = random.choice(DISRUPTION_TEMPLATES[disruption_type])
    
    loc = random.choice(LOCATIONS)
    car = random.choice(CARRIERS)
    commodity = random.choice(COMMODITIES)
    
    description = template.format(location=loc["name"], carrier=car["name"], commodity=commodity)
    
    return {
        "description": description,
        "disruption_details": {
            "disruption_type": disruption_type,
            "scope": "shipment",
            "identifier": f"{random.choice(['CNTR', 'TRK'])}-{random.randint(10000, 99999)}",
            "time_discovered_ist": created_at.strftime("%d/%m/%Y %H:%M IST"),
            "source": "System Integration"
        },
        "shipment_identifiers": {
            "ids": [f"ID-{random.randint(1000, 9999)}"],
            "routes": [f"{loc['name']} - Hub"],
            "carriers": [car["name"]]
        },
        "status": get_status_by_age(days_old),
        "created_at": created_at,
        "updated_at": created_at + timedelta(hours=random.randint(4, 72)),
        
        # --- NEW ENTERPRISE FIELDS ---
        "financial_impact": generate_financial_impact(disruption_type),
        "structured_context": {
            "carrier_code": car["code"],
            "location_code": loc["code"],
            "commodity": commodity
        }
    }

async def bulk_insert_mongo():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Clean existing for clean demo
    # await db.cases.delete_many({}) # Optional: Uncomment to wipe slate
    
    user = await db.users.find_one({"email": "manager@logistics.com"})
    if not user:
        print("Manager user not found. Run basic setup first.")
        return

    user_id = str(user["_id"])
    email = user["email"]
    
    cases_to_insert = []
    
    print(f"Generating 500 Enterprise-Ready cases...")
    
    for i in range(500):
        data = generate_case_data(i)
        
        case_doc = {
            "operator_id": user_id,
            "operator_email": email,
            "decision_owner_id": user_id if data["status"] != "REPORTED" else None,
            "decision_owner_email": email if data["status"] != "REPORTED" else None,
            "description": data["description"],
            "disruption_details": data["disruption_details"],
            "shipment_identifiers": data["shipment_identifiers"],
            "status": data["status"],
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
            "financial_impact": data["financial_impact"],
            "structured_context": data["structured_context"]
        }
        cases_to_insert.append(case_doc)
    
    if cases_to_insert:
        result = await db.cases.insert_many(cases_to_insert)
        print(f"✅ Successfully inserted {len(result.inserted_ids)} enriched cases.")

    client.close()

if __name__ == "__main__":
    asyncio.run(bulk_insert_mongo())
