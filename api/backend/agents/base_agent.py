"""Base Agent Class for Ward AI Agent System"""

from enum import Enum
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass
import asyncio


class AgentState(str, Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class AgentMessage:
    """Message passed between agents"""
    from_agent: str
    to_agent: str
    content: Dict[str, Any]
    timestamp: datetime
    message_id: str


class BaseAgent:
    """Base class for all Ward AI agents"""
    
    def __init__(self, agent_id: str, db):
        self.agent_id = agent_id
        self.state = AgentState.IDLE
        self.db = db
        self.message_queue = asyncio.Queue()
        self.logger = []
    
    async def log(self, message: str, level: str = "info"):
        """Log agent activity"""
        log_entry = {
            "agent_id": self.agent_id,
            "timestamp": datetime.now(timezone.utc),
            "level": level,
            "message": message
        }
        self.logger.append(log_entry)
        print(f"[{self.agent_id}] {message}")
    
    async def send_message(self, to_agent: str, content: Dict[str, Any]):
        """Send message to another agent"""
        message = AgentMessage(
            from_agent=self.agent_id,
            to_agent=to_agent,
            content=content,
            timestamp=datetime.now(timezone.utc),
            message_id=f"{self.agent_id}-{to_agent}-{datetime.now().timestamp()}"
        )
        await self.log(f"Sending message to {to_agent}")
        return message
    
    async def receive_message(self) -> Optional[AgentMessage]:
        """Receive message from queue"""
        try:
            message = await asyncio.wait_for(self.message_queue.get(), timeout=1.0)
            await self.log(f"Received message from {message.from_agent}")
            return message
        except asyncio.TimeoutError:
            return None
    
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Main execution method - override in subclasses"""
        raise NotImplementedError("Subclasses must implement execute()")
    
    async def cleanup(self):
        """Cleanup resources"""
        await self.log("Agent cleanup")
        self.state = AgentState.IDLE
