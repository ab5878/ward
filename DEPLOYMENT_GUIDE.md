# Ward Deployment Guide

**Date:** December 2024  
**Status:** Ready for Production Deployment

---

## 🚀 Quick Deployment Steps

### 1. Verify Prerequisites

- [ ] Supabase database set up
- [ ] Database migrations run (001_initial_schema.sql, 002_api_v0_tables.sql)
- [ ] Environment variables ready
- [ ] Vercel account connected

### 2. Set Environment Variables in Vercel

Go to Vercel Dashboard → Project Settings → Environment Variables

**Required Variables:**
```
SUPABASE_DB_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres?pgbouncer=true
JWT_SECRET=your-secret-key-change-in-production
CORS_ORIGINS=https://ward-logic.vercel.app,https://your-custom-domain.com
OPENAI_API_KEY=sk-... (optional, for AI features)
SARVAM_API_KEY=... (optional, for voice features)
REACT_APP_BACKEND_URL=https://ward-logic.vercel.app
```

**Important:** Use the **Session Pooler** connection string from Supabase (not the direct connection).

### 3. Deploy to Vercel

```bash
cd /Users/abhishekvyas/ward
vercel --prod
```

Or push to GitHub to trigger auto-deployment.

### 4. Verify Deployment

1. **Check Health Endpoint:**
   ```bash
   curl https://ward-logic.vercel.app/api/health
   ```
   Should return: `{"status":"ok","database":"connected",...}`

2. **Test Frontend:**
   - Visit: https://ward-logic.vercel.app
   - Verify landing page loads
   - Test navigation links

3. **Test Authentication:**
   - Register a new user
   - Login with registered user
   - Verify JWT token is stored

4. **Test API v0 Endpoints:**
   ```bash
   python3 backend/test_api_v0_http.py https://ward-logic.vercel.app
   ```

---

## 📋 Pre-Deployment Checklist

### Database
- [x] Migration 001_initial_schema.sql run
- [x] Migration 002_api_v0_tables.sql run
- [x] All tables exist (users, cases, timeline_events, facilities, parties, dispute_packets, attachments)
- [x] Indexes created
- [x] Connection pooler configured

### Backend
- [x] All API v0 endpoints implemented (18 endpoints)
- [x] Database adapter methods working
- [x] Authentication working
- [x] Error handling in place
- [x] CORS configured

### Frontend
- [x] Landing page complete
- [x] All routes configured
- [x] API service configured
- [x] Build succeeds (`yarn build`)

### Testing
- [x] Structure tests passing
- [x] No linting errors
- [x] All imports working

---

## 🔧 Environment Variables Reference

### Backend (Vercel)

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_DB_URL` | ✅ Yes | PostgreSQL connection string (Session Pooler) |
| `JWT_SECRET` | ✅ Yes | Secret key for JWT tokens |
| `CORS_ORIGINS` | ✅ Yes | Comma-separated list of allowed origins |
| `OPENAI_API_KEY` | ⚠️ Optional | For AI features (decision generation, RCA) |
| `SARVAM_API_KEY` | ⚠️ Optional | For voice transcription (Indian languages) |

### Frontend (Vercel)

| Variable | Required | Description |
|----------|----------|-------------|
| `REACT_APP_BACKEND_URL` | ✅ Yes | Backend URL (e.g., `https://ward-logic.vercel.app`) |

---

## 🐛 Troubleshooting

### Database Connection Issues

**Error:** `[Errno 99] Cannot assign requested address`

**Solution:**
1. Verify `SUPABASE_DB_URL` uses Session Pooler (port 6543)
2. Check connection string format: `postgresql://postgres:[PASSWORD]@[HOST]:6543/postgres?pgbouncer=true`
3. Verify IP is whitelisted in Supabase (Settings → Database → Connection pooling)

### CORS Errors

**Error:** `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution:**
1. Add your domain to `CORS_ORIGINS` in Vercel environment variables
2. Format: `https://ward-logic.vercel.app,https://your-domain.com`
3. Redeploy after updating environment variables

### 404 Errors on API Endpoints

**Error:** `404 Not Found` on `/api/v0/*` endpoints

**Solution:**
1. Verify `vercel.json` has correct rewrite rules
2. Check `api/index.py` exists and imports `server.py` correctly
3. Verify backend code is not in `.vercelignore`

### Build Failures

**Error:** `Module not found` or build errors

**Solution:**
1. Check `api/requirements.txt` has all dependencies
2. Check `frontend/package.json` has all dependencies
3. Verify build commands in `vercel.json` are correct

---

## 📊 Post-Deployment Verification

### 1. Health Check
```bash
curl https://ward-logic.vercel.app/api/health
```

Expected: `{"status":"ok","database":"connected",...}`

### 2. Test Authentication Flow
1. Register: `POST /api/auth/register`
2. Login: `POST /api/auth/login`
3. Get user: `GET /api/auth/me`

### 3. Test API v0 Endpoints
```bash
# After authentication, test:
POST /api/v0/facilities
GET /api/v0/facilities
POST /api/v0/parties
GET /api/v0/parties
POST /api/v0/movements
GET /api/v0/movements
```

### 4. Test Frontend
1. Visit landing page
2. Navigate to all pages
3. Test registration/login flow
4. Test dashboard (if logged in)

---

## 🔄 Continuous Deployment

### GitHub Integration

1. Connect GitHub repo to Vercel
2. Push to `main` branch triggers auto-deployment
3. Preview deployments for pull requests

### Manual Deployment

```bash
vercel --prod
```

### Rollback

1. Go to Vercel Dashboard → Deployments
2. Find previous successful deployment
3. Click "..." → "Promote to Production"

---

## 📈 Monitoring

### Vercel Function Logs

1. Go to Vercel Dashboard → Deployments
2. Click on deployment → Functions tab
3. View real-time logs

### Database Monitoring

1. Go to Supabase Dashboard → Database → Logs
2. Monitor query performance
3. Check connection pool usage

### Error Tracking

- Check Vercel function logs for errors
- Check browser console for frontend errors
- Monitor API response times

---

## 🎯 Next Steps After Deployment

1. **Test All Features**
   - Registration and login
   - Case creation
   - Dispute packet generation
   - API v0 endpoints

2. **Frontend Integration**
   - Update web console to use API v0 endpoints
   - Add facility/party selection
   - Integrate dispute packet generation

3. **Mobile App** (Future)
   - Use `/api/v0/events` for incident logging
   - Use `/api/v0/attachments` for photo/audio uploads

4. **Lighthouse Customers**
   - Onboard first customers
   - Run experiments per GTM playbook
   - Collect feedback and iterate

---

## 📞 Support

If deployment fails:

1. Check Vercel function logs
2. Verify environment variables
3. Check database connection
4. Review error messages in logs
5. Test locally first: `cd backend && python3 -m uvicorn server:app --port 8001`

---

**Last Updated:** December 2024  
**Status:** ✅ Ready for Deployment

