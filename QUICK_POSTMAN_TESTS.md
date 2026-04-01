# Quick Postman Test Reference

## 🔑 Test Credentials

```
Admin:    username=admin, password=admin123
Analyst:  username=analyst_user, password=analyst123
Viewer:   username=viewer_user, password=viewer123
```

---

## 📋 Quick Test Flow (10 Minutes)

### 1️⃣ Get Token (POST)
```
URL: http://127.0.0.1:8000/api/token/
Body: {"username": "admin", "password": "admin123"}
```
✅ Copy `access` token to collection variable

### 2️⃣ Test Users (GET)
```
URL: http://127.0.0.1:8000/api/users/
```
✅ Should see 3 users

### 3️⃣ Create Record (POST)
```
URL: http://127.0.0.1:8000/api/records/
Body: {
  "amount": 1000,
  "record_type": "income",
  "category": "freelance",
  "date": "2024-04-01",
  "description": "Test project"
}
```
✅ Record created (201)

### 4️⃣ List Records (GET)
```
URL: http://127.0.0.1:8000/api/records/
```
✅ See all records with pagination

### 5️⃣ Dashboard Summary (GET)
```
URL: http://127.0.0.1:8000/api/dashboard/summary/
```
✅ See totals: income, expense, net balance

### 6️⃣ Test Permissions (POST as Viewer)
```
1. Get viewer token
2. Try to create record
3. Should get 403 Forbidden
```
✅ Permissions working!

---

## 🎯 Essential Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/token/` | Login |
| GET | `/api/users/` | List users |
| POST | `/api/users/` | Create user |
| GET | `/api/records/` | List records |
| POST | `/api/records/` | Create record |
| GET | `/api/dashboard/summary/` | Get summary |
| GET | `/api/dashboard/category-breakdown/` | Category stats |
| GET | `/api/dashboard/monthly-trends/` | Monthly trends |

---

## 🔍 Quick Filters

```
?record_type=income          # Income only
?category=salary             # Salary only
?date_from=2024-01-01        # From date
?date_to=2024-12-31          # To date
?amount_min=1000             # Min amount
?amount_max=5000             # Max amount
?search=lunch                # Search text
?page=2                      # Page 2
```

Combine: `?record_type=income&category=salary&date_from=2024-01-01`

---

## ✅ Expected Status Codes

- **200 OK** - Success (GET, PUT, PATCH)
- **201 Created** - Resource created (POST)
- **204 No Content** - Deleted successfully
- **400 Bad Request** - Validation error
- **401 Unauthorized** - Missing/invalid token
- **403 Forbidden** - No permission
- **404 Not Found** - Resource doesn't exist

---

## 🐛 Common Issues

**Problem:** 401 Unauthorized  
**Fix:** Check token is in Variables → accessToken

**Problem:** Connection refused  
**Fix:** Run `python manage.py runserver`

**Problem:** 403 on create  
**Fix:** Login as admin or analyst (not viewer)

---

## 📊 Sample Response

**Dashboard Summary:**
```json
{
  "total_income": "16650.00",
  "total_expense": "9510.00",
  "net_balance": "7140.00",
  "record_count": 29,
  "average_income": "1850.00"
}
```

---

## 🚀 One-Line Tests

```bash
# Get token
curl -X POST http://127.0.0.1:8000/api/token/ -H "Content-Type: application/json" -d "{\"username\":\"admin\",\"password\":\"admin123\"}"

# List records
curl http://127.0.0.1:8000/api/records/ -H "Authorization: Bearer YOUR_TOKEN"

# Dashboard
curl http://127.0.0.1:8000/api/dashboard/summary/ -H "Authorization: Bearer YOUR_TOKEN"
```

---

**Full guide:** See `POSTMAN_TESTING_GUIDE.md`
