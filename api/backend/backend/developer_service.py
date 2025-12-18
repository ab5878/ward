"""
Developer/Webhook Service
Manages API Keys and Webhooks.
"""

from datetime import datetime, timezone
import secrets

class DeveloperService:
    def __init__(self, db):
        self.db = db

    async def generate_api_key(self, user_id: str, name: str):
        """Generate a new API key for external integration"""
        key_prefix = "sk_ward_"
        key_secret = secrets.token_urlsafe(32)
        full_key = f"{key_prefix}{key_secret}"
        
        key_doc = {
            "user_id": user_id,
            "name": name,
            "key_hash": full_key, # In prod, hash this!
            "created_at": datetime.now(timezone.utc),
            "last_used_at": None,
            "is_active": True
        }
        
        await self.db.api_keys.insert_one(key_doc)
        return {"api_key": full_key, "name": name}

    async def register_webhook(self, user_id: str, url: str, events: list):
        """Register a webhook endpoint"""
        webhook = {
            "user_id": user_id,
            "url": url,
            "events": events,
            "secret": secrets.token_hex(16),
            "created_at": datetime.now(timezone.utc),
            "status": "active"
        }
        
        result = await self.db.webhooks.insert_one(webhook)
        webhook["_id"] = str(result.inserted_id)
        return webhook

    async def list_webhooks(self, user_id: str):
        cursor = self.db.webhooks.find({"user_id": user_id})
        return await cursor.to_list(length=100)

    async def list_api_keys(self, user_id: str):
        cursor = self.db.api_keys.find({"user_id": user_id})
        keys = await cursor.to_list(length=100)
        # Obfuscate keys for display
        for k in keys:
            k["key_hash"] = f"{k['key_hash'][:12]}..." 
            k["_id"] = str(k["_id"])
        return keys
