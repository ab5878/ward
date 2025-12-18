# Rename Vercel Project to `ward-logic`

## Quick Steps

### Option 1: Via Vercel Dashboard (Easiest)

1. Go to your project settings:
   ```
   https://vercel.com/abhishek-vyas-projects/ward/settings/general
   ```

2. Find the **"Project Name"** field

3. Change it from `ward` to `ward-logic`

4. Click **"Save"**

5. Your new URL will be: `https://ward-logic.vercel.app`

### Option 2: Via Vercel CLI

```bash
# Install Vercel CLI if not already installed
npm i -g vercel

# Login to Vercel
vercel login

# Link to your project (if not already linked)
cd /Users/abhishekvyas/ward
vercel link

# Rename the project
vercel project rename ward-logic
```

### Option 3: Create New Project with New Name

If renaming doesn't work, you can:

1. Create a new project in Vercel named `ward-logic`
2. Connect it to the same Git repository
3. Deploy

## After Renaming

1. **Update Environment Variables** (if needed):
   - Go to: `https://vercel.com/abhishek-vyas-projects/ward-logic/settings/environment-variables`
   - Verify all variables are still set

2. **Update CORS_ORIGINS** (if you have it set):
   - Add `https://ward-logic.vercel.app` to your `CORS_ORIGINS` environment variable

3. **Test the new URL**:
   - Visit: `https://ward-logic.vercel.app`
   - Test login/registration
   - Verify API endpoints work

## Notes

- The old URL (`ward-*.vercel.app`) will redirect to the new one for a while
- All deployments will now use the new URL
- Git integration remains the same
- Environment variables are preserved

