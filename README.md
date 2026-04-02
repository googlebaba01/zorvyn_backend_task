# Finance Data Processing API 🚀

Production-ready Django REST API with role-based access control for financial data management.

## ✨ Features

- ✅ **User Management** - Role-based access (Viewer, Analyst, Admin)
- ✅ **Financial Records** - Complete CRUD with filtering & search
- ✅ **Dashboard Analytics** - Summary, trends, category breakdowns
- ✅ **JWT Authentication** - Secure token-based auth
- ✅ **Production Ready** - Deploy on Render in 5 minutes
- ✅ **API Documentation** - Swagger/OpenAPI included

## 🚀 Quick Start

### Local Development (5 mins)

```bash
# Clone repo
git clone https://github.com/googlebaba01/zorvyn_backend_task
cd zorvyn_backend

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Start server
python manage.py runserver
```

### Deploy to Render (5 mins)

1. Push to GitHub
2. Create Web Service on Render
3. Connect repository
4. Build: `pip install -r requirements.txt`
5. Start: `./start.sh`
6. Add environment variables


## 📡 API Endpoints

### Authentication
- `POST /api/token/` - Get JWT tokens
- `POST /api/token/refresh/` - Refresh token

### Users (Admin)
- `GET/POST /api/users/` - List/Create users
- `PUT/DELETE /api/users/{id}/` - Update/Delete user
- `PATCH /api/users/{id}/status/` - Toggle status

### Financial Records
- `GET/POST /api/records/` - List/Create records
- `PUT/DELETE /api/records/{id}/` - Update/Delete record
- `PATCH /api/records/{id}/restore/` - Restore deleted

**Filters:** `?record_type=income&category=salary&date_from=2024-01-01`

### Dashboard
- `GET /api/dashboard/summary/` - Totals & balance
- `GET /api/dashboard/category-breakdown/` - Category analysis
- `GET /api/dashboard/monthly-trends/` - Monthly trends
- `GET /api/dashboard/recent-activity/` - Recent transactions

## 👥 User Roles

| Role | Permissions |
|------|-------------|
| **Viewer** | Read-only access to dashboard and own records |
| **Analyst** | View all + create/edit own records |
| **Admin** | Full access - manage users & all CRUD |

## 🧪 Testing

### Default Credentials (after deployment)
- Username: `admin`
- Password: `admin123`

⚠️ **Change immediately after deployment!**

### Get Token
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### Test API
```bash
curl http://localhost:8000/api/records/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 🛠️ Tech Stack

- **Backend:** Django 5.0 + Django REST Framework 3.15
- **Database:** SQLite (dev) / PostgreSQL ready (prod)
- **Auth:** JWT (djangorestframework-simplejwt)
- **Deployment:** Render + Gunicorn + WhiteNoise
- **Docs:** drf-yasg (Swagger/OpenAPI)

## 📁 Project Structure

```
zorvyn_backend/
├── finance_api/      # Django config
├── users/           # User management
├── records/         # Financial records
├── dashboard/       # Analytics
├── requirements.txt
├── start.sh         # Deployment script
└── README.md        # This file
```

## 🔐 Security

- DEBUG=False by default
- JWT authentication
- Role-based permissions
- CORS configured
- Security headers enabled
- Input validation

## 🎯 What's Implemented

✅ User & Role Management  
✅ Financial Records CRUD  
✅ Advanced Filtering & Search  
✅ Dashboard Analytics  
✅ Role-Based Access Control  
✅ JWT Authentication  
✅ Input Validation  
✅ Soft Delete  
✅ Pagination  
✅ API Documentation  
✅ Production Deployment Ready  
