# DEPLOYMENT GUIDE

## Deploying on Render.com

This guide walks you through deploying the Finance Data Processing API to Render.com.

### Prerequisites

1. GitHub account
2. Render.com account (free tier available)
3. Git installed locally

---

## Step 1: Prepare Your Repository

### Push Code to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Finance Data Processing Backend"

# Create main branch
git branch -M main

# Add your remote repository (replace with your repo URL)
git remote add origin https://github.com/your-username/your-repository.git

# Push to GitHub
git push -u origin main
```

---

## Step 2: Deploy on Render.com

### Option A: Using render.yaml (Recommended)

1. **Go to [Render.com](https://render.com)**
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub account
4. Select your repository
5. Render will automatically detect `render.yaml`
6. Click **"Apply"**

The service will be created with all settings from `render.yaml`.

### Option B: Manual Setup

1. **Create New Web Service**
   - Go to Dashboard → New + → Web Service
   - Connect your GitHub repository
   - Select the repository

2. **Configure Settings**
   ```
   Name: finance-data-api
   Region: Oregon (or closest to you)
   Branch: main
   Root Directory: (leave blank)
   Runtime: Python 3
   ```

3. **Build & Start Commands**
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn finance_api.wsgi:application
   ```

4. **Choose Plan**
   - Select **Free** plan for testing
   - Upgrade later if needed

5. **Advanced Settings**
   - Auto-Deploy: Enabled (default)
   - Health Check Path: `/api/docs/`

---

## Step 3: Configure Environment Variables

In Render Dashboard, go to **Environment** tab and add:

```bash
# Security
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=*

# Database (SQLite for simplicity)
DATABASE_PATH=db.sqlite3

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60
JWT_REFRESH_TOKEN_LIFETIME=1440

# CORS (Add your frontend URL)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.com
```

**Important:** 
- Set `DEBUG=False` in production
- Generate a strong `SECRET_KEY` using: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
- Update `ALLOWED_HOSTS` with your actual domain

---

## Step 4: Deploy and Run Migrations

### Initial Deployment

1. Click **"Create Web Service"**
2. Wait for build to complete (~2-5 minutes)
3. Once deployed, open the web service URL

### Run Database Migrations

You need to run migrations after deployment:

#### Method 1: Render Shell (Recommended)

1. In Render Dashboard, click on your service
2. Go to **"Shell"** tab
3. Click **"New Shell"**
4. Run commands:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

#### Method 2: One-Time Script

Create a startup script that runs migrations before starting the server:

```bash
# Add to render.yaml or manually run in shell
python manage.py migrate --noinput
```

---

## Step 5: Access Your API

### Get Your Production URL

Your API will be available at:
```
https://finance-data-api.onrender.com
```

### Test Endpoints

1. **API Documentation**: 
   ```
   https://finance-data-api.onrender.com/api/docs/
   ```

2. **Admin Panel**:
   ```
   https://finance-data-api.onrender.com/admin/
   ```

3. **Health Check**:
   ```
   https://finance-data-api.onrender.com/api/dashboard/summary/
   ```

---

## Step 6: Create Initial Admin User

After running migrations and creating superuser:

1. Go to admin panel: `https://your-app.onrender.com/admin/`
2. Login with credentials created during `createsuperuser`
3. Create additional users through admin interface or API

---

## Production Checklist

Before going live:

- [ ] Set `DEBUG = False`
- [ ] Generate strong `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up proper `CORS_ALLOWED_ORIGINS`
- [ ] Run database migrations
- [ ] Create admin superuser
- [ ] Test all API endpoints
- [ ] Review security settings
- [ ] Set up monitoring (Render provides basic monitoring)

---

## Troubleshooting

### Issue: Static Files Not Loading

**Solution:** WhiteNoise is already configured. Ensure:
```python
# settings.py
MIDDLEWARE = [
    # ... other middleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
]
```

### Issue: Database Errors

**Solution:** Make sure migrations are run:
```bash
python manage.py migrate
```

### Issue: CORS Errors

**Solution:** Update CORS origins in environment variables:
```bash
CORS_ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:3000
```

### Issue: 500 Internal Server Error

**Solution:** Check logs in Render Dashboard → Logs tab
Common fixes:
- Missing environment variables
- Database not migrated
- Import errors (check requirements.txt)

---

## Monitoring & Maintenance

### View Logs

In Render Dashboard:
- **Logs Tab**: Real-time application logs
- **Events Tab**: Deployment history

### Auto-Deploy

Every push to the `main` branch triggers automatic deployment.

### Manual Redeploy

If needed:
1. Go to Render Dashboard
2. Click **"Manual Deploy"**
3. Select branch and deploy

---

## Database Backup (Important!)

Since we're using SQLite:

### Download Database File

1. Connect via SSH or use Render Shell
2. Download the `db.sqlite3` file
3. Store securely

### Recommendation for Production

For better reliability, consider upgrading to PostgreSQL:

1. Create PostgreSQL database on Render
2. Install psycopg2-binary (already in requirements.txt)
3. Update DATABASES setting in settings.py:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'HOST': config('DB_HOST'),
           'NAME': config('DB_NAME'),
           'USER': config('DB_USER'),
           'PASSWORD': config('DB_PASSWORD'),
           'PORT': '5432',
       }
   }
   ```

---

## Cost Estimation

### Free Tier Includes:
- 750 hours/month (enough for one service running 24/7)
- 100GB bandwidth/month
- Basic monitoring

### Paid Plans (if needed):
- Starter: $7/month
- Standard: Varies by usage

---

## Support Resources

- [Render Documentation](https://render.com/docs)
- [Django Deployment Guide](https://docs.djangoproject.com/en/stable/howto/deployment/)
- [DRF Best Practices](https://www.django-rest-framework.org/)

---

## Next Steps

After successful deployment:

1. ✅ Share API documentation URL with team
2. ✅ Test all endpoints with tools like Postman
3. ✅ Set up frontend integration
4. ✅ Monitor usage and performance
5. ✅ Implement rate limiting if needed
6. ✅ Set up error tracking (e.g., Sentry)

---

**Deployment Complete! 🚀**

Your Finance Data Processing API is now live and ready to use!
