# How to Disable Vercel Deployment Protection

The API is showing "Authentication Required" because Vercel's deployment protection is enabled. This is a security feature that requires authentication to access preview deployments.

## Quick Fix: Disable Deployment Protection

### For API Project

1. **Go to Vercel Dashboard:**
   - Visit: https://vercel.com/dashboard
   - Select the **`api`** project

2. **Navigate to Settings:**
   - Click **Settings** in the top navigation
   - Click **Deployment Protection** in the left sidebar

3. **Disable Protection:**
   - Find **Production** environment
   - Toggle **Deployment Protection** to **OFF**
   - Optionally disable for **Preview** and **Development** as well
   - Click **Save**

4. **Redeploy (if needed):**
   - Go to **Deployments** tab
   - Click **"..."** on the latest deployment
   - Click **Redeploy**

### For Frontend Project

The frontend typically doesn't need deployment protection disabled unless you want public access to preview deployments.

## Alternative: Use Bypass Token

If you want to keep protection enabled but allow programmatic access:

1. **Get Bypass Token:**
   - Go to: https://vercel.com/dashboard
   - Select your project → **Settings** → **Deployment Protection**
   - Scroll to **Bypass Token** section
   - Click **Generate Token**
   - Copy the token

2. **Use Token in Requests:**
   ```bash
   curl "https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/health?x-vercel-set-bypass-cookie=true&x-vercel-protection-bypass=YOUR_TOKEN"
   ```

## Recommended Setup

For production APIs that need to be publicly accessible:

- **Production:** Disable deployment protection
- **Preview:** Keep enabled (for security)
- **Development:** Keep enabled (for security)

## After Disabling Protection

Once disabled, you should be able to access:
- `https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/health`
- `https://api-dbx3kihob-abhishek-vyas-projects.vercel.app/api/health/detailed`
- All other API endpoints

## Note

The frontend should work regardless of API protection settings if:
- Frontend and API are in the same project (ward-logic monorepo)
- Or frontend has proper CORS configuration
- Or you're using the monorepo setup with rewrites

