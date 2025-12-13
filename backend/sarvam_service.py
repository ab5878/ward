"""Sarvam AI Service for Voice-First Disruption Capture"""

import os
import httpx
import asyncio
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_BASE_URL = "https://api.sarvam.ai"

class SarvamService:
    """Handles Sarvam AI Speech-to-Text and Text-to-Speech operations"""
    
    def __init__(self):
        self.api_key = SARVAM_API_KEY
        self.headers = {
            "api-subscription-key": self.api_key
        }
    
    async def speech_to_text(self, audio_file_path: str, language_code: Optional[str] = None) -> Dict[str, Any]:
        """
        Convert speech to text using Sarvam AI
        Supports 10+ Indian languages with auto-detection
        
        Args:
            audio_file_path: Path to audio file (MP3, WAV, AAC, FLAC)
            language_code: Optional language code (auto-detects if None)
        
        Returns:
            Dictionary with transcript and metadata
        """
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                with open(audio_file_path, 'rb') as audio_file:
                    files = {
                        'file': (os.path.basename(audio_file_path), audio_file, 'audio/wav')
                    }
                    
                    # Use Saarika model for transcription in original language
                    data = {
                        'model': 'saarika:v1'
                    }
                    
                    if language_code:
                        data['language_code'] = language_code
                    
                    response = await client.post(
                        f"{SARVAM_BASE_URL}/speech-to-text",
                        headers=self.headers,
                        files=files,
                        data=data
                    )
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    return {
                        "transcript": result.get("transcript", ""),
                        "language_code": result.get("language_code", "unknown"),
                        "duration": result.get("duration"),
                        "timestamps": result.get("timestamps", []),
                        "success": True
                    }
        
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": f"Sarvam API error: {e.response.status_code} - {e.response.text}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Speech-to-text failed: {str(e)}"
            }
    
    async def text_to_speech(self, text: str, language_code: str = "hi-IN", speaker: str = "anushka") -> bytes:
        """
        Convert text to speech using Sarvam AI Bulbul v2
        Supports 11 Indian languages with natural voices
        
        Args:
            text: Text to convert (up to 1500 characters)
            language_code: Language code (e.g., hi-IN, en-IN, ta-IN)
            speaker: Voice name (anushka, vidya, manisha, arya, etc.)
        
        Returns:
            Audio bytes in WAV format
        """
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                payload = {
                    "inputs": [text],
                    "target_language_code": language_code,
                    "speaker": speaker,
                    "model": "bulbul:v1",
                    "enable_preprocessing": True  # Better handling of numbers, dates, currencies
                }
                
                response = await client.post(
                    f"{SARVAM_BASE_URL}/text-to-speech",
                    headers={
                        **self.headers,
                        "Content-Type": "application/json"
                    },
                    json=payload
                )
                
                response.raise_for_status()
                
                # Sarvam returns base64 encoded audio
                result = response.json()
                import base64
                audio_base64 = result.get("audios", [""])[0]
                audio_bytes = base64.b64decode(audio_base64)
                
                return audio_bytes
        
        except Exception as e:
            print(f"Text-to-speech error: {e}")
            return b""  # Return empty bytes on error
    
    async def translate_and_transcribe(self, audio_file_path: str) -> Dict[str, Any]:
        """
        Transcribe and translate to English using Sarvam AI
        Uses Saaras model for English translation
        
        Args:
            audio_file_path: Path to audio file
        
        Returns:
            Dictionary with English translation and original language
        """
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                with open(audio_file_path, 'rb') as audio_file:
                    files = {
                        'file': (os.path.basename(audio_file_path), audio_file, 'audio/wav')
                    }
                    
                    data = {
                        'model': 'saaras:v1'  # Translation model
                    }
                    
                    response = await client.post(
                        f"{SARVAM_BASE_URL}/speech-to-text-translate",
                        headers=self.headers,
                        files=files,
                        data=data
                    )
                    
                    response.raise_for_status()
                    result = response.json()
                    
                    return {
                        "transcript": result.get("transcript", ""),  # English translation
                        "language_code": result.get("language_code", "unknown"),
                        "duration": result.get("duration"),
                        "success": True
                    }
        
        except Exception as e:
            return {
                "success": False,
                "error": f"Translation failed: {str(e)}"
            }

# Singleton instance
sarvam_service = SarvamService()
