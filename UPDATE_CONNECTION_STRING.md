# Update Supabase Connection String

**Password:** `Mridulahemant1*`

---

## 🔧 Quick Steps

### 1. Get Connection String from Supabase

1. Go to: https://supabase.com/dashboard/project/gjwzaylkzknsykjvtpcd
2. Navigate to: **Settings** → **Database**
3. Scroll to **Connection string** section

### 2. Choose Connection Type

**Option A: Session Pooler (Recommended for local dev)**
- Click **Connection Pooling** tab
- Select **Session pooler**
- Copy the connection string
- It will look like:
  ```
  postgresql://postgres.gjwzaylkzknsykjvtpcd:[YOUR-PASSWORD]@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
  ```

**Option B: Direct Connection**
- Click **URI** tab
- Copy the connection string
- It will look like:
  ```
  postgresql://postgres:[YOUR-PASSWORD]@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres
  ```

### 3. Replace Password

Replace `[YOUR-PASSWORD]` with: `Mridulahemant1*`

**Important:** If copying directly from Supabase, the password field might be empty. You need to manually insert the password.

### 4. Update .env File

Edit `backend/.env`:

```bash
SUPABASE_DB_URL=postgresql://postgres.gjwzaylkzknsykjvtpcd:Mridulahemant1*@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

**Note:** If the password contains special characters like `*`, you may need to URL-encode it:
- `*` becomes `%2A`
- So: `Mridulahemant1*` → `Mridulahemant1%2A`

### 5. Test Connection

```bash
cd /Users/abhishekvyas/ward/backend
python3 test_db_connection.py
```

---

## 🎯 Expected Connection Strings

Based on your project ref `gjwzaylkzknsykjvtpcd`:

### Session Pooler:
```
postgresql://postgres.gjwzaylkzknsykjvtpcd:Mridulahemant1*@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
```

### Direct Connection (if pooler doesn't work):
```
postgresql://postgres:Mridulahemant1*@db.gjwzaylkzknsykjvtpcd.supabase.co:5432/postgres
```

---

## ✅ After Updating

1. Test connection:
   ```bash
   cd backend && python3 test_db_connection.py
   ```

2. Start server:
   ```bash
   ./start_server.sh
   ```

3. You should see:
   ```
   ✅ Connected to Supabase PostgreSQL
   ```

---

**Last Updated:** December 2024

