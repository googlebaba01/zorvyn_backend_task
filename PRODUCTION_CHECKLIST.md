# 🚀 Production Deployment Checklist for Render.com

## ✅ Pre-Deployment Verification

### 1. Environment Variables (Set in Render Dashboard)
```bash
# REQUIRED - Generate at https://djecrety.ir/
SECRET_KEY=your-super-secret-key-min-50-chars-random

# REQUIRED - Must be False in production
DEBUG=False

# REQUIRED - Your Render domain
ALLOWED_HOSTS=finance-data-api-saav.onrender.com,localhost,127.0.0.1

# OPTIONAL - SQLite fallback path
DATABASE_PATH=db.sqlite3

# JWT Settings (in minutes)
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# CORS (use * for testing, specific URL for production)
CORS_ALLOWED_ORIGINS=*
```

### 2. Render Service Configuration
- ✅ **Build Command**: `pip install -r requirements.txt`
- ✅ **Start Command**: `./start.sh`
- ✅ **Environment**: Python
- ✅ **Region**: Oregon (or closest to you)
- ✅ **Branch**: main

### 3. Database Setup
**Option A: PostgreSQL (Recommended)**
1. Create PostgreSQL database on Render
2. Attach to web service
3. `DATABASE_URL` will be set automatically
4. App will use PostgreSQL instead of SQLite

**Option B: SQLite (Free Tier)**
- Uses `db.sqlite3` file
- No additional setup needed
- Data persists in Render's ephemeral storage

---

## 🔧 Deployment Steps

### Step 1: Test Locally with Production Settings
```bash
# Set production-like environment locally
export DEBUG=False
export SECRET_KEY=test-key-for-local-prod-testing
export ALLOWED_HOSTS=localhost,127.0.0.1

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Test the server
python manage.py runserver
```

### Step 2: Commit and Push to GitHub
```bash
git add .
git commit -m "Production deployment - fixed root endpoint and settings"
git push origin main
```

### Step 3: Deploy on Render
1. Go to https://dashboard.render.com
2. Select your service: **finance-data-api**
3. Click **"Manual Deploy"** → **"Deploy latest commit"**
4. Wait 2-3 minutes for build and deploy

### Step 4: Verify Deployment
After deployment completes, test these URLs:

#### ✅ Health Check (Should work immediately)
```
https://finance-data-api-saav.onrender.com/
https://finance-data-api-saav.onrender.com/health/
```

**Expected Response:**
```json
{
  "status": "healthy",
  "message": "Finance Data Processing API is running",
  "timestamp": "2024-04-02T12:34:56.789",
  "version": "1.0.0"
}
```

#### ✅ API Documentation
```
https://finance-data-api-saav.onrender.com/api/docs/
https://finance-data-api-saav.onrender.com/api/redoc/
```

#### ✅ Admin Panel
```
https://finance-data-api-saav.onrender.com/admin/
```
- Username: `admin`
- Password: `admin123` (⚠️ Change this!)

#### ✅ Authentication Endpoints
```bash
# Login (get token)
POST https://finance-data-api-saav.onrender.com/api/token/
Body: {"username": "admin", "password": "admin123"}

# Refresh token
POST https://finance-data-api-saav.onrender.com/api/token/refresh/
Body: {"refresh": "your-refresh-token"}
```

---

## 🐛 Troubleshooting

### Issue: Still Getting 500 Error

**Check Render Logs:**
1. Go to Render dashboard
2. Click on your service
3. Go to **"Logs"** tab
4. Look for errors

**Common Causes:**
- ❌ Missing `SECRET_KEY` environment variable
- ❌ `DEBUG=True` in production
- ❌ Missing `ALLOWED_HOSTS` configuration
- ❌ Database migration failures
- ❌ Static files not collected

**Solution:**
```bash
# In Render Shell, run manually:
python manage.py migrate
python manage.py collectstatic --noinput --clear
python manage.py createsuperuser
```

