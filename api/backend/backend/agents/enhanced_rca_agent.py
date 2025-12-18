"""Enhanced RCA Agent - Performs root cause analysis with stakeholder data"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from .base_agent import BaseAgent, AgentState
from llm_client import LlmChat, UserMessage
import os
import json


class EnhancedRCAAgent(BaseAgent):
    """Performs enhanced RCA with data from multiple stakeholders"""
    
    def __init__(self, db):
        super().__init__("enhanced_rca_agent", db)
        self.api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("EMERGENT_LLM_KEY")
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform enhanced RCA with stakeholder responses
        
        Input:
            - case_id: str
            - disruption_data: Dict
            - initial_timeline: List[Dict]
            - stakeholder_responses: List[Dict]
        
        Output:
            - rca_result: Dict (root cause, actions, preventive measures)
        """
        self.state = AgentState.WORKING
        await self.log("Starting enhanced RCA")
        
        case_id = input_data.get("case_id")
        disruption_data = input_data.get("disruption_data", {})
        initial_timeline = input_data.get("initial_timeline", [])
        stakeholder_responses = input_data.get("stakeholder_responses", [])
        
        # Build rich context from all data sources
        context = self._build_rich_context(
            disruption_data,
            initial_timeline,
            stakeholder_responses
        )
        
        # Perform AI-powered RCA
        rca_result = await self._perform_ai_rca(context)
        
        # Store RCA result
        await self._store_rca_result(case_id, rca_result)
        
        await self.log("Enhanced RCA completed")
        self.state = AgentState.COMPLETED
        
        return {
            "rca_result": rca_result,
            "case_id": case_id,
            "data_sources_count": len(stakeholder_responses) + 1  # +1 for initial report
        }
    
    def _build_rich_context(
        self,
        disruption_data: Dict,
        initial_timeline: List[Dict],
        stakeholder_responses: List[Dict]
    ) -> str:
        """Build comprehensive context from all data sources"""
        
        context = f"""DISRUPTION DETAILS:
Type: {disruption_data.get('disruption_details', {}).get('disruption_type', 'N/A')}
Location: {disruption_data.get('disruption_details', {}).get('identifier', 'N/A')}
Description: {disruption_data.get('description', 'N/A')}
Discovered: {disruption_data.get('disruption_details', {}).get('time_discovered_ist', 'N/A')}
Source: {disruption_data.get('disruption_details', {}).get('source', 'N/A')}

INITIAL TIMELINE:
"""
        
        for event in initial_timeline[:5]:  # First 5 events
            context += f"- [{event.get('timestamp')}] {event.get('actor')}: {event.get('content')}\n"
        
        context += "\nSTAKEHOLDER RESPONSES:\n"
        
        for response in stakeholder_responses:
            context += f"\n[{response.get('stakeholder')}] (Reliability: {response.get('reliability')}):\n{response.get('content')}\n"
        
        return context
    
    async def _perform_ai_rca(self, context: str) -> Dict[str, Any]:
        """Use AI to perform root cause analysis"""
        
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"enhanced-rca-{datetime.now().timestamp()}",
                system_message=self._get_system_prompt()
            ).with_model("gemini", "gemini-2.5-flash")
            
            prompt = f"""Analyze this disruption with data from multiple stakeholders:

{context}

Provide comprehensive RCA in JSON format."""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            # Parse JSON response
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response.split("```json")[1]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.split("```", 1)[1]
            if "```" in cleaned_response:
                cleaned_response = cleaned_response.split("```")[0]
            
            cleaned_response = cleaned_response.strip()
            
            rca = json.loads(cleaned_response)
            return rca
        
        except Exception as e:
            await self.log(f"AI RCA failed: {str(e)}", level="error")
            return self._fallback_rca(context)
    
    def _get_system_prompt(self) -> str:
        return """You are Ward's Enhanced Root Cause Analysis engine.

You analyze disruptions using data from MULTIPLE sources:
- Initial report from field operator
- Responses from CHAs, port operations, shipping lines
- External API data

Your job:
1. ROOT CAUSE - The fundamental reason (not symptoms), with EVIDENCE from stakeholders
2. IMMEDIATE BLOCKER - What's stopping resolution right now
3. RESPONSIBLE PARTY - Who owns fixing this (be specific)
4. CONTRIBUTING FACTORS - What made it worse
5. RECOMMENDED ACTIONS - Specific WHO does WHAT by WHEN
6. ESTIMATED RESOLUTION TIME - Based on similar cases
7. PREVENTIVE MEASURES - How to avoid next time

CRITICAL RULES:
- Cite evidence from stakeholders ("According to CHA...")
- Distinguish root cause from symptoms
- Actions must have: WHO (owner), WHAT (action), WHEN (deadline)
- Base on Indian logistics reality (customs, CHAs, ports)

Format response as JSON:
{
  "root_cause": "...",
  "immediate_blocker": "...",
  "responsible_party": "...",
  "contributing_factors": ["...", "..."],
  "recommended_actions": [
    {"action": "...", "owner": "...", "timeline": "...", "priority": "high/medium/low"}
  ],
  "estimated_resolution_time": "...",
  "preventive_measures": ["...", "..."],
  "evidence_sources": ["CHA", "Port Ops", "API"],
  "confidence": "high/medium/low",
  "similar_cases_reference": "..."
}"""
    
    def _fallback_rca(self, context: str) -> Dict[str, Any]:
        """Fallback RCA if AI fails"""
        return {
            "root_cause": "Unable to determine root cause - AI analysis unavailable",
            "immediate_blocker": "Insufficient data",
            "responsible_party": "To be determined",
            "contributing_factors": ["Limited stakeholder responses"],
            "recommended_actions": [
                {
                    "action": "Gather more information from stakeholders",
                    "owner": "Manager",
                    "timeline": "Immediate",
                    "priority": "high"
                }
            ],
            "estimated_resolution_time": "Unknown",
            "preventive_measures": ["Improve data collection"],
            "evidence_sources": [],
            "confidence": "low",
            "similar_cases_reference": "N/A"
        }
    
    async def _store_rca_result(self, case_id: str, rca_result: Dict[str, Any]):
        """Store RCA result in database"""
        try:
            # Update case with RCA
            await self.db.cases.update_one(
                {"_id": case_id},
                {
                    "$set": {
                        "rca": rca_result,
                        "rca_performed_at": datetime.now(timezone.utc),
                        "rca_performed_by": "Ward AI (Enhanced RCA Agent)",
                        "updated_at": datetime.now(timezone.utc)
                    }
                }
            )
            
            # Add to timeline
            await self.db.timeline_events.insert_one({
                "case_id": case_id,
                "actor": "Ward AI (Enhanced RCA Agent)",
                "action": "ENHANCED_RCA_PERFORMED",
                "content": f"Enhanced RCA completed. Root Cause: {rca_result.get('root_cause', 'N/A')}",
                "source_type": "system",
                "reliability": "high",
                "timestamp": datetime.now(timezone.utc),
                "metadata": rca_result
            })
            
        except Exception as e:
            await self.log(f"Failed to store RCA: {str(e)}", level="error")
