# Deployment Guide for Render.com

## Files Updated for Production

The following files have been configured for production deployment:

1. **requirements.txt** - All dependencies including PostgreSQL support
2. **render.yaml** - Render.com service configuration
3. **start.sh** - Startup script for migrations and static files
4. **settings.py** - Production-ready database and security settings
5. **.gitignore** - Prevents sensitive files from being uploaded

## Environment Variables Required on Render

When deploying to Render.com, configure these environment variables:

### Required Variables:
- `SECRET_KEY`: Generate a long random string (use Django's `get_random_secret_key()`)
- `DEBUG`: Set to `False`
- `ALLOWED_HOSTS`: `finance-data-api-saav.onrender.com,localhost,127.0.0.1`
- `DATABASE_PATH`: `db.sqlite3` (fallback if DATABASE_URL not set)
- `JWT_ACCESS_TOKEN_LIFETIME`: `60` (minutes)
- `JWT_REFRESH_TOKEN_LIFETIME`: `1440` (minutes = 24 hours)
- `CORS_ALLOWED_ORIGINS`: `*` (or specify your frontend URL)

### Optional (Render auto-provides):
- `DATABASE_URL`: Automatically provided by Render when you attach a PostgreSQL database
- `PORT`: Automatically provided by Render

## Deployment Steps on Render

### Step 1: Push Code to GitHub
```bash
git add .
git commit -m "Production ready deployment configuration"
git push origin main
```

### Step 2: Create New Web Service on Render
1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the `main` branch

### Step 3: Configure the Service
- **Name**: finance-data-api
- **Environment**: Python
- **Region**: Oregon (or closest to you)
- **Branch**: main
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `./start.sh`

### Step 4: Add Environment Variables
Click "Environment" tab and add all the variables listed above.

### Step 5: Attach PostgreSQL Database (Recommended)
1. In Render dashboard, click "New +" → "PostgreSQL"
2. Choose free tier
3. After creation, go back to your web service
4. Click "Add Database" and select your PostgreSQL instance
5. Render will automatically set `DATABASE_URL` environment variable

### Step 6: Deploy
1. Click "Save Changes"
2. Render will start building and deploying
3. Monitor logs in the "Logs" tab

## Post-Deployment Tasks

### Run Migrations (if not using start.sh)
```bash
python manage.py migrate --noinput
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

## Testing the Deployment

After deployment completes:

1. **Health Check**: Visit `https://finance-data-api-saav.onrender.com/`
   - Should return JSON response (not 500 error)

2. **API Documentation**: Visit `https://finance-data-api-saav.onrender.com/api/docs/`
   - Should show Swagger UI with all endpoints

3. **Alternative Docs**: Visit `https://finance-data-api-saav.onrender.com/api/redoc/`
   - Should show ReDoc documentation

4. **Admin Panel**: Visit `https://finance-data-api-saav.onrender.com/admin/`
   - Login with superuser credentials

## Troubleshooting

### Issue: Internal Server Error (500)
**Possible causes:**
- Missing environment variables
- Database connection issues
- SECRET_KEY not set properly

**Solution:**
1. Check Render logs in dashboard
2. Verify all environment variables are set
3. Ensure DATABASE_URL is correctly configured

### Issue: Database Migration Errors
**Solution:**
```bash
# SSH into Render or run locally with production DB
python manage.py migrate
python manage.py migrate --run-syncdb
```

### Issue: Static Files Not Loading
**Solution:**
```bash
python manage.py collectstatic --noinput --clear
```

### Issue: CORS Errors
**Solution:**
- Update `CORS_ALLOWED_ORIGINS` to include your frontend domain
- For testing, use `*` (not recommended for production)

## Security Notes

✅ **Production Settings Enabled:**
- HTTPS redirect (when DEBUG=False)
- Secure cookies
- HSTS (HTTP Strict Transport Security)
- XSS Protection
- Content Type sniffing protection
- Clickjacking protection

⚠️ **Important:**
- Never commit `.env` files or secrets to GitHub
- Use Render's environment variable UI for all secrets
- Keep DEBUG=False in production
- Change SECRET_KEY regularly

## Monitoring

- **Logs**: Available in Render dashboard under "Logs" tab
- **Metrics**: CPU, Memory, and Request stats in "Metrics" tab
- **Incidents**: Render will notify you of any downtime

## Next Steps

1. Test all API endpoints
2. Create initial admin user
3. Set up monitoring alerts
4. Consider upgrading to paid plan for better performance
5. Set up automated backups for PostgreSQL

## Support

If you encounter issues:
1. Check Render logs first
2. Verify environment variables
3. Test locally with production settings
4. Consult Django deployment documentation
5. Check Render community forums
