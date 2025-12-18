"""Action Executor Agent - Executes approved action plans"""

from typing import Dict, Any, List
from datetime import datetime, timezone
from .base_agent import BaseAgent, AgentState
import asyncio


class ActionExecutorAgent(BaseAgent):
    """Executes the action plan approved by the manager"""
    
    def __init__(self, db):
        super().__init__("action_executor", db)
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the approved action plan
        
        Input:
            - case_id: str
            - action_plan: List[Dict]
        
        Output:
            - execution_report: List[Dict]
        """
        self.state = AgentState.WORKING
        await self.log("Starting action plan execution")
        
        case_id = input_data.get("case_id")
        action_plan = input_data.get("action_plan", [])
        
        results = []
        tasks = []
        
        for action in action_plan:
            task = self._execute_single_action(action, case_id)
            tasks.append(task)
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Log completion
        await self._log_execution_to_timeline(case_id, results)
        
        await self.log(f"Executed {len(results)} actions")
        self.state = AgentState.COMPLETED
        
        return {
            "execution_report": results,
            "case_id": case_id,
            "actions_completed": len(results)
        }
    
    async def _execute_single_action(self, action: Dict[str, Any], case_id: str) -> Dict[str, Any]:
        """Execute a single action item"""
        
        action_type = action.get("type", "unknown")
        description = action.get("description", "")
        owner = action.get("owner", "system")
        
        try:
            if action_type == "notify":
                await self._notify_stakeholder(action, case_id)
            elif action_type == "reminder":
                await self._set_reminder(action, case_id)
            elif action_type == "api_call":
                await self._call_external_system(action, case_id)
            
            return {
                "action_id": action.get("id"),
                "status": "completed",
                "timestamp": datetime.now(timezone.utc),
                "details": f"Executed: {description}"
            }
            
        except Exception as e:
            await self.log(f"Failed to execute action {description}: {str(e)}", level="error")
            return {
                "action_id": action.get("id"),
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc)
            }
    
    async def _notify_stakeholder(self, action: Dict, case_id: str):
        """Send notification to stakeholder"""
        # In a real system, this would call the messaging service
        # For now, we simulate success
        await self.log(f"[MOCK] Notifying {action.get('owner')}: {action.get('description')}")
        await asyncio.sleep(0.5) # Simulate network delay
    
    async def _set_reminder(self, action: Dict, case_id: str):
        """Set a system reminder"""
        # Mock implementation
        await self.log(f"[MOCK] Setting reminder for {action.get('deadline')}: {action.get('description')}")
    
    async def _call_external_system(self, action: Dict, case_id: str):
        """Call external API"""
        # Mock implementation
        await self.log(f"[MOCK] Calling external system: {action.get('system')}")
    
    async def _log_execution_to_timeline(self, case_id: str, results: List[Dict]):
        """Log execution summary to timeline"""
        
        # Count successes and failures
        success_count = sum(1 for r in results if isinstance(r, dict) and r.get("status") == "completed")
        
        await self.db.timeline_events.insert_one({
            "case_id": case_id,
            "actor": "Ward AI (Action Executor)",
            "action": "PLAN_EXECUTED",
            "content": f"Executed {success_count} actions from the approved plan.",
            "source_type": "system",
            "reliability": "high",
            "timestamp": datetime.now(timezone.utc),
            "metadata": {"results": results}
        })
