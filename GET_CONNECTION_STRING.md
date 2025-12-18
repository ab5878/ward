# How to Get Your Supabase Connection String

## Quick Steps

1. **Go to Supabase Dashboard**
   - Visit: https://supabase.com/dashboard
   - Sign in to your account

2. **Select Your Project**
   - Click on your project (or create a new one)
   - Your project ref: `gjwzaylkzknsykjvtpcd`

3. **Navigate to Database Settings**
   - Click **Settings** (gear icon in left sidebar)
   - Click **Database** in the settings menu

4. **Get Connection String**
   - Scroll down to **Connection string** section
   - Click on the **URI** tab (not "Connection pooling")
   - You'll see something like:
     ```
     postgresql://postgres.[PROJECT-REF]:[YOUR-PASSWORD]@aws-0-[REGION].pooler.supabase.com:6543/postgres
     ```
   - **OR** use the direct connection (recommended for serverless):
     ```
     postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
     ```

5. **Replace Placeholder**
   - Replace `[YOUR-PASSWORD]` with your actual database password
   - This is the password you set when creating the project

6. **Set Environment Variable**
   ```bash
   export SUPABASE_DB_URL='postgresql://postgres:YOUR_ACTUAL_PASSWORD@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres'
   ```

## For Your Project

Based on your project ref `gjwzaylkzknsykjvtpcd`, your connection string should be:

```
postgresql://postgres:[YOUR-PASSWORD]@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres
```

Replace `[YOUR-PASSWORD]` with your actual password.

## Verify It Works

After setting the connection string, test it:

```bash
cd backend
export SUPABASE_DB_URL='postgresql://postgres:YOUR_PASSWORD@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres'
export JWT_SECRET='your-secret-key'
python3 verify_auth_flow.py
```

## Important Notes

- **Use direct connection** (`db.xxx.supabase.co:5432`) for serverless functions
- **Don't use connection pooling** (`pooler.supabase.com:6543`) for serverless
- **Keep your password secure** - never commit it to git
- **Use environment variables** - don't hardcode passwords

## Troubleshooting

If you get "invalid literal for int() with base 10: 'port'":
- You're using a placeholder connection string
- Get the real one from Supabase dashboard

If you get "password authentication failed":
- Check that you replaced `[YOUR-PASSWORD]` with your actual password
- The password is case-sensitive

If you get "connection refused":
- Check that your IP is allowed in Supabase (Settings → Database → Connection Pooling)
- Or use the direct connection string instead

