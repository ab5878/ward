"""
Responsibility Attribution Agent
Analyzes case data to determine who is responsible for the disruption.
"""

from typing import Dict, Any
from llm_client import LlmChat, UserMessage
import os
import json

class ResponsibilityAgent:
    def __init__(self, db):
        self.db = db
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("EMERGENT_LLM_KEY")

    async def analyze_responsibility(self, case_id: str):
        """
        Analyze voice, documents, and timeline to attribute responsibility.
        """
        case = await self.db.cases.find_one({"_id": case_id})
        if not case:
            return None

        # Build Context
        context = f"""
        Description: {case.get('description')}
        Disruption Type: {case.get('disruption_details', {}).get('disruption_type')}
        Source: {case.get('disruption_details', {}).get('source')}
        
        Transcript: {case.get('voice_transcript', 'No transcript available.')}
        
        Timeline Events:
        """
        
        cursor = await self.db.timeline_events.find({"case_id": case_id}, sort=[("timestamp", 1)])
        events = await cursor.to_list(length=20)
        for e in events:
            context += f"- [{e.get('actor')}]: {e.get('content')}\n"

        # AI Analysis
        chat = LlmChat(
            api_key=self.api_key,
            session_id=f"resp-{case_id}",
            system_message="You are a logistics dispute arbitrator. Assign responsibility for the delay based on evidence."
        ).with_model("gemini", "gemini-2.5-flash")

        prompt = f"""
        Based on the following case data, determine the PRIMARY responsible party for the disruption.
        
        Possible Parties: Driver, Transporter, CHA, Port, Customs, Shipper, Consignee, Force Majeure (Weather/Strike), Unknown.

        Context:
        {context}

        Return strictly valid JSON:
        {{
            "primary_party": "Party Name",
            "confidence": "High/Medium/Low",
            "reasoning": "One sentence explanation citing specific evidence (e.g. 'CHA admitted to late filing')."
        }}
        """

        try:
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            # Clean JSON
            text = response.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
            
            result = json.loads(text.strip())
            
            # Update DB
            await self.db.cases.update_one(
                {"_id": case_id},
                {"$set": {"responsibility": result}}
            )
            
            return result

        except Exception as e:
            print(f"Responsibility analysis failed: {e}")
            return {
                "primary_party": "Unknown",
                "confidence": "Low",
                "reasoning": " AI analysis failed. Please set manually."
            }
