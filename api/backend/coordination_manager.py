"""Coordination Manager - Master Orchestrator for Active Coordination"""

import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from agents.stakeholder_identifier import StakeholderIdentifierAgent
from agents.outreach_agent import OutreachAgent
from agents.response_collector import ResponseCollectorAgent
from agents.enhanced_rca_agent import EnhancedRCAAgent
from agents.action_executor_agent import ActionExecutorAgent

class CoordinationManager:
    """
    Master orchestrator that sequences the AI agents to deliver
    the full "Active Coordination" workflow.
    """
    
    def __init__(self, db):
        self.db = db
        # Initialize agents
        self.identifier = StakeholderIdentifierAgent(db)
        self.outreach = OutreachAgent(db)
        self.collector = ResponseCollectorAgent(db)
        self.rca = EnhancedRCAAgent(db)
        self.executor = ActionExecutorAgent(db)
        
    async def start_coordination(self, case_id: str, disruption_summary: str, disruption_type: str, location: str):
        """
        Phase 1 & 2: Identify Stakeholders -> Initiate Outreach
        """
        # 1. Identify Stakeholders
        id_result = await self.identifier.execute({
            "disruption_type": disruption_type,
            "location": location,
            "case_id": case_id
        })
        stakeholders = id_result.get("stakeholders", [])
        
        # 2. Initiate Outreach
        outreach_result = await self.outreach.execute({
            "stakeholders": stakeholders,
            "case_id": case_id,
            "disruption_summary": disruption_summary
        })
        
        # Update case status to indicate coordination started
        await self.db.cases.update_one(
            {"_id": case_id}, # Note: Assume case_id is converted to ObjectId by caller or handled
            {"$set": {"coordination_status": "outreach_sent", "stakeholders": stakeholders}}
        )
        
        return {
            "status": "started",
            "stakeholders": stakeholders,
            "outreach_result": outreach_result
        }
        
    async def perform_enhanced_rca(self, case_id: str):
        """
        Phase 3: Analyze with Stakeholder Data
        """
        # 1. Collect all responses currently available
        # Note: In a real system we might wait/poll, but here we just grab what we have
        collection_result = await self.collector.execute({
            "case_id": case_id,
            "expected_responses": 3, # arbitrary default
            "timeout_minutes": 0 # Immediate collection
        })
        
        responses = collection_result.get("responses", [])
        
        # 2. Perform Enhanced RCA
        # We need to fetch the case to get the initial report
        # case = await self.db.cases.find_one(...) # Logic moved to agent or passed in
        
        # For now, we assume the agent handles DB lookups if needed, or we pass basic data
        rca_result = await self.rca.execute({
            "case_id": case_id,
            "stakeholder_responses": responses
        })
        
        return rca_result

    async def execute_plan(self, case_id: str, action_plan: List[Dict]):
        """
        Phase 5: Execute Approved Actions
        """
        result = await self.executor.execute({
            "case_id": case_id,
            "action_plan": action_plan
        })
        
        return result

    async def simulate_response(self, case_id: str, actor: str, content: str):
        """
        Helper for Demo: Inject a response into the timeline
        """
        event = {
            "case_id": case_id,
            "actor": actor,
            "action": "STAKEHOLDER_RESPONSE",
            "content": content,
            "source_type": "text",
            "reliability": "high",
            "timestamp": datetime.now(timezone.utc),
            "metadata": {"simulated": True}
        }
        
        await self.db.timeline_events.insert_one(event)
        return event
