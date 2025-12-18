# Quick Deploy to Vercel

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **Vercel CLI**: Install with `npm i -g vercel`
3. **Backend URL**: You'll need your backend deployed separately (see below)

## Step 1: Deploy Backend (Choose One)

### Option A: Railway (Recommended - Easiest)

1. Go to [railway.app](https://railway.app) and sign up
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your Ward repository
4. Railway will auto-detect it's a Python app
5. Set Root Directory to `backend`
6. Add environment variables:
   ```
   MONGO_URL=your_mongodb_connection_string
   DB_NAME=ward_production
   JWT_SECRET=generate_a_random_secret_key
   CORS_ORIGINS=https://your-vercel-app.vercel.app
   EMERGENT_LLM_KEY=your_emergent_key
   SARVAM_API_KEY=your_sarvam_key
   ```
7. Railway will give you a URL like `https://ward-production.up.railway.app`
8. Copy this URL - you'll need it for the frontend

### Option B: Render

1. Go to [render.com](https://render.com) and sign up
2. Click "New" → "Web Service"
3. Connect your GitHub repo
4. Settings:
   - **Name**: `ward-backend`
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Add environment variables (same as Railway)
6. Deploy and copy the URL

## Step 2: Deploy Frontend to Vercel

### Using Vercel CLI (Recommended)

1. **Navigate to project root**:
   ```bash
   cd /Users/abhishekvyas/ward
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```
   - Follow the prompts
   - When asked about settings, accept defaults
   - **Important**: When asked about environment variables, you can skip for now

4. **Set Environment Variable**:
   ```bash
   vercel env add REACT_APP_BACKEND_URL
   ```
   - When prompted, enter your backend URL (e.g., `https://ward-production.up.railway.app`)
   - Select "Production", "Preview", and "Development"

5. **Deploy to Production**:
   ```bash
   vercel --prod
   ```

### Using Vercel Dashboard (Alternative)

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your GitHub repository
3. Configure:
   - **Framework Preset**: Other
   - **Root Directory**: `frontend`
   - **Build Command**: `yarn build`
   - **Output Directory**: `build`
4. Add Environment Variable:
   - `REACT_APP_BACKEND_URL` = `https://your-backend-url.railway.app`
5. Click "Deploy"

## Step 3: Verify Deployment

1. Visit your Vercel deployment URL
2. Open browser console (F12)
3. Check for any connection errors
4. Try registering a new user
5. Test creating a case

## Environment Variables Checklist

### Frontend (Vercel)
- ✅ `REACT_APP_BACKEND_URL` - Your backend API URL

### Backend (Railway/Render)
- ✅ `MONGO_URL` - MongoDB connection string
- ✅ `DB_NAME` - Database name
- ✅ `JWT_SECRET` - Random secret key (generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`)
- ✅ `CORS_ORIGINS` - Your Vercel frontend URL
- ✅ `EMERGENT_LLM_KEY` - Your Emergent API key
- ✅ `SARVAM_API_KEY` - Your Sarvam AI API key

## MongoDB Setup

1. Create free account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free cluster (M0)
3. Click "Connect" → "Connect your application"
4. Copy connection string
5. Replace `<password>` with your database password
6. Add your deployment IPs to Network Access (or use 0.0.0.0/0 for development)

## Troubleshooting

### "Cannot connect to backend"
- Check `REACT_APP_BACKEND_URL` is set correctly in Vercel
- Check backend is running (visit `/api/health` endpoint)
- Check CORS settings on backend include your Vercel URL

### "401 Unauthorized" errors
- Check JWT_SECRET is set on backend
- Try logging in again

### Build fails
- Check Node.js version (should be 18+)
- Check all dependencies are in `package.json`
- Check build logs in Vercel dashboard

## Next Steps

- Set up custom domain in Vercel
- Update CORS_ORIGINS to include your custom domain
- Set up monitoring and error tracking
- Configure CI/CD for automatic deployments

