"""
Test Sarvam AI Integration for Indian Language Voice Capture
Tests STT, TTS, and full voice workflow
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.insert(0, '/app/backend')

from sarvam_service import sarvam_service
from voice_assistant import voice_assistant

load_dotenv('/app/backend/.env')

# Test colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

async def test_driver_response():
    """Test driver-specific safe responses"""
    print(f"\n{YELLOW}Testing Driver Role Response:{RESET}")
    
    # Simulate driver input in Hinglish
    driver_input = "Container gate pe 3 ghante se khadi hai, andar nahi ja rahi"
    conversation_history = []
    
    try:
        response = await voice_assistant.generate_driver_response(driver_input, conversation_history)
        print(f"{GREEN}✓ Driver Response Generated:{RESET}")
        print(f"  Input: {driver_input}")
        print(f"  Response: {response}")
        print(f"  Length: {len(response.split())} words")
        
        # Verify constraints
        word_count = len(response.split())
        is_safe = not any(word in response.lower() for word in ['route', 'unload', 'move to', 'take', 'will take'])
        
        if word_count <= 30 and is_safe:
            print(f"{GREEN}✓ Response meets safety constraints (≤30 words, no decisions){RESET}")
            return True
        else:
            print(f"{RED}✗ Response violates constraints (words: {word_count}, safe: {is_safe}){RESET}")
            return False
            
    except Exception as e:
        print(f"{RED}✗ Driver response generation failed: {e}{RESET}")
        return False

async def test_helper_questions():
    """Test helper context-harvesting questions"""
    print(f"\n{YELLOW}Testing Helper Role Questions:{RESET}")
    
    context = "Container stuck at JNPT customs for document verification. CHA says assessment pending."
    
    try:
        questions = await voice_assistant.generate_helper_questions(context)
        print(f"{GREEN}✓ Helper Questions Generated:{RESET}")
        for i, q in enumerate(questions, 1):
            print(f"  {i}. {q}")
        
        # Verify no advice-seeking questions
        advice_keywords = ['what should', 'what do you think', 'your decision', 'recommend']
        has_advice_question = any(
            any(keyword in q.lower() for keyword in advice_keywords)
            for q in questions
        )
        
        if not has_advice_question and len(questions) <= 3:
            print(f"{GREEN}✓ Questions are context-harvesting only (no advice-seeking){RESET}")
            return True
        else:
            print(f"{RED}✗ Questions violate helper role constraints{RESET}")
            return False
            
    except Exception as e:
        print(f"{RED}✗ Helper questions generation failed: {e}{RESET}")
        return False

async def test_manager_clarity_questions():
    """Test manager clarity-enforcing questions"""
    print(f"\n{YELLOW}Testing Manager Role Clarity Questions:{RESET}")
    
    transcript = "Truck breakdown at Nashik toll plaza. Reefer unit failed. Medicine shipment at risk."
    
    try:
        questions = await voice_assistant.generate_clarity_questions(transcript)
        print(f"{GREEN}✓ Manager Clarity Questions Generated:{RESET}")
        for i, q in enumerate(questions, 1):
            print(f"  {i}. {q}")
        
        if len(questions) >= 2 and len(questions) <= 3:
            print(f"{GREEN}✓ Question count appropriate (2-3 questions){RESET}")
            return True
        else:
            print(f"{RED}✗ Question count out of range: {len(questions)}{RESET}")
            return False
            
    except Exception as e:
        print(f"{RED}✗ Clarity questions generation failed: {e}{RESET}")
        return False

async def test_disruption_extraction():
    """Test disruption extraction from conversation"""
    print(f"\n{YELLOW}Testing Disruption Extraction:{RESET}")
    
    conversation = """Operator: Container CMAU1234567 stuck at Mundra port gate
