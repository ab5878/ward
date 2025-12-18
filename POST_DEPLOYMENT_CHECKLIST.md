# Post-Deployment Checklist
**After successful deployment, verify everything is working**

---

## ✅ Immediate Checks

### 1. Verify Deployment Status
- [ ] Backend deployed successfully
- [ ] Frontend deployed successfully
- [ ] No import errors in logs
- [ ] Functions are ready

### 2. Test Health Endpoint
```bash
curl https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2024-12-15T..."
}
```

### 3. Check Vercel Logs
- [ ] No ModuleNotFoundError
- [ ] No import errors
- [ ] Database connection successful
- [ ] No runtime errors

---

## 🔧 Configuration Steps

### 1. Disable Deployment Protection (If Needed)

If you see "Authentication Required":
1. Go to: https://vercel.com/dashboard
2. Select `api` project
3. Settings → Deployment Protection
4. Disable for preview/production

### 2. Set Environment Variables

**Backend (api project):**
- [ ] `SUPABASE_DB_URL` - Database connection string
- [ ] `JWT_SECRET` - Strong random secret
- [ ] `OPENAI_API_KEY` - (Optional) For AI features
- [ ] `SARVAM_API_KEY` - (Optional) For voice transcription
- [ ] `CORS_ORIGINS` - Allowed origins

**Frontend (frontend project):**
- [ ] `REACT_APP_API_URL` - Backend API URL

### 3. Run Database Migrations

Ensure all migrations are run:
```bash
# Connect to Supabase and run:
psql $SUPABASE_DB_URL -f supabase/migrations/001_initial_schema.sql
psql $SUPABASE_DB_URL -f supabase/migrations/002_api_v0_tables.sql
psql $SUPABASE_DB_URL -f supabase/migrations/003_operator_tables.sql
```

---

## 🧪 Testing Checklist

### API Endpoints
- [ ] `GET /api/health` - Health check
- [ ] `POST /api/auth/register` - User registration
- [ ] `POST /api/auth/login` - User login
- [ ] `GET /api/auth/me` - Get current user
- [ ] `POST /api/operators/create` - Create operator
- [ ] `GET /api/operators/dashboard` - Dashboard metrics

### Frontend
- [ ] Landing page loads
- [ ] Registration works
- [ ] Login works
- [ ] Dashboard loads
- [ ] Operator onboarding works
- [ ] Driver app accessible

### Operator Flow
- [ ] Create operator account
- [ ] Add fleet vehicles
- [ ] Generate magic links
- [ ] Driver can access app
- [ ] Driver can report disruption

---

## 🐛 Troubleshooting

### If Health Check Fails

1. **Check Logs:**
   ```bash
   vercel logs https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app
   ```

2. **Common Issues:**
   - Missing environment variables
   - Database connection failed
   - Import errors (should be fixed now)

### If Frontend Can't Connect to Backend

1. **Check API URL:**
   - Verify `REACT_APP_API_URL` is set correctly
   - Should be: `https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api`

2. **Check CORS:**
   - Verify `CORS_ORIGINS` includes frontend URL
   - Check browser console for CORS errors

### If Database Errors

1. **Verify Connection:**
   - Check `SUPABASE_DB_URL` is correct
   - Test connection from local machine

2. **Check Migrations:**
   - Ensure all migrations are run
   - Verify tables exist in Supabase

---

## 📊 Monitoring

### Set Up Monitoring
- [ ] Enable Vercel Analytics
- [ ] Set up error tracking
- [ ] Configure alerts
- [ ] Monitor API response times

### Key Metrics to Track
- API response times
- Error rates
- Database connection pool usage
- Function execution times

---

## 🚀 Next Steps

1. **Test Full Flow:**
   - Register → Login → Create Operator → Add Fleet → Generate Links → Test Driver App

2. **Onboard First Operator:**
   - Use real operator data
   - Test complete onboarding flow
   - Verify all features work

3. **Set Up Custom Domain:**
   - Configure `ward-logic.vercel.app` or custom domain
   - Update environment variables
   - Test with new domain

4. **Production Hardening:**
   - Set up monitoring
   - Configure backups
   - Review security settings
   - Set up rate limiting

---

## ✅ Success Criteria

- [ ] Health endpoint returns 200 OK
- [ ] No errors in Vercel logs
- [ ] Frontend loads successfully
- [ ] User can register and login
- [ ] Operator onboarding works
- [ ] Driver app is accessible
- [ ] All API endpoints respond correctly

---

**Last Updated:** December 2024

