# API Documentation

## Overview

This document provides comprehensive documentation for the Finance Data Processing and Access Control Backend API.

**Base URL (Development):** `http://127.0.0.1:8000`  
**API Version:** v1  
**Authentication:** JWT (JSON Web Tokens)

---

## Table of Contents

1. [Authentication](#authentication)
2. [User Management](#user-management)
3. [Financial Records](#financial-records)
4. [Dashboard Analytics](#dashboard-analytics)
5. [Error Handling](#error-handling)
6. [Role-Based Permissions](#role-based-permissions)

---

## Authentication

All API endpoints (except token generation) require JWT authentication.

### Obtain Token

**Endpoint:** `POST /api/token/`

**Request:**
```json
{
  "username": "admin",
  "password": "newadmin456"
}

or 
{
  "username": "admin",
  "password": "admin123"
}

```

**Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Usage:** Include the access token in all requests:
```
Authorization: Bearer <access_token>
```

### Refresh Token

**Endpoint:** `POST /api/token/refresh/`

**Request:**
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

---

## User Management

### List Users

**Endpoint:** `GET /api/users/`  
**Permission:** Admin only

**Query Parameters:**
- `role` - Filter by role (viewer, analyst, admin)
- `is_active` - Filter by status (true/false)
- `search` - Search by username or email
- `ordering` - Sort field (-date_joined, username, etc.)

**Example:**
```bash
GET /api/users/?role=analyst&is_active=true
```

### Create User

**Endpoint:** `POST /api/users/`  
**Permission:** Admin only

**Request:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "securepass123",
  "password_confirm": "securepass123",
  "first_name": "John",
  "last_name": "Doe",
  "role": "analyst"
}
```

**Response:**
```json
{
  "id": 5,
  "username": "newuser",
  "email": "newuser@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "role": "analyst",
  "is_active": true,
  "date_joined": "2024-04-01T10:00:00Z",
  "can_create_records": true,
  "can_delete_records": false,
  "can_manage_users": false
}
```

### Get User Details

**Endpoint:** `GET /api/users/{id}/`

**Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "Admin User",
  "first_name": "Admin",
  "last_name": "User",
  "role": "admin",
  "is_active": true,
  "date_joined": "2024-04-01T08:00:00Z",
  "updated_at": "2024-04-01T09:00:00Z",
  "can_create_records": true,
  "can_delete_records": true,
  "can_manage_users": true
}
```

### Update User

**Endpoint:** `PUT /api/users/{id}/` or `PATCH /api/users/{id}/`  
**Permission:** Admin only

**Request (PATCH example):**
```json
{
  "first_name": "Updated",
  "role": "admin"
}
```

### Delete User

**Endpoint:** `DELETE /api/users/{id}/`  
**Permission:** Admin only  
**Note:** Cannot delete your own account

### Update User Status

**Endpoint:** `PATCH /api/users/{id}/status/`  
**Permission:** Admin only

**Request:**
```json
{
  "is_active": false
}
```

### Change Password

**Endpoint:** `POST /api/users/{id}/change-password/`

**Request:**
```json
{
  "old_password": "oldpass123",
  "new_password": "newsecurepass456",
  "new_password_confirm": "newsecurepass456"
}
```

---

## Financial Records

### List Records

**Endpoint:** `GET /api/records/`  
**Permission:** All authenticated users

**Query Parameters:**
- `record_type` - Filter by type (income, expense)
- `category` - Filter by category (can specify multiple)
- `date_from` - Start date (YYYY-MM-DD)
- `date_to` - End date (YYYY-MM-DD)
- `amount_min` - Minimum amount
- `amount_max` - Maximum amount
- `created_by` - Filter by user ID
- `is_mine` - Show only my records (true/false)
- `search` - Search in description/notes
- `ordering` - Sort field (-date, amount, etc.)

**Example:**
```bash
GET /api/records/?record_type=income&category=salary&date_from=2024-01-01&ordering=-amount
```

**Response:**
```json
{
  "count": 25,
  "next": "http://api/records/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "amount": "5000.00",
      "record_type": "income",
      "category": "salary",
      "category_display": "Salary",
      "date": "2024-04-01",
      "description": "Monthly salary",
      "formatted_amount": "+$5,000.00",
      "created_by": 1,
      "created_by_username": "admin",
      "created_at": "2024-04-01T10:00:00Z"
    }
  ]
}
```

### Create Record

**Endpoint:** `POST /api/records/`  
**Permission:** Analyst and Admin only

**Request:**
```json
{
  "amount": 1500.00,
  "record_type": "income",
  "category": "freelance",
  "date": "2024-04-01",
  "description": "Website development project",
  "notes": "Payment from client XYZ"
}
```

**Response:**
```json
{
  "id": 51,
  "amount": "1500.00",
  "record_type": "income",
  "category": "freelance",
  "date": "2024-04-01",
  "description": "Website development project",
  "notes": "Payment from client XYZ",
  "created_by": 1,
  "created_by_username": "admin",
  "formatted_amount": "+$1,500.00",
  "effect_amount": "1500.00",
  "category_display": "Freelance",
  "type_display": "Income",
  "is_deleted": false,
  "created_at": "2024-04-01T12:00:00Z",
  "updated_at": "2024-04-01T12:00:00Z"
}
```

### Get Record Details

**Endpoint:** `GET /api/records/{id}/`

### Update Record

**Endpoint:** `PUT /api/records/{id}/` or `PATCH /api/records/{id}/`

**Permission Rules:**
- Admin: Can update any record
- Analyst: Can only update their own records
- Viewer: Cannot update

**Request (PATCH):**
```json
{
  "amount": 2000.00,
  "notes": "Updated payment amount"
}
```

### Delete Record (Soft Delete)

**Endpoint:** `DELETE /api/records/{id}/`  
**Permission:** Admin only

**Response:** `204 No Content`

### Restore Deleted Record

**Endpoint:** `PATCH /api/records/{id}/restore/`  
**Permission:** Admin only

**Response:** Returns restored record details

---

## Dashboard Analytics

### Get Dashboard Summary

**Endpoint:** `GET /api/dashboard/summary/`  
**Permission:** All authenticated users

**Query Parameters:**
- `date_from` - Filter from date
- `date_to` - Filter to date
- `record_type` - Filter by type

**Response:**
```json
{
  "total_income": "25000.00",
  "total_expense": "12000.00",
  "net_balance": "13000.00",
  "record_count": 50,
  "income_count": 20,
  "expense_count": 30,
  "average_income": "1250.00",
  "average_expense": "400.00",
  "date_range": {
    "from": "All time",
    "to": "Present"
  }
}
```

### Get Category Breakdown

**Endpoint:** `GET /api/dashboard/category-breakdown/`

**Query Parameters:**
- `date_from`, `date_to` - Date range
- `record_type` - income or expense

**Response:**
```json
[
  {
    "category": "salary",
    "category_display": "Salary",
    "total_amount": "15000.00",
    "record_count": 3,
    "percentage": "60.00",
    "record_type": "income",
    "average_amount": "5000.00"
  },
  {
    "category": "food",
    "category_display": "Food & Dining",
    "total_amount": "2500.00",
    "record_count": 8,
    "percentage": "20.83",
    "record_type": "expense",
    "average_amount": "312.50"
  }
]
```

### Get Monthly Trends

**Endpoint:** `GET /api/dashboard/monthly-trends/`

**Query Parameters:**
- `months` - Number of months (default: 12)
- `year` - Specific year

**Response:**
```json
[
  {
    "month": "April",
    "month_number": 4,
    "year": 2024,
    "income": "8500.00",
    "expense": "3200.00",
    "net": "5300.00",
    "savings_rate": "62.35",
    "record_count": 15
  },
  {
    "month": "March",
    "month_number": 3,
    "year": 2024,
    "income": "7200.00",
    "expense": "2800.00",
    "net": "4400.00",
    "savings_rate": "61.11",
    "record_count": 12
  }
]
```

### Get Recent Activity

**Endpoint:** `GET /api/dashboard/recent-activity/`

**Query Parameters:**
- `limit` - Number of records (default: 10)

**Response:**
```json
[
  {
    "id": 51,
    "amount": "1500.00",
    "formatted_amount": "+$1,500.00",
    "record_type": "income",
    "category": "freelance",
    "category_display": "Freelance",
    "description": "Website development project",
    "date": "2024-04-01",
    "created_by_username": "admin",
    "created_at": "2024-04-01T12:00:00Z"
  }
]
```

---

## Error Handling

### Standard Error Response Format

```json
{
  "error": "Error message here",
  "details": {
    "field_name": ["Specific field error"]
  }
}
```

### Common HTTP Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `204 No Content` - Successful deletion
- `400 Bad Request` - Invalid input data
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

### Validation Errors

```json
{
  "amount": ["Amount must be greater than zero"],
  "password": ["Password must be at least 8 characters long"],
  "password_confirm": ["Passwords do not match"]
}
```

---

## Role-Based Permissions

### Permission Matrix

| Operation | Viewer | Analyst | Admin |
|-----------|--------|---------|-------|
| View dashboard summary | ✅ | ✅ | ✅ |
| View records | ✅ (own only) | ✅ (all) | ✅ (all) |
| Create records | ❌ | ✅ | ✅ |
| Update own records | ❌ | ✅ | ✅ |
| Update any records | ❌ | ❌ | ✅ |
| Delete records | ❌ | ❌ | ✅ |
| Manage users | ❌ | ❌ | ✅ |
| View analytics | ✅ | ✅ | ✅ |

### Testing Different Roles

**Viewer Account:**
```bash
# Login
curl -X POST http://127.0.0.1:8000/api/token/ \
  -d '{"username":"viewer_user","password":"viewer123"}'

# Try to view records - Works
curl http://127.0.0.1:8000/api/records/ \
  -H "Authorization: Bearer <token>"

# Try to create record - Fails with 403
curl -X POST http://127.0.0.1:8000/api/records/ \
  -H "Authorization: Bearer <token>" \
  -d '{"amount": 100, "record_type": "income", ...}'
```

---

## Interactive Documentation

For interactive testing, visit:
- **Swagger UI:** `/api/docs/`
- **ReDoc:** `/api/redoc/`

These provide:
- Live API testing
- Request/response schemas
- Try-it-out functionality
- Downloadable OpenAPI spec

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider adding:
- Django Ratelimit
- Throttling classes in DRF

---

## Versioning

Current API version: v1

To add new versions in future:
- Use URL versioning: `/api/v2/...`
- Or header versioning: `Accept: application/vnd.api.v2+json`

---

## Support

For issues or questions:
1. Check this documentation
2. Review inline code comments
3. Examine test cases
4. Contact development team

---

**Last Updated:** April 1, 2024  
**API Version:** 1.0.0
