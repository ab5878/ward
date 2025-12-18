# Ward Operator API Documentation
**For Transport Operators - Plug & Play Integration**

---

## 🔑 Authentication

All operator endpoints require JWT authentication (except driver endpoints).

```bash
# Get token
POST /api/auth/login
{
  "email": "operator@company.com",
  "password": "password"
}

# Use token
Authorization: Bearer {token}
```

---

## 📋 Operator Endpoints

### 1. Create Operator Account
```http
POST /api/operators/create
Authorization: Bearer {token}
Content-Type: application/json

{
  "company_name": "ABC Transporters Pvt Ltd",
  "email": "ops@abctrans.com",
  "phone": "+91-98765-43210",
  "fleet_size": 50,
  "account_type": "pilot"
}
```

**Response:**
```json
{
  "operator_id": "uuid",
  "status": "created"
}
```

---

### 2. Add Fleet Vehicle
```http
POST /api/operators/fleet/add
Authorization: Bearer {token}
Content-Type: application/json

{
  "vehicle_number": "MH-12-AB-1234",
  "vehicle_type": "truck",
  "driver_name": "Ramesh Kumar",
  "driver_phone": "+91-98765-43211",
  "route": "JNPT-Delhi"
}
```

**Response:**
```json
{
  "vehicle_id": "uuid",
  "status": "added"
}
```

---

### 3. Bulk Upload Fleet (CSV)
```http
POST /api/operators/fleet/bulk-upload
Authorization: Bearer {token}
Content-Type: multipart/form-data

file: vehicles.csv
```

**CSV Format:**
```csv
vehicle_number,driver_name,driver_phone,route,vehicle_type
MH-12-AB-1234,Ramesh Kumar,+91-98765-43211,JNPT-Delhi,truck
MH-12-AB-1235,Suresh Singh,+91-98765-43212,Mundra-Mumbai,truck
```

**Response:**
```json
{
  "success": 2,
  "failed": 0,
  "errors": []
}
```

---

### 4. Get Fleet
```http
GET /api/operators/fleet
Authorization: Bearer {token}
```

**Response:**
```json
[
  {
    "_id": "uuid",
    "vehicle_number": "MH-12-AB-1234",
    "driver_name": "Ramesh Kumar",
    "driver_phone": "+91-98765-43211",
    "route": "JNPT-Delhi",
    "status": "active"
  }
]
```

---

### 5. Get Operator Dashboard
```http
GET /api/operators/dashboard?days=7
Authorization: Bearer {token}
```

**Response:**
```json
{
  "fleet_size": 50,
  "total_cases": 25,
  "active_cases": 8,
  "total_financial_impact": 125000,
  "evidence_ready_cases": 15,
  "evidence_readiness_rate": 60.0,
  "cases_by_route": {
    "JNPT-Delhi": 10,
    "Mundra-Mumbai": 8,
    "Chennai-Bangalore": 7
  },
  "period_days": 7
}
```

---

### 6. Generate Driver Links
```http
POST /api/operators/drivers/generate-links?method=magic_link
Authorization: Bearer {token}
```

**Response:**
```json
{
  "method": "magic_link",
  "links": [
    {
      "vehicle_number": "MH-12-AB-1234",
      "driver_name": "Ramesh Kumar",
      "link": "https://ward-logic.vercel.app/driver/abc123..."
    }
  ]
}
```

**QR Code Method:**
```http
POST /api/operators/drivers/generate-links?method=qr_code
```

**Response:**
```json
{
  "method": "qr_code",
  "links": [
    {
      "vehicle_number": "MH-12-AB-1234",
      "driver_name": "Ramesh Kumar",
      "qr_url": "https://api.qrserver.com/v1/create-qr-code/...",
      "link": "https://ward-logic.vercel.app/driver/abc123..."
    }
  ]
}
```

---

## 🚗 Driver Endpoints (No Auth Required)

### 1. Verify Magic Link
```http
GET /api/driver/verify/{token}
```

**Response:**
```json
{
  "vehicle_number": "MH-12-AB-1234",
  "driver_name": "Ramesh Kumar",
  "route": "JNPT-Delhi",
  "valid": true
}
```

---

### 2. Report Disruption
```http
POST /api/driver/report
Content-Type: application/json

{
  "token": "magic-link-token",
  "audio_base64": "base64-encoded-audio",
  "audio_format": "webm",
  "language_code": "hi-IN"
}
```

**Response:**
```json
{
  "case_id": "uuid",
  "status": "created",
  "message": "Disruption reported successfully",
  "vehicle_number": "MH-12-AB-1234"
}
```

---

## 🔗 Webhook Integration

### Configure Webhook
```http
POST /api/developer/webhooks
Authorization: Bearer {token}
Content-Type: application/json

{
  "url": "https://your-system.com/ward-webhook",
  "events": [
    "disruption_reported",
    "evidence_ready",
    "dispute_generated"
  ]
}
```

### Webhook Payload
```json
{
  "event": "disruption_reported",
  "operator_id": "uuid",
  "movement_id": "uuid",
  "case_id": "uuid",
  "timestamp": "2024-12-15T10:30:00Z",
  "data": {
    "description": "Container stuck at gate",
    "vehicle_number": "MH-12-AB-1234",
    "financial_impact": 5000,
    "evidence_score": 45
  }
}
```

---

## 📊 Integration Examples

### Python
```python
import requests

BASE_URL = "https://ward-logic.vercel.app/api"
TOKEN = "your-jwt-token"

# Add vehicle
response = requests.post(
    f"{BASE_URL}/operators/fleet/add",
    headers={"Authorization": f"Bearer {TOKEN}"},
    json={
        "vehicle_number": "MH-12-AB-1234",
        "driver_name": "Ramesh Kumar",
        "driver_phone": "+91-98765-43211",
        "route": "JNPT-Delhi"
    }
)
```

### JavaScript
```javascript
const BASE_URL = 'https://ward-logic.vercel.app/api';
const token = 'your-jwt-token';

// Get dashboard
const response = await fetch(`${BASE_URL}/operators/dashboard?days=7`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
});
const dashboard = await response.json();
```

---

## 🎯 Use Cases

### 1. Onboard New Operator
1. Create operator account
2. Add fleet (bulk CSV upload)
3. Generate driver links
4. Share links via WhatsApp/SMS

### 2. Daily Operations
1. Drivers report via magic link
2. Operator sees cases on dashboard
3. Evidence auto-collected
4. Generate dispute packets when needed

### 3. Integration with TMS
1. Sync movements via API
2. Receive webhook notifications
3. Update TMS with case status
4. Export dispute packets

---

## 📚 Full API Reference

See: `WARD_MASTER_PRODUCT_DOC.md` for complete API v0 specification.

---

**Last Updated:** December 2024

