# Ward Deployment Guide

This guide covers deploying Ward to Vercel.

## Architecture Overview

- **Frontend**: React app deployed to Vercel
- **Backend**: FastAPI app (can be deployed to Vercel serverless OR separate service)

## Option 1: Frontend on Vercel + Backend on Separate Service (Recommended)

This is the recommended approach for production.

### Step 1: Deploy Backend Separately

Deploy your FastAPI backend to one of these services:

#### Option A: Railway (Easiest)
1. Go to [Railway.app](https://railway.app)
2. Create new project from GitHub repo
3. Select the `backend` directory
4. Set environment variables (see below)
5. Railway will auto-detect FastAPI and deploy

#### Option B: Render
1. Go to [Render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repo
4. Set:
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Set environment variables

#### Option C: Fly.io
```bash
cd backend
fly launch
# Follow prompts
fly deploy
```

### Step 2: Deploy Frontend to Vercel

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy from project root**:
   ```bash
   cd /Users/abhishekvyas/ward
   vercel
   ```

4. **Set Environment Variables in Vercel Dashboard**:
   - Go to your project settings → Environment Variables
   - Add: `REACT_APP_BACKEND_URL` = `https://your-backend-url.railway.app` (or your backend URL)

5. **Redeploy** after setting environment variables:
   ```bash
   vercel --prod
   ```

## Option 2: Full Stack on Vercel (Advanced)

For deploying both frontend and backend on Vercel:

### Prerequisites

1. Install mangum adapter:
   ```bash
   cd backend
   pip install mangum
   ```

2. Update `backend/requirements.txt` to include:
   ```
   mangum==0.18.0
   ```

### Deploy

1. The `api/` directory contains serverless function setup
2. Deploy to Vercel:
   ```bash
   vercel
   ```

3. Set all environment variables (see below)

## Environment Variables

### Frontend (Vercel)
- `REACT_APP_BACKEND_URL`: Your backend API URL (e.g., `https://ward-backend.railway.app`)

### Backend (Railway/Render/Fly.io or Vercel)
- `MONGO_URL`: MongoDB connection string
- `DB_NAME`: Database name (e.g., `ward_production`)
- `JWT_SECRET`: Secret key for JWT tokens (generate a strong random string)
- `CORS_ORIGINS`: Allowed CORS origins (comma-separated, e.g., `https://ward.vercel.app,https://ward.com`)
- `EMERGENT_LLM_KEY`: Your Emergent/Gemini API key
- `SARVAM_API_KEY`: Your Sarvam AI API key

### Generate JWT Secret
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## MongoDB Setup

1. Create a MongoDB Atlas account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster
3. Get connection string
4. Add your deployment IP to whitelist (or use 0.0.0.0/0 for development)
5. Set `MONGO_URL` environment variable

## Post-Deployment Checklist

- [ ] Backend is accessible and health check works (`/api/health`)
- [ ] Frontend can connect to backend (check browser console)
- [ ] Environment variables are set correctly
- [ ] CORS is configured properly
- [ ] MongoDB connection is working
- [ ] Test user registration/login
- [ ] Test voice case creation
- [ ] Test case creation and viewing

## Troubleshooting

### Frontend can't connect to backend
- Check `REACT_APP_BACKEND_URL` is set correctly
- Check CORS settings on backend
- Check backend is accessible (try `/api/health` endpoint)

### Backend errors
- Check MongoDB connection string
- Check all environment variables are set
- Check logs in your hosting service

### Build errors
- Make sure all dependencies are in `package.json` (frontend) or `requirements.txt` (backend)
- Check Node.js version (should be 18+)
- Check Python version (should be 3.11+)

## Quick Deploy Commands

```bash
# Deploy frontend to Vercel
vercel

# Deploy to production
vercel --prod

# View deployment logs
vercel logs

# List deployments
vercel ls
```

## Custom Domain

1. Go to Vercel project settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Update `CORS_ORIGINS` in backend to include your domain

