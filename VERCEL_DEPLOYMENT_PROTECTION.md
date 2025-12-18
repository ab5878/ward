# Vercel Deployment Protection - Quick Fix
**How to disable authentication for your API endpoints**

---

## 🔒 Issue

Your API endpoint is showing "Authentication Required" because Vercel has deployment protection enabled by default for preview deployments.

---

## ✅ Solution: Disable Deployment Protection

### Option 1: Via Vercel Dashboard (Recommended)

1. **Go to Vercel Dashboard**
   - Visit: https://vercel.com/dashboard
   - Select your project: `api` (backend)

2. **Navigate to Settings**
   - Click on your project
   - Go to **Settings** → **Deployment Protection**

3. **Disable Protection**
   - Find **"Deployment Protection"** section
   - Toggle **OFF** for preview deployments
   - Or set it to **"None"** for production

4. **Save Changes**
   - Click **Save**
   - Redeploy if needed

### Option 2: Via Vercel CLI

```bash
# Disable deployment protection for preview deployments
vercel env rm VERCEL_DEPLOYMENT_PROTECTION --yes

# Or set it to "none"
vercel env add VERCEL_DEPLOYMENT_PROTECTION production "none"
```

### Option 3: Via Vercel Dashboard (Only Method)

**Note:** Deployment protection cannot be configured via `vercel.json`. It must be done through the Vercel Dashboard.

The `vercel.json` file is only for function configuration, not deployment protection settings.

---

## 🚀 Alternative: Use Production Deployment

Production deployments typically don't have this protection by default. You can:

1. **Deploy to Production**
   ```bash
   vercel deploy --prod
   ```

2. **Or Set Custom Domain**
   - Configure `ward-logic.vercel.app` in Vercel
   - Production domains usually don't have protection

---

## 🔍 Verify Fix

After disabling protection, test the health endpoint:

```bash
curl https://api-kx36mq90x-abhishek-vyas-projects.vercel.app/api/health
```

You should see:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-12-15T..."
}
```

---

## 📋 Quick Steps Summary

1. ✅ Go to Vercel Dashboard
2. ✅ Select your `api` project
3. ✅ Settings → Deployment Protection
4. ✅ Disable for preview/production
5. ✅ Test health endpoint
6. ✅ Done!

---

## ⚠️ Security Note

- **Preview deployments**: Safe to disable protection (they're temporary)
- **Production deployments**: Consider keeping protection or using API keys
- **Custom domains**: Usually don't have protection by default

---

**Last Updated:** December 2024

