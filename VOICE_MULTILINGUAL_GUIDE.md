# Ward v0 - Multilingual Voice Interface Guide

## Overview
Ward's voice interface allows operators to report disruptions by speaking naturally in their preferred Indian language. The system uses Sarvam AI for speech recognition and synthesis across 11 Indian languages.

## Supported Languages

### Full List (11 Languages)
1. 🇮🇳 **Hindi (हिन्दी)** - `hi-IN` [Default]
2. 🇮🇳 **English (Indian)** - `en-IN`
3. 🇮🇳 **Tamil (தமிழ்)** - `ta-IN`
4. 🇮🇳 **Telugu (తెలుగు)** - `te-IN`
5. 🇮🇳 **Kannada (ಕನ್ನಡ)** - `kn-IN`
6. 🇮🇳 **Malayalam (മലയാളം)** - `ml-IN`
7. 🇮🇳 **Marathi (मराठी)** - `mr-IN`
8. 🇮🇳 **Gujarati (ગુજરાતી)** - `gu-IN`
9. 🇮🇳 **Punjabi (ਪੰਜਾਬੀ)** - `pa-IN`
10. 🇮🇳 **Bengali (বাংলা)** - `bn-IN`
11. 🇮🇳 **Odia (ଓଡ଼ିଆ)** - `od-IN`

## How It Works

### 1. Language Selection
- User selects their preferred language from dropdown
- Language is stored and used for:
  - Speech-to-Text (STT) transcription
  - Text-to-Speech (TTS) responses
  - AI-generated clarity questions

### 2. Voice Flow (5 Steps)

#### Step 1: SPEAK
- User clicks "Start Speaking" button
- Browser requests microphone permission
- User describes the disruption in their chosen language
- Example (Hindi): "Ward, container ABCD Mumbai port mein ruka hai. CHA ne kaha customs hold hai."

#### Step 2: CLARIFY
- Ward transcribes the speech
- Gemini AI generates 3-4 clarity questions based on the input
- Ward asks questions **in the same language** via TTS
- User answers each question
- Example questions:
  - "Container number kya hai?"
  - "Exact location kahan hai?"
  - "Problem kab start hua?"

#### Step 3: LOCK
- Ward extracts structured disruption details from the full conversation
- Shows structured data for review:
  - Disruption type
  - Scope
  - Location identifier
  - Time discovered
  - Source

#### Step 4: GUIDE (Future)
- AI decision support based on structured data
- Currently: User approves or edits

#### Step 5: DONE
- Case created with:
  - Full voice transcript
  - Timeline entry with "voice" source type
  - Status: REPORTED
  - Ready for ownership assignment

### 3. Language Detection
- System detects the actual language spoken (may differ from selection)
- Uses detected language for TTS responses
- Ensures continuity in the user's natural language

## Technical Implementation

### Frontend (`/app/frontend/src/pages/VoiceCase.js`)
```javascript
// Language selection state
const [selectedLanguage, setSelectedLanguage] = useState('hi-IN');
const [detectedLanguage, setDetectedLanguage] = useState('');

// STT with language code
const transcribeResponse = await api.post('/voice/transcribe', {
  audio_base64: audioBase64,
  audio_format: 'wav',
  language_code: selectedLanguage  // User's choice
});

// TTS with detected or selected language
const ttsResponse = await api.post('/voice/text-to-speech', {
  response_text: text,
  language_code: detectedLanguage || selectedLanguage,
  context: 'clarity'
});
```

### Backend (`/app/backend/server.py`)
```python
# TTS endpoint accepts language_code
class VoiceResponse(BaseModel):
    response_text: str
    language_code: Optional[str] = "hi-IN"  # Default to Hindi
    context: str = "clarity"

@app.post("/api/voice/text-to-speech")
async def synthesize_speech(voice_response: VoiceResponse, ...):
    language_code = voice_response.language_code or "hi-IN"
    audio_bytes = await sarvam_service.text_to_speech(
        text=text,
        language_code=language_code,
        speaker="anushka"
    )
```

### AI Integration (`/app/backend/voice_assistant.py`)
- Uses Google Gemini for clarity questions
- Gemini automatically responds in the same language as the input
- No explicit language translation needed

## Microphone Permission Handling

### Browser Permission Flow
1. User clicks "Start Speaking"
2. Browser shows permission prompt: "Allow microphone access?"
3. User must click "Allow"

