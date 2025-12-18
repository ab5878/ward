# Fix Database Connection Error

## 🔍 Problem

The API is returning:
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "error": "500: Database connection failed: [Errno 99] Cannot assign requested address"
}
```

This means the API can't connect to Supabase PostgreSQL.

## ✅ Solution: Set Database Environment Variables

The API project needs the `SUPABASE_DB_URL` environment variable.

### Step 1: Get Your Supabase Connection String

1. Go to: https://supabase.com/dashboard
2. Select your project
3. Go to **Settings** → **Database**
4. Scroll to **Connection string** section
5. Copy the **URI** connection string
   - It should look like: `postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:5432/postgres`
   - Or use the **Connection Pooler** (recommended for serverless):
     - **Session mode**: `postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:6543/postgres?pgbouncer=true`
     - **Transaction mode**: `postgresql://postgres:[PASSWORD]@db.xxxxx.supabase.co:6543/postgres?pgbouncer=true`

### Step 2: Set Environment Variable in Vercel

1. Go to: https://vercel.com/dashboard
2. Select the **`api`** project (not `frontend`)
3. Go to **Settings** → **Environment Variables**
4. Click **"Add New"**
5. Add:

   **Key:**
   ```
   SUPABASE_DB_URL
   ```

   **Value:**
   ```
   postgresql://postgres:YOUR_PASSWORD@db.xxxxx.supabase.co:5432/postgres
   ```
   (Replace `YOUR_PASSWORD` and `xxxxx` with your actual values)

   **Environments:**
   - ✅ Production
   - ✅ Preview
   - ✅ Development

6. Click **Save**

### Step 3: Redeploy API

1. Go to **Deployments** tab
2. Find the latest deployment
3. Click **"..."** → **"Redeploy"**
4. Wait for deployment to complete (1-2 minutes)

### Step 4: Test Again

```bash
curl https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "..."
}
```

## 🔧 Using Connection Pooler (Recommended for Serverless)

For Vercel serverless functions, use the **Connection Pooler** instead of direct connection:

1. In Supabase Dashboard → Settings → Database
2. Find **Connection Pooler** section
3. Copy the **Transaction mode** connection string
4. It will have port **6543** (not 5432)
5. Use this as your `SUPABASE_DB_URL`

**Example:**
```
postgresql://postgres.xxxxx:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

## 📋 Required Environment Variables for API Project

Make sure these are set in the **`api`** project:

1. **SUPABASE_DB_URL** (required)
   - Your PostgreSQL connection string

2. **JWT_SECRET** (required)
   - Secret key for JWT tokens
   - Generate with: `python3 -c "import secrets; print(secrets.token_urlsafe(32))"`

3. **CORS_ORIGINS** (required)
   - Comma-separated list of allowed origins
   - Example: `https://frontend-5s7sl9joj-abhishek-vyas-projects.vercel.app`

4. **OPENAI_API_KEY** (optional)
   - For AI features

5. **SARVAM_API_KEY** (optional)
   - For voice transcription

## 🧪 Verify Environment Variables

1. Go to Vercel Dashboard → `api` project
2. Settings → Environment Variables
3. Verify all required variables are set
4. Check that values are correct (no typos, correct format)

## ⚠️ Common Issues

### Issue 1: Wrong Connection String Format

**Symptom:** Still getting connection errors

**Fix:**
- Make sure connection string starts with `postgresql://`
- Include password in the URL: `postgresql://postgres:PASSWORD@...`
- Use correct port (5432 for direct, 6543 for pooler)

### Issue 2: Password with Special Characters

**Symptom:** Connection fails with authentication error

**Fix:**
- URL-encode special characters in password
- Or change password to one without special characters

### Issue 3: Network/Firewall

**Symptom:** `[Errno 99] Cannot assign requested address`

**Fix:**
- Use Connection Pooler (port 6543) instead of direct connection
- Check Supabase firewall settings
- Make sure IP restrictions allow Vercel's IPs

### Issue 4: Database Not Initialized

**Symptom:** Connection works but tables don't exist

**Fix:**
- Run database migrations in Supabase
- Check `supabase/migrations/` folder
- Run migrations via Supabase Dashboard → SQL Editor

## 🎯 Quick Checklist

- [ ] Got Supabase connection string
- [ ] Set `SUPABASE_DB_URL` in `api` project
- [ ] Set for Production, Preview, Development
- [ ] Redeployed API project
- [ ] Tested `/api/health` endpoint
- [ ] Database shows as "connected"

## 📝 Your Connection String

Based on previous setup, your connection string should be:
```
postgresql://postgres:Mridulahemant1*@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres
```

**Important:** Make sure this is set in the **`api`** project, not `frontend`!
