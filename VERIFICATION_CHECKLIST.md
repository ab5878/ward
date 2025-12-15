# Ward Deployment Verification Checklist

This checklist helps verify that all components of Ward are properly deployed and functioning.

## ✅ Backend API (Vercel)

### Health Checks
- [ ] **Basic Health**: `GET /api/health`
  - Expected: `200 OK` with `{"status": "healthy", "database": "connected"}`
  - Command: `curl https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api/health`

- [ ] **Detailed Health**: `GET /api/health/detailed`
  - Expected: `200 OK` with detailed system status
  - Command: `curl https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api/health/detailed`

### Authentication
- [ ] **User Registration**: `POST /api/register`
  - Expected: `201 Created` with JWT token
  - Test: `curl -X POST https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api/register -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"Test123456"}'`

- [ ] **User Login**: `POST /api/login`
  - Expected: `200 OK` with JWT token
  - Test: `curl -X POST https://api-f24h6n5ld-abhishek-vyas-projects.vercel.app/api/login -H "Content-Type: application/json" -d '{"email":"test@example.com","password":"Test123456"}'`

### Protected Endpoints
- [ ] **Get Cases**: `GET /api/cases` (requires auth token)
- [ ] **Create Case**: `POST /api/cases` (requires auth token)
- [ ] **Operator Dashboard**: `GET /api/operators/dashboard` (requires auth token)

### Operator Endpoints
- [ ] **Create Operator**: `POST /api/operators` (requires auth token)
- [ ] **Add Fleet Vehicle**: `POST /api/operators/fleet` (requires auth token)
- [ ] **Get Fleet**: `GET /api/operators/fleet` (requires auth token)
- [ ] **Generate Magic Link**: `POST /api/operators/magic-links` (requires auth token)

## ✅ Frontend (Vercel)

### Basic Access
- [ ] **Homepage loads**: `https://ward-logic.vercel.app`
- [ ] **No console errors**: Check browser console
- [ ] **API connection**: Frontend can reach backend API

### Authentication Flow
- [ ] **Registration page**: `/register` loads correctly
- [ ] **Login page**: `/login` loads correctly
- [ ] **Registration works**: Can create new user account
- [ ] **Login works**: Can login with existing credentials
- [ ] **Token storage**: JWT token is stored in localStorage
- [ ] **Protected routes**: Redirects to login if not authenticated

### Dashboard
- [ ] **Dashboard loads**: `/dashboard` accessible after login
- [ ] **Cases list**: Can view cases (if any)
- [ ] **Navigation**: All navigation links work

### Operator Features
- [ ] **Operator Onboarding**: `/operator/onboard` accessible
- [ ] **Fleet Management**: Can add/view fleet vehicles
- [ ] **Magic Links**: Can generate magic links for drivers
- [ ] **Driver App**: Magic link works for driver reporting

## ✅ Database (Supabase)

### Connection
- [ ] **Database accessible**: Backend can connect to Supabase
- [ ] **Migrations applied**: All migrations (001, 002, 003) are applied
- [ ] **Tables exist**: Check for `users`, `cases`, `operators`, `fleet_vehicles`, etc.

### Data Integrity
- [ ] **User creation**: Users can be created via API
- [ ] **Password hashing**: Passwords are hashed (not plain text)
- [ ] **Foreign keys**: Relationships between tables work correctly

## ✅ Environment Variables

### Backend (api project)
- [ ] `SUPABASE_DB_URL`: Set and correct
- [ ] `JWT_SECRET`: Set and secure
- [ ] `CORS_ORIGINS`: Includes frontend URL
- [ ] `OPENAI_API_KEY`: Set (if using AI features)
- [ ] `SARVAM_API_KEY`: Set (if using voice features)

### Frontend (frontend project)
- [ ] `REACT_APP_API_URL`: Points to backend API URL

## 🧪 Quick Test Script

Run the automated test script:
```bash
./test_api_endpoints.sh
```

Or set custom API URL:
```bash
REACT_APP_API_URL=https://your-api-url.vercel.app/api ./test_api_endpoints.sh
```

## 📋 Production Readiness

### Security
- [ ] **HTTPS enabled**: All URLs use HTTPS
- [ ] **CORS configured**: Only allowed origins can access API
- [ ] **JWT secret**: Strong, unique secret used
- [ ] **Environment variables**: Not exposed in client-side code

### Performance
- [ ] **API response times**: < 500ms for most endpoints
- [ ] **Frontend load time**: < 3 seconds
- [ ] **Database queries**: Optimized and indexed

### Monitoring
- [ ] **Error logging**: Errors are logged and visible
- [ ] **Health checks**: Monitoring health endpoints
- [ ] **Uptime**: Service is stable and available

## 🚨 Common Issues

### Backend Issues
- **404 on `/`**: ✅ Expected - API doesn't have root route
- **404 on `/favicon.ico`**: ✅ Expected - Browser request, not an error
- **ModuleNotFoundError**: Check that all dependencies are in `requirements.txt`
- **Database connection errors**: Verify `SUPABASE_DB_URL` is correct

### Frontend Issues
- **CORS errors**: Check `CORS_ORIGINS` includes frontend URL
- **API connection errors**: Verify `REACT_APP_API_URL` is correct
- **Build failures**: Check React version compatibility (should be 18.3.1)

### Database Issues
- **Migration errors**: Run migrations in order (001, 002, 003)
- **Connection pool errors**: Check Supabase connection pooler settings
- **Foreign key violations**: Ensure related records exist before creating references

## 📞 Support

If you encounter issues:
1. Check Vercel deployment logs
2. Check Supabase logs
3. Run `test_api_endpoints.sh` to diagnose API issues
4. Check browser console for frontend errors