### Issue: Database Errors

**SQLite → PostgreSQL Migration:**
```bash
# If using PostgreSQL, ensure DATABASE_URL is set
# Check in Render dashboard → Environment

# Run migrations
python manage.py migrate --run-syncdb
```

### Issue: Static Files Not Loading

**Fix:**
```bash
# In Render Shell:
python manage.py collectstatic --noinput --clear
```

### Issue: Can't Access Admin Panel

**Create Superuser:**
```bash
# In Render Shell:
python manage.py createsuperuser
# Follow prompts to set username/email/password
```

**Or use default:**
- Username: `admin`
- Password: `admin123`

---

## 🔒 Security Hardening (Post-Deployment)

### 1. Change Default Superuser Password
```bash
# In Render Shell:
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> admin = User.objects.get(username='admin')
>>> admin.set_password('your-new-strong-password')
>>> admin.save()
```

### 2. Update CORS Settings
Replace `*` with your actual frontend URL:
```bash
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

### 3. Rotate SECRET_KEY
Generate new key at https://djecrety.ir/ and update in Render dashboard.

### 4. Enable HTTPS Redirect
Already enabled in `settings.py` when `DEBUG=False`.

---

## 📊 Monitoring

### Health Check Endpoint
```bash
GET https://finance-data-api-saav.onrender.com/health/
```

**Monitor:**
- Response time < 500ms
- Status: "healthy"
- Timestamp updates

### Render Metrics
- **CPU Usage**: Should be < 50% on free tier
- **Memory**: Should be < 512MB
- **Requests**: Track daily limits

### Application Logs
Check daily for:
- 500 errors
- Database connection issues
- Authentication failures

---

## 🎯 Testing All Endpoints

### 1. User Management
```bash
# List users (requires auth)
GET /api/users/
Authorization: Bearer {access_token}

# Create user (admin only)
POST /api/users/
Content-Type: application/json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "securepass123",
  "role": "analyst"
}
```

### 2. Financial Records
```bash
# List records
GET /api/records/?record_type=income

# Create record
POST /api/records/
{
  "title": "Salary",
  "amount": 5000.00,
  "record_type": "income",
  "category": "salary",
  "date": "2024-04-01"
}
```

### 3. Dashboard Analytics
```bash
# Summary
GET /api/dashboard/summary/

# Monthly trends
GET /api/dashboard/monthly-trends/?months=6

# Category breakdown
GET /api/dashboard/category-breakdown/?record_type=expense
```

---

## 📝 Important Notes

### ⚠️ Free Tier Limitations
- **Spin Down**: Service sleeps after 15 min inactivity
- **First Request**: Takes 30-50 seconds to wake up
- **Database**: SQLite data may reset (use PostgreSQL for persistence)
- **Hours/Month**: 750 hours free tier limit

### 💡 Best Practices
1. **Use PostgreSQL** for production data persistence
2. **Set strong SECRET_KEY** (50+ random characters)
3. **Keep DEBUG=False** always in production
4. **Monitor logs** daily for errors
5. **Backup database** regularly if using PostgreSQL
6. **Update dependencies** monthly

### 🆘 Support Resources
- **Render Docs**: https://render.com/docs
- **Django Docs**: https://docs.djangoproject.com
- **DRF Docs**: https://www.django-rest-framework.org
- **Community**: Render forums, Stack Overflow

---

## ✨ Success Criteria

Your deployment is successful when:
- ✅ `/` returns API info (not 500 error)
- ✅ `/health/` returns healthy status
- ✅ `/api/docs/` loads Swagger UI
- ✅ `/admin/` accessible with superuser credentials
- ✅ All CRUD endpoints work with authentication
- ✅ No 500 errors in Render logs
- ✅ Response time < 1 second

---

**Last Updated**: April 2026  
**Version**: 1.0.0  
**Status**: Production Ready ✅
