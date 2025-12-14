"""
Master Data Service
Manages standardized logistics entities (Carriers, Locations, Vendors).
"""

from motor.motor_asyncio import AsyncIOMotorClient
import asyncio

class MasterDataService:
    def __init__(self, db):
        self.db = db

    async def seed_master_data(self):
        """Seed the database with industry-standard master data"""
        
        # 1. Locations (Ports, ICDs)
        locations = [
            {"code": "INNSA", "name": "JNPT (Nhava Sheva)", "type": "Port", "region": "West"},
            {"code": "INMUN", "name": "Mundra Port", "type": "Port", "region": "West"},
            {"code": "INMAA", "name": "Chennai Port", "type": "Port", "region": "South"},
            {"code": "INTKD", "name": "ICD Tughlakabad", "type": "ICD", "region": "North"},
            {"code": "INCCU", "name": "Kolkata Port", "type": "Port", "region": "East"},
            {"code": "INBLR", "name": "ICD Whitefield", "type": "ICD", "region": "South"},
            {"code": "INCOK", "name": "Cochin Port", "type": "Port", "region": "South"}
        ]
        
        # 2. Carriers (Shipping Lines, Transporters)
        carriers = [
            {"code": "MAEU", "name": "Maersk Line", "type": "Sea"},
            {"code": "MSCU", "name": "MSC", "type": "Sea"},
            {"code": "CMDU", "name": "CMA CGM", "type": "Sea"},
            {"code": "HLCU", "name": "Hapag-Lloyd", "type": "Sea"},
            {"code": "VRL", "name": "VRL Logistics", "type": "Road"},
            {"code": "GATI", "name": "Gati KWE", "type": "Road"},
            {"code": "SAFE", "name": "Safexpress", "type": "Road"},
            {"code": "CONC", "name": "CONCOR", "type": "Rail"}
        ]
        
        # 3. Vendors (CHAs, Surveyors)
        vendors = [
            {"name": "Jagdish Customs Clearing", "type": "CHA", "location": "INNSA"},
            {"name": "Seahorse Shipping", "type": "CHA", "location": "INMAA"},
            {"name": "Jeena & Company", "type": "CHA", "location": "INTKD"},
            {"name": "Tulsi Clearing", "type": "CHA", "location": "INMUN"}
        ]

        # 4. Reason Codes (Granular Status)
        reason_codes = [
            {"category": "customs_hold", "code": "CUST_01", "description": "Assessment Pending"},
            {"category": "customs_hold", "code": "CUST_02", "description": "Examination Order Issued"},
            {"category": "customs_hold", "code": "CUST_03", "description": "Query Raised (Document Mismatch)"},
            {"category": "customs_hold", "code": "CUST_04", "description": "Duty Payment Pending"},
            {"category": "port_congestion", "code": "PORT_01", "description": "Gate Automation Failure"},
            {"category": "port_congestion", "code": "PORT_02", "description": "Vessel Berthing Delay"},
            {"category": "truck_breakdown", "code": "TRK_01", "description": "Mechanical Failure"},
            {"category": "truck_breakdown", "code": "TRK_02", "description": "Accident/Incident"}
        ]

        # Upsert logic
        for loc in locations:
            await self.db.master_locations.update_one({"code": loc["code"]}, {"$set": loc}, upsert=True)
            
        for car in carriers:
            await self.db.master_carriers.update_one({"code": car["code"]}, {"$set": car}, upsert=True)
            
        for ven in vendors:
            await self.db.master_vendors.update_one({"name": ven["name"]}, {"$set": ven}, upsert=True)
            
        for rc in reason_codes:
            await self.db.master_reason_codes.update_one({"code": rc["code"]}, {"$set": rc}, upsert=True)

        print("✅ Master Data Seeded Successfully")

    async def lookup_entity(self, text: str):
        """Intelligent lookup to link text to master data"""
        # Simple string match for MVP
        text_lower = text.lower()
        
        # Find Carrier
        carrier = await self.db.master_carriers.find_one({"$or": [
            {"name": {"$regex": text_lower, "$options": "i"}},
            {"code": {"$regex": text_lower, "$options": "i"}}
        ]})
        
        # Find Location
        location = await self.db.master_locations.find_one({"$or": [
            {"name": {"$regex": text_lower, "$options": "i"}},
            {"code": {"$regex": text_lower, "$options": "i"}}
        ]})
        
        return {
            "carrier": carrier,
            "location": location
        }
