"""
LLM Client - Replaces emergentintegrations with OpenAI
"""

import os
from typing import Optional, List, Union
from openai import AsyncOpenAI
import json

class LlmChat:
    """Replacement for emergentintegrations LlmChat using OpenAI"""
    
    def __init__(self, api_key: str, session_id: str, system_message: str):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.session_id = session_id
        self.system_message = system_message
        self.model = "gpt-4o-mini"  # Default model
        self.messages = [{"role": "system", "content": system_message}]
    
    def with_model(self, provider: str, model: str):
        """Set the model (for compatibility with emergentintegrations API)"""
        # Map Gemini models to OpenAI equivalents
        if "gemini" in model.lower() or "flash" in model.lower():
            # Use vision-capable model if images are expected
            self.model = "gpt-4o"  # Vision-capable model
        elif "gpt" in model.lower():
            self.model = model
        else:
            self.model = "gpt-4o-mini"
        return self
    
    async def send_message(self, message) -> str:
        """Send a message and get response"""
        # Handle UserMessage objects with images
        if hasattr(message, 'text'):
            content = []
            # Add text
            if message.text:
                content.append({"type": "text", "text": message.text})
            # Add images if present
            if hasattr(message, 'images') and message.images:
                for img_base64 in message.images:
                    # Determine mime type (assume png/jpeg)
                    mime_type = "image/png"
                    if isinstance(img_base64, str):
                        # Check if it's a data URL
                        if img_base64.startswith("data:"):
                            mime_type = img_base64.split(";")[0].split(":")[1]
                            img_base64 = img_base64.split(",")[1]
                        content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{img_base64}"
                            }
                        })
            user_content = content if len(content) > 1 else (content[0]["text"] if content else "")
        elif isinstance(message, str):
            user_content = message
        else:
            user_content = str(message)
        
        # Add user message
        self.messages.append({"role": "user", "content": user_content})
        
        # Use vision model if images are present
        model = "gpt-4o" if (hasattr(message, 'images') and message.images) else self.model
        
        # Call OpenAI
        response = await self.client.chat.completions.create(
            model=model,
            messages=self.messages,
            temperature=0.7
        )
        
        # Extract response text
        response_text = response.choices[0].message.content
        
        # Add assistant response to history
        self.messages.append({"role": "assistant", "content": response_text})
        
        return response_text


class UserMessage:
    """Replacement for emergentintegrations UserMessage"""
    
    def __init__(self, text: str, images: Optional[List[str]] = None):
        self.text = text
        self.images = images or []

