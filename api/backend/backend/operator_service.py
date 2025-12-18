"""
Transport Operator Service
Handles operator-specific features: fleet management, driver onboarding, bulk operations
"""

from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List, Optional
from uuid import uuid4
import csv
import io

class OperatorService:
    def __init__(self, db):
        self.db = db
    
    async def create_operator_account(self, operator_data: Dict[str, Any]) -> str:
        """
        Create operator account with company details
        """
        operator_id = str(uuid4())
        operator = {
            "id": operator_id,
            "company_name": operator_data["company_name"],
            "email": operator_data["email"],
            "phone": operator_data.get("phone"),
            "fleet_size": operator_data.get("fleet_size", 0),
            "account_type": operator_data.get("account_type", "pilot"),  # pilot, standard, enterprise
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc),
            "settings": {
                "notifications": {
                    "email": True,
                    "whatsapp": False,
                    "sms": False
                },
                "webhook_url": operator_data.get("webhook_url"),
                "branding": {
                    "logo_url": operator_data.get("logo_url"),
                    "primary_color": operator_data.get("primary_color", "#2563eb")
                }
            }
        }
        
        result = await self.db.operators.insert_one(operator)
        return operator_id
        return operator_id
    
    async def add_fleet_vehicle(self, operator_id: str, vehicle_data: Dict[str, Any]) -> str:
        """
        Add a single vehicle to operator's fleet
        """
        vehicle_id = str(uuid4())
        vehicle = {
            "id": vehicle_id,
            "operator_id": operator_id,
            "vehicle_number": vehicle_data["vehicle_number"],
            "vehicle_type": vehicle_data.get("vehicle_type", "truck"),  # truck, container, trailer
            "driver_name": vehicle_data.get("driver_name"),
            "driver_phone": vehicle_data.get("driver_phone"),
            "route": vehicle_data.get("route"),  # e.g., "JNPT-Delhi"
            "status": "active",
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
        
        result = await self.db.fleet_vehicles.insert_one(vehicle)
        return vehicle_id
    
    async def bulk_upload_fleet(self, operator_id: str, csv_content: str) -> Dict[str, Any]:
        """
        Bulk upload fleet from CSV
        Format: vehicle_number,driver_name,driver_phone,route,vehicle_type
        """
        reader = csv.DictReader(io.StringIO(csv_content))
        results = {
            "success": 0,
            "failed": 0,
            "errors": []
        }
        
        for row in reader:
            try:
                vehicle_data = {
                    "vehicle_number": row.get("vehicle_number", "").strip(),
                    "driver_name": row.get("driver_name", "").strip(),
                    "driver_phone": row.get("driver_phone", "").strip(),
                    "route": row.get("route", "").strip(),
                    "vehicle_type": row.get("vehicle_type", "truck").strip()
                }
                
                if not vehicle_data["vehicle_number"]:
                    results["failed"] += 1
                    results["errors"].append(f"Row {reader.line_num}: Missing vehicle_number")
                    continue
                
                await self.add_fleet_vehicle(operator_id, vehicle_data)
                results["success"] += 1
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"Row {reader.line_num}: {str(e)}")
        
        return results
    
    async def generate_driver_magic_link(self, operator_id: str, vehicle_id: str) -> str:
        """
        Generate magic link for driver (no login required)
        Link expires in 30 days
        """
        link_token = str(uuid4())
        magic_link = {
            "id": str(uuid4()),
            "operator_id": operator_id,
            "vehicle_id": vehicle_id,
            "token": link_token,
            "expires_at": datetime.now(timezone.utc) + timedelta(days=30),
            "created_at": datetime.now(timezone.utc),
            "used_count": 0
        }
        
        result = await self.db.magic_links.insert_one(magic_link)
        
        # Return full URL
        base_url = "https://ward-logic.vercel.app"  # TODO: Get from config
        return f"{base_url}/driver/{link_token}"
    
    async def generate_driver_qr_code(self, operator_id: str, vehicle_id: str) -> Dict[str, Any]:
        """
        Generate QR code data for vehicle
        Returns: {qr_data: str, qr_url: str}
        """
        magic_link = await self.generate_driver_magic_link(operator_id, vehicle_id)
        
        # QR code contains the magic link
        return {
            "qr_data": magic_link,
            "qr_url": f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={magic_link}"
        }
    
    async def get_operator_dashboard(self, operator_id: str, days: int = 7) -> Dict[str, Any]:
        """
        Get operator dashboard metrics
        """
        # Get fleet size
        fleet_cursor = await self.db.fleet_vehicles.find({"operator_id": operator_id})
        fleet = await fleet_cursor.to_list(length=1000)
        fleet_size = len(fleet)
        
        # Get cases for operator's vehicles
        try:
            cases_cursor = await self.db.cases.find({
                "operator_id": operator_id
            })
            cases = await cases_cursor.to_list(length=1000)
            # Filter by date in Python (since we can't easily do date filtering in query)
            cutoff_date = datetime.now(timezone.utc) - timedelta(days=days)
            cases = [c for c in cases if c.get("created_at") and c.get("created_at") >= cutoff_date] if cases else []
        except Exception as e:
            print(f"Warning: Failed to fetch cases: {e}")
            cases = []
        
        # Calculate metrics
        total_cases = len(cases)
        active_cases = len([c for c in cases if c.get("status") != "RESOLVED"])
        total_financial_impact = sum([
            c.get("financial_impact", {}).get("amount", 0) 
            for c in cases 
            if c.get("financial_impact")
        ])
        
        # Evidence readiness
        evidence_ready = len([
            c for c in cases 
            if c.get("evidence_score", {}).get("score", 0) >= 70
        ])
        
        # Cases by route
        cases_by_route = {}
        for case in cases:
            route = case.get("lane") or "Unknown"
            cases_by_route[route] = cases_by_route.get(route, 0) + 1
        
        return {
            "fleet_size": fleet_size,
            "total_cases": total_cases,
            "active_cases": active_cases,
            "total_financial_impact": total_financial_impact,
            "evidence_ready_cases": evidence_ready,
            "evidence_readiness_rate": (evidence_ready / total_cases * 100) if total_cases > 0 else 0,
            "cases_by_route": cases_by_route,
            "period_days": days
        }
    
    async def get_operator_vehicles(self, operator_id: str) -> List[Dict[str, Any]]:
        """
        Get all vehicles for operator
        """
        cursor = await self.db.fleet_vehicles.find({"operator_id": operator_id})
        vehicles = await cursor.to_list(length=1000)
        return vehicles
    
    async def update_operator_settings(self, operator_id: str, settings: Dict[str, Any]) -> bool:
        """
        Update operator settings (notifications, webhooks, branding)
        """
        update_data = {
            "settings": settings,
            "updated_at": datetime.now(timezone.utc)
        }
        
        result = await self.db.operators.update_one(
            {"id": operator_id},
            {"$set": update_data}
        )
        
        return result.matched_count > 0

