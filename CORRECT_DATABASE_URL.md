# Correct Database URL for Vercel Serverless

## 🔍 Problem

The error `[Errno 99] Cannot assign requested address` happens because:

1. **Password contains `*`** which needs URL encoding
2. **Direct connection (port 5432)** can have issues with serverless

## ✅ Solution: Use Connection Pooler URL

For Vercel serverless functions, use the **Supabase Connection Pooler** (port 6543) instead of direct connection (port 5432).

### Step 1: Get the Correct URL from Supabase

1. Go to: https://supabase.com/dashboard
2. Select your project
3. Go to **Settings** → **Database**
4. Scroll to **Connection Pooler** section
5. Select **Session mode**
6. Copy the connection string

It should look like:
```
postgresql://postgres.gjwzaylkzknsykjvtpcd:[PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

### Step 2: URL-Encode the Password

Your password `Mridulahemant1*` contains `*` which needs to be encoded as `%2A`.

**Encoded password:** `Mridulahemant1%2A`

### Step 3: The Correct URL

**Option A: Connection Pooler (Recommended for Serverless)**
```
postgresql://postgres.gjwzaylkzknsykjvtpcd:Mridulahemant1%2A@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

**Option B: Direct Connection (if pooler not available)**
```
postgresql://postgres:Mridulahemant1%2A@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres
```

### Step 4: Update in Vercel

1. Go to Vercel Dashboard → `api` project
2. Settings → Environment Variables
3. Update `SUPABASE_DB_URL` with the correct URL (Option A recommended)
4. Save
5. Redeploy

## 📋 Quick Copy-Paste URLs

### For Connection Pooler (Recommended):
```
postgresql://postgres.gjwzaylkzknsykjvtpcd:Mridulahemant1%2A@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

### For Direct Connection:
```
postgresql://postgres:Mridulahemant1%2A@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres
```

## ⚠️ Important Notes

1. **Use `%2A` instead of `*`** in the password (URL encoding)
2. **Port 6543** for connection pooler, **port 5432** for direct
3. **Redeploy after changing** environment variables
4. The code has been updated to handle URL encoding automatically, but it's safer to use the pre-encoded URL

## 🧪 Test After Redeploying

```bash
curl https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/health
```

Expected response:
```json
{"status":"healthy","database":"connected","timestamp":"..."}
```

