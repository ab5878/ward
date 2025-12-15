"""Outreach Agent - Sends messages to stakeholders"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from .base_agent import BaseAgent, AgentState
import asyncio


class OutreachAgent(BaseAgent):
    """Sends messages to stakeholders via multiple channels"""
    
    def __init__(self, db):
        super().__init__("outreach_agent", db)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send outreach messages to all stakeholders
        
        Input:
            - stakeholders: List[Dict]
            - case_id: str
            - disruption_summary: str
        
        Output:
            - outreach_results: List[Dict]
        """
        self.state = AgentState.WORKING
        await self.log("Starting outreach to stakeholders")
        
        stakeholders = input_data.get("stakeholders", [])
        case_id = input_data.get("case_id")
        disruption_summary = input_data.get("disruption_summary", "")
        
        # Send messages in parallel
        tasks = []
        for stakeholder in stakeholders:
            task = self._send_to_stakeholder(stakeholder, case_id, disruption_summary)
            tasks.append(task)
        
        outreach_results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Log to timeline
        await self._log_outreach_to_timeline(case_id, outreach_results)
        
        await self.log(f"Outreach completed: {len(outreach_results)} stakeholders contacted")
        self.state = AgentState.COMPLETED
        
        return {
            "outreach_results": outreach_results,
            "case_id": case_id,
            "total_contacted": len(outreach_results)
        }
    
    async def _send_to_stakeholder(
        self,
        stakeholder: Dict[str, Any],
        case_id: str,
        disruption_summary: str
    ) -> Dict[str, Any]:
        """Send message to a single stakeholder"""
        
        role = stakeholder.get("role")
        contact_method = stakeholder.get("contact_method")
        contact_info = stakeholder.get("contact")
        
        # Generate message based on role
        message = self._generate_message(role, disruption_summary, case_id)
        
        # Send via appropriate channel
        try:
            if contact_method == "whatsapp":
                result = await self._send_whatsapp(contact_info, message, case_id)
            elif contact_method == "sms":
                result = await self._send_sms(contact_info, message, case_id)
            elif contact_method == "email":
                result = await self._send_email(contact_info, message, case_id)
            elif contact_method == "api":
                result = await self._call_api(contact_info, case_id)
            else:
                result = {"status": "skipped", "reason": f"Unknown contact method: {contact_method}"}
            
            return {
                "stakeholder": role,
                "contact_method": contact_method,
                "status": result.get("status"),
                "message_id": result.get("message_id"),
                "timestamp": datetime.now(timezone.utc)
            }
        
        except Exception as e:
            await self.log(f"Failed to contact {role}: {str(e)}", level="error")
            return {
                "stakeholder": role,
                "contact_method": contact_method,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc)
            }
    
    def _generate_message(self, role: str, disruption_summary: str, case_id: str) -> str:
        """Generate appropriate message for stakeholder role"""
        
        messages = {
            "CHA": f"""Ward Disruption Alert #{case_id}

{disruption_summary}

We need your help. Please reply with:
1. Current customs status
2. Officer handling this
3. Expected clearance time

Reply here or update on Ward app.
- Ward AI""",
            
            "shipping_line": f"Case #{case_id}: Need documentation status for {disruption_summary}",
            
            "shipper": f"""Urgent: Container Issue #{case_id}

{disruption_summary}

We need corrected documentation. Please check and send ASAP.

Reply here when sent.
- Ward AI""",
            
            "port_ops": f"Query #{case_id}: {disruption_summary}. Need container location and status. Reply with details."
        }
        
        return messages.get(role, f"Case #{case_id}: {disruption_summary}. Need your input.")
    
    async def _send_whatsapp(self, contact_info: Dict, message: str, case_id: str) -> Dict:
        """Send WhatsApp message (mock for now)"""
        await self.log(f"[MOCK] Sending WhatsApp to {contact_info.get('name')}: {message[:50]}...")
        # TODO: Integrate with WhatsApp Business API
        return {
            "status": "sent",
            "message_id": f"wa_{case_id}_{datetime.now().timestamp()}",
            "channel": "whatsapp"
        }
    
    async def _send_sms(self, contact_info: Dict, message: str, case_id: str) -> Dict:
        """Send SMS (mock for now)"""
        await self.log(f"[MOCK] Sending SMS to {contact_info.get('name')}: {message[:50]}...")
        # TODO: Integrate with SMS provider (Twilio, etc.)
        return {
            "status": "sent",
            "message_id": f"sms_{case_id}_{datetime.now().timestamp()}",
            "channel": "sms"
        }
    
    async def _send_email(self, contact_info: Dict, message: str, case_id: str) -> Dict:
        """Send email (mock for now)"""
        await self.log(f"[MOCK] Sending email to {contact_info.get('name')}")
        # TODO: Integrate with email service
        return {
            "status": "sent",
            "message_id": f"email_{case_id}_{datetime.now().timestamp()}",
            "channel": "email"
        }
    
    async def _call_api(self, contact_info: Dict, case_id: str) -> Dict:
        """Call external API (mock for now)"""
        await self.log(f"[MOCK] Calling API: {contact_info.get('api_endpoint')}")
        # TODO: Make actual API call
        return {
            "status": "success",
            "message_id": f"api_{case_id}_{datetime.now().timestamp()}",
            "channel": "api",
            "data": {"mock": "api_response"}
        }
    
    async def _log_outreach_to_timeline(self, case_id: str, results: List[Dict]):
        """Log outreach attempts to case timeline"""
        try:
            for result in results:
                if isinstance(result, dict) and result.get("status") == "sent":
                    await self.db.timeline_events.insert_one({
                        "case_id": case_id,
                        "actor": "Ward AI (Outreach Agent)",
                        "action": "STAKEHOLDER_CONTACTED",
                        "content": f"Contacted {result.get('stakeholder')} via {result.get('contact_method')}",
                        "source_type": "system",
                        "reliability": "high",
                        "timestamp": datetime.now(timezone.utc),
                        "metadata": result
                    })
        except Exception as e:
            await self.log(f"Failed to log to timeline: {str(e)}", level="error")
