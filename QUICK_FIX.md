# 🚨 Quick Fix for Login/Registration

## The Problem
Vercel **Deployment Protection** is blocking your API endpoints. This is why login/registration fails.

## ✅ Solution (2 Steps)

### Step 1: Disable Deployment Protection

**Option A: Via Vercel Dashboard (Easiest)**
1. Go to: https://vercel.com/abhishek-vyas-projects/ward/settings/deployment-protection
2. Click **"Disable"** or **"Remove Protection"**
3. Save changes

**Option B: Via Vercel CLI**
```bash
vercel project settings --disable-deployment-protection
```

### Step 2: Redeploy

```bash
cd /Users/abhishekvyas/ward
vercel --prod
```

## ✅ What I Fixed

1. **Frontend API URL**: Now uses relative URLs (`/api`) in production instead of `localhost`
2. **Backend initialization**: Database connection properly initializes in serverless functions

## 🧪 Test It

After disabling protection and redeploying:

1. **Test API health**:
   ```bash
   curl https://ward-juvkr86yz-abhishek-vyas-projects.vercel.app/api/health
   ```
   Should return: `{"status":"ok"}`

2. **Test registration**:
   - Go to your deployed site
   - Try registering a new user
   - Should work now!

## 📋 Verify Environment Variables

Make sure these are set in Vercel Dashboard → Settings → Environment Variables:

- ✅ `SUPABASE_DB_URL` - Your Supabase connection string
- ✅ `JWT_SECRET` - Any random string (e.g., `ward-secret-2024`)
- ✅ `CORS_ORIGINS` - Can be `*` or your frontend URL
- ✅ `OPENAI_API_KEY` - Your OpenAI key
- ✅ `SARVAM_API_KEY` - Your Sarvam key

## 🐛 Still Not Working?

1. **Check Vercel Function Logs**:
   - Dashboard → Deployments → Latest → Functions tab
   - Look for errors

2. **Check Browser Console** (F12):
   - Look for network errors
   - Check if API calls are being made

3. **Verify Database**:
   - Go to Supabase Dashboard
   - Check if `users` table exists
   - If not, run: `supabase/migrations/001_initial_schema.sql`
