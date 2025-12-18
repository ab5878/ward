# Get Correct Supabase Connection Pooler URL

The error `[Errno 99] Cannot assign requested address` means the database hostname can't be reached.

## Step 1: Get the Correct URL from Supabase Dashboard

1. Go to: https://supabase.com/dashboard
2. Select your project: `gjwzaylkzknsykjvtpcd`
3. Click **Settings** (gear icon) in the left sidebar
4. Click **Database** in the settings menu
5. Scroll down to **Connection string** section
6. Look for **Connection pooling** subsection
7. Click on **URI** tab
8. Copy the connection string

## Step 2: What You Should See

The Supabase connection pooler URL looks like this:
```
postgres://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
```

For your project, it should be something like:
```
postgres://postgres.gjwzaylkzknsykjvtpcd:[YOUR-PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

**Important:** 
- Replace `[YOUR-PASSWORD]` with your actual database password
- The `*` in your password needs to be URL-encoded as `%2A`
- So `Mridulahemant1*` becomes `Mridulahemant1%2A`

## Step 3: Verify Your Supabase Project is Active

1. In Supabase Dashboard, check if your project is **paused**
2. If paused, click **Restore** to wake it up
3. Wait a minute for it to become active

## Step 4: Check the Exact Region

Your pooler URL region might be different. Common regions:
- `aws-0-ap-south-1` (Mumbai, India)
- `aws-0-us-east-1` (Virginia, USA)
- `aws-0-us-west-1` (N. California, USA)

Copy the exact URL from your Supabase dashboard!

## Step 5: Update in Vercel

1. Go to Vercel Dashboard → `api` project
2. Settings → Environment Variables
3. Delete the old `SUPABASE_DB_URL`
4. Add new `SUPABASE_DB_URL` with the correct URL from Supabase
5. Make sure to:
   - URL-encode the password (`*` → `%2A`)
   - Include all parts of the URL exactly as shown
6. Save
7. Redeploy

## Alternative: Use Direct Connection (if pooler doesn't work)

If the connection pooler URL doesn't work, try the direct connection:

```
postgresql://postgres:[YOUR-PASSWORD]@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres
```

With your password URL-encoded:
```
postgresql://postgres:Mridulahemant1%2A@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres
```

## Verify Environment Variable is Set

After setting the variable in Vercel:
1. Go to Vercel Dashboard → `api` project
2. Click **Deployments**
3. Click on the latest deployment
4. Click **Functions** or **Logs**
5. Check if you see any error messages about the database

## Quick Checklist

- [ ] Got the connection pooler URL from Supabase Dashboard
- [ ] Verified Supabase project is not paused
- [ ] URL-encoded the password (replaced `*` with `%2A`)
- [ ] Set `SUPABASE_DB_URL` in Vercel `api` project
- [ ] Selected all environments (Production, Preview, Development)
- [ ] Saved the environment variable
- [ ] Redeployed the `api` project
- [ ] Waited for deployment to complete
- [ ] Tested `/api/health` endpoint

