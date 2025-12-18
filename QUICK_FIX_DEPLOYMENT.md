# Quick Fix: Deployment Protection & Configuration
**5-minute guide to get your API working**

---

## 🚀 Quick Fix Steps

### Step 1: Disable Deployment Protection (2 minutes)

1. **Go to Vercel Dashboard:**
   - Visit: https://vercel.com/dashboard
   - Click on `api` project

2. **Disable Protection:**
   - Click **Settings** (left sidebar)
   - Click **Deployment Protection**
   - Toggle **OFF** for both Preview and Production
   - Click **Save**

3. **Test:**
   ```bash
   curl https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api/health
   ```
   
   Should return JSON, not HTML.

### Step 2: Set Environment Variables (3 minutes)

1. **Backend Environment Variables:**
   - Still in `api` project settings
   - Click **Environment Variables**
   - Add these (select Production, Preview, Development):
   
   ```
   SUPABASE_DB_URL=your-connection-string
   JWT_SECRET=your-secret-key
   ```

2. **Frontend Environment Variables:**
   - Go to `frontend` project
   - Settings → Environment Variables
   - Add:
   
   ```
   REACT_APP_API_URL=https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api
   ```

3. **Redeploy:**
   - Vercel will auto-redeploy after env vars are set
   - Or manually: Click Deployments → Redeploy

---

## ✅ Verify It Works

```bash
# Test health
curl https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api/health

# Test registration
curl -X POST https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"Test123!"}'
```

---

## 🎯 That's It!

Your API should now be publicly accessible and working!

---

**Time:** ~5 minutes  
**Difficulty:** Easy

