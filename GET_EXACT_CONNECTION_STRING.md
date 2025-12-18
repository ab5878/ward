# Get Exact Connection String from Supabase

**Password:** `Mridulahemant1*`

---

## 🎯 Step-by-Step Instructions

### 1. Go to Supabase Dashboard

Open: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd

### 2. Navigate to Database Settings

1. Click **Settings** (gear icon in left sidebar)
2. Click **Database** in the settings menu
3. Scroll down to **Connection string** section

### 3. Get Session Pooler Connection String (Recommended)

1. Click the **Connection Pooling** tab
2. You'll see different pooler modes
3. Select **Session pooler**
4. You'll see a connection string like:
   ```
   postgresql://postgres.gjwzaylkzknsykjvtpcd:[YOUR-PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
   ```
5. **Click the "Copy" button** next to the connection string
6. **Paste it into a text editor**
7. **Replace `[YOUR-PASSWORD]` with:** `Mridulahemant1*`

### 4. Alternative: Get Direct Connection String

If Session Pooler doesn't work:

1. Click the **URI** tab (under Connection string)
2. Copy the connection string
3. Replace `[YOUR-PASSWORD]` with: `Mridulahemant1*`

### 5. Update .env File

Edit `backend/.env` and update the line:

```bash
SUPABASE_DB_URL=<paste-the-connection-string-here>
```

**Example:**
```bash
SUPABASE_DB_URL=postgresql://postgres.gjwzaylkzknsykjvtpcd:Mridulahemant1*@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

### 6. Test Connection

```bash
cd /Users/abhishekvyas/ward/backend
python3 test_db_connection.py
```

---

## ⚠️ Important Notes

1. **Password with special characters:** If the connection string builder in Supabase doesn't handle `*` correctly, you may need to URL-encode it:
   - `*` → `%2A`
   - So: `Mridulahemant1*` → `Mridulahemant1%2A`

2. **Project must be active:** Make sure your Supabase project is not paused

3. **Exact format matters:** The connection string format from Supabase dashboard is the authoritative source

---

## 🔍 Verify Project Status

1. Go to: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd
2. Check if project shows as "Active" (not "Paused")
3. If paused, click "Restore" to resume it

---

## ✅ After Updating

1. Test: `python3 backend/test_db_connection.py`
2. Start server: `./start_server.sh`
3. Should see: `✅ Connected to Supabase PostgreSQL`

---

**Last Updated:** December 2024

