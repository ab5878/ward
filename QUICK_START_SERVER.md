# Quick Start Server Guide

**Date:** December 2024

---

## 🚀 Starting the Server

### Option 1: Using the Helper Script (Recommended)

```bash
cd /Users/abhishekvyas/ward
./start_server.sh
```

This will:
- Navigate to the backend directory
- Start the server on port 8001
- Enable auto-reload on code changes

### Option 2: Manual Start

```bash
cd /Users/abhishekvyas/ward/backend
python3 -m uvicorn server:app --port 8001 --host 0.0.0.0 --reload
```

**Important:** You must be in the `backend` directory for the import to work!

---

## ✅ Verify Server is Running

Once started, test the health endpoint:

```bash
curl http://localhost:8001/api/health
```

Expected response:
```json
{
  "status": "ok",
  "database": "connected",
  "timestamp": "..."
}
```

---

## 🧪 Run Demo Tests

### After Server is Running:

**Option 1: Using Helper Script**
```bash
./run_demo.sh
```

**Option 2: Manual**
```bash
python3 tests/create_demo_data.py
```

---

## 🔧 Troubleshooting

### Error: "Could not import module 'server'"

**Solution:** Make sure you're in the `backend` directory:
```bash
cd /Users/abhishekvyas/ward/backend
python3 -m uvicorn server:app --port 8001
```

### Error: "Connection refused"

**Solution:** Server is not running. Start it first:
```bash
./start_server.sh
```

### Error: "Port 8001 already in use"

**Solution:** Kill the existing process:
```bash
lsof -ti:8001 | xargs kill -9
```

Or use a different port:
```bash
python3 -m uvicorn server:app --port 8002
```

---

## 📋 Environment Variables

Make sure you have these set (in `.env` file or environment):

```bash
SUPABASE_DB_URL=postgresql://...
JWT_SECRET=your-secret-key
CORS_ORIGINS=http://localhost:3000
```

---

## 🎯 Quick Test Flow

1. **Start Server:**
   ```bash
   ./start_server.sh
   ```

2. **In another terminal, test health:**
   ```bash
   curl http://localhost:8001/api/health
   ```

3. **Run demo data:**
   ```bash
   ./run_demo.sh
   ```

---

**Last Updated:** December 2024

