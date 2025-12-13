"""Voice-First Decision Assistant for Ward v0

Guides operators through the 5-step voice protocol:
1. Capture disruption via voice
2. Ask clarity-enforcing questions
3. Lock disruption with human approval
4. Guide through decision protocol
5. Output written decision with transcript
"""

import json
from typing import Dict, Any, List, Optional
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY")

class VoiceDecisionAssistant:
    """Manages voice-guided decision workflow"""
    
    def __init__(self):
        self.api_key = EMERGENT_LLM_KEY
    
    def get_clarity_questions_prompt(self) -> str:
        """System prompt for generating clarity-enforcing questions"""
        return """You are Ward v0's clarity assistant. Your ONLY job is to ask clarity-enforcing questions about a disruption.

You MUST NOT:
- Provide recommendations
- Predict outcomes
- Suggest solutions
- Make decisions
- Optimize anything

You MUST:
- Ask ONLY about facts vs unknowns
- Clarify scope (single shipment vs corridor)
- Verify source reliability (port notice vs CHA call)
- Identify what is explicitly unknown
- Keep questions short and operational

INDIA CONTEXT:
- Use Indian logistics language (CHA, port gate, customs hold)
- Reference Indian realities (monsoon, strikes, congestion)
- Time in IST, dates in DD/MM/YYYY

Generate 2-3 clarity questions max. Be direct and operational."""
    
    async def generate_clarity_questions(self, initial_transcript: str) -> List[str]:
        """
        Generate 2-3 clarity-enforcing questions based on initial disruption
        
        Args:
            initial_transcript: Voice transcript of disruption description
        
        Returns:
            List of clarity questions
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"clarity-{id(initial_transcript)}",
                system_message=self.get_clarity_questions_prompt()
            ).with_model("gemini", "gemini-2.5-flash")
            
            prompt = f"""The operator said:

\"{initial_transcript}\"

Generate 2-3 clarity-enforcing questions to understand:
1. What is confirmed fact vs assumption?
2. What is the exact scope?
3. What is explicitly unknown?

Return ONLY the questions, one per line, numbered."""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            # Parse questions from response
            questions = []
            for line in response.strip().split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):
                    # Remove numbering
                    question = line.split('.', 1)[-1].strip() if '.' in line else line.lstrip('- ')
                    if question:
                        questions.append(question)
            
            return questions[:3]  # Max 3 questions
        
        except Exception as e:
            print(f"Error generating clarity questions: {e}")
            return [
                "Is this confirmed by a port notice or only verbal communication?",
                "Is the impact limited to this shipment or are other shipments affected?",
                "What information is still unknown or uncertain?"
            ]
    
    def get_disruption_extraction_prompt(self) -> str:
        """System prompt for extracting structured disruption from conversation"""
        return """You are Ward v0's disruption extraction assistant.

Extract structured disruption details from the conversation transcript.

You must extract:
- disruption_type: (customs_hold, port_congestion, truck_breakdown, route_closure, etc.)
- scope: Brief description of impact scope
- identifier: Shipment ID, container number, truck registration, etc.
- time_discovered_ist: When discovered (DD/MM/YYYY HH:MM IST format)
- source: How it was discovered (call from CHA, WhatsApp from driver, port notice, etc.)
- full_description: Complete narrative of what happened
- explicit_unknowns: List of what is NOT known

Return ONLY valid JSON with these fields. Use Indian context (JNPT, Mundra, CHA, etc.).

Example:
{
  "disruption_type": "customs_hold",
  "scope": "single container",
  "identifier": "CMAU1234567",
  "time_discovered_ist": "13/12/2024 14:30 IST",
  "source": "Call from CHA (Jagdish Customs)",
  "full_description": "Container held at JNPT for document verification...",
  "explicit_unknowns": ["Exact clearance timeline", "Additional documents needed"]
}"""
    
    async def extract_disruption_details(self, conversation_transcript: str) -> Dict[str, Any]:
        """
        Extract structured disruption details from voice conversation
        
        Args:
            conversation_transcript: Full transcript of voice interaction
        
        Returns:
            Structured disruption details
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"extract-{id(conversation_transcript)}",
                system_message=self.get_disruption_extraction_prompt()
            ).with_model("gemini", "gemini-2.5-flash")
            
            prompt = f"""Conversation transcript:

{conversation_transcript}

Extract structured disruption details as JSON."""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            # Clean and parse JSON
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned.split("```json")[1].split("```")[0]
            elif cleaned.startswith("```"):
                cleaned = cleaned.split("```", 1)[1].split("```")[0]
            
            disruption = json.loads(cleaned.strip())
            return disruption
        
        except Exception as e:
            print(f"Error extracting disruption: {e}")
            return {
                "error": f"Failed to extract disruption details: {str(e)}"
            }
    
    async def generate_decision_guidance(self, disruption_summary: str) -> Dict[str, str]:
        """
        Generate voice guidance for the 6-step decision protocol
        
        Args:
            disruption_summary: Summary of the locked disruption
        
        Returns:
            Dictionary with guidance for each decision step
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"guidance-{id(disruption_summary)}",
                system_message="""You are Ward v0's decision guidance assistant.

Generate brief voice prompts to guide the operator through each step of the decision protocol.

Be concise, operational, and calm. Use Indian logistics context.

Return JSON with keys: decision_framing, known_inputs, assumptions, alternatives, risks, recommendation"""
            ).with_model("gemini", "gemini-2.5-flash")
            
            prompt = f"""Disruption: {disruption_summary}

Generate brief voice guidance for each decision step. Keep each prompt under 30 words."""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            # Parse JSON
            cleaned = response.strip()
            if cleaned.startswith("```json"):
                cleaned = cleaned.split("```json")[1].split("```")[0]
            elif cleaned.startswith("```"):
                cleaned = cleaned.split("```", 1)[1].split("```")[0]
            
            guidance = json.loads(cleaned.strip())
            return guidance
        
        except Exception as e:
            print(f"Error generating guidance: {e}")
            return {
                "decision_framing": "What exact decision needs to be made right now?",
                "known_inputs": "What facts do you know for certain?",
                "assumptions": "What are you assuming, and what breaks if you're wrong?",
                "alternatives": "What are your options, including doing nothing?",
                "risks": "What's the worst that could happen with each option?",
                "recommendation": "Which option minimizes regret under uncertainty?"
            }

# Singleton instance
voice_assistant = VoiceDecisionAssistant()