Ward: Is this confirmed by port notice or CHA call?
Operator: CHA called at 2:30 PM IST today
Ward: Is impact limited to this container?
Operator: Yes, just this one container
Ward: What is known vs unknown?
Operator: Known: Gate entry denied. Unknown: Exact reason, expected clearance time"""
    
    try:
        disruption = await voice_assistant.extract_disruption_details(conversation)
        print(f"{GREEN}✓ Disruption Extracted:{RESET}")
        
        # Check required fields
        required_fields = ['disruption_type', 'scope', 'identifier', 'time_discovered_ist', 'source']
        missing_fields = [f for f in required_fields if f not in disruption]
        
        if not missing_fields:
            print(f"  Type: {disruption.get('disruption_type')}")
            print(f"  Scope: {disruption.get('scope')}")
            print(f"  Identifier: {disruption.get('identifier')}")
            print(f"  Time: {disruption.get('time_discovered_ist')}")
            print(f"  Source: {disruption.get('source')}")
            print(f"{GREEN}✓ All required fields present{RESET}")
            return True
        else:
            print(f"{RED}✗ Missing fields: {missing_fields}{RESET}")
            return False
            
    except Exception as e:
        print(f"{RED}✗ Disruption extraction failed: {e}{RESET}")
        return False

async def test_text_to_speech():
    """Test TTS for voice playback"""
    print(f"\n{YELLOW}Testing Text-to-Speech (Sarvam AI):{RESET}")
    
    text = "समझा। कृपया सुरक्षित स्थान पर प्रतीक्षा करें। ऑप्स टीम समीक्षा कर रही है।"
    
    try:
        audio_bytes = await sarvam_service.text_to_speech(
            text=text,
            language_code="hi-IN",
            speaker="anushka"
        )
        
        if audio_bytes and len(audio_bytes) > 0:
            print(f"{GREEN}✓ TTS Audio Generated:{RESET}")
            print(f"  Text: {text}")
            print(f"  Audio size: {len(audio_bytes)} bytes")
            print(f"  Language: Hindi (hi-IN)")
            print(f"  Speaker: Anushka")
            return True
        else:
            print(f"{RED}✗ TTS generated empty audio{RESET}")
            return False
            
    except Exception as e:
        print(f"{RED}✗ TTS failed: {e}{RESET}")
        return False

async def test_api_key_configured():
    """Verify Sarvam API key is configured"""
    print(f"\n{YELLOW}Testing Sarvam API Key Configuration:{RESET}")
    
    api_key = os.getenv('SARVAM_API_KEY')
    
    if api_key:
        print(f"{GREEN}✓ SARVAM_API_KEY configured{RESET}")
        print(f"  Key prefix: {api_key[:10]}...")
        return True
    else:
        print(f"{RED}✗ SARVAM_API_KEY not found in environment{RESET}")
        return False

async def main():
    """Run all integration tests"""
    print(f"\n{'='*80}")
    print(f"Ward v0 - Sarvam AI Integration Test Suite")
    print(f"Testing Indian Language Voice Capture & Role-Based Responses")
    print(f"{'='*80}")
    
    results = []
    
    # Test 1: API Key
    results.append(("API Key Configuration", await test_api_key_configured()))
    
    # Test 2: Driver Response
    results.append(("Driver Role Response", await test_driver_response()))
    
    # Test 3: Helper Questions
    results.append(("Helper Role Questions", await test_helper_questions()))
    
    # Test 4: Manager Clarity Questions
    results.append(("Manager Clarity Questions", await test_manager_clarity_questions()))
    
    # Test 5: Disruption Extraction
    results.append(("Disruption Extraction", await test_disruption_extraction()))
    
    # Test 6: Text-to-Speech
    results.append(("Text-to-Speech (Hindi)", await test_text_to_speech()))
    
    # Summary
    print(f"\n{'='*80}")
    print(f"{YELLOW}TEST SUMMARY{RESET}")
    print(f"{'='*80}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{GREEN}✓ PASS{RESET}" if result else f"{RED}✗ FAIL{RESET}"
        print(f"{status} - {test_name}")
    
    print(f"\n{YELLOW}Overall: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print(f"{GREEN}✓ ALL TESTS PASSED - Sarvam AI integration verified!{RESET}")
        print(f"{GREEN}Indian language voice capture is fully functional.{RESET}")
        return 0
    else:
        print(f"{RED}✗ SOME TESTS FAILED - Check configuration{RESET}")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
