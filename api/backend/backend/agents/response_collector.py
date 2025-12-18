"""Response Collector Agent - Collects responses from stakeholders"""

from typing import Dict, Any, List
from datetime import datetime, timezone, timedelta
from .base_agent import BaseAgent, AgentState
import asyncio


class ResponseCollectorAgent(BaseAgent):
    """Collects and organizes responses from stakeholders"""
    
    def __init__(self, db):
        super().__init__("response_collector", db)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect responses from stakeholders
        
        Input:
            - case_id: str
            - expected_responses: int
            - timeout_minutes: int (default 30)
        
        Output:
            - responses: List[Dict]
            - complete: bool (all responses received)
        """
        self.state = AgentState.WORKING
        await self.log("Starting response collection")
        
        case_id = input_data.get("case_id")
        expected_responses = input_data.get("expected_responses", 3)
        timeout_minutes = input_data.get("timeout_minutes", 30)
        
        responses = []
        deadline = datetime.now(timezone.utc) + timedelta(minutes=timeout_minutes)
        
        # Poll for responses until deadline or all received
        while datetime.now(timezone.utc) < deadline:
            # Check timeline for new responses
            new_responses = await self._check_for_new_responses(case_id, responses)
            
            if new_responses:
                responses.extend(new_responses)
                await self.log(f"Collected {len(new_responses)} new responses")
            
            # Check if we have all expected responses
            if len(responses) >= expected_responses:
                await self.log("All expected responses received")
                break
            
            # Wait before next poll
            await asyncio.sleep(10)  # Poll every 10 seconds
        
        # Organize responses by stakeholder
        organized_responses = self._organize_responses(responses)
        
        self.state = AgentState.COMPLETED
        
        return {
            "responses": organized_responses,
            "case_id": case_id,
            "total_responses": len(responses),
            "complete": len(responses) >= expected_responses
        }
    
    async def _check_for_new_responses(
        self,
        case_id: str,
        existing_responses: List[Dict]
    ) -> List[Dict]:
        """Check timeline for new stakeholder responses"""
        
        # Get existing response IDs
        existing_ids = {r.get("_id") for r in existing_responses}
        
        # Query timeline for stakeholder responses
        cursor = self.db.timeline_events.find({
            "case_id": case_id,
            "action": {"$in": ["STAKEHOLDER_RESPONSE", "CONTEXT_ADDED"]}
        }).sort("timestamp", -1)
        
        timeline_events = await cursor.to_list(length=100)
        
        # Filter for new responses
        new_responses = [
            event for event in timeline_events
            if event.get("_id") not in existing_ids
        ]
        
        return new_responses
    
    def _organize_responses(self, responses: List[Dict]) -> List[Dict[str, Any]]:
        """Organize responses by stakeholder for RCA"""
        
        organized = []
        for response in responses:
            organized.append({
                "stakeholder": response.get("actor", "Unknown"),
                "content": response.get("content", ""),
                "timestamp": response.get("timestamp"),
                "reliability": response.get("reliability", "medium"),
                "source_type": response.get("source_type", "text"),
                "metadata": response.get("metadata", {})
            })
        
        return organized
    
    async def add_mock_responses(self, case_id: str, disruption_type: str):
        """Add mock stakeholder responses for demo"""
        
        mock_responses = {
            "customs_hold": [
                {
                    "actor": "CHA Jagdish",
                    "content": "Customs Officer Sharma handling this. Issue is invoice-BL description mismatch. Invoice says 'Computer Parts', BL says 'Electronics'. Need corrected invoice from shipper.",
                    "reliability": "high",
                    "source_type": "text"
                },
                {
                    "actor": "Port Operations",
                    "content": "Container located at Gate 7. Physical inspection complete. Awaiting customs clearance only.",
                    "reliability": "high",
                    "source_type": "text"
                },
                {
                    "actor": "Maersk Line API",
                    "content": "BL #MAEU1234567 shows: Description='Electronics', HS Code=8517. Invoice shows 'Computer Parts'.",
                    "reliability": "high",
                    "source_type": "system"
                }
            ]
        }
        
        responses_for_type = mock_responses.get(disruption_type, [])
        
        for response in responses_for_type:
            await self.db.timeline_events.insert_one({
                "case_id": case_id,
                "actor": response["actor"],
                "action": "STAKEHOLDER_RESPONSE",
                "content": response["content"],
                "source_type": response["source_type"],
                "reliability": response["reliability"],
                "timestamp": datetime.now(timezone.utc),
                "metadata": {"mock": True}
            })
        
        await self.log(f"Added {len(responses_for_type)} mock responses")
