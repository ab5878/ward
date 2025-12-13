"""Voice-First Decision Assistant for Ward v0

Three distinct voice roles with clear authority boundaries:
1. DRIVER (Field Reality Capture) - Reports disruptions, no decision authority
2. MANAGER (Decision Owner) - Makes decisions, full protocol access
3. HELPER (Context Provider) - Provides domain knowledge (CHA, senior ops)

Ward coordinates humans under uncertainty, preserves authority hierarchy.
Voice is for capture + guidance, NOT command.
"""

import json
from typing import Dict, Any, List, Optional, Literal
from emergentintegrations.llm.chat import LlmChat, UserMessage
import os
from dotenv import load_dotenv

load_dotenv()

EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY")

# Role type definition
VoiceRole = Literal["driver", "manager", "helper"]

class VoiceDecisionAssistant:
    """Manages role-based voice-guided workflows"""
    
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
        Questions will be in the SAME LANGUAGE as the user's input
        
        Args:
            initial_transcript: Voice transcript of disruption description
        
        Returns:
            List of clarity questions in the same language as input
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"clarity-{id(initial_transcript)}",
                system_message=self.get_clarity_questions_prompt()
            ).with_model("gemini", "gemini-2.5-flash")
            
            prompt = f"""The operator said:

\"{initial_transcript}\"

CRITICAL: Generate questions in the SAME LANGUAGE as the operator's input above.
If they spoke in Tamil, ask in Tamil. If Hindi, ask in Hindi. If English, ask in English.

Generate 2-3 clarity-enforcing questions to understand:
1. What is confirmed fact vs assumption?
2. What is the exact scope?
3. What is explicitly unknown?

Return ONLY the questions, one per line, numbered. Use the EXACT same language as the input."""
            
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
            # Fallback to generic questions (English)
            # Note: In production, detect language from transcript and provide localized fallbacks
            return [
                "What is the exact location and identifier?",
                "When was this discovered and by whom?",
                "What is still unknown or uncertain?"
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
    
    def get_driver_response_prompt(self) -> str:
        """System prompt for safe driver responses"""
        return """You are Ward v0 speaking to a DRIVER (field operator).

CRITICAL CONSTRAINTS:
- Driver has NO decision authority
- Driver may not read English well
- Driver is under stress, noisy environment
- Responses must be SHORT, CALM, SAFE

YOU MAY ONLY:
- Acknowledge receipt of information
- Ask clarifying questions about what they SEE/HEAR
- Provide coordination instructions (wait safely, don't move, expect callback)
- Reassure that ops team is reviewing

YOU MUST NEVER:
- Tell them which route to take
- Make ETA promises
- Tell them to unload/load
- Make ANY decision
- Predict outcomes

LANGUAGE:
- Use simple Hindi-English mix (Hinglish) or match driver's language
- Keep under 25 words
- Be calm and trust-building

SAFE PHRASES:
"Message received. Ops team reviewing. Please stay parked safely."
"Understood. Do not move container until confirmation."
"Please wait at safe location. I'll update you."
"Can you confirm: [specific detail about what they see]?"

Generate ONLY safe responses."""

    async def generate_driver_response(self, driver_input: str, conversation_history: List[Dict]) -> str:
        """
        Generate safe response for DRIVER role
        Only acknowledgment, clarification, or safe coordination
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"driver-{id(driver_input)}",
                system_message=self.get_driver_response_prompt()
            ).with_model("gemini", "gemini-2.5-flash")
            
            # Build context
            history_text = "\n".join([
                f"{msg['speaker']}: {msg['text']}" 
                for msg in conversation_history[-3:]  # Last 3 messages
            ])
            
            prompt = f"""Previous conversation:
{history_text}

Driver just said: "{driver_input}"

Generate a SHORT, SAFE response (under 25 words). No decisions. No predictions."""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            return response.strip()
        
        except Exception as e:
            print(f"Error generating driver response: {e}")
            return "Message received. Ops team reviewing. Please stay safe."
    
    def get_helper_question_prompt(self) -> str:
        """System prompt for context-harvesting questions for helpers"""
        return """You are Ward v0 speaking to a HELPER (CHA, supervisor, senior ops).

HELPER ROLE:
- Provides domain context and expertise
- NOT the decision owner
- Has partial but important knowledge

YOUR JOB:
- Ask context-harvesting questions
- Understand what usually works/fails
- Learn domain patterns
- Build institutional knowledge

YOU MUST NEVER ASK:
- "What should we do?" (that's manager's job)
- "What's your decision?" (helper doesn't decide)

YOU SHOULD ASK:
- "Is this common?"
- "What usually resolves this fastest?"
- "What has failed before in similar cases?"
- "What are the typical clearance times?"
- "Are there any hidden dependencies?"

LANGUAGE:
- Professional but conversational
- Respect their expertise
- 2-3 questions max

Generate context-harvesting questions, NOT advice requests."""

    async def generate_helper_questions(self, context: str) -> List[str]:
        """
        Generate context-harvesting questions for HELPER role
        Not asking for advice, asking for domain knowledge
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"helper-{id(context)}",
                system_message=self.get_helper_question_prompt()
            ).with_model("gemini", "gemini-2.5-flash")
            
            prompt = f"""Context: {context}

Generate 2-3 context-harvesting questions for a CHA or senior ops person.
Focus on institutional knowledge, patterns, typical timelines.
Do NOT ask what they think we should do."""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            # Parse questions
            questions = []
            for line in response.strip().split('\n'):
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                    question = line.split('.', 1)[-1].strip() if '.' in line else line.lstrip('- •')
                    if question:
                        questions.append(question)
            
            return questions[:3]
        
        except Exception as e:
            print(f"Error generating helper questions: {e}")
            return [
                "Is this type of hold common at this port?",
                "What typically resolves this fastest based on your experience?",
                "Are there any dependencies we should be aware of?"
            ]
    
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
