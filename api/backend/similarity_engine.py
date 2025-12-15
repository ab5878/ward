"""
Similarity Search Engine
Uses embedding-based search to find similar historical cases.
"""

import os
from typing import List, Dict, Any
from llm_client import LlmChat, UserMessage
from dotenv import load_dotenv

load_dotenv()

EMERGENT_LLM_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("EMERGENT_LLM_KEY")

class SimilarityEngine:
    def __init__(self, db):
        self.db = db
        self.api_key = EMERGENT_LLM_KEY

    async def find_similar_cases(self, current_case: Dict, limit: int = 3) -> List[Dict[str, Any]]:
        """
        Find historically similar cases using text similarity.
        """
        # Note: In a production system, we would use vector embeddings (Pinecone/Milvus).
        # For this PoC environment without vector DBs, we will use a hybrid approach:
        # 1. Filter by Disruption Type (hard filter)
        # 2. Use LLM to rank relevance of candidate cases based on description
        
        disruption_type = current_case.get("disruption_details", {}).get("disruption_type")
        if not disruption_type:
            return []
            
        # 1. Fetch candidates (same type, resolved)
        # Get current case ID - handle both _id and id
        current_case_id = current_case.get("_id") or current_case.get("id")
        if not current_case_id:
            return []
        
        # PostgreSQL doesn't support nested field queries like "disruption_details.disruption_type"
        # We'll fetch all resolved cases and filter in Python
        cursor = await self.db.cases.find({"status": "RESOLVED"}, sort=[("created_at", -1)], limit=100)
        all_resolved = await cursor.to_list(length=100)
        
        # Filter by disruption type and exclude current case
        candidates = [
            c for c in all_resolved 
            if c.get("disruption_details", {}).get("disruption_type") == disruption_type
            and (c.get("_id") or c.get("id")) != current_case_id
        ][:20]  # Limit to 20
        
        if not candidates:
            return []
            
        # 2. AI Ranking
        # Construct a prompt with the current case and candidates
        candidates_text = ""
        for i, c in enumerate(candidates):
            candidates_text += f"CASE_{i}: {c.get('description')} | Resolution: {c.get('rca', {}).get('root_cause', 'Unknown')}\n"
            
        chat = LlmChat(
            api_key=self.api_key,
            session_id=f"similarity-{current_case_id}",
            system_message="You are a logistics expert. Rank historical cases by similarity to the current issue."
        ).with_model("gemini", "gemini-2.5-flash")
        
        prompt = f"""Current Issue: {current_case.get('description')}
        
        Historical Candidates:
        {candidates_text}
        
        Return the indices (CASE_0, CASE_1...) of the top {limit} most relevant cases.
        Format: Just the indices separated by commas, e.g., "CASE_2, CASE_0".
        If none are relevant, return "NONE"."""
        
        message = UserMessage(text=prompt)
        response = await chat.send_message(message)
        
        # Parse response
        response_text = response.strip()
        if "NONE" in response_text:
            return []
            
        # Extract indices
        similar_cases = []
        for i, candidate in enumerate(candidates):
            if f"CASE_{i}" in response_text:
                candidate_id = candidate.get("_id") or candidate.get("id")
                similar_cases.append({
                    "case_id": str(candidate_id),
                    "description": candidate.get("description"),
                    "resolution": candidate.get("rca", {}).get("root_cause"),
                    "resolution_time": "24h", # Placeholder, calculate real diff if needed
                    "similarity_score": "High" # Mock score
                })
                
        return similar_cases[:limit]
