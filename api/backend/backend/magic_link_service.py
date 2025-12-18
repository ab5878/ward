"""
Magic Link Service
Generates temporary, secure access links for drivers/vendors without accounts.
"""

from datetime import datetime, timedelta, timezone
import secrets

class MagicLinkService:
    def __init__(self, db):
        self.db = db

    async def create_magic_link(self, case_id: str, role: str = "guest", expires_in_hours: int = 24):
        """Generate a magic link token for a specific case"""
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now(timezone.utc) + timedelta(hours=expires_in_hours)
        
        link_doc = {
            "token": token,
            "case_id": case_id,
            "role": role,
            "expires_at": expires_at,
            "created_at": datetime.now(timezone.utc),
            "is_active": True
        }
        
        await self.db.magic_links.insert_one(link_doc)
        return {"token": token, "expires_at": expires_at, "url": f"/guest/case/{token}"}

    async def validate_magic_link(self, token: str):
        """Validate a token and return the context"""
        link = await self.db.magic_links.find_one({"token": token})
        
        if not link:
            return None
            
        if not link["is_active"]:
            return None
            
        # Ensure expires_at is timezone-aware for comparison
        expires_at = link["expires_at"]
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
            
        if datetime.now(timezone.utc) > expires_at:
            return None
            
        return link
