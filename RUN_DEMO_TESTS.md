# Running Demo Tests - Quick Guide

**Date:** December 2024

---

## 🧪 Available Test Scripts

### 1. API v0 Structure Tests ✅
**File:** `backend/test_api_v0_structure.py`

**What it tests:**
- All 18 API v0 endpoints are defined
- Pydantic models can be instantiated
- Database adapter methods exist
- DB compatibility layer works

**Run:**
```bash
cd /Users/abhishekvyas/ward/backend
python3 test_api_v0_structure.py
```

**Status:** ✅ All tests passing

---

### 2. Evidence Scoring & Responsibility Tests ✅
**What it tests:**
- EvidenceService can be imported
- ResponsibilityAgent can be imported
- API endpoints are registered

**Run:**
```bash
cd /Users/abhishekvyas/ward
python3 -c "import sys; sys.path.insert(0, 'backend'); from evidence_service import EvidenceService; from responsibility_agent import ResponsibilityAgent; print('✅ All services available')"
```

**Status:** ✅ All services available

---

### 3. Demo Data Creation
**File:** `tests/create_demo_data.py`

**What it does:**
- Creates demo users (driver, manager, warehouse)
- Creates realistic Indian logistics cases
- Adds timeline events
- Tests full workflow

**Run (requires server running):**
```bash
# Start server first
cd /Users/abhishekvyas/ward/backend
python3 -m uvicorn server:app --port 8001

# In another terminal
cd /Users/abhishekvyas/ward
python3 tests/create_demo_data.py
```

**Note:** Requires server to be running on `http://localhost:8001`

---

### 4. Indian Voice Workflow Demo
**File:** `tests/demo_indian_voice_workflow.py`

**What it does:**
- Simulates Hindi/Hinglish voice input
- Tests voice assistant responses
- Tests clarity questions
- Tests decision generation

**Run:**
```bash
cd /Users/abhishekvyas/ward
python3 tests/demo_indian_voice_workflow.py
```

**Note:** Requires `OPENAI_API_KEY` or `EMERGENT_LLM_KEY` in environment

---

### 5. Registration Test
**File:** `backend/test_registration.py`

**What it tests:**
- Database connection
- Users table exists
- Registration endpoint works

**Run:**
```bash
cd /Users/abhishekvyas/ward/backend
python3 test_registration.py
```

---

## 🚀 Quick Test Run

### Test All Structure (No Server Required):
```bash
cd /Users/abhishekvyas/ward/backend
python3 test_api_v0_structure.py
```

### Test Services Import:
```bash
cd /Users/abhishekvyas/ward
python3 -c "import sys; sys.path.insert(0, 'backend'); from evidence_service import EvidenceService; from responsibility_agent import ResponsibilityAgent; print('✅ All services available')"
```

### Test API Endpoints Registered:
```bash
cd /Users/abhishekvyas/ward
python3 -c "import sys; sys.path.insert(0, 'backend'); from server import app; routes = [(r.path, list(r.methods)) for r in app.routes if hasattr(r, 'path') and ('evidence' in r.path or 'responsibility' in r.path)]; print(f'✅ Found {len(routes)} evidence/responsibility endpoints')"
```

---

## 📊 Test Results Summary

### ✅ Passing Tests:
- [x] API v0 Structure Tests (18/18 endpoints)
- [x] Pydantic Models (6/6 models)
- [x] Database Adapter Methods (16/16 methods)
- [x] Evidence Service Import
- [x] Responsibility Agent Import
- [x] Evidence Score Endpoints (2/2)
- [x] Responsibility Endpoints (2/2)

### ⚠️ Requires Server:
- [ ] Demo Data Creation (needs server on port 8001)
- [ ] HTTP API Tests (needs deployed server)
- [ ] Voice Workflow Demo (needs API keys)

---

## 🎯 Next Steps

1. **Start Local Server:**
   ```bash
   cd /Users/abhishekvyas/ward/backend
   python3 -m uvicorn server:app --port 8001
   ```

2. **Run Demo Data Creation:**
   ```bash
   cd /Users/abhishekvyas/ward
   python3 tests/create_demo_data.py
   ```

3. **Test Evidence Score:**
   - Create a case
   - Add timeline event → score auto-calculates
   - Upload document → score auto-recalculates
   - Check: `GET /api/cases/{case_id}/evidence`

4. **Test Responsibility Attribution:**
   - Create a case with timeline events
   - Call: `POST /api/cases/{case_id}/responsibility/analyze`
   - Check: `GET /api/cases/{case_id}/responsibility`

---

**Last Updated:** December 2024

