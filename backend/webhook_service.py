"""
Webhook Service
Handles webhook triggers for operator integrations
"""

import aiohttp
import json
import hmac
import hashlib
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

class WebhookService:
    def __init__(self, db):
        self.db = db
    
    async def trigger_webhook(self, operator_id: str, event: str, data: Dict[str, Any]):
        """
        Trigger webhook for operator
        """
        try:
            # Get active webhooks for operator
            webhooks = await self.get_operator_webhooks(operator_id, event)
            
            if not webhooks:
                return
            
            for webhook in webhooks:
                await self.send_webhook(webhook, event, data)
        except Exception as e:
            print(f"Error triggering webhook: {e}")
    
    async def get_operator_webhooks(self, operator_id: str, event: str) -> List[Dict[str, Any]]:
        """
        Get active webhooks for operator that listen to this event
        """
        try:
            # Query webhooks table
            # Note: This requires webhooks_find method in db_adapter
            # For now, return empty list
            return []
        except Exception as e:
            print(f"Error getting webhooks: {e}")
            return []
    
    async def send_webhook(self, webhook: Dict[str, Any], event: str, data: Dict[str, Any]):
        """
        Send webhook payload to URL
        """
        url = webhook.get("url")
        secret = webhook.get("secret")
        
        if not url:
            return
        
        payload = {
            "event": event,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": data
        }
        
        # Create signature if secret provided
        headers = {"Content-Type": "application/json"}
        if secret:
            signature = self.create_signature(json.dumps(payload), secret)
            headers["X-Ward-Signature"] = signature
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        # Update last_triggered_at
                        await self.update_webhook_status(webhook["id"], success=True)
                    else:
                        # Increment failure count
                        await self.update_webhook_status(webhook["id"], success=False)
        except Exception as e:
            print(f"Error sending webhook to {url}: {e}")
            await self.update_webhook_status(webhook["id"], success=False)
    
    def create_signature(self, payload: str, secret: str) -> str:
        """
        Create HMAC signature for webhook payload
        """
        return hmac.new(
            secret.encode('utf-8'),
            payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
    
    async def update_webhook_status(self, webhook_id: str, success: bool):
        """
        Update webhook status (last_triggered_at, failure_count)
        """
        try:
            # Update webhook record
            # Note: This requires webhooks_update_one method in db_adapter
            pass
        except Exception as e:
            print(f"Error updating webhook status: {e}")

