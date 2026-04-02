# Quick Postman Testing Guide

## Setup

### 1. Get Authentication Token

**Request:** Create Token
```
POST http://localhost:8000/api/token/
Content-Type: application/json

{
  "username": "admin",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Save the `access` token for all subsequent requests.**

---

## User Management (Admin Only)

### 2. List All Users
```
GET http://localhost:8000/api/users/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 3. Create New User
```
POST http://localhost:8000/api/users/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "username": "newuser",
  "email": "new@example.com",
  "password": "securepass123",
  "role": "analyst",
  "first_name": "New",
  "last_name": "User"
}
```

### 4. Update User Status
```
PATCH http://localhost:8000/api/users/1/status/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "is_active": false
}
```

---

## Financial Records

### 5. Create Record (Analyst/Admin)
```
POST http://localhost:8000/api/records/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "amount": 5000.00,
  "record_type": "income",
  "category": "salary",
  "date": "2024-01-15",
  "description": "Monthly salary",
  "notes": "January 2024"
}
```

### 6. List Records with Filters
```
GET http://localhost:8000/api/records/?record_type=income&category=salary
Authorization: Bearer YOUR_ACCESS_TOKEN
```

Common filters:
- `?record_type=income` or `expense`
- `?category=salary&category=food`
- `?date_from=2024-01-01&date_to=2024-12-31`
- `?amount_min=100&amount_max=1000`

### 7. Update Record
```
PUT http://localhost:8000/api/records/1/
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "amount": 5500.00,
  "record_type": "income",
  "category": "salary",
  "date": "2024-01-15",
  "description": "Updated salary"
}
```

### 8. Delete Record (Soft Delete - Admin only)
```
DELETE http://localhost:8000/api/records/1/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 9. Restore Deleted Record
```
PATCH http://localhost:8000/api/records/1/restore/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## Dashboard Analytics

### 10. Get Summary
```
GET http://localhost:8000/api/dashboard/summary/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

**Response:**
```json
{
  "total_income": 15000.00,
  "total_expense": 8500.00,
  "net_balance": 6500.00,
  "record_count": 25,
  "average_income": 3000.00,
  "average_expense": 850.00
}
```

### 11. Category Breakdown
```
GET http://localhost:8000/api/dashboard/category-breakdown/
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 12. Monthly Trends
```
GET http://localhost:8000/api/dashboard/monthly-trends/?months=6
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### 13. Recent Activity
```
GET http://localhost:8000/api/dashboard/recent-activity/?limit=10
Authorization: Bearer YOUR_ACCESS_TOKEN
```

---

## Role-Based Testing

### Test as Viewer
1. Login with viewer credentials
2. Try to view records - ✅ Should work
3. Try to view dashboard - ✅ Should work
4. Try to create record - ❌ Should fail (403 Forbidden)
5. Try to delete record - ❌ Should fail (403 Forbidden)

### Test as Analyst
1. Login with analyst credentials
2. View records - ✅ Should work
3. Create record - ✅ Should work
4. Update own record - ✅ Should work
5. Delete record - ❌ Should fail (403 Forbidden)

### Test as Admin
1. Login with admin credentials
2. All operations should work ✅

---

## Common Issues

### 401 Unauthorized
- Token expired or invalid
- Get new token using `/api/token/`

### 403 Forbidden
- User doesn't have permission for that action
- Check user role

### Token Expired
```
POST http://localhost:8000/api/token/refresh/
Content-Type: application/json

{
  "refresh": "YOUR_REFRESH_TOKEN"
}
```

---

## Import to Postman

1. Open Postman
2. Create new collection: "Finance API"
3. Add requests as shown above
4. Set up Authorization tab:
   - Type: Bearer Token
   - Token: `{{access_token}}`
5. Add environment variable `access_token` with your token value

Happy Testing! 🚀
