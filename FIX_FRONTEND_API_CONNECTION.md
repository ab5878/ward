# Fix Frontend → API Connection

## 🔍 Problem

The frontend is getting a **405 (Method Not Allowed)** error when trying to POST to `/api/auth/login`.

**Root Cause:**
- Frontend is deployed as a **separate project**: `frontend-5s7sl9joj-abhishek-vyas-projects.vercel.app`
- API is deployed as a **separate project**: `api-dbx3kihob-abhishek-vyas-projects.vercel.app`
- When frontend calls `/api/auth/login`, it's making a request to its own domain (frontend), not the API domain
- The frontend project doesn't have the API, so it returns 405

## ✅ Solution: Set Environment Variable

You need to tell the frontend where the API is located.

### Step 1: Go to Vercel Dashboard

1. Visit: https://vercel.com/dashboard
2. Select the **`frontend`** project (not `api` or `ward-logic`)

### Step 2: Add Environment Variable

1. Go to **Settings** → **Environment Variables**
2. Click **Add New**
3. Add the following:

   **Key:**
   ```
   REACT_APP_BACKEND_URL
   ```

   **Value:**
   ```
   https://api-dbx3kihob-abhishek-vyas-projects.vercel.app
   ```

   **Environments:**
   - ✅ Production
   - ✅ Preview
   - ✅ Development

4. Click **Save**

### Step 3: Redeploy Frontend

After adding the environment variable, you need to redeploy:

1. Go to **Deployments** tab
2. Find the latest deployment
3. Click **"..."** (three dots)
4. Click **Redeploy**
5. Select **"Use existing Build Cache"** (optional)
6. Click **Redeploy**

### Step 4: Wait and Test

1. Wait 1-2 minutes for deployment to complete
2. Visit: https://frontend-5s7sl9joj-abhishek-vyas-projects.vercel.app
3. Try to register/login
4. Check browser console - should no longer see 405 error

## 🔍 How It Works

The frontend code in `frontend/src/services/api.js` checks for `REACT_APP_BACKEND_URL`:

```javascript
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 
  (process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8001');
```

- **Without `REACT_APP_BACKEND_URL`**: Uses relative URLs (`/api`) → goes to frontend domain ❌
- **With `REACT_APP_BACKEND_URL`**: Uses absolute URL → goes to API domain ✅

## 📋 Alternative: Use Monorepo Project

If you want to use the `ward-logic` monorepo project instead:

1. Deploy the `ward-logic` project (root directory)
2. It has rewrites configured in `vercel.json` to route `/api/*` to the API
3. Frontend and API will be on the same domain
4. No need for `REACT_APP_BACKEND_URL`

## 🧪 Verify Fix

After redeploying, check:

1. **Browser Console (F12):**
   - Should see successful API requests
   - No more 405 errors
   - Requests should go to `api-dbx3kihob-abhishek-vyas-projects.vercel.app`

2. **Network Tab:**
   - POST requests to `/api/auth/login` should show:
     - **Status:** 200 (or 401 if wrong credentials, but not 405)
     - **Request URL:** Should include the API domain

3. **Application Flow:**
   - Registration should work
   - Login should work
   - Dashboard should load after login

## ⚠️ Important Notes

- **Environment variables are only available at build time** for React apps
- You **must redeploy** after adding/changing environment variables
- The variable name must be exactly `REACT_APP_BACKEND_URL` (React requires `REACT_APP_` prefix)
- Make sure to set it for **all environments** (Production, Preview, Development)

## 🎯 Quick Checklist

- [ ] Go to Vercel Dashboard → `frontend` project
- [ ] Settings → Environment Variables
- [ ] Add `REACT_APP_BACKEND_URL` = `https://api-dbx3kihob-abhishek-vyas-projects.vercel.app`
- [ ] Set for Production, Preview, Development
- [ ] Save
- [ ] Redeploy frontend project
- [ ] Wait for deployment to complete
- [ ] Test registration/login
- [ ] Verify no 405 errors in console

