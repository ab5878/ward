"""
Dispute Bundle Service
Generates a ZIP file containing all evidence for a demurrage dispute.
"""

import io
import zipfile
import json
import yaml
from datetime import datetime

class DisputeBundleService:
    def __init__(self, db):
        self.db = db

    async def generate_bundle(self, case_id: str):
        """
        Gathers all case evidence and zips it.
        Returns: (zip_bytes, filename)
        """
        case = await self.db.cases.find_one({"_id": case_id})
        if not case:
            raise ValueError("Case not found")

        # Create in-memory zip
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zf:
            
            # 1. Structured Case Summary (YAML)
            summary = {
                "case_id": str(case["_id"]),
                "description": case.get("description"),
                "disruption_details": case.get("disruption_details"),
                "financial_impact": case.get("financial_impact"),
                "created_at": str(case.get("created_at")),
                "status": case.get("status")
            }
            zf.writestr("Case_Summary.yaml", yaml.dump(summary, default_flow_style=False))

            # 2. Responsibility Report
            resp = case.get("responsibility") or {}
            if not isinstance(resp, dict):
                resp = {}
            resp_text = f"""RESPONSIBILITY ATTRIBUTION REPORT
--------------------------------
Primary Responsible Party: {resp.get('primary_party', 'Unknown')}
Confidence: {resp.get('confidence', 'N/A')}
Reasoning: {resp.get('reasoning', 'N/A')}
Override Applied: {resp.get('is_override', False)}
"""
            zf.writestr("Responsibility_Attribution.txt", resp_text)

            # 3. Full Timeline & Transcript
            timeline_cursor = await self.db.timeline_events.find({"case_id": case_id}, sort=[("timestamp", 1)])
            timeline = await timeline_cursor.to_list(length=1000)
            
            transcript_text = "OFFICIAL TIMELINE & TRANSCRIPT LOG\n==================================\n\n"
            for event in timeline:
                timestamp = event.get("timestamp", "").isoformat() if hasattr(event.get("timestamp"), "isoformat") else str(event.get("timestamp"))
                transcript_text += f"[{timestamp}] {event.get('actor')} ({event.get('source_type')}): {event.get('content')}\n"
                
            zf.writestr("Timeline_and_Transcript.txt", transcript_text)

            # 4. Evidence Score Report
            score = case.get("evidence_score") or {}
            if not isinstance(score, dict):
                score = {}
            score_text = f"""EVIDENCE COMPLETENESS CERTIFICATE
---------------------------------
Score: {score.get('score', 0)}/100
Generated: {score.get('last_calculated', 'N/A')}

SECURED ITEMS:
{chr(10).join(['[x] ' + s for s in score.get('breakdown', [])]) if score.get('breakdown') else '[ ] No items secured yet'}

MISSING ITEMS:
{chr(10).join(['[ ] ' + s for s in score.get('missing_actions', [])]) if score.get('missing_actions') else '[x] All items secured'}
"""
            zf.writestr("Evidence_Score_Certificate.txt", score_text)

            # 5. Documents (Extracted Data)
            # Since we don't store raw binaries in this MVP, we verify extraction content
            docs_cursor = await self.db.documents.find({"case_id": case_id}, limit=100)
            docs = await docs_cursor.to_list(length=100)
            
            if docs:
                zf.writestr("Documents/README.txt", "This folder contains AI-extracted data from uploaded documents.")
                for doc in docs:
                    doc_content = f"""DOCUMENT ANALYSIS RECORD
--------------------------
Filename: {doc.get('filename')}
Type: {doc.get('doc_type')}
Uploaded By: {doc.get('uploaded_by')}
Uploaded At: {doc.get('uploaded_at')}

AI EXTRACTION:
{json.dumps(doc.get('analysis', {}), indent=2)}
"""
                    zf.writestr(f"Documents/{doc.get('filename')}_Analysis.txt", doc_content)

        zip_buffer.seek(0)
        timestamp = datetime.now().strftime("%Y%m%d")
        filename = f"Demurrage_Dispute_{case_id}_{timestamp}.zip"
        
        return zip_buffer, filename
