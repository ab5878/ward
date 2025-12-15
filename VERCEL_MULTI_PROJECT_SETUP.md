# Vercel Multi-Project Setup Guide

You have **3 separate Vercel projects** for Ward:

1. **frontend** - React application
2. **api** - Backend API (Python/FastAPI serverless functions)
3. **ward-logic** - Root project (monorepo setup)

---

## Project 1: Frontend

**Location:** `frontend/` directory  
**Type:** React application  
**Configuration:** `frontend/vercel.json`

### Configuration

The `frontend/vercel.json` should be:
```json
{
  "buildCommand": "npm install --legacy-peer-deps && npm run build",
  "installCommand": "npm install --legacy-peer-deps",
  "outputDirectory": "build",
  "framework": null
}
```

### Environment Variables

Set in Vercel Dashboard → frontend project → Settings → Environment Variables:

```
REACT_APP_API_URL=https://api-xxxxx.vercel.app/api
```

Or if using ward-logic as monorepo:
```
REACT_APP_API_URL=https://ward-logic.vercel.app/api
```

### Deploy

```bash
cd frontend
vercel --prod
```

---

## Project 2: API

**Location:** `api/` directory  
**Type:** Python serverless functions  
**Configuration:** `api/vercel.json`

### Configuration

The `api/vercel.json` should be:
```json
{
  "functions": {
    "**/*.py": {
      "runtime": "python3.12"
    }
  }
}
```

### Requirements

Make sure `api/requirements.txt` exists with all dependencies:
- fastapi
- mangum
- asyncpg
- etc.

### Environment Variables

Set in Vercel Dashboard → api project → Settings → Environment Variables:

```
SUPABASE_DB_URL=postgresql://...
JWT_SECRET=...
CORS_ORIGINS=https://frontend-xxxxx.vercel.app,https://ward-logic.vercel.app
OPENAI_API_KEY=...
SARVAM_API_KEY=...
```

### Deploy

```bash
cd api
./prepare_deployment.sh  # Copies backend files
vercel --prod
```

---

## Project 3: ward-logic (Root/Monorepo)

**Location:** Root directory  
**Type:** Monorepo (frontend + backend)  
**Configuration:** `vercel.json` (root)

### Configuration

The root `vercel.json` should be:
```json
{
  "version": 2,
  "buildCommand": "cd frontend && npm install --legacy-peer-deps && npm run build",
  "outputDirectory": "frontend/build",
  "installCommand": "cd frontend && npm install --legacy-peer-deps",
  "framework": null,
  "functions": {
    "api/**/*.py": {
      "runtime": "python3.12"
    }
  },
  "rewrites": [
    {
      "source": "/api/(.*)",
      "destination": "/api/index.py"
    },
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

### Environment Variables

Set in Vercel Dashboard → ward-logic project → Settings → Environment Variables:

**For Frontend:**
```
REACT_APP_API_URL=https://ward-logic.vercel.app/api
```

**For Backend:**
```
SUPABASE_DB_URL=postgresql://...
JWT_SECRET=...
CORS_ORIGINS=https://ward-logic.vercel.app
OPENAI_API_KEY=...
SARVAM_API_KEY=...
```

### Deploy

```bash
# From root directory
cd api
./prepare_deployment.sh  # Copies backend files
cd ..
vercel --prod
```

---

## Recommended Setup

### Option A: Use ward-logic (Monorepo) - Recommended

**Pros:**
- Single deployment
- Frontend and backend on same domain
- Easier CORS configuration
- Single project to manage

**Setup:**
1. Use root `vercel.json` (already configured)
2. Deploy from root: `vercel --prod`
3. Frontend at: `https://ward-logic.vercel.app`
4. API at: `https://ward-logic.vercel.app/api`

### Option B: Separate Projects

**Pros:**
- Independent deployments
- Can scale separately
- Clear separation of concerns

**Setup:**
1. Deploy frontend separately: `cd frontend && vercel --prod`
2. Deploy API separately: `cd api && vercel --prod`
3. Set `REACT_APP_API_URL` in frontend to point to API project URL

---

## Current Issue Fix

The API project needs Python runtime configuration. Update `api/vercel.json`:

```json
{
  "functions": {
    "**/*.py": {
      "runtime": "python3.12"
    }
  }
}
```

This ensures Vercel installs `requirements.txt` for Python functions.

---

## Deployment Checklist

### For ward-logic (Monorepo):
- [ ] Root `vercel.json` has functions configuration
- [ ] `api/requirements.txt` exists with all dependencies
- [ ] `api/prepare_deployment.sh` copies backend files
- [ ] Environment variables set in ward-logic project
- [ ] Deploy from root: `vercel --prod`

### For separate projects:
- [ ] Frontend: `frontend/vercel.json` configured
- [ ] API: `api/vercel.json` has functions configuration
- [ ] API: `api/requirements.txt` exists
- [ ] Frontend: `REACT_APP_API_URL` points to API project
- [ ] API: `CORS_ORIGINS` includes frontend URL
- [ ] Deploy each separately

---

## Quick Fix for Current Error

The `ModuleNotFoundError: No module named 'fastapi'` means the API project isn't installing Python dependencies.

**Fix:**
1. Update `api/vercel.json` to include functions configuration
2. Ensure `api/requirements.txt` exists
3. Redeploy API project

