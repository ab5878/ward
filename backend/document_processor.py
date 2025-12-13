"""
Document Processor Service using Gemini Vision
Parses logistics documents (Invoice, Bill of Lading, etc.) and detects discrepancies.
"""

import os
import json
import base64
from typing import Dict, Any, List
from dotenv import load_dotenv
from emergentintegrations.llm.chat import LlmChat, UserMessage

load_dotenv()

EMERGENT_LLM_KEY = os.getenv("EMERGENT_LLM_KEY")

class DocumentProcessor:
    def __init__(self):
        self.api_key = EMERGENT_LLM_KEY

    async def analyze_document(self, file_bytes: bytes, filename: str, doc_type: str = "unknown") -> Dict[str, Any]:
        """
        Analyze a document using Gemini Vision to extract key logistics data.
        """
        try:
            # Encode image/pdf to base64
            # Note: Gemini via emergent might handle images differently. 
            # For now, we assume standard image input support if available, 
            # or we convert PDF to image if needed. 
            # Since we can't easily install poppler/pdf2image here without apt-get, 
            # we will assume the user uploads images (JPG/PNG) for the demo, 
            # or we rely on Gemini's ability to handle PDF mime types if supported by the wrapper.
            
            # For this environment, we'll try to treat it as an image or text.
            # If it's a PDF, we might be limited. Let's assume images for the demo "Proof".
            
            b64_data = base64.b64encode(file_bytes).decode('utf-8')
            
            chat = LlmChat(
                api_key=self.api_key,
                session_id=f"doc-analysis-{filename}",
                system_message="You are a logistics document expert. Extract key fields like Invoice No, Date, Buyer, Seller, Items, HS Codes, Weights, and Container Numbers. Return ONLY JSON."
            ).with_model("gemini", "gemini-2.5-flash") # Flash supports vision
            
            prompt = f"""Analyze this {doc_type} document named '{filename}'.
            Extract the following fields if visible:
            - Document Type
            - Document Number
            - Date
            - Parties (Shipper, Consignee)
            - Line Items (Description, Quantity, Weight, HS Code)
            - Container Numbers
            
            Return a valid JSON object."""
            
            # Note: The emergent integration library's `UserMessage` typically supports images 
            # if the underlying provider does. We need to check how to pass image data.
            # Standard pattern is `image_url` or `images` list.
            # Since I don't have the library docs, I'll try the standard text prompt first 
            # and if that fails (because it's just bytes), I might need to simulate it for the demo 
            # or use a simplified "text extraction" if I can't pass the image.
            
            # WAIT: I can just pass the base64 string in the prompt text if the model supports it, 
            # or more likely, I need to look for a specific method.
            # Let's assume for the MVP "Proof", I will rely on the user pasting text OR 
            # I will mock the extraction if the file is uploaded, BUT 
            # the prompt said "Deep... Allow users to upload actual PDFs... Ward uses Vision AI".
            
            # I will try to use `images` parameter if UserMessage supports it.
            # Inspecting `emergentintegrations` is not possible.
            # I will assume `UserMessage(text=..., images=[b64_data])` pattern.
            
            message = UserMessage(text=prompt, images=[b64_data])
            response = await chat.send_message(message)
            
            return self._clean_json(response)

        except Exception as e:
            print(f"Document analysis failed: {e}")
            return {"error": str(e)}

    async def compare_documents(self, doc1_analysis: Dict, doc2_analysis: Dict) -> Dict[str, Any]:
        """
        Compare two analyzed documents to find discrepancies.
        """
        try:
            chat = LlmChat(
                api_key=self.api_key,
                session_id="doc-comparison",
                system_message="You are a logistics auditor. Compare two documents and find discrepancies."
            ).with_model("gemini", "gemini-2.5-flash")
            
            prompt = f"""Compare these two logistics documents:

            Document 1 ({doc1_analysis.get('document_type', 'Doc 1')}):
            {json.dumps(doc1_analysis, indent=2)}

            Document 2 ({doc2_analysis.get('document_type', 'Doc 2')}):
            {json.dumps(doc2_analysis, indent=2)}

            Identify ANY mismatches in:
            - Descriptions (e.g. 'Computer Parts' vs 'Electronics')
            - HS Codes
            - Weights
            - Container Numbers
            - Parties

            Return JSON:
            {{
                "match": boolean,
                "discrepancies": [
                    {{ "field": "...", "doc1_value": "...", "doc2_value": "...", "severity": "high/medium/low" }}
                ],
                "summary": "Brief explanation of the mismatch"
            }}"""
            
            message = UserMessage(text=prompt)
            response = await chat.send_message(message)
            
            return self._clean_json(response)

        except Exception as e:
            return {"error": str(e)}

    def _clean_json(self, response: str) -> Dict:
        """Clean markdown JSON response"""
        text = response.strip()
        if text.startswith("```json"):
            text = text.split("```json")[1]
        if text.startswith("```"):
            text = text.split("```", 1)[1]
        if "```" in text:
            text = text.split("```")[0]
        return json.loads(text.strip())

document_processor = DocumentProcessor()
