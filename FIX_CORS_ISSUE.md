# Fix CORS Issue

## Problem
The frontend and backend are on different Vercel deployment URLs:
- Frontend: `https://ward-mew7zg07c-abhishek-vyas-projects.vercel.app`
- Backend: `https://ward-juvkr86yz-abhishek-vyas-projects.vercel.app`

This causes CORS errors because they're different origins.

## Solution

Since we're deploying full-stack on Vercel, both frontend and backend should be on the **same domain**. The `vercel.json` already configures `/api/*` routes to go to the serverless function.

### Step 1: Remove REACT_APP_BACKEND_URL Environment Variable

The frontend code is already configured to use relative URLs (`/api`) when `REACT_APP_BACKEND_URL` is not set. But if it's set in Vercel, it's overriding this.

**Remove it from Vercel Dashboard:**
1. Go to: https://vercel.com/abhishek-vyas-projects/ward/settings/environment-variables
2. Find `REACT_APP_BACKEND_URL`
3. Click "..." → "Delete"
4. Confirm deletion

### Step 2: Update CORS Settings

The backend CORS is set to allow all origins (`*`), which should work. But let's make sure it includes your frontend domain.

**Option A: Keep CORS as `*` (easiest)**
- Already configured in `backend/server.py`
- Should work for all origins

**Option B: Set specific CORS origins**
1. Go to Vercel Dashboard → Environment Variables
2. Add/Update `CORS_ORIGINS`:
   - Value: `https://ward-mew7zg07c-abhishek-vyas-projects.vercel.app,https://ward.vercel.app`
   - (Add your production domain when you have one)

### Step 3: Redeploy

After removing `REACT_APP_BACKEND_URL`:

```bash
cd /Users/abhishekvyas/ward
vercel --prod
```

### Step 4: Verify

After redeployment, both frontend and backend should be on the same domain:
- Frontend: `https://ward-[hash]-abhishek-vyas-projects.vercel.app`
- Backend API: `https://ward-[hash]-abhishek-vyas-projects.vercel.app/api/*`

The frontend will use relative URLs (`/api`) which will work on the same domain.

## Why This Works

1. **Same Domain**: Frontend and backend are on the same Vercel deployment
2. **Relative URLs**: Frontend uses `/api` instead of absolute URLs
3. **Vercel Routing**: `vercel.json` routes `/api/*` to the serverless function
4. **No CORS**: Same origin = no CORS issues

## Chrome Extension Errors (Ignore These)

The errors about `chrome-extension://pejdijmoenmkgeppbflobdenhhabjlaj/` are from a browser extension (likely Cursor or an AI assistant). These are harmless and can be ignored - they don't affect your app.

