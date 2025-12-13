"""
Ward v0 - Core POC Test Script
Tests Gemini's ability to generate structured decision drafts following the 6-step protocol
"""

import asyncio
import json
import os
import sys
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

# Load environment variables
load_dotenv('/app/backend/.env')

# Validation colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

class WardPOCValidator:
    """Validates AI-generated decision structures against Ward v0 requirements"""
    
    def __init__(self):
        self.api_key = os.environ.get('EMERGENT_LLM_KEY')
        if not self.api_key:
            raise ValueError("EMERGENT_LLM_KEY not found in environment")
        
        # Initialize Gemini chat client
        self.chat = LlmChat(
            api_key=self.api_key,
            session_id="ward-poc-test",
            system_message=self.get_system_prompt()
        ).with_model("gemini", "gemini-2.5-flash")
        
        self.validation_results = []
    
    def get_system_prompt(self):
        """Returns the Ward v0 system prompt with strict output requirements"""
        return """You are Ward v0, the decision layer of a logistics product.

Your job is to structure live logistics disruptions into auditable, risk-aware decisions with explicit alternatives.

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
3. Label all evidence with source, freshness, reliability (low/medium/high), relevance
4. List unknowns explicitly - never hide uncertainty
5. Worst-case outcomes must be shown first and clearly
6. Optimize for "lowest regret under uncertainty" NOT cost/speed/efficiency
7. REFUSE any requests for:
   - Long-term planning or forecasting (more than 24 hours out)
   - Network optimization or capacity planning
   - Hypothetical "what if" futures
   - Strategy or policy decisions

If a request violates scope, respond ONLY with:
{"error": "OUT_OF_SCOPE", "reason": "Brief explanation of why this is forbidden"}

Do not generate a decision structure for out-of-scope requests.

IMPORTANT: Your entire response must be valid JSON. No markdown, no code blocks, just the JSON object."""

    async def test_scenario(self, scenario_name: str, disruption_description: str, shipment_data: dict) -> dict:
        """Test a single disruption scenario"""
        print(f"\n{'='*80}")
        print(f"Testing Scenario: {scenario_name}")
        print(f"{'='*80}")
        
        # Construct the prompt
        prompt = f"""Disruption Description:
{disruption_description}

Shipment Identifiers:
- Shipment IDs: {', '.join(shipment_data.get('ids', []))}
- Routes: {', '.join(shipment_data.get('routes', []))}
- Carriers: {', '.join(shipment_data.get('carriers', []))}

Generate the complete decision structure following the required JSON format."""
        
        try:
            # Send message to Gemini
            message = UserMessage(text=prompt)
            response = await self.chat.send_message(message)
            
            print(f"\n{YELLOW}Raw AI Response:{RESET}")
            print(response[:500] + "..." if len(response) > 500 else response)
            
            # Parse JSON response
            # Clean up response if it contains markdown code blocks
            cleaned_response = response.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response.split("```json")[1]
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.split("```", 1)[1]
            if "```" in cleaned_response:
                cleaned_response = cleaned_response.split("```")[0]
            cleaned_response = cleaned_response.strip()
            
            decision_structure = json.loads(cleaned_response)
            
            # Validate the structure
            validation_results = self.validate_decision_structure(decision_structure)
            
            return {
                "scenario": scenario_name,
                "success": validation_results["all_passed"],
                "decision_structure": decision_structure,
                "validations": validation_results
            }
            
        except json.JSONDecodeError as e:
            print(f"{RED}JSON Parse Error: {e}{RESET}")
            return {
                "scenario": scenario_name,
                "success": False,
                "error": f"Invalid JSON response: {str(e)}"
            }
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")
            return {
                "scenario": scenario_name,
                "success": False,
                "error": str(e)
            }
    
    def validate_decision_structure(self, structure: dict) -> dict:
        """Validate that the decision structure meets all Ward v0 requirements"""
        results = {
            "all_passed": True,
            "checks": []
        }
        
        def add_check(name: str, passed: bool, details: str = ""):
            results["checks"].append({
                "name": name,
                "passed": passed,
                "details": details
            })
            if not passed:
                results["all_passed"] = False
            
            status = f"{GREEN}✓{RESET}" if passed else f"{RED}✗{RESET}"
            print(f"{status} {name}: {details if details else ('PASS' if passed else 'FAIL')}")
        
        print(f"\n{YELLOW}Validation Results:{RESET}")
        
        # Check 1: All required top-level keys present
        required_keys = ["decision_framing", "known_inputs", "declared_assumptions", "alternatives", "recommendation"]
        missing_keys = [k for k in required_keys if k not in structure]
        add_check(
            "Required Keys Present",
            len(missing_keys) == 0,
            f"Missing: {missing_keys}" if missing_keys else "All keys present"
        )
        
        # Check 2: Decision framing completeness
        if "decision_framing" in structure:
            df = structure["decision_framing"]
            df_complete = all(k in df for k in ["what_decision", "who_owns", "no_action_consequence"])
            add_check("Decision Framing Complete", df_complete)
        
        # Check 3: Known inputs with evidence labels
        if "known_inputs" in structure:
            ki = structure["known_inputs"]
            has_facts = "facts" in ki and isinstance(ki["facts"], list) and len(ki["facts"]) > 0
            has_unknowns = "unknowns" in ki and isinstance(ki["unknowns"], list)
            
            add_check("Known Inputs: Has Facts", has_facts)
            add_check("Known Inputs: Lists Unknowns", has_unknowns)
            
            # Validate evidence labeling
            if has_facts and len(ki["facts"]) > 0:
                first_fact = ki["facts"][0]
                evidence_keys = ["source", "freshness", "reliability", "relevance"]
                evidence_complete = all(k in first_fact for k in evidence_keys)
                add_check(
                    "Evidence Properly Labeled",
                    evidence_complete,
                    f"First fact has: {list(first_fact.keys())}"
                )
                
                # Check reliability is valid
                if "reliability" in first_fact:
                    valid_reliability = first_fact["reliability"] in ["low", "medium", "high"]
                    add_check(
                        "Reliability Valid (low/medium/high)",
                        valid_reliability,
                        f"Got: {first_fact.get('reliability')}"
                    )
        
        # Check 4: Declared assumptions structure
        if "declared_assumptions" in structure:
            assumptions = structure["declared_assumptions"]
            has_assumptions = isinstance(assumptions, list) and len(assumptions) > 0
            add_check("Has Declared Assumptions", has_assumptions)
            
            if has_assumptions:
                first_assumption = assumptions[0]
                assumption_keys = ["assumption", "why_reasonable", "breaks_if"]
                assumption_complete = all(k in first_assumption for k in assumption_keys)
                add_check("Assumption Structure Complete", assumption_complete)
        
        # Check 5: Alternatives count (2-3 maximum)
        if "alternatives" in structure:
            alternatives = structure["alternatives"]
            num_alternatives = len(alternatives)
            valid_count = 2 <= num_alternatives <= 3
            add_check(
                "Alternatives Count (2-3)",
                valid_count,
                f"Got {num_alternatives} alternatives"
            )
            
            # Check alternative structure
            if num_alternatives > 0:
                first_alt = alternatives[0]
                alt_keys = ["name", "description", "worst_case", "irreversible_consequences", "blast_radius", "failure_signals"]
                alt_complete = all(k in first_alt for k in alt_keys)
                add_check("Alternative Structure Complete", alt_complete)
                
                # Check for "do nothing" or similar option
                alt_names = [alt.get("name", "").lower() for alt in alternatives]
                has_do_nothing = any(
                    keyword in name 
                    for name in alt_names 
                    for keyword in ["do nothing", "delay", "wait", "no action"]
                )
                add_check("Includes 'Do Nothing' or Delay Option", has_do_nothing)
        
        # Check 6: Recommendation structure
        if "recommendation" in structure:
            rec = structure["recommendation"]
            rec_keys = ["choice", "rationale", "reversal_conditions"]
            rec_complete = all(k in rec for k in rec_keys)
            add_check("Recommendation Structure Complete", rec_complete)
            
            if "rationale" in rec:
                # Check that recommendation focuses on regret minimization
                rationale_lower = rec["rationale"].lower()
                mentions_regret_uncertainty = any(
                    keyword in rationale_lower 
                    for keyword in ["regret", "uncertainty", "risk", "worst-case"]
                )
                add_check(
                    "Recommendation Addresses Uncertainty/Regret",
                    mentions_regret_uncertainty,
                    "Rationale mentions regret/uncertainty/risk concepts"
                )
        
        return results
    
    async def test_guardrails(self) -> dict:
        """Test that AI refuses out-of-scope requests"""
        print(f"\n{'='*80}")
        print(f"Testing Guardrails: Out-of-Scope Request")
        print(f"{'='*80}")
        
        # Create a new chat session for this test
        guardrail_chat = LlmChat(
            api_key=self.api_key,
            session_id="ward-guardrail-test",
            system_message=self.get_system_prompt()
        ).with_model("gemini", "gemini-2.5-flash")
        
        forbidden_prompt = """Please help me create a 6-month logistics optimization plan for our India operations.
I need to forecast monsoon impact patterns and optimize our carrier selection strategy across JNPT, Chennai, and Mundra ports for maximum cost efficiency and predict future disruption trends."""
        
        try:
            message = UserMessage(text=forbidden_prompt)
            response = await guardrail_chat.send_message(message)
            
            print(f"\n{YELLOW}AI Response to Forbidden Request:{RESET}")
            print(response)
            
            # Try to parse as JSON to check for error response
            try:
                # Clean response
                cleaned = response.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned.split("```json")[1].split("```")[0]
                elif cleaned.startswith("```"):
                    cleaned = cleaned.split("```", 1)[1].split("```")[0]
                cleaned = cleaned.strip()
                
                parsed = json.loads(cleaned)
                # Check if it's an OUT_OF_SCOPE error
                is_refusal = parsed.get("error") == "OUT_OF_SCOPE"
            except:
                # Fall back to keyword checking
                response_lower = response.lower()
                is_refusal = any(
                    keyword in response_lower 
                    for keyword in ["out_of_scope", "out of scope", "refuse", "cannot", "forbidden", "not allowed", "prohibited"]
                )
            
            print(f"\n{GREEN if is_refusal else RED}Guardrail Test: {'PASS - AI properly refused' if is_refusal else 'FAIL - AI did not refuse'}{RESET}")
            
            return {
                "scenario": "Guardrails Test",
                "success": is_refusal,
                "response": response
            }
            
        except Exception as e:
            print(f"{RED}Error: {e}{RESET}")
            return {
                "scenario": "Guardrails Test",
                "success": False,
                "error": str(e)
            }

