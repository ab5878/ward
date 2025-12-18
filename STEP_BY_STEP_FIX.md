# Step-by-Step Fix: Frontend → API Connection

## 🎯 Goal
Fix the 405 error by telling the frontend where the API is located.

---

## Step 1: Open Vercel Dashboard

1. Go to: https://vercel.com/dashboard
2. Make sure you're logged in
3. You should see a list of your projects

**✅ Checkpoint:** Can you see your projects? Look for:
- `frontend`
- `api`
- `ward-logic`

**Tell me when you're ready for Step 2!**

---

## Step 2: Select the Frontend Project

1. Click on the **`frontend`** project
2. You should now be on the frontend project's overview page

**✅ Checkpoint:** Are you on the frontend project page? You should see:
- Project name: `frontend`
- Recent deployments
- Settings in the top navigation

**Tell me when you're ready for Step 3!**

---

## Step 3: Go to Settings

1. Click **"Settings"** in the top navigation bar
2. You should see a left sidebar with different settings sections

**✅ Checkpoint:** Can you see the Settings page with a left sidebar?

**Tell me when you're ready for Step 4!**

---

## Step 4: Open Environment Variables

1. In the left sidebar, look for **"Environment Variables"**
2. Click on it
3. You should see a page with environment variables (might be empty if none are set)

**✅ Checkpoint:** Are you on the Environment Variables page?

**Tell me when you're ready for Step 5!**

---

## Step 5: Add New Environment Variable

1. Click the **"Add New"** button (usually at the top right)
2. You should see a form with fields for:
   - Key
   - Value
   - Environments (checkboxes for Production, Preview, Development)

**✅ Checkpoint:** Do you see the "Add New" form?

**Tell me when you're ready for Step 6!**

---

## Step 6: Enter the Environment Variable

1. In the **"Key"** field, type exactly:
   ```
   REACT_APP_BACKEND_URL
   ```

2. In the **"Value"** field, type exactly:
   ```
   https://api-dbx3kihob-abhishek-vyas-projects.vercel.app
   ```

3. Check the boxes for:
   - ✅ Production
   - ✅ Preview
   - ✅ Development

**✅ Checkpoint:** Have you filled in all three fields and checked all three environments?

**Tell me when you're ready for Step 7!**

---

## Step 7: Save the Environment Variable

1. Click the **"Save"** button
2. You should see the new environment variable appear in the list

**✅ Checkpoint:** Do you see `REACT_APP_BACKEND_URL` in your environment variables list?

**Tell me when you're ready for Step 8!**

---

## Step 8: Go to Deployments

1. Click **"Deployments"** in the top navigation bar
2. You should see a list of deployments

**✅ Checkpoint:** Can you see the deployments list?

**Tell me when you're ready for Step 9!**

---

## Step 9: Redeploy the Frontend

1. Find the **latest deployment** (should be at the top)
2. Click the **"..."** (three dots) button on that deployment
3. Click **"Redeploy"** from the dropdown menu
4. You might see options - select **"Use existing Build Cache"** (optional)
5. Click **"Redeploy"** button

**✅ Checkpoint:** Has the redeployment started? You should see a new deployment being created.

**Tell me when the deployment is complete!**

---

## Step 10: Test the Fix

1. Wait for the deployment to complete (usually 1-2 minutes)
2. Visit: https://frontend-5s7sl9joj-abhishek-vyas-projects.vercel.app
3. Open browser console (F12)
4. Try to register or login
5. Check if you still see the 405 error

**✅ Checkpoint:** What do you see in the console? Any errors?

---

## 🎉 Done!

If everything worked:
- ✅ No more 405 errors
- ✅ API requests go to the correct domain
- ✅ Registration and login should work

If you see any issues, let me know what error you're getting!

