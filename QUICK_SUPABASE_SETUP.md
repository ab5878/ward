# Quick Supabase Setup

## 1. Create Supabase Project (2 minutes)

1. Go to https://supabase.com and sign up/login
2. Click "New Project"
3. Name: `ward-production`
4. Set a strong database password (save it!)
5. Region: Choose closest (Mumbai for India)
6. Click "Create new project"
7. Wait 2-3 minutes

## 2. Get Connection String (1 minute)

1. In Supabase dashboard → **Settings** → **Database**
2. Scroll to **Connection string** → **URI** tab
3. Copy the connection string
4. Replace `[YOUR-PASSWORD]` with your actual password
5. Example: `postgresql://postgres:yourpassword@db.xxxxx.supabase.co:5432/postgres`

## 3. Run Migration (1 minute)

1. In Supabase dashboard → **SQL Editor**
2. Click "New query"
3. Open `supabase/migrations/001_initial_schema.sql`
4. Copy all contents and paste into SQL editor
5. Click "Run" (Cmd/Ctrl + Enter)
6. Should see "Success. No rows returned"

## 4. Set Environment Variables

### For Local Development

Add to `backend/.env`:

```bash
SUPABASE_DB_URL=postgresql://postgres:yourpassword@db.xxxxx.supabase.co:5432/postgres
JWT_SECRET=your-secret-key-here
CORS_ORIGINS=http://localhost:3000
EMERGENT_LLM_KEY=your-key
SARVAM_API_KEY=your-key
```

### For Production (Railway/Render)

Add these environment variables:
- `SUPABASE_DB_URL` - Your connection string
- `JWT_SECRET` - Generate: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- `CORS_ORIGINS` - Your Vercel frontend URL
- `EMERGENT_LLM_KEY` - Your API key
- `SARVAM_API_KEY` - Your API key

## 5. Test Connection

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
    print('✅ Connected!')
    await adapter.close()

asyncio.run(test())
"
```

## 6. Deploy Backend

### Railway (Easiest)

1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Select your repo
4. Root Directory: `backend`
5. Add environment variables (from step 4)
6. Deploy!

### Render

1. Go to https://render.com
2. New Web Service
3. Connect GitHub repo
4. Settings:
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Add environment variables
6. Deploy!

## 7. Update Frontend

In Vercel dashboard:
1. Settings → Environment Variables
2. Update `REACT_APP_BACKEND_URL` to your backend URL
3. Redeploy

## Done! 🎉

Your Ward app is now running on:
- Frontend: Vercel
- Backend: Railway/Render
- Database: Supabase PostgreSQL

## Troubleshooting

**"Connection refused"**
- Check connection string has correct password
- No brackets `[YOUR-PASSWORD]` - use actual password

**"Table does not exist"**
- Make sure you ran the migration (step 3)
- Check in SQL Editor: `SELECT * FROM cases LIMIT 1;`

**"Invalid UUID"**
- The code now uses UUIDs (Supabase default)
- All IDs are UUIDs, not ObjectIds

## Next Steps

- Set up Row Level Security (RLS) for multi-tenant
- Configure connection pooling
- Set up database backups
- Monitor in Supabase dashboard

