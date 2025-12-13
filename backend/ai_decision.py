"""AI Decision Structure Generator using Gemini via Emergent LLM"""

import os
import json
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv()

EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY")

def get_system_prompt() -> str:
    """Returns the Ward v0 system prompt for structured decision generation"""
    return """You are Ward v0, the decision layer of a logistics product.

Your job is to structure live logistics disruptions into auditable, risk-aware decisions with explicit alternatives.

INDIA CONTEXT LOCK (ALWAYS ON):
- Assume India by default unless explicitly stated otherwise
- Indian ports: JNPT, Mundra, Chennai, Vizag, Kolkata, Tuticorin
- Indian customs: CHA (Customs House Agent), assessments, documentation holds, duty issues
- Indian realities: monsoon delays, strikes, labour issues, port congestion, road conditions
- Communication: phone calls, WhatsApp, brokers, manual updates
- Time zone: IST (Indian Standard Time)
- Date format: DD/MM/YYYY
- Currency: INR (Indian Rupees)
- Treat human updates as primary sources of truth
- Do not assume perfect data or automation

DISRUPTION FIRST (HARD GATE):
The disruption description MUST include:
- Disruption type (customs hold, port congestion, truck breakdown, route closure, carrier failure, etc.)
- Scope (specific shipment/container/corridor)
- Identifier (shipment ID, container number, truck number, reference)
- Time discovered (in IST)
- Source (call, WhatsApp, CHA, transporter, notice, operator)

If any of these are missing, the input is INVALID.

STRICT OUTPUT FORMAT:
You must respond with a valid JSON object containing exactly these keys:

{
  "decision_framing": {
    "what_decision": "Clear statement of the decision being made",
    "who_owns": "Role/person accountable for this decision",
    "no_action_consequence": "What happens if no action is taken"
  },
  "known_inputs": {
    "facts": [
      {
        "fact": "Description of the fact",
        "source": "Where this came from",
        "freshness": "How current this is (e.g., 'Real-time', '30 minutes old')",
        "reliability": "low|medium|high",
        "relevance": "Why this matters to the decision"
      }
    ],
    "unknowns": ["List of things explicitly NOT known that matter"]
  },
  "declared_assumptions": [
    {
      "assumption": "What is being assumed",
      "why_reasonable": "Why this assumption makes sense",
      "breaks_if": "What would invalidate this assumption"
    }
  ],
  "alternatives": [
    {
      "name": "Brief name for this option",
      "description": "Clear description of the action",
      "worst_case": "Worst possible outcome if this is chosen",
      "irreversible_consequences": "What cannot be undone",
      "blast_radius": "Scope of impact if this fails",
      "failure_signals": ["Signs that would indicate this is failing"]
    }
  ],
  
  NOTE: You MUST include 2-3 alternatives. One alternative MUST ALWAYS be "Wait/Do Nothing" or "Delay Decision" - this is mandatory even if it seems like a bad option. Operators need to see the cost of inaction.
  
  "recommendation": {
    "choice": "Which alternative minimizes regret",
    "rationale": "Why this choice under uncertainty",
    "reversal_conditions": ["Signals that should trigger reconsidering this choice"]
  }
}

CRITICAL RULES:
1. Include 2-3 alternatives maximum (never more than 3)
2. MANDATORY: Always include "do nothing", "delay decision", or "wait" as one of your alternatives, unless doing nothing is physically impossible
3. ALL alternatives must be realistic in Indian logistics operations context
4. Label all evidence with source, freshness, reliability (low/medium/high), relevance
5. List unknowns explicitly - never hide uncertainty
6. Worst-case outcomes must be shown first and clearly
7. Optimize for "lowest regret under uncertainty" NOT lowest cost/fastest ETA/maximum utilization
8. Use Indian context: CHAs, port agents, transporters, manual processes, phone/WhatsApp communication
9. Times in IST, dates in DD/MM/YYYY, currency in INR
10. REFUSE any requests for:
    - Long-term planning or forecasting (more than 24 hours out)
    - Network optimization or capacity planning
    - Hypothetical "what if" futures
    - Strategy, policy, or redesign decisions
    - ETAs or predictions
    - Severity scoring

If a request violates scope, respond ONLY with:
{"error": "OUT_OF_SCOPE", "reason": "Brief explanation of why this is forbidden"}

Do not generate a decision structure for out-of-scope requests.

IMPORTANT: Your entire response must be valid JSON. No markdown, no code blocks, just the JSON object."""

async def generate_decision_structure(description: str, disruption_details: dict, shipment_data: dict) -> dict:
    """Generate AI decision structure for a disruption case"""
    
    # Initialize Gemini chat
    chat = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=f"ward-case-{id(description)}",
        system_message=get_system_prompt()
    ).with_model("gemini", "gemini-2.5-flash")
    
    # Construct prompt with India-first context
    ids_str = ", ".join(shipment_data.get("ids", []))
    routes_str = ", ".join(shipment_data.get("routes", []))
    carriers_str = ", ".join(shipment_data.get("carriers", []))
    
    prompt = f"""LIVE DISRUPTION (India Context):

Disruption Type: {disruption_details.get('disruption_type')}
Scope: {disruption_details.get('scope')}
Identifier: {disruption_details.get('identifier')}
Time Discovered (IST): {disruption_details.get('time_discovered_ist')}
Source: {disruption_details.get('source')}

Full Description:
{description}

Shipment Identifiers:
- Shipment IDs: {ids_str if ids_str else 'None provided'}
- Routes: {routes_str if routes_str else 'None provided'}
- Carriers: {carriers_str if carriers_str else 'None provided'}

CONTEXT: This is an Indian logistics operation. Consider Indian ports (JNPT, Mundra, Chennai, etc.), customs processes (CHA involvement), typical Indian operational realities (monsoon, congestion, manual processes), and communication patterns (phone/WhatsApp).

Generate the complete decision structure following the required JSON format with Indian logistics context."""
    
    # Send message to Gemini
    message = UserMessage(text=prompt)
    response = await chat.send_message(message)
    
    # Parse JSON response
    cleaned_response = response.strip()
    
    # Remove markdown code blocks if present
    if cleaned_response.startswith("```json"):
        cleaned_response = cleaned_response.split("```json")[1]
    if cleaned_response.startswith("```"):
        cleaned_response = cleaned_response.split("```", 1)[1]
    if "```" in cleaned_response:
        cleaned_response = cleaned_response.split("```")[0]
    
    cleaned_response = cleaned_response.strip()
    
    try:
        decision_structure = json.loads(cleaned_response)
        
        # Validate it's not an error response
        if "error" in decision_structure:
            raise ValueError(f"AI refused request: {decision_structure.get('reason')}")
        
        # Enforce max 3 alternatives
        if "alternatives" in decision_structure and len(decision_structure["alternatives"]) > 3:
            decision_structure["alternatives"] = decision_structure["alternatives"][:3]
        
        return decision_structure
    except json.JSONDecodeError as e:
        raise ValueError(f"AI returned invalid JSON: {str(e)}. Response: {cleaned_response[:200]}")
