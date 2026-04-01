# Quick Start Guide

## Getting Started in 5 Minutes

This guide will help you get the Finance Data Processing API up and running quickly.

---

## Step 1: Installation

### Clone or Navigate to Project

```bash
cd c:\Users\Asus\OneDrive\Desktop\zorvyn_backend
```

### Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/Mac
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Step 2: Initial Setup

### Create Environment File

```bash
# Copy example env file
copy .env.example .env  # Windows
cp .env.example .env    # Linux/Mac
```

The default settings work out of the box for development. No changes needed!

### Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Admin User

```bash
python manage.py createsuperuser
```

Enter:
- Username: admin
- Email: admin@example.com
- Password: (choose a secure password)

---

## Step 3: Populate Sample Data (Optional)

To quickly populate the database with test users and sample financial records:

```bash
python manage.py populate_sample_data
```

This creates:
- ✅ 3 test users (admin, analyst, viewer)
- ✅ 50+ sample financial records
- ✅ Mix of income and expenses

**Default Credentials:**
```
Admin:   username=admin, password=admin123
Analyst: username=analyst_user, password=analyst123
Viewer:  username=viewer_user, password=viewer123
```

---

## Step 4: Start Development Server

```bash
python manage.py runserver
```

Your API is now running at: **http://127.0.0.1:8000/**

---

## Step 5: Explore the API

### 1. API Documentation (Swagger UI)

Visit: **http://127.0.0.1:8000/api/docs/**

Interactive documentation where you can:
- View all endpoints
- Test APIs directly from browser
- See request/response schemas

### 2. Alternative Documentation (ReDoc)

Visit: **http://127.0.0.1:8000/api/redoc/**

Clean, readable documentation format.

### 3. Django Admin Panel

Visit: **http://127.0.0.1:8000/admin/**

Manage users and records through the admin interface.

---

## Step 6: Make Your First API Calls

### Get Authentication Token

```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

Response:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### List Financial Records

```bash
curl http://127.0.0.1:8000/api/records/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Dashboard Summary

```bash
curl http://127.0.0.1:8000/api/dashboard/summary/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Common Tasks

### Create a New User (as Admin)

```bash
curl -X POST http://127.0.0.1:8000/api/users/ \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "securepass123",
    "role": "analyst"
  }'
```

### Create a Financial Record

```bash
curl -X POST http://127.0.0.1:8000/api/records/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1500.00,
    "record_type": "income",
    "category": "freelance",
    "date": "2024-04-01",
    "description": "Freelance project payment"
  }'
```

### Filter Records by Category

```bash
curl "http://127.0.0.1:8000/api/records/?category=salary&record_type=income" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Get Monthly Trends

```bash
curl "http://127.0.0.1:8000/api/dashboard/monthly-trends/?months=6" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Testing Different Roles

### As Viewer (Read-Only)

1. Login with viewer credentials
2. Try to view records: ✅ Works
3. Try to create record: ❌ Forbidden (403)

### As Analyst (Create & Read)

1. Login with analyst credentials
2. Create records: ✅ Works
3. Update own records: ✅ Works
4. Delete records: ❌ Forbidden (403)

### As Admin (Full Access)

1. Login with admin credentials
2. All operations: ✅ Works

---

## Troubleshooting

### Port Already in Use

```bash
# Run on different port
python manage.py runserver 8001
```

### Database Errors

```bash
# Delete database and migrate again
rm db.sqlite3  # Linux/Mac
del db.sqlite3  # Windows

python manage.py makemigrations
python manage.py migrate
```

### Import Errors

```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

---

## Next Steps

1. ✅ **Explore API Documentation**: http://127.0.0.1:8000/api/docs/
2. ✅ **Test Different Endpoints**: Try all CRUD operations
3. ✅ **Experiment with Roles**: Test viewer, analyst, admin permissions
4. ✅ **Check Filtering**: Try various filter combinations
5. ✅ **Review Code**: Study the implementation in each app folder

---

## Development Workflow

### Making Changes

1. Edit code in your IDE
2. Server auto-reloads (DEBUG=True)
3. Test changes via API docs or curl
4. Commit to git

### Adding New Features

1. Create new app: `python manage.py startapp feature_name`
2. Add to INSTALLED_APPS in settings.py
3. Create models, serializers, views
4. Add URL routes
5. Test thoroughly

---

## Useful Commands

```bash
# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Check for issues
python manage.py check
```

---

## Need Help?

1. Check **README.md** for detailed documentation
2. Check **DEPLOYMENT.md** for deployment guide
3. Review inline code comments
4. Visit API docs at `/api/docs/`

---

**You're all set! 🚀**

Happy coding!
