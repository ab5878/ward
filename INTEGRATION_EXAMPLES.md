# Ward Operator Integration Examples
**Real-world integration patterns for transport operators**

---

## 🔌 Integration Patterns

### Pattern 1: TMS Integration (Real-time Sync)

**Use Case:** Sync movements from TMS to Ward, get webhook notifications

```python
import requests
from datetime import datetime

WARD_API_URL = "https://ward-logic.vercel.app/api"
WARD_API_KEY = "your-api-key"

# 1. Create movement in Ward when shipment starts
def create_movement_in_ward(shipment_data):
    response = requests.post(
        f"{WARD_API_URL}/v0/movements",
        headers={"Authorization": f"Bearer {WARD_API_KEY}"},
        json={
            "external_id": shipment_data["shipment_id"],
            "container_id": shipment_data["container_number"],
            "truck_id": shipment_data["vehicle_number"],
            "bill_of_lading": shipment_data["bl_number"],
            "lane": f"{shipment_data['origin']}-{shipment_data['destination']}",
            "planned_start_date": shipment_data["pickup_date"],
            "planned_end_date": shipment_data["delivery_date"]
        }
    )
    return response.json()

# 2. Set up webhook to receive notifications
def setup_webhook():
    response = requests.post(
        f"{WARD_API_URL}/developer/webhooks",
        headers={"Authorization": f"Bearer {WARD_API_KEY}"},
        json={
            "url": "https://your-tms.com/ward-webhook",
            "events": [
                "disruption_reported",
                "evidence_ready",
                "dispute_generated"
            ]
        }
    )
    return response.json()

# 3. Handle webhook notifications
@app.route('/ward-webhook', methods=['POST'])
def handle_ward_webhook():
    data = request.json
    event = data.get("event")
    
    if event == "disruption_reported":
        # Update TMS with disruption
        update_shipment_status(data["data"]["case_id"], "DISRUPTED")
    elif event == "evidence_ready":
        # Notify operations team
        notify_operations_team(data["data"])
    elif event == "dispute_generated":
        # Download dispute packet
        download_dispute_packet(data["data"]["case_id"])
    
    return {"status": "ok"}
```

---

### Pattern 2: ERP Integration (Batch Sync)

**Use Case:** Daily sync of fleet and movements from ERP

```python
import requests
import csv
from datetime import datetime, timedelta

WARD_API_URL = "https://ward-logic.vercel.app/api"
WARD_API_KEY = "your-api-key"

# Daily fleet sync
def sync_fleet_from_erp():
    # Get fleet from ERP
    fleet = get_fleet_from_erp()
    
    # Bulk upload to Ward
    csv_data = []
    for vehicle in fleet:
        csv_data.append({
            "vehicle_number": vehicle["number"],
            "driver_name": vehicle["driver"]["name"],
            "driver_phone": vehicle["driver"]["phone"],
            "route": vehicle["route"],
            "vehicle_type": "truck"
        })
    
    # Upload CSV
    files = {'file': ('fleet.csv', generate_csv(csv_data))}
    response = requests.post(
        f"{WARD_API_URL}/operators/fleet/bulk-upload",
        headers={"Authorization": f"Bearer {WARD_API_KEY}"},
        files=files
    )
    return response.json()

# Daily movement sync
def sync_movements_from_erp():
    # Get movements from ERP
    movements = get_movements_from_erp(datetime.now() - timedelta(days=1))
    
    # Create movements in Ward
    for movement in movements:
        create_movement_in_ward(movement)
```

---

### Pattern 3: WhatsApp Business API Integration

**Use Case:** Send magic links via WhatsApp automatically

```python
from twilio.rest import Client

TWILIO_ACCOUNT_SID = "your-account-sid"
TWILIO_AUTH_TOKEN = "your-auth-token"
TWILIO_WHATSAPP_NUMBER = "whatsapp:+14155238886"

def send_magic_link_via_whatsapp(driver_phone, magic_link, vehicle_number):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    message = f"""
🚛 Ward Driver App

Vehicle: {vehicle_number}
Click to report disruptions: {magic_link}

No login required. Works on any smartphone.
    """
    
    client.messages.create(
        from_=TWILIO_WHATSAPP_NUMBER,
        body=message,
        to=f"whatsapp:+91{driver_phone.replace('+91', '').replace('-', '')}"
    )
```

---

### Pattern 4: SMS Gateway Integration

**Use Case:** Send SMS alerts for critical disruptions

```python
import requests

SMS_API_KEY = "your-sms-api-key"
SMS_API_URL = "https://api.sms-gateway.com/send"

def send_sms_alert(operator_phone, case_id, vehicle_number):
    message = f"URGENT: Disruption reported for {vehicle_number}. Case ID: {case_id}. Check Ward dashboard."
    
    response = requests.post(
        SMS_API_URL,
        json={
            "api_key": SMS_API_KEY,
            "to": operator_phone,
            "message": message
        }
    )
    return response.json()
```

---

### Pattern 5: Embedded Widget

**Use Case:** Embed Ward driver app in your existing app

```html
<!-- Embed Ward driver app in your app -->
<iframe 
    src="https://ward-logic.vercel.app/driver/{magic-link-token}"
    width="100%"
    height="600px"
    frameborder="0"
></iframe>
```

---

## 📊 Webhook Payload Examples

### Disruption Reported
```json
{
  "event": "disruption_reported",
  "operator_id": "uuid",
  "case_id": "uuid",
  "timestamp": "2024-12-15T10:30:00Z",
  "data": {
    "vehicle_number": "MH-12-AB-1234",
    "description": "Container stuck at gate",
    "financial_impact": 5000,
    "evidence_score": 45
  }
}
```

### Evidence Ready
```json
{
  "event": "evidence_ready",
  "operator_id": "uuid",
  "case_id": "uuid",
  "timestamp": "2024-12-15T11:00:00Z",
  "data": {
    "evidence_score": 75,
    "ready_for_dispute": true,
    "missing_items": []
  }
}
```

### Dispute Generated
```json
{
  "event": "dispute_generated",
  "operator_id": "uuid",
  "case_id": "uuid",
  "dispute_packet_id": "uuid",
  "timestamp": "2024-12-15T12:00:00Z",
  "data": {
    "download_url": "https://ward-logic.vercel.app/api/v0/dispute-packets/{id}/export",
    "file_size": 1024000
  }
}
```

---

## 🔐 Authentication

### API Key Authentication
```python
import requests

headers = {
    "Authorization": "Bearer your-api-key",
    "Content-Type": "application/json"
}

response = requests.get(
    "https://ward-logic.vercel.app/api/operators/dashboard",
    headers=headers
)
```

### JWT Token Authentication
```python
# 1. Login to get token
login_response = requests.post(
    "https://ward-logic.vercel.app/api/auth/login",
    json={
        "email": "operator@company.com",
        "password": "password"
    }
)
token = login_response.json()["access_token"]

# 2. Use token for API calls
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
```

---

## 🧪 Testing Integration

### Test Webhook Endpoint
```python
# Use ngrok to expose local endpoint
# ngrok http 8000

# Test webhook
import requests

test_payload = {
    "event": "disruption_reported",
    "data": {
        "case_id": "test-case-id",
        "vehicle_number": "TEST-123"
    }
}

response = requests.post(
    "https://your-ngrok-url.ngrok.io/ward-webhook",
    json=test_payload
)
```

---

## 📚 Full API Reference

See `OPERATOR_API_DOCS.md` for complete API documentation.

---

**Last Updated:** December 2024

