# Debug Frontend → API Connection

## 🔍 Common Issues After Setting Environment Variable

### Issue 1: Environment Variable Not Picked Up

**Symptom:** Still getting 405 or requests going to wrong domain

**Check:**
1. In browser, open DevTools (F12)
2. Go to **Console** tab
3. Type: `console.log(process.env.REACT_APP_BACKEND_URL)`
4. What does it show?

**If it shows `undefined`:**
- Environment variable wasn't set correctly
- Frontend wasn't rebuilt (React env vars are build-time only)
- Need to do a fresh rebuild

**Fix:**
1. Go to Vercel Dashboard → frontend project
2. Settings → Environment Variables
3. Verify `REACT_APP_BACKEND_URL` exists and value is correct
4. Go to Deployments → Create a **new deployment** (not redeploy)
5. Or trigger a new build by pushing a commit

### Issue 2: Browser Cache

**Symptom:** Old JavaScript bundle still being used

**Fix:**
1. Hard refresh: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)
2. Or clear browser cache
3. Or open in incognito/private window

### Issue 3: API Still Protected

**Symptom:** Getting 401 or "Authentication Required" page

**Check:**
1. Try accessing API directly: https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/health
2. If you see "Authentication Required", deployment protection is still enabled

**Fix:**
- Disable deployment protection on API project (see previous guides)

### Issue 4: CORS Error

**Symptom:** Browser console shows CORS error

**Check:**
- Error message mentions "CORS" or "Access-Control-Allow-Origin"

**Fix:**
1. Go to Vercel Dashboard → `api` project
2. Settings → Environment Variables
3. Check `CORS_ORIGINS` includes: `https://frontend-5s7sl9joj-abhishek-vyas-projects.vercel.app`
4. If not, add it and redeploy API

### Issue 5: Wrong API URL

**Symptom:** 404 or connection refused

**Check:**
1. Verify the API URL is correct: `https://api-dbx3kihob-abhishek-vyas-projects.vercel.app`
2. Check Network tab - what URL is the request actually going to?

**Fix:**
- Make sure `REACT_APP_BACKEND_URL` value is exactly: `https://api-dbx3kihob-abhishek-vyas-projects.vercel.app`
- No trailing slash
- Include `https://`

## 🧪 Quick Diagnostic Steps

### Step 1: Check Environment Variable in Browser

Open browser console (F12) and run:
```javascript
// This won't work in production (env vars are build-time)
// But check Network tab instead
```

### Step 2: Check Network Tab

1. Open DevTools (F12)
2. Go to **Network** tab
3. Try to login/register
4. Look for the `/api/auth/login` request
5. Check:
   - **Request URL:** Should be `https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/auth/login`
   - **Status Code:** What is it? (200, 401, 405, 404, etc.)
   - **Response:** What does it say?

### Step 3: Check API Directly

Try in terminal:
```bash
curl https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/health
```

- If you get JSON: API is working ✅
- If you get HTML "Authentication Required": API is protected 🔒
- If you get connection error: API might be down ❌

### Step 4: Verify Environment Variable in Vercel

1. Go to Vercel Dashboard → frontend project
2. Settings → Environment Variables
3. Verify:
   - Key: `REACT_APP_BACKEND_URL`
   - Value: `https://api-dbx3kihob-abhishek-vyas-projects.vercel.app`
   - Environments: All checked (Production, Preview, Development)

### Step 5: Force New Build

React environment variables are embedded at **build time**, not runtime. So:

1. Go to Vercel Dashboard → frontend project
2. Deployments → Click "..." → "Redeploy"
3. **Important:** Make sure it's doing a fresh build
4. Or better: Make a small change to trigger a new build:
   ```bash
   # In your local repo
   echo "// Build trigger" >> frontend/src/App.js
   git add frontend/src/App.js
   git commit -m "Trigger rebuild"
   git push
   ```

## 📋 What to Share for Debugging

Please share:

1. **Exact error message** from browser console
2. **Network tab screenshot** or details:
   - Request URL
   - Status code
   - Response body
3. **What you see** when accessing API directly:
   ```bash
   curl https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/health
   ```
4. **Environment variable** in Vercel (screenshot or confirmation it's set)

## 🎯 Most Likely Issues

Based on common problems:

1. **Environment variable not picked up** (most common)
   - Solution: Force a new build, not just redeploy

2. **API still protected**
   - Solution: Disable deployment protection

3. **Browser cache**
   - Solution: Hard refresh or incognito window

4. **CORS issue**
   - Solution: Add frontend URL to `CORS_ORIGINS` in API project