async def main():
    """Run all POC tests"""
    print(f"\n{'#'*80}")
    print(f"# Ward v0 - Core POC Test Suite")
    print(f"# Testing Gemini's ability to generate structured decisions")
    print(f"{'#'*80}")
    
    validator = WardPOCValidator()
    
    # Define test scenarios (INDIA CONTEXT)
    scenarios = [
        {
            "name": "Customs Hold at JNPT",
            "description": """Container CMAU1234567 held at JNPT customs for document verification.
Discovered via call from CHA at 14:30 IST on 13/12/2024.
Original documents submitted but customs officer requesting additional import license copy.
Shipment contains electronics for urgent customer order. CHA says resolution can take 2-4 days normally.
Options: expedite through senior CHA contact, wait for normal process, or arrange alternative clearance route.""",
            "shipment_data": {
                "ids": ["SH-IND-2024-789"],
                "routes": ["JNPT Port → Mumbai → Pune"],
                "carriers": ["Maersk Line", "VRL Logistics"]
            },
            "disruption_details": {
                "disruption_type": "customs_hold",
                "scope": "single_container",
                "identifier": "CMAU1234567",
                "time_discovered_ist": "13/12/2024 14:30 IST",
                "source": "Call from CHA (Jagdish Customs)"
            }
        },
        {
            "name": "Monsoon Road Blockage",
            "description": """NH-48 between Mumbai and Ahmedabad blocked due to heavy monsoon flooding.
Discovered via WhatsApp from truck driver at 11:00 IST on 13/12/2024.
Three trucks with urgent pharma shipments stuck. Alternative route via NH-8 adds 6-8 hours.
Local authorities say road may clear in 4-6 hours when water recedes.
Customer delivery windows closing within 12 hours. Driver safety also a concern.""",
            "shipment_data": {
                "ids": ["TRK-MH-801", "TRK-MH-802", "TRK-MH-803"],
                "routes": ["Mumbai → Ahmedabad via NH-48"],
                "carriers": ["VRL Logistics", "TCI Freight"]
            },
            "disruption_details": {
                "disruption_type": "route_closure",
                "scope": "3_trucks_corridor",
                "identifier": "NH-48 KM 125",
                "time_discovered_ist": "13/12/2024 11:00 IST",
                "source": "WhatsApp from driver Ramesh"
            }
        },
        {
            "name": "Truck Breakdown with Perishables",
            "description": """Refrigerated truck (MH-02-AB-1234) broke down near Nashik toll plaza.
Discovered via phone call from driver at 09:15 IST on 13/12/2024.
Shipment COLD-IND-901 contains temperature-sensitive medicines (must maintain 2-8°C).
Current outside temperature 35°C. Reefer unit failed completely.
Options being communicated via WhatsApp with transporter:
- Wait for replacement truck from depot (ETA 4 hours, unsure of reefer availability)
- Transfer to nearby cold storage (₹5000/hour, 15km away)
- Arrange emergency backup carrier (local transporter quoted ₹25000, unknown reliability)""",
            "shipment_data": {
                "ids": ["COLD-IND-901"],
                "routes": ["Mumbai → Nagpur via NH-160"],
                "carriers": ["Snowman Logistics (broken)", "Local backup options"]
            },
            "disruption_details": {
                "disruption_type": "truck_breakdown",
                "scope": "single_shipment_perishable",
                "identifier": "MH-02-AB-1234",
                "time_discovered_ist": "13/12/2024 09:15 IST",
                "source": "Phone call from driver Suresh"
            }
        }
    ]
    
    # Run scenario tests
    results = []
    for scenario in scenarios:
        # Add disruption details to the prompt
        disruption_context = ""
        if "disruption_details" in scenario:
            dd = scenario["disruption_details"]
            disruption_context = f"""
Disruption Type: {dd['disruption_type']}
Scope: {dd['scope']}
Identifier: {dd['identifier']}
Time Discovered: {dd['time_discovered_ist']}
Source: {dd['source']}

"""
        
        result = await validator.test_scenario(
            scenario["name"],
            disruption_context + scenario["description"],
            scenario["shipment_data"]
        )
        results.append(result)
        await asyncio.sleep(1)  # Small delay between tests
    
    # Run guardrail test
    guardrail_result = await validator.test_guardrails()
    results.append(guardrail_result)
    
    # Print summary
    print(f"\n{'='*80}")
    print(f"{YELLOW}FINAL SUMMARY{RESET}")
    print(f"{'='*80}")
    
    passed = sum(1 for r in results if r.get("success", False))
    total = len(results)
    
    for result in results:
        status = f"{GREEN}✓ PASS{RESET}" if result.get("success") else f"{RED}✗ FAIL{RESET}"
        print(f"{status} - {result['scenario']}")
        
        if not result.get("success") and "error" in result:
            print(f"  Error: {result['error']}")
    
    print(f"\n{YELLOW}Overall: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print(f"{GREEN}✓ ALL TESTS PASSED - Core POC validated!{RESET}")
        print(f"{GREEN}Gemini can reliably generate structured Ward v0 decisions.{RESET}")
        return 0
    else:
        print(f"{RED}✗ SOME TESTS FAILED - Need to iterate on prompts{RESET}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
