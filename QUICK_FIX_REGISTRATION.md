# Quick Fix for Registration Error

## The Issue

Registration is failing. Most likely causes:

1. **Database migration not run** (users table doesn't exist)
2. **Backend not deployed** or not accessible
3. **Environment variables not set** in Vercel

## Quick Fix Steps

### Step 1: Verify Database Migration

1. Go to: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd/sql/new
2. Run this query to check if users table exists:
   ```sql
   SELECT * FROM users LIMIT 1;
   ```
3. If it errors, run the migration:
   - Open `supabase/migrations/001_initial_schema.sql`
   - Copy all contents
   - Paste and run in SQL editor

### Step 2: Check Backend Health

Visit in browser:
```
https://ward-juvkr86yz-abhishek-vyas-projects.vercel.app/api/health
```

Should return: `{"status":"healthy",...}`

If it errors or 404:
- Backend not deployed yet
- Deploy: `vercel --prod`

### Step 3: Check Environment Variables in Vercel

Go to: https://vercel.com/abhishek-vyas-projects/ward/settings/environment-variables

Verify these are set:
- ✅ `SUPABASE_DB_URL` = `postgresql://postgres:Mridulahemant1*@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres`
- ✅ `JWT_SECRET` = `yn8mz5USbcWuY8MIJhGB2ViMg-ngsYeIa-fE5Ddht_A`
- ✅ `CORS_ORIGINS` = `https://ward-juvkr86yz-abhishek-vyas-projects.vercel.app`
- ✅ `REACT_APP_BACKEND_URL` = `https://ward-juvkr86yz-abhishek-vyas-projects.vercel.app`

### Step 4: Check Browser Console

1. Open your app: https://ward-juvkr86yz-abhishek-vyas-projects.vercel.app
2. Open DevTools (F12)
3. Go to Console tab
4. Try to register
5. Check for errors - this will show the actual error message

### Step 5: Check Vercel Function Logs

1. Go to: https://vercel.com/abhishek-vyas-projects/ward
2. Click "Deployments" tab
3. Click on latest deployment
4. Click "Functions" tab
5. Click on `/api/index.py`
6. Check logs for errors

## Most Common Issues

**"Table does not exist"**
→ Run migration (Step 1)

**"Connection refused" or "Database not connected"**
→ Check `SUPABASE_DB_URL` is correct
→ Check database password
→ Check IP whitelist in Supabase

**"404 Not Found" on /api/health**
→ Backend not deployed
→ Deploy: `vercel --prod`

**CORS errors in browser**
→ Check `CORS_ORIGINS` includes your Vercel URL
→ Check `REACT_APP_BACKEND_URL` is set

**Network error / Failed to fetch**
→ Backend URL incorrect
→ Backend not deployed
→ Check Vercel function logs

## Test Registration Directly

You can test the registration endpoint directly:

```bash
curl -X POST https://ward-juvkr86yz-abhishek-vyas-projects.vercel.app/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456"}'
```

This will show you the actual error message.

