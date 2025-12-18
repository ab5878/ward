# Troubleshooting Guide

## Registration Failed Error

If you're seeing "Registration failed. Please try again.", check these:

### 1. Database Migration Not Run

**Symptom**: Registration fails with database errors

**Solution**: 
1. Go to: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd/sql/new
2. Copy contents of `supabase/migrations/001_initial_schema.sql`
3. Paste and run in SQL editor
4. Verify tables exist: `SELECT * FROM users LIMIT 1;`

### 2. Database Connection Not Working

**Symptom**: Connection errors in logs

**Check**:
- `SUPABASE_DB_URL` is set correctly in Vercel environment variables
- Password is correct (no brackets `[YOUR-PASSWORD]`)
- IP is whitelisted in Supabase (Settings → Database → Connection pooling)

**Test connection**:
```bash
cd backend
python3 -c "
import asyncio
from db_adapter import SupabaseAdapter
import os
from dotenv import load_dotenv
load_dotenv()

async def test():
    adapter = SupabaseAdapter(os.getenv('SUPABASE_DB_URL'))
    await adapter.connect()
    print('✅ Connected!')
    await adapter.close()

asyncio.run(test())
"
```

### 3. Backend Not Deployed or Not Accessible

**Symptom**: Network errors, 404, or CORS errors

**Check**:
- Backend is deployed to Vercel
- `REACT_APP_BACKEND_URL` is set correctly in Vercel
- Backend health endpoint works: `https://your-app.vercel.app/api/health`

**Test backend**:
```bash
curl https://ward-juvkr86yz-abhishek-vyas-projects.vercel.app/api/health
```

### 4. Environment Variables Not Set

**Symptom**: Missing configuration errors

**Check in Vercel Dashboard**:
- Settings → Environment Variables
- All required variables are set:
  - `SUPABASE_DB_URL`
  - `JWT_SECRET`
  - `CORS_ORIGINS`
  - `OPENAI_API_KEY` or `EMERGENT_LLM_KEY`
  - `SARVAM_API_KEY`
  - `REACT_APP_BACKEND_URL`

### 5. Check Browser Console

Open browser DevTools (F12) → Console tab:
- Look for network errors
- Check if API calls are being made
- See actual error messages

### 6. Check Vercel Function Logs

1. Go to Vercel Dashboard
2. Your project → Deployments
3. Click on latest deployment
4. Go to "Functions" tab
5. Click on `/api/index.py`
6. Check logs for errors

### 7. Common Errors

**"Table does not exist"**
- Run the migration (see #1)

**"Connection refused"**
- Check database password
- Check IP whitelist in Supabase

**"Invalid UUID"**
- Make sure migration was run
- Check database schema

**"CORS error"**
- Check `CORS_ORIGINS` includes your Vercel URL
- Check backend is receiving the environment variable

## Quick Debug Steps

1. **Check backend health**:
   ```
   curl https://ward-juvkr86yz-abhishek-vyas-projects.vercel.app/api/health
   ```

2. **Check database connection**:
   - Go to Supabase SQL Editor
   - Run: `SELECT * FROM users LIMIT 1;`
   - Should not error (even if empty)

3. **Check environment variables**:
   - Vercel Dashboard → Settings → Environment Variables
   - Verify all are set

4. **Check browser console**:
   - Open DevTools (F12)
   - Try registration
   - Check Network tab for failed requests
   - Check Console for errors

5. **Check Vercel logs**:
   - Dashboard → Deployments → Latest → Functions → Logs

## Still Not Working?

1. Check if migration was run successfully
2. Verify database connection string is correct
3. Check Vercel function logs for specific errors
4. Test backend endpoint directly with curl/Postman

