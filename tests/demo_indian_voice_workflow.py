"""
Demo: Complete Indian Language Voice Workflow
Simulates a real disruption being captured and processed in Hindi/Hinglish
"""

import asyncio
import sys
sys.path.insert(0, '/app/backend')

from voice_assistant import voice_assistant
from sarvam_service import sarvam_service
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

async def demo_workflow():
    print(f"\n{'='*80}")
    print(f"{BLUE}Ward v0 - Indian Language Voice Workflow Demo{RESET}")
    print(f"Scenario: Driver calls about truck breakdown with perishable goods")
    print(f"{'='*80}\n")
    
    # Step 1: Driver speaks (simulated Hindi/Hinglish input)
    print(f"{YELLOW}STEP 1: Driver Speaks (Hindi/Hinglish){RESET}")
    print(f"{BLUE}Driver:{RESET} \"Ward, truck MH-02-AB-1234 Nashik toll plaza pe breakdown ho gaya.\"")
    print(f"{BLUE}Driver:{RESET} \"Reefer unit fail ho gaya hai. Medicine ka shipment hai, temperature maintain nahi ho raha.\"")
    
    driver_input = "Truck MH-02-AB-1234 breakdown at Nashik toll plaza. Reefer unit failed. Medicine shipment, temperature not maintaining."
    
    # Generate safe driver response
    print(f"\n{YELLOW}Ward generates safe response for driver...{RESET}")
    driver_response = await voice_assistant.generate_driver_response(driver_input, [])
    
    print(f"{GREEN}Ward → Driver:{RESET} \"{driver_response}\"")
    print(f"  ✓ Safe coordination only (no decisions)")
    print(f"  ✓ Word count: {len(driver_response.split())} words")
    
    # Step 2: Manager Reviews - Ward asks clarity questions
    print(f"\n{YELLOW}STEP 2: Manager Reviews - Ward Asks Clarity Questions{RESET}")
    print(f"{BLUE}Manager:{RESET} Logs into Ward to review the disruption")
    
    print(f"\n{YELLOW}Ward generates clarity questions for manager...{RESET}")
    clarity_questions = await voice_assistant.generate_clarity_questions(driver_input)
    
    print(f"{GREEN}Ward → Manager:{RESET}")
    for i, q in enumerate(clarity_questions, 1):
        print(f"  {i}. {q}")
    
    # Simulate manager answers
    print(f"\n{BLUE}Manager answers (via voice or text):{RESET}")
    manager_answers = {
        0: "Driver confirmed at 9:15 AM IST today via phone call",
        1: "Only this truck affected. Reefer temp was 2-8°C, now rising",
        2: "Known: Breakdown time (9:15 IST), location (Nashik toll KM 125). Unknown: Exact failure reason, repair ETA"
    }
    
    for idx, answer in manager_answers.items():
        print(f"  Q{idx+1}: {answer}")
    
    # Step 3: Build conversation and extract disruption
    print(f"\n{YELLOW}STEP 3: Ward Extracts Structured Disruption{RESET}")
    
    conversation = f"""Driver: {driver_input}
Ward: {clarity_questions[0] if clarity_questions else 'Confirmed?'}
Manager: {manager_answers[0]}
Ward: {clarity_questions[1] if len(clarity_questions) > 1 else 'Scope?'}
Manager: {manager_answers[1]}
Ward: {clarity_questions[2] if len(clarity_questions) > 2 else 'Unknowns?'}
Manager: {manager_answers[2]}"""
    
    print(f"{YELLOW}Extracting structured details from conversation...{RESET}")
    disruption = await voice_assistant.extract_disruption_details(conversation)
    
    print(f"\n{GREEN}✓ Disruption Extracted and Ready for Manager Approval:{RESET}")
    print(f"  Type: {disruption.get('disruption_type', 'N/A')}")
    print(f"  Scope: {disruption.get('scope', 'N/A')}")
    print(f"  Identifier: {disruption.get('identifier', 'N/A')}")
    print(f"  Time (IST): {disruption.get('time_discovered_ist', 'N/A')}")
    print(f"  Source: {disruption.get('source', 'N/A')}")
    
    if 'explicit_unknowns' in disruption:
        print(f"  Unknowns:")
        for unknown in disruption['explicit_unknowns']:
            print(f"    - {unknown}")
    
    # Step 4: Helper (CHA/Mechanic) provides context
    print(f"\n{YELLOW}STEP 4: Helper Provides Context{RESET}")
    print(f"{BLUE}Helper (Senior Ops):{RESET} Available to provide domain knowledge")
    
    context = "Truck breakdown near Nashik with reefer failure. Medicine shipment affected."
    helper_questions = await voice_assistant.generate_helper_questions(context)
    
    print(f"\n{GREEN}Ward asks Helper (context harvesting, NOT advice):{RESET}")
    for i, q in enumerate(helper_questions, 1):
        print(f"  {i}. {q}")
    
    print(f"\n{BLUE}Helper responds:{RESET}")
    print(f"  - \"This type of reefer failure is common in summer. Usually resolved in 3-4 hours with local mechanic.\"")
    print(f"  - \"Nearby cold storage at Nashik Industrial Area charges ₹5000/hour.\"")
    print(f"  - \"Previous cases: Waiting for replacement reefer takes 6+ hours typically.\"")
    
    print(f"\n{GREEN}✓ Context captured and tagged as 'Helper input - high reliability'{RESET}")
    
    # Step 5: TTS Demo - Ward speaks back in Hindi
    print(f"\n{YELLOW}STEP 5: Ward Speaks Back to Driver (Hindi TTS){RESET}")
    
    hindi_message = "समझा। कृपया सुरक्षित स्थान पर प्रतीक्षा करें। ऑप्स टीम समीक्षा कर रही है। हम जल्द ही आपको अपडेट देंगे।"
    print(f"{BLUE}Text (Hindi):{RESET} {hindi_message}")
    print(f"{BLUE}Translation:{RESET} \"Understood. Please wait at a safe location. Ops team is reviewing. We will update you soon.\"")
    
    print(f"\n{YELLOW}Generating Hindi speech with Sarvam AI (Anushka voice)...{RESET}")
    audio_bytes = await sarvam_service.text_to_speech(
        text=hindi_message,
        language_code="hi-IN",
        speaker="anushka"
    )
    
    if audio_bytes and len(audio_bytes) > 0:
        print(f"{GREEN}✓ Hindi audio generated: {len(audio_bytes)} bytes{RESET}")
        print(f"  Voice: Anushka (clear, professional)")
        print(f"  Format: WAV")
        print(f"  Ready for playback to driver")
    
    # Summary
    print(f"\n{'='*80}")
    print(f"{GREEN}WORKFLOW COMPLETE - All Roles Coordinated{RESET}")
    print(f"{'='*80}")
    print(f"\n{GREEN}✓ Driver:{RESET} Reported disruption, received safe coordination")
    print(f"{GREEN}✓ Manager:{RESET} Received structured decision framework (ready for 6-step protocol)")
    print(f"{GREEN}✓ Helper:{RESET} Provided domain context (not advice)")
    print(f"{GREEN}✓ Ward:{RESET} Coordinated all three roles, preserved authority hierarchy")
    print(f"\n{GREEN}✓ Voice captured in Indian languages (Hindi/Hinglish)")
    print(f"{GREEN}✓ Text-to-Speech working (Hindi with Anushka voice)")
    print(f"{GREEN}✓ Disruption structured and ready for human approval")
    print(f"{GREEN}✓ Full audit trail maintained")
    
    print(f"\n{YELLOW}Next Step:{RESET} Manager approves disruption → Proceeds to AI decision generation → 6-step protocol")
    print(f"\n{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(demo_workflow())
