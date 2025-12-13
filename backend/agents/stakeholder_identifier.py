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
                {"role": "depot_manager", "contact_method": "whatsapp", "priority": "medium"},
                {"role": "backup_truck", "contact_method": "sms", "priority": "high"}
            ]
        },
        "port_congestion": {
            "required": [
                {"role": "port_ops", "contact_method": "phone", "priority": "high"},
                {"role": "shipping_line", "contact_method": "api", "priority": "high"}
            ],
            "optional": [
                {"role": "alternate_port", "contact_method": "api", "priority": "medium"}
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
        }
    }
    
    def __init__(self, db):
        super().__init__("stakeholder_identifier", db)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Identify stakeholders based on disruption type and location
        
        Input:
            - disruption_type: str
            - location: str
            - case_id: str
        
        Output:
            - stakeholders: List[Dict]
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
        """Fetch actual contact details from database"""
        
        stakeholders = []
        
        # For demo: Return mock contacts
        # In production: Query database for actual contacts
        
        for stakeholder_type in template["required"]:
            stakeholder = {
                "role": stakeholder_type["role"],
                "contact_method": stakeholder_type["contact_method"],
                "priority": stakeholder_type["priority"],
                "required": True,
                # Mock contact - in prod, fetch from DB
                "contact": self._get_mock_contact(stakeholder_type["role"], location)
            }
            stakeholders.append(stakeholder)
        
        for stakeholder_type in template["optional"]:
            stakeholder = {
                "role": stakeholder_type["role"],
                "contact_method": stakeholder_type["contact_method"],
                "priority": stakeholder_type["priority"],
                "required": False,
                "contact": self._get_mock_contact(stakeholder_type["role"], location)
            }
            stakeholders.append(stakeholder)
        
        return stakeholders
    
    def _get_mock_contact(self, role: str, location: str) -> Dict[str, str]:
        """Get mock contact info (for demo)"""
        contacts = {
            "CHA": {
                "name": "Jagdish Customs Clearing",
                "phone": "+91-98765-43210",
                "whatsapp": "+91-98765-43210",
                "email": "jagdish@customsclearance.com"
            },
            "shipping_line": {
                "name": "Maersk Line India",
                "api_endpoint": "https://api.maersk.com/india",
                "email": "india@maersk.com"
            },
            "shipper": {
                "name": "Raj Electronics Pvt Ltd",
                "phone": "+91-98765-00000",
                "whatsapp": "+91-98765-00000",
                "email": "logistics@rajelectronics.com"
            },
            "port_ops": {
                "name": f"{location} Port Operations",
                "phone": "+91-22-1234-5678",
                "sms": "+91-22-1234-5678"
            }
        }
        return contacts.get(role, {"name": f"Unknown {role}"})
