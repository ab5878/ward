# Supabase Quick Start for Your Project

## Your Supabase Project

- **Project URL**: https://gjwzaylkzknsykjvtpcd.supabase.co
- **Project ID**: gjwzaylkzknsykjvtpcd
- **API Key**: (configured in .env.example)

## Step 1: Get Database Connection String

1. Go to: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd/settings/database
2. Scroll to **Connection string** section
3. Click on **URI** tab
4. Copy the connection string
5. Replace `[YOUR-PASSWORD]` with the password you set when creating the project

**Example format:**
```
postgresql://postgres:yourpassword@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres
```

## Step 2: Run Database Migration

1. Go to: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd/sql/new
2. Open the file: `supabase/migrations/001_initial_schema.sql`
3. Copy ALL contents
4. Paste into the SQL editor
5. Click **Run** (or press Cmd/Ctrl + Enter)
6. You should see: "Success. No rows returned"

## Step 3: Set Environment Variables

### Option A: Using the Setup Script

```bash
./setup_supabase.sh
```

This will:
- Ask for your database password
- Test the connection
- Show you the connection string

### Option B: Manual Setup

Create `backend/.env` file:

```bash
# Database
SUPABASE_DB_URL=postgresql://postgres:yourpassword@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres

# JWT Secret (generate one)
JWT_SECRET=your-secret-key-here

# CORS
CORS_ORIGINS=http://localhost:3000,https://ward-juvkr86yz-abhishek-vyas-projects.vercel.app

# AI Keys
EMERGENT_LLM_KEY=your-key
SARVAM_API_KEY=your-key
```

Generate JWT secret:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Step 4: Test Connection

```bash
cd backend
pip install asyncpg
python -c "
import asyncio
from db_adapter import SupabaseAdapter
import os
from dotenv import load_dotenv

load_dotenv()

async def test():
    adapter = SupabaseAdapter(os.getenv('SUPABASE_DB_URL'))
    await adapter.connect()
    print('✅ Connected to Supabase!')
    await adapter.close()

asyncio.run(test())
"
```

## Step 5: Start Backend

```bash
cd backend
uvicorn server:app --reload
```

The backend will automatically use Supabase if `SUPABASE_DB_URL` is set.

## Step 6: Deploy Backend

### Railway

1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select your repo
4. Root Directory: `backend`
5. Add environment variables:
   - `SUPABASE_DB_URL` = Your connection string
   - `JWT_SECRET` = Your secret
   - `CORS_ORIGINS` = Your Vercel URL
   - `EMERGENT_LLM_KEY` = Your key
   - `SARVAM_API_KEY` = Your key
6. Deploy!

### Render

1. Go to https://render.com
2. New Web Service
3. Connect GitHub repo
4. Settings:
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Add same environment variables
6. Deploy!

## Step 7: Update Frontend

In Vercel dashboard:
1. Settings → Environment Variables
2. Update `REACT_APP_BACKEND_URL` to your deployed backend URL
3. Redeploy

## Useful Links

- **Supabase Dashboard**: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd
- **SQL Editor**: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd/sql
- **Database Settings**: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd/settings/database
- **API Settings**: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd/settings/api

## Troubleshooting

### "Connection refused"
- Check your password is correct (no brackets)
- Check your IP is whitelisted: Settings → Database → Connection pooling → Add your IP

### "Table does not exist"
- Make sure you ran the migration (Step 2)
- Check in SQL Editor: `SELECT * FROM cases LIMIT 1;`

### "Invalid password"
- Make sure you're using the database password, not the API key
- Password should be the one you set when creating the project

## Next Steps

- ✅ Database migration complete
- ✅ Connection tested
- ⏭️ Deploy backend
- ⏭️ Update frontend backend URL
- ⏭️ Test full stack

