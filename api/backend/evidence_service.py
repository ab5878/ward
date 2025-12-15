"""
Evidence Scoring Service
Calculates the 'Audit-Grade' quality of the evidence collected for a disruption.
"""

from datetime import datetime, timezone
from bson import ObjectId

class EvidenceService:
    def __init__(self, db):
        self.db = db

    async def calculate_and_update_score(self, case_id: str):
        """
        Calculate Evidence Completeness Score (0-100) and update the case.
        """
        case = await self.db.cases.find_one({"_id": case_id})
        if not case:
            return None

        # Fetch related data
        try:
            docs_cursor = await self.db.documents.find({"case_id": case_id})
            docs_list = await docs_cursor.to_list(length=100)
            docs_count = len(docs_list) if docs_list else 0
        except Exception as e:
            print(f"Warning: Failed to fetch documents: {e}")
            docs_count = 0
        
        try:
            timeline_cursor = await self.db.timeline_events.find({"case_id": case_id})
            timeline = await timeline_cursor.to_list(length=100)
            timeline = timeline if timeline else []
        except Exception as e:
            print(f"Warning: Failed to fetch timeline: {e}")
            timeline = []

        score = 0
        breakdown = []
        missing_actions = []

        # 1. Voice/Audio Report (+30)
        has_voice = case.get("voice_transcript") or any(e.get("source_type") == "voice" for e in timeline)
        if has_voice:
            score += 30
            breakdown.append("Voice report captured")
        else:
            missing_actions.append("Record driver/field voice report")

        # 2. Timestamped Transcript (+10)
        # We assume if voice exists, it's timestamped by our system
        if has_voice:
            score += 10
            breakdown.append("Transcript timestamped")
        else:
            missing_actions.append("Generate transcript")

        # 3. Speaker Attribution (+15)
        # Check if we have specific actors identified in timeline
        # Simple heuristic: explicit 'actor' field that isn't generic
        has_attribution = any(e.get("actor") and "@" not in e.get("actor") for e in timeline) # Crude check for names vs emails
        # Or check if structured_context has specific fields
        if case.get("disruption_details", {}).get("source"):
             has_attribution = True
             
        if has_attribution:
            score += 15
            breakdown.append("Source/Speaker attributed")
        else:
            missing_actions.append("Identify specific speaker/source")

        # 4. Supporting Document (+20)
        if docs_count > 0:
            score += 20
            breakdown.append(f"{docs_count} Documents secured")
        else:
            missing_actions.append("Upload Invoice, BL, or Notice")

        # 5. Counterparty Identified (+15)
        # Check if we have a 'stakeholder' or 'carrier' linked
        structured_context = case.get("structured_context") or {}
        if not isinstance(structured_context, dict):
            structured_context = {}
        has_counterparty = (
            structured_context.get("carrier_code") or 
            structured_context.get("vendor_id") or
            len(case.get("stakeholders", []) or []) > 0
        )
        if has_counterparty:
            score += 15
            breakdown.append("Counterparty identified")
        else:
            missing_actions.append("Link valid Counterparty (Carrier/CHA)")

        # 6. No RCA Contradictions (+10)
        # We check if RCA exists and confidence is high
        rca = case.get("rca")
        if rca and rca.get("confidence") == "high":
            score += 10
            breakdown.append("RCA consistent")
        elif rca:
            # RCA exists but low confidence
            missing_actions.append("Resolve RCA ambiguities")
        else:
            missing_actions.append("Perform Root Cause Analysis")

        # Cap at 100
        score = min(score, 100)

        # 7. Check for Evidence Readiness (70% Threshold)
        # If score >= 70 and not previously marked, timestamp it.
        update_dict = {}
        if score >= 70 and not case.get("evidence_ready_at"):
            update_dict["evidence_ready_at"] = datetime.now(timezone.utc)

        # Update DB
        evidence_data = {
            "score": score,
            "breakdown": breakdown,
            "missing_actions": missing_actions,
            "last_calculated": datetime.now(timezone.utc).isoformat()
        }
        
        update_dict["evidence_score"] = evidence_data

        try:
            await self.db.cases.update_one(
                {"_id": case_id},
                {"$set": update_dict}
            )
        except Exception as e:
            print(f"Warning: Failed to update evidence score in DB: {e}")
            # Still return the calculated score even if update fails

        return evidence_data
