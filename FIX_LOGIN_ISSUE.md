# Fix Login/Registration Issue

## Problem
The login and registration are failing because:
1. **Vercel Deployment Protection** is blocking API access
2. Frontend was trying to connect to `localhost` instead of the deployed backend

## ✅ Fixed
- Updated frontend to use relative URLs in production (same domain as frontend)
- Frontend now automatically uses `/api` when deployed on Vercel

## 🔧 Action Required: Disable Vercel Deployment Protection

**You MUST disable deployment protection for the API to work:**

1. Go to: https://vercel.com/abhishek-vyas-projects/ward/settings/deployment-protection
2. **Disable** deployment protection for this project
3. Or add an exception for `/api/*` routes

### Alternative: Use Vercel CLI
```bash
vercel project settings --disable-deployment-protection
```

## 🧪 Test After Fix

1. **Redeploy** to Vercel:
   ```bash
   vercel --prod
   ```

2. **Test registration**:
   - Go to your deployed site
   - Try registering a new user
   - Check browser console (F12) for any errors

3. **Test API directly** (after disabling protection):
   ```bash
   curl https://ward-juvkr86yz-abhishek-vyas-projects.vercel.app/api/health
   ```
   Should return: `{"status":"ok"}`

## 📋 Environment Variables to Check

Make sure these are set in Vercel Dashboard → Settings → Environment Variables:

- `SUPABASE_DB_URL` - Your Supabase connection string
- `JWT_SECRET` - Random secret for JWT tokens
- `CORS_ORIGINS` - Your frontend URL (or `*` for development)
- `OPENAI_API_KEY` - Your OpenAI API key
- `SARVAM_API_KEY` - Your Sarvam API key

## 🐛 If Still Not Working

1. **Check Vercel Function Logs**:
   - Go to: https://vercel.com/abhishek-vyas-projects/ward
   - Click on latest deployment
   - Go to "Functions" tab
   - Check logs for errors

2. **Check Browser Console**:
   - Open DevTools (F12)
   - Go to Console tab
   - Look for error messages

3. **Verify Database Migration**:
   - Go to Supabase Dashboard
   - Check if `users` table exists
   - Run migration if needed: `supabase/migrations/001_initial_schema.sql`

