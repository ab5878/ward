# Supabase Setup Guide for Ward

This guide will help you set up Supabase as the backend database for Ward.

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click "New Project"
3. Fill in:
   - **Name**: `ward-production` (or your preferred name)
   - **Database Password**: Generate a strong password (save it!)
   - **Region**: Choose closest to your users (e.g., `Southeast Asia (Mumbai)` for India)
4. Click "Create new project"
5. Wait 2-3 minutes for project to be created

## Step 2: Get Database Connection String

1. In your Supabase project dashboard, go to **Settings** → **Database**
2. Scroll down to **Connection string**
3. Select **URI** tab
4. Copy the connection string (it looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres`)
5. Replace `[YOUR-PASSWORD]` with the password you set when creating the project
6. Save this as `SUPABASE_DB_URL` (you'll need it later)

## Step 3: Run Database Migration

1. In Supabase dashboard, go to **SQL Editor**
2. Click "New query"
3. Copy the contents of `supabase/migrations/001_initial_schema.sql`
4. Paste into the SQL editor
5. Click "Run" (or press Cmd/Ctrl + Enter)
6. You should see "Success. No rows returned"

## Step 4: Set Up Environment Variables

### For Local Development

Create/update `.env` file in the `backend` directory:

```bash
# Supabase Database
SUPABASE_DB_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres

# Or use DATABASE_URL (both work)
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.xxxxx.supabase.co:5432/postgres

# Other required variables
JWT_SECRET=your-jwt-secret-key-here
CORS_ORIGINS=http://localhost:3000,https://your-vercel-app.vercel.app
EMERGENT_LLM_KEY=your-emergent-key
SARVAM_API_KEY=your-sarvam-key
```

### For Production Deployment

Set these environment variables in your hosting platform (Railway, Render, etc.):

- `SUPABASE_DB_URL` or `DATABASE_URL` - Your Supabase connection string
- `JWT_SECRET` - Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"`
- `CORS_ORIGINS` - Your frontend URL(s)
- `EMERGENT_LLM_KEY` - Your Emergent API key
- `SARVAM_API_KEY` - Your Sarvam AI API key

## Step 5: Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

The `asyncpg` package is now included for PostgreSQL support.

## Step 6: Test the Connection

```bash
cd backend
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

## Step 7: Deploy Backend

### Option A: Railway (Recommended)

1. Go to [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Select your repo
4. Set Root Directory: `backend`
5. Add environment variables (see Step 4)
6. Railway will auto-detect and deploy

### Option B: Render

1. Go to [render.com](https://render.com)
2. New Web Service
3. Connect GitHub repo
4. Settings:
   - Root Directory: `backend`
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. Add environment variables

## Step 8: Update Frontend Backend URL

1. In Vercel dashboard, go to your project
2. Settings → Environment Variables
3. Update `REACT_APP_BACKEND_URL` to your deployed backend URL
4. Redeploy

## Migration from MongoDB (Optional)

If you have existing MongoDB data, you'll need to migrate it:

1. Export data from MongoDB
2. Transform ObjectIds to UUIDs
3. Import into Supabase using the SQL editor or a migration script

## Troubleshooting

### "Connection refused" error
- Check your Supabase connection string is correct
- Verify password is correct (no brackets)
- Check if your IP needs to be whitelisted (Settings → Database → Connection pooling)

### "Table does not exist" error
- Make sure you ran the migration (Step 3)
- Check in Supabase SQL Editor: `SELECT * FROM cases LIMIT 1;`

### "Invalid UUID" error
- The code now uses UUIDs instead of ObjectIds
- Make sure all ID references use UUID format

## Supabase Features You Can Use

- **Real-time subscriptions**: Subscribe to case updates in real-time
- **Row Level Security**: Add RLS policies for multi-tenant support
- **Storage**: Use Supabase Storage for document uploads
- **Auth**: Consider migrating to Supabase Auth (optional)

## Next Steps

- Set up Row Level Security (RLS) policies
- Configure connection pooling for better performance
- Set up database backups
- Monitor usage in Supabase dashboard

## Support

- Supabase Docs: https://supabase.com/docs
- Supabase Discord: https://discord.supabase.com

