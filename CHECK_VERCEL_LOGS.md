# How to Check Vercel Logs

## Method 1: Via Vercel Dashboard (Recommended)

1. Go to: https://vercel.com/dashboard
2. Select your project: `api`
3. Go to **Deployments** tab
4. Click on the latest deployment
5. Go to **Functions** tab
6. Click on the function (usually `index`)
7. View **Runtime Logs**

## Method 2: Via Vercel CLI

```bash
# Get logs for a specific deployment
vercel logs https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app

# Or use deployment ID
vercel logs dpl_FSQe2gMLvYAeLAwtTLVu4ZA68Vr8

# JSON format (for filtering)
vercel logs dpl_FSQe2gMLvYAeLAwtTLVu4ZA68Vr8 --json | jq 'select(.level == "error")'
```

## Method 3: Trigger an Error to See Logs

Make a request to your API to trigger logs:

```bash
# This will trigger the import error and show in logs
curl https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api/health
```

Then check logs immediately after.

## Common Errors to Look For

1. **ModuleNotFoundError** - Missing Python modules
2. **ImportError** - Can't find backend files
3. **Database connection errors** - Missing SUPABASE_DB_URL
4. **Environment variable errors** - Missing JWT_SECRET, etc.

## Quick Check

The deployment shows:
- **Status:** ● Ready
- **Function Size:** 11.59MB
- **Location:** iad1 (US East)

If you see errors, they'll appear in the Runtime Logs section of the deployment.