### Permission Denied Error
If user denies or blocks microphone:
```
Microphone access denied. Please:
1. Click the 🔒 lock icon in your browser address bar
2. Allow microphone access for this site
3. Refresh the page and try again
```

### Browser Compatibility
- ✅ Chrome (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Edge
- ❌ Internet Explorer (not supported)

### Common Issues & Fixes

#### Issue 1: "No speech detected"
**Cause**: Audio too short or silent
**Fix**: Speak clearly for at least 2-3 seconds

#### Issue 2: "Microphone not found"
**Cause**: No microphone connected
**Fix**: Connect microphone and refresh

#### Issue 3: "Transcript is required"
**Cause**: Empty transcription from STT
**Fix**: 
- Speak louder
- Reduce background noise
- Check microphone is not muted

## India-First Features

### 1. Logistics Vocabulary
System understands Indian logistics terms:
- CHA (Customs House Agent)
- Port gate
- Customs hold
- Assessment pending
- DO (Delivery Order)
- IGM (Import General Manifest)

### 2. Code-Mixed Speech
Supports natural code-mixing (e.g., Hindi-English):
- "Container ABCD Mumbai port mein stuck hai"
- "CHA ne bola customs clearance pending hai"

### 3. IST Timezone
All timestamps stored and displayed in IST (Indian Standard Time)

### 4. Regional Context
AI understands:
- Indian port names (JNPT, Mundra, Chennai, Cochin)
- Indian cities and routes
- Local transportation terms

## Testing Multilingual Voice

### Test Script (Hindi Example)
```bash
# 1. Select Hindi from dropdown
# 2. Click "Start Speaking"
# 3. Grant microphone permission
# 4. Say: "Ward, container MSKU Mumbai mein ruka hai. CHA ne bola customs problem hai."
# 5. Ward will ask: "Container number kya hai?"
# 6. Answer: "MSKU1234567"
# 7. Ward will ask more questions in Hindi
# 8. Approve the final structured data
```

### Test Script (Tamil Example)
```bash
# 1. Select Tamil from dropdown
# 2. Click "Start Speaking"
# 3. Say: "Ward, container Chennai port-il irukku. Customs hold-la irukku."
# 4. Ward will ask questions in Tamil
# 5. Complete the flow
```

## Architecture Benefits

### 1. Zero Training Friction
- No need to learn English
- Speak naturally in mother tongue
- Reduces adoption barrier for field operators

### 2. Fluid Indian Ops Reality
- Drivers at ports speak regional languages
- CHAs communicate in local language
- Mixed Hindi-English is natural

### 3. Accurate Context Capture
- Better understanding when speaking native language
- Less misinterpretation
- Richer detail in disruption reports

## Future Enhancements (Phase 2)

### Voice Hotline
- Toll-free number for disruption reporting
- Call from any location
- No app/login required
- Transcription + case creation via phone

### WhatsApp Voice Notes
- Send voice note to Ward's WhatsApp
- Automatic transcription
- Case created and manager notified

### Offline Voice (PWA)
- Record voice offline
- Upload when network available
- Sync to Ward

## API Reference

### POST `/api/voice/transcribe`
**Request:**
```json
{
  "audio_base64": "...",
  "audio_format": "wav",
  "language_code": "hi-IN"
}
```
**Response:**
```json
{
  "transcript": "Container ABCD Mumbai mein stuck hai",
  "language_code": "hi-IN"
}
```

### POST `/api/voice/text-to-speech`
**Request:**
```json
{
  "response_text": "Container number kya hai?",
  "language_code": "hi-IN",
  "context": "clarity"
}
```
**Response:**
```json
{
  "audio_base64": "...",
  "format": "wav",
  "text": "Container number kya hai?"
}
```

### POST `/api/voice/clarity-questions`
**Request:**
```json
{
  "transcript": "Container Mumbai mein stuck hai"
}
```
**Response:**
```json
{
  "questions": [
    "Container number kya hai?",
    "Exact location kahan hai?",
    "Problem kab shuru hua?"
  ],
  "role": "manager",
  "count": 3
}
```

## Conclusion

Ward's multilingual voice interface removes the language barrier in Indian logistics operations. By supporting 11 Indian languages with intelligent AI that responds in the user's chosen language, Ward ensures that critical disruption information is captured accurately, regardless of the operator's language preference.

**Key Principle**: If the operator speaks Tamil, Ward speaks Tamil. If they speak Hindi, Ward speaks Hindi. The system adapts to the user, not the other way around.
