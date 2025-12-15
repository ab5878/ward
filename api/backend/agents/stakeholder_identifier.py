"""Stakeholder Identifier Agent"""

from typing import Dict, Any, List
from .base_agent import BaseAgent, AgentState


class StakeholderIdentifierAgent(BaseAgent):
    """Identifies stakeholders to contact based on disruption type"""
    
    # Stakeholder database for Indian logistics
    STAKEHOLDER_MATRIX = {
        "customs_hold": {
            "required": [
                {"role": "CHA", "contact_method": "whatsapp", "priority": "high"},
                {"role": "shipping_line", "contact_method": "api", "priority": "high"}
            ],
            "optional": [
                {"role": "customs_officer", "contact_method": "phone", "priority": "medium"},
                {"role": "port_ops", "contact_method": "sms", "priority": "low"}
            ]
        },
        "truck_breakdown": {
            "required": [
                {"role": "driver", "contact_method": "phone", "priority": "high"},
                {"role": "mechanic", "contact_method": "phone", "priority": "high"}
            ],
            "optional": [
                {"role": "transporter_ops", "contact_method": "whatsapp", "priority": "medium"},
                {"role": "backup_truck", "contact_method": "sms", "priority": "high"}
            ]
        },
        "port_congestion": {
            "required": [
                {"role": "port_ops", "contact_method": "phone", "priority": "high"},
                {"role": "cfs_manager", "contact_method": "whatsapp", "priority": "high"}
            ],
            "optional": [
                {"role": "shipping_line", "contact_method": "api", "priority": "medium"}
            ]
        },
        "documentation_issue": {
            "required": [
                {"role": "shipper", "contact_method": "whatsapp", "priority": "high"},
                {"role": "CHA", "contact_method": "whatsapp", "priority": "high"}
            ],
            "optional": [
                {"role": "documentation_team", "contact_method": "email", "priority": "medium"}
            ]
        },
        "transit_delay": {
            "required": [
                {"role": "transporter_ops", "contact_method": "whatsapp", "priority": "high"}
            ],
            "optional": [
                {"role": "driver", "contact_method": "phone", "priority": "medium"}
            ]
        },
        "system_outage": {
            "required": [
                {"role": "it_support", "contact_method": "email", "priority": "high"},
                {"role": "cha_association", "contact_method": "whatsapp", "priority": "medium"}
            ],
            "optional": []
        }
    }
    
    def __init__(self, db):
        super().__init__("stakeholder_identifier", db)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify stakeholders based on disruption type and location
        """
        self.state = AgentState.WORKING
        await self.log("Identifying stakeholders")
        
        disruption_type = input_data.get("disruption_type", "")
        location = input_data.get("location", "")
        case_id = input_data.get("case_id")
        
        # Get stakeholder template
        stakeholders_template = self.STAKEHOLDER_MATRIX.get(
            disruption_type,
            {"required": [], "optional": []}
        )
        
        # Fetch actual contact details from database
        stakeholders = await self._fetch_stakeholder_contacts(
            stakeholders_template,
            location,
            case_id
        )
        
        await self.log(f"Identified {len(stakeholders)} stakeholders")
        self.state = AgentState.COMPLETED
        
        return {
            "stakeholders": stakeholders,
            "case_id": case_id,
            "disruption_type": disruption_type
        }
    
    async def _fetch_stakeholder_contacts(
        self,
        template: Dict[str, List],
        location: str,
        case_id: str
    ) -> List[Dict[str, Any]]:
        """Fetch actual contact details (Mocked with Indian Context)"""
        
        stakeholders = []
        
        for group in ["required", "optional"]:
            for s_type in template[group]:
                contact_info = self._get_indian_contact(s_type["role"], location)
                stakeholders.append({
                    "role": s_type["role"],
                    "contact_method": s_type["contact_method"],
                    "priority": s_type["priority"],
                    "required": group == "required",
                    "contact": contact_info
                })
        
        return stakeholders
    
    def _get_indian_contact(self, role: str, location: str) -> Dict[str, str]:
        """Get context-aware Indian contacts"""
        
        # Determine region based on location string
        region = "mumbai" # Default
        loc_lower = location.lower()
        if "chennai" in loc_lower or "walayar" in loc_lower or "blr" in loc_lower:
            region = "south"
        elif "delhi" in loc_lower or "tughlakabad" in loc_lower or "dadri" in loc_lower:
            region = "north"
        elif "mundra" in loc_lower or "gujarat" in loc_lower:
            region = "west_gujarat"
            
        contacts_db = {
            "CHA": {
                "mumbai": {"name": "Jagdish Customs Clearing (JNPT)", "phone": "+91-98200-12345", "whatsapp": "+91-98200-12345"},
                "south": {"name": "Seahorse Shipping (Chennai)", "phone": "+91-98400-67890", "whatsapp": "+91-98400-67890"},
                "north": {"name": "Jeena & Co (Delhi)", "phone": "+91-98100-54321", "whatsapp": "+91-98100-54321"},
                "west_gujarat": {"name": "Tulsi Clearing (Mundra)", "phone": "+91-98250-99887", "whatsapp": "+91-98250-99887"}
            },
            "port_ops": {
                "mumbai": {"name": "JNPT Terminal Ops", "phone": "022-2724-1234"},
                "south": {"name": "Chennai Port Trust", "phone": "044-2536-2201"},
                "west_gujarat": {"name": "Adani Ports Control", "phone": "02838-255000"}
            },
            "transporter_ops": {
                "default": {"name": "VRL Logistics Ops", "phone": "+91-99999-88888", "whatsapp": "+91-99999-88888"}
            },
            "cfs_manager": {
                "default": {"name": "Gateway Distriparks CFS", "phone": "+91-98765-43210"}
            }
        }
        
        # Helper to safely get contact
        role_group = contacts_db.get(role, {})
        contact = role_group.get(region, role_group.get("default", {"name": f"Unknown {role}"}))
        
        return contact
