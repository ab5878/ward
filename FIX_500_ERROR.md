# Fix 500 Internal Server Error

## Problem
The backend is returning 500 errors when trying to login or register. This means the backend code is crashing.

## Most Likely Causes

### 1. Missing SUPABASE_DB_URL Environment Variable

The backend needs `SUPABASE_DB_URL` to connect to your Supabase database.

**Check if it's set:**
1. Go to: https://vercel.com/abhishek-vyas-projects/ward/settings/environment-variables
2. Look for `SUPABASE_DB_URL`
3. If it's missing, add it (see below)

**Get your Supabase connection string:**
1. Go to: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd/settings/database
2. Scroll to "Connection string"
3. Select "URI" tab
4. Copy the connection string (it should look like: `postgresql://postgres:[PASSWORD]@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres`)
5. Replace `[PASSWORD]` with your actual database password: `Mridulahemant1*`

**Add to Vercel:**
1. Go to Vercel Dashboard → Environment Variables
2. Add new variable:
   - Key: `SUPABASE_DB_URL`
   - Value: `postgresql://postgres:Mridulahemant1*@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres`
   - Select: Production, Preview, Development
3. Save

### 2. Database Migration Not Run

The `users` table might not exist in your Supabase database.

**Run the migration:**
1. Go to: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd/sql/new
2. Copy the contents of `supabase/migrations/001_initial_schema.sql`
3. Paste and run it
4. Verify the `users` table was created

### 3. Check Vercel Function Logs

To see the actual error:

1. Go to: https://vercel.com/abhishek-vyas-projects/ward
2. Click on the latest deployment
3. Go to "Functions" tab
4. Click on `/api/index.py`
5. Check the "Logs" tab
6. Look for error messages

## Quick Fix Steps

1. **Verify SUPABASE_DB_URL is set in Vercel**
2. **Run the database migration** (if not already done)
3. **Redeploy:**
   ```bash
   vercel --prod
   ```
4. **Test again**

## Test Database Connection

After setting the environment variable, test the health endpoint:

```bash
curl https://ward-y0lptjo9m-abhishek-vyas-projects.vercel.app/api/health
```

Should return:
```json
{"status":"ok","database":"connected","timestamp":"..."}
```

If it shows `"database":"error"`, check the error message in the response.

## Common Errors

### "Database not configured"
- **Fix**: Set `SUPABASE_DB_URL` in Vercel environment variables

### "Connection refused" or "Connection timeout"
- **Fix**: Check your Supabase connection string is correct
- **Fix**: Make sure your database password is correct

### "relation 'users' does not exist"
- **Fix**: Run the migration SQL script in Supabase

### "password authentication failed"
- **Fix**: Check your database password in the connection string

