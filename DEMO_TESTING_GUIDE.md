# Demo Testing Guide

**Date:** December 2024  
**Status:** ✅ Demo Data Creation Working

---

## ✅ What's Working

- ✅ Database connection to Supabase
- ✅ Server startup
- ✅ Demo data creation script
- ✅ Indian logistics scenarios created

---

## 🧪 Test the Full Stack

### 1. Start Server (Terminal 1)

```bash
cd /Users/abhishekvyas/ward
./start_server.sh
```

Server will be available at: `http://localhost:8001`

### 2. Start Frontend (Terminal 2) - Optional

```bash
cd /Users/abhishekvyas/ward/frontend
yarn start
```

Frontend will be available at: `http://localhost:3000`

### 3. Run Demo Data (Terminal 3)

```bash
cd /Users/abhishekvyas/ward
./run_demo.sh
```

---

## 📊 Test API Endpoints

### Health Check
```bash
curl http://localhost:8001/api/health
```

### Register User
```bash
curl -X POST http://localhost:8001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Test123!"}'
```

### Login
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "Test123!"}'
```

### List Cases (requires auth token)
```bash
TOKEN="your-jwt-token-here"
curl http://localhost:8001/api/cases \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🎯 Test New Features

### 1. Evidence Scoring

**Create a case, then add events:**
```bash
# Create case
curl -X POST http://localhost:8001/api/cases \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Container stuck at port gate",
    "disruption_details": {"disruption_type": "customs_hold"},
    "shipment_identifiers": {"ids": ["CON123"]}
  }'

# Add timeline event (evidence score auto-calculates)
curl -X POST http://localhost:8001/api/cases/{case_id}/timeline \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Driver called: stuck at gate 4",
    "source_type": "voice",
    "reliability": "high"
  }'

# Check evidence score
curl http://localhost:8001/api/cases/{case_id}/evidence \
  -H "Authorization: Bearer $TOKEN"
```

### 2. Responsibility Attribution

```bash
# Analyze responsibility
curl -X POST http://localhost:8001/api/cases/{case_id}/responsibility/analyze \
  -H "Authorization: Bearer $TOKEN"

# Get responsibility
curl http://localhost:8001/api/cases/{case_id}/responsibility \
  -H "Authorization: Bearer $TOKEN"
```

### 3. API v0 Endpoints

**Create Facility:**
```bash
curl -X POST http://localhost:8001/api/v0/facilities \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "JNPT Terminal 4",
    "type": "port",
    "code": "JNPT"
  }'
```

**Create Movement:**
```bash
curl -X POST http://localhost:8001/api/v0/movements \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "container_id": "MSKU987654",
    "truck_id": "MH-12-AB-1234",
    "lane": "JNPT-Delhi"
  }'
```

**Create Event (with GPS):**
```bash
curl -X POST http://localhost:8001/api/v0/events \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "movement_id": "{movement_id}",
    "event_type": "incident",
    "incident_type": "stuck_at_port_gate",
    "device_id": "android-abc123",
    "location": {
      "latitude": 18.9519,
      "longitude": 72.9619,
      "accuracy_meters": 15.5,
      "source": "gps"
    },
    "content": {
      "text": "Container stuck at JNPT gate 4"
    },
    "reliability": "high"
  }'
```

---

## 📋 Test Checklist

### Core Features
- [ ] User registration
- [ ] User login
- [ ] Create case
- [ ] Add timeline event
- [ ] Upload document
- [ ] Evidence score calculation
- [ ] Responsibility attribution

### API v0 Features
- [ ] Create facility
- [ ] Create party
- [ ] Create movement
- [ ] Create event (with GPS)
- [ ] Upload attachment
- [ ] Create dispute packet
- [ ] Export dispute packet

### Frontend Features
- [ ] Landing page loads
- [ ] Registration flow
- [ ] Login flow
- [ ] Dashboard displays cases
- [ ] Case detail page
- [ ] Evidence score display
- [ ] Responsibility card display

---

## 🐛 Troubleshooting

### Server not starting
- Check if port 8001 is already in use
- Verify database connection
- Check `.env` file has correct `SUPABASE_DB_URL`

### Demo script fails
- Make sure server is running first
- Check server logs for errors
- Verify authentication is working

### Database errors
- Run: `python3 backend/test_db_connection.py`
- Verify migrations are run
- Check Supabase project is active

---

**Last Updated:** December 2024

