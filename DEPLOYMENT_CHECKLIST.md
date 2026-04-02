# 🚀 Quick Deployment Checklist

## Pre-Deployment (Local)

- [x] Code cleaned and documented
- [x] Dependencies in requirements.txt
- [x] Migrations created and tested
- [x] Settings production-ready
- [x] Documentation files created

## Deploy to Render

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Production-ready finance API"
git push origin main
```

### Step 2: Create Render Web Service
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the repository

### Step 3: Configure Service
**Basic Settings:**
- Name: `finance-data-api` (or your choice)
- Region: Choose closest to you
- Branch: `main`
- Root Directory: (leave blank)
- Runtime: `Python 3`
- Auto-Deploy: `Yes`

**Build & Start:**
- Build Command: `pip install -r requirements.txt`
- Start Command: `./start.sh`

### Step 4: Environment Variables
Add these in Render dashboard:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Click "Generate" for random value |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `*.onrender.com,localhost,127.0.0.1` |
| `DATABASE_PATH` | `db.sqlite3` |
| `JWT_ACCESS_TOKEN_LIFETIME` | `60` |
| `JWT_REFRESH_TOKEN_LIFETIME` | `1440` |
| `CORS_ALLOWED_ORIGINS` | `*` (or your frontend URL) |

### Step 5: Deploy
- Click "Create web service"
- Wait for build (~2-5 minutes)
- Once deployed, note your URL: `https://your-app-name.onrender.com`

---

## Post-Deployment Testing

### Test 1: Health Check
Visit: `https://YOUR_APP.onrender.com/health/`
Expected: `{"status": "healthy", ...}`

### Test 2: API Documentation
Visit: `https://YOUR_APP.onrender.com/api/docs/`
Expected: Swagger UI with all endpoints

### Test 3: Get Token
```bash
curl -X POST https://YOUR_APP.onrender.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```
Expected: Access and refresh tokens

### Test 4: List Records
```bash
curl https://YOUR_APP.onrender.com/api/records/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
Expected: JSON array of records

### Test 5: Dashboard Summary
```bash
curl https://YOUR_APP.onrender.com/api/dashboard/summary/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
Expected: Summary statistics

---

## Troubleshooting

### Issue: Application won't start
**Check logs in Render dashboard**
- Missing dependencies? → Update requirements.txt
- Migration errors? → Check database settings
- Port binding? → Already handled in start.sh

### Issue: 500 Internal Server Error
**Check logs**
- SECRET_KEY not set? → Add to environment variables
- ALLOWED_HOSTS wrong? → Add your domain
- Database error? → Check DATABASE_PATH

### Issue: Can't access API
- CORS error? → Add your frontend to CORS_ALLOWED_ORIGINS
- 403 Forbidden? → Check JWT token is valid
- 404 Not Found? → Check URL paths

---

## Default Credentials

After deployment, default admin user is created:
- **Username:** `admin`
- **Password:** `admin123`

⚠️ **Change this immediately after deployment!**

To change password via API:
```bash
curl -X POST https://YOUR_APP.onrender.com/api/users/1/change-password/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"current_password":"admin123","new_password":"NEW_SECURE_PASSWORD"}'
```

---

## What's Working Out-of-the-Box

✅ SQLite database (file-based, no setup needed)
✅ Auto-migrations on startup
✅ Static files served via WhiteNoise
✅ JWT authentication
✅ Role-based permissions
✅ Swagger/OpenAPI docs
✅ CORS headers
✅ Security headers (HTTPS, HSTS, etc.)
✅ Gunicorn workers
✅ Health check endpoint

---

## Optional: PostgreSQL Setup

For better performance on Render:

1. Create PostgreSQL database on Render
2. Copy DATABASE_URL from Render dashboard
3. Add to environment variables:
   ```
   DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```
4. Redeploy (migrations will run automatically)

The app will automatically use PostgreSQL instead of SQLite.

---

## Monitoring

### View Logs
- Go to Render dashboard
- Select your service
- Click "Logs" tab
- Real-time application logs

### Metrics
- Response times
- Request counts
- Error rates
- Memory/CPU usage

All available in Render dashboard.

---

## Cost

**Free Tier Includes:**
- 750 hours/month (enough for 24/7)
- 100GB bandwidth/month
- Unlimited services
- Automatic SSL

**No credit card required for free tier!**

---

## Support

If you encounter issues:
1. Check Render logs first
2. Review this checklist
3. Check Django documentation
4. Review error messages carefully

Most issues are related to:
- Missing environment variables
- Incorrect ALLOWED_HOSTS
- Database migration problems
- Dependency conflicts

---

**You're ready to deploy!** 🎉

Good luck with your submission!
