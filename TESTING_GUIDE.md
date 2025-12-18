# Ward Application Testing Guide

## 🎯 Current Deployment Status

### ✅ Working
- **Frontend**: https://frontend-5s7sl9joj-abhishek-vyas-projects.vercel.app
- **Frontend Build**: Successfully deployed with React 18

### 🔒 Needs Configuration
- **API**: https://api-dbx3kihob-abhishek-vyas-projects.vercel.app
- **Status**: Protected by Vercel deployment protection
- **Action Required**: Disable deployment protection OR use monorepo routing

## 🧪 Testing Options

### Option 1: Test via Frontend (Recommended)

The frontend is configured to use relative URLs (`/api`) in production, which means:

1. **If using `ward-logic` monorepo project:**
   - Frontend can access API through Vercel rewrites
   - No need to disable deployment protection on separate `api` project
   - Test at: https://ward-logic.vercel.app (if deployed)

2. **If using separate `frontend` project:**
   - Frontend needs `REACT_APP_API_URL` environment variable
   - Should point to the `api` project URL
   - OR disable deployment protection on `api` project

### Option 2: Disable Deployment Protection

1. Go to Vercel Dashboard → `api` project
2. Settings → **Deployment Protection** (NOT "Secure Backend Access")
3. Set Production to **"None"**
4. Save and redeploy
5. Test API directly: `curl https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/health`

## 📋 Testing Checklist

### 1. Frontend Access
- [ ] Visit: https://frontend-5s7sl9joj-abhishek-vyas-projects.vercel.app
- [ ] Verify homepage loads
- [ ] Check browser console for errors

### 2. User Registration
- [ ] Click "Sign Up" or navigate to `/register`
- [ ] Enter email and password
- [ ] Submit registration
- [ ] Check for success/error messages
- [ ] Verify redirect to dashboard

### 3. User Login
- [ ] Navigate to `/login`
- [ ] Enter credentials
- [ ] Submit login
- [ ] Verify JWT token is stored in localStorage
- [ ] Verify redirect to dashboard

### 4. Dashboard Access
- [ ] After login, verify dashboard loads
- [ ] Check for any API errors in console
- [ ] Verify user data is displayed

### 5. API Endpoints (if protection disabled)
```bash
# Health check
curl https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/health

# Registration
curl -X POST https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'

# Login
curl -X POST https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

## 🔧 Frontend Configuration

The frontend is configured in `frontend/src/services/api.js`:

```javascript
// In production, uses relative URLs (/api)
// In development, uses http://localhost:8001
const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 
  (process.env.NODE_ENV === 'production' ? '' : 'http://localhost:8001');
```

**For separate `frontend` project:**
- Set environment variable: `REACT_APP_BACKEND_URL=https://api-dbx3kihob-abhishek-vyas-projects.vercel.app`
- Redeploy frontend

**For `ward-logic` monorepo:**
- No configuration needed (uses rewrites from `vercel.json`)

## 🚀 Next Steps

1. **Test frontend → API connection:**
   - Visit frontend URL
   - Try to register/login
   - Check browser console for API errors

2. **If frontend can't access API:**
   - Option A: Disable deployment protection on `api` project
   - Option B: Deploy via `ward-logic` monorepo project
   - Option C: Set `REACT_APP_BACKEND_URL` in frontend project

3. **Verify full application flow:**
   - Registration → Login → Dashboard
   - Create case
   - Operator onboarding
   - Driver app access

## 📊 Expected Behavior

### ✅ Success Indicators
- Frontend loads without errors
- Registration creates user and returns JWT token
- Login authenticates and returns JWT token
- Dashboard displays user data
- No CORS errors in browser console
- API responses return JSON (not HTML)

### ❌ Error Indicators
- "Authentication Required" page (deployment protection)
- CORS errors (CORS_ORIGINS not configured)
- 401 Unauthorized (JWT token issues)
- 500 Internal Server Error (backend errors)
- Network errors (API URL incorrect)

## 🔍 Debugging

### Check Browser Console
1. Open browser DevTools (F12)
2. Go to Console tab
3. Look for:
   - API request errors
   - CORS errors
   - Network failures

### Check Network Tab
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try to register/login
4. Check API requests:
   - Status codes (200 = success, 401 = auth, 403 = forbidden)
   - Response body (JSON vs HTML)
   - Request URL (correct API endpoint)

### Check Vercel Logs
1. Go to Vercel Dashboard
2. Select project (`api` or `frontend`)
3. Go to **Deployments** → Latest deployment → **Functions** tab
4. Check for runtime errors

## 📝 Notes

- The frontend uses relative URLs in production, which works with monorepo routing
- Separate projects need explicit API URL configuration
- Deployment protection blocks direct API access but may not block monorepo routing
- Test the actual user flow, not just individual endpoints

