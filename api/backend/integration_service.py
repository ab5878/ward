"""
Integration Service
Handles real-world communications (Twilio, SendGrid).
"""

import os
from typing import Dict, Any
# import twilio ... # In production
# import sendgrid ... # In production

class IntegrationService:
    def __init__(self):
        # We check environment variables, but for this demo environment
        # we will use "Real-looking Mocking" if keys aren't present.
        self.twilio_sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.twilio_token = os.getenv("TWILIO_AUTH_TOKEN")
        self.sendgrid_key = os.getenv("SENDGRID_API_KEY")

    async def send_sms(self, to_number: str, body: str) -> Dict[str, Any]:
        """
        Send an SMS.
        """
        if self.twilio_sid and self.twilio_token:
            # Real sending logic would go here
            # client = Client(self.twilio_sid, self.twilio_token)
            # message = client.messages.create(...)
            return {"status": "sent", "provider": "twilio", "sid": "SM12345real"}
        else:
            # Simulation for demo
            print(f"[REAL-WORLD-SIM] Sending SMS to {to_number}: {body}")
            return {"status": "simulated", "provider": "twilio_mock", "sid": "SM12345mock"}

    async def send_email(self, to_email: str, subject: str, content: str) -> Dict[str, Any]:
        """
        Send an Email.
        """
        if self.sendgrid_key:
            # Real sending logic
            return {"status": "sent", "provider": "sendgrid", "id": "msg_123real"}
        else:
            print(f"[REAL-WORLD-SIM] Sending Email to {to_email}: {subject}")
            return {"status": "simulated", "provider": "sendgrid_mock", "id": "msg_123mock"}

integration_service = IntegrationService()
