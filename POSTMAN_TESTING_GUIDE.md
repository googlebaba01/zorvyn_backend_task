# Postman Testing Guide - Finance Data API

## Complete Step-by-Step Testing Workflow

This guide walks you through testing every feature of the Finance Data Processing API using Postman, from authentication to advanced filtering.

---

## Prerequisites

1. **Postman installed** (download from https://www.postman.com/downloads/)
2. **Django server running** on http://127.0.0.1:8000
3. **Sample data populated** (run `python manage.py populate_sample_data`)

---

## Table of Contents

1. [Setup Postman Collection](#1-setup-postman-collection)
2. [Authentication - Get JWT Token](#2-authentication---get-jwt-token)
3. [Test Admin Operations](#3-test-admin-operations)
4. [Test Financial Records](#4-test-financial-records)
5. [Test Dashboard Analytics](#5-test-dashboard-analytics)
6. [Test Role-Based Permissions](#6-test-role-based-permissions)
7. [Advanced Filtering Tests](#7-advanced-filtering-tests)

---

## 1. Setup Postman Collection

### Step 1.1: Create New Collection

1. Open Postman
2. Click **"New"** → **"Collection"**
3. Name it: **"Finance Data API"**
4. Add description: "Testing finance backend with RBAC"

### Step 1.2: Add Base URL Variable

1. Click on the collection name
2. Go to **"Variables"** tab
3. Add variable:
   - **Variable:** `baseUrl`
   - **Initial Value:** `http://127.0.0.1:8000`
   - **Current Value:** `http://127.0.0.1:8000`

### Step 1.3: Add Authentication Token Variable

1. Still in Variables tab
2. Add another variable:
   - **Variable:** `accessToken`
   - **Initial Value:** (leave empty)
   - **Current Value:** (leave empty)

### Step 1.4: Set Up Authorization Helper

1. Go to **"Authorization"** tab in collection
2. **Type:** Bearer Token
3. **Token:** `{{accessToken}}`

Now all requests in this collection will automatically use the token!

---

## 2. Authentication - Get JWT Token

### Test 2.1: Login as Admin

**Request Details:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/token/`
- **Headers:** 
  - `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Expected Response (200 OK):**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Save Token:**
1. Copy the `access` token value
2. Go to Collection Variables
3. Paste it into `accessToken` variable's **Current Value**

### Test 2.2: Verify Token Works

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/users/`

**Expected:** List of users (should show admin user)

---

## 3. Test Admin Operations

### Test 3.1: List All Users

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/users/`

**Expected Response (200 OK):**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "admin",
      "email": "admin@example.com",
      "role": "admin",
      "is_active": true,
      ...
    }
  ]
}
```

### Test 3.2: Create New User (Analyst)

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/users/`
- **Body:**
```json
{
  "username": "test_analyst",
  "email": "test.analyst@example.com",
  "password": "testpass123",
  "password_confirm": "testpass123",
  "first_name": "Test",
  "last_name": "Analyst",
  "role": "analyst"
}
```

**Expected (201 Created):**
```json
{
  "id": 4,
  "username": "test_analyst",
  "email": "test.analyst@example.com",
  "role": "analyst",
  "is_active": true,
  "can_create_records": true,
  "can_delete_records": false,
  "can_manage_users": false
}
```

### Test 3.3: Update User Status

**Request:**
- **Method:** PATCH
- **URL:** `{{baseUrl}}/api/users/4/status/`
- **Body:**
```json
{
  "is_active": false
}
```

**Expected (200 OK):** User status updated to inactive

### Test 3.4: Change Your Password

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/users/1/change-password/`
- **Body:**
```json
{
  "old_password": "admin123",
  "new_password": "newadmin456",
  "new_password_confirm": "newadmin456"
}
```

**Expected (200 OK):**
```json
{
  "message": "Password changed successfully"
}
```

⚠️ **Note:** Remember your new password now!

---

## 4. Test Financial Records

### Test 4.1: List All Records

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/records/`

**Expected (200 OK):** Paginated list of financial records

### Test 4.2: Create Income Record

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/records/`
- **Body:**
```json
{
  "amount": 2500.00,
  "record_type": "income",
  "category": "freelance",
  "date": "2024-04-01",
  "description": "Website development project",
  "notes": "Payment from client ABC Corp"
}
```

**Expected (201 Created):**
```json
{
  "id": 29,
  "amount": "2500.00",
  "record_type": "income",
  "category": "freelance",
  "formatted_amount": "+$2,500.00",
  "effect_amount": "2500.00",
  "created_by_username": "admin",
  ...
}
```

### Test 4.3: Create Expense Record

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/records/`
- **Body:**
```json
{
  "amount": 350.00,
  "record_type": "expense",
  "category": "food",
  "date": "2024-04-02",
  "description": "Team lunch meeting",
  "notes": "Quarterly planning session lunch"
}
```

**Expected (201 Created):** Record created successfully

### Test 4.4: Update a Record

**Request:**
- **Method:** PATCH
- **URL:** `{{baseUrl}}/api/records/29/`
- **Body:**
```json
{
  "amount": 3000.00,
  "notes": "Updated: Payment from client ABC Corp - Final"
}
```

**Expected (200 OK):** Record updated with new values

### Test 4.5: Get Single Record Details

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/records/29/`

**Expected (200 OK):** Full record details with all fields

### Test 4.6: Soft Delete Record (Admin Only)

**Request:**
- **Method:** DELETE
- **URL:** `{{baseUrl}}/api/records/29/`

**Expected (204 No Content):** Empty response

### Test 4.7: Restore Deleted Record (Admin Only)

**Request:**
- **Method:** PATCH
- **URL:** `{{baseUrl}}/api/records/29/restore/`

**Expected (200 OK):** Restored record details

---

## 5. Test Dashboard Analytics

### Test 5.1: Get Dashboard Summary

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/dashboard/summary/`

**Expected (200 OK):**
```json
{
  "total_income": "16650.00",
  "total_expense": "9510.00",
  "net_balance": "7140.00",
  "record_count": 29,
  "income_count": 9,
  "expense_count": 20,
  "average_income": "1850.00",
  "average_expense": "475.50",
  "date_range": {
    "from": "All time",
    "to": "Present"
  }
}
```

### Test 5.2: Get Category Breakdown

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/dashboard/category-breakdown/`

**Expected (200 OK):** Array of categories with totals and percentages

```json
[
  {
    "category": "salary",
    "category_display": "Salary",
    "total_amount": "5000.00",
    "record_count": 1,
    "percentage": "30.03",
    "record_type": "income",
    "average_amount": "5000.00"
  },
  ...
]
```

### Test 5.3: Get Monthly Trends

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/dashboard/monthly-trends/?months=6`

**Expected (200 OK):** Monthly income/expense trends

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
  }
]
```

### Test 5.4: Get Recent Activity

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/dashboard/recent-activity/?limit=5`

**Expected (200 OK):** Last 5 transactions

```json
[
  {
    "id": 29,
    "amount": "3000.00",
    "formatted_amount": "+$3,000.00",
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

## 6. Test Role-Based Permissions

### Test 6.1: Login as Viewer

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/token/`
- **Body:**
```json
{
  "username": "viewer_user",
  "password": "viewer123"
}
```

**Action:** Save the new access token in `accessToken` variable

### Test 6.2: Viewer Tries to View Records (Should Work)

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/records/?is_mine=true`

**Expected (200 OK):** Only viewer's own records (5 records)

### Test 6.3: Viewer Tries to Create Record (Should Fail)

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/records/`
- **Body:**
```json
{
  "amount": 100.00,
  "record_type": "expense",
  "category": "food",
  "date": "2024-04-01",
  "description": "Test expense"
}
```

**Expected (403 Forbidden):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

✅ **Permission working correctly!**

### Test 6.4: Viewer Tries to View Dashboard (Should Work)

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/dashboard/summary/`

**Expected (200 OK):** Dashboard summary visible

### Test 6.5: Login as Analyst

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/token/`
- **Body:**
```json
{
  "username": "analyst_user",
  "password": "analyst123"
}
```

**Action:** Save the new access token

### Test 6.6: Analyst Creates Record (Should Work)

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/records/`
- **Body:**
```json
{
  "amount": 500.00,
  "record_type": "income",
  "category": "freelance",
  "date": "2024-04-01",
  "description": "Analyst test record"
}
```

**Expected (201 Created):** Record created successfully

### Test 6.7: Analyst Tries to Delete Record (Should Fail)

**Request:**
- **Method:** DELETE
- **URL:** `{{baseUrl}}/api/records/30/`

**Expected (403 Forbidden):** Analyst cannot delete

✅ **All role permissions working!**

---

## 7. Advanced Filtering Tests

### Test 7.1: Filter by Record Type

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/records/?record_type=income`

**Expected:** Only income records returned

### Test 7.2: Filter by Category

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/records/?category=salary&category=freelance`

**Expected:** Only salary and freelance income records

### Test 7.3: Filter by Date Range

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/records/?date_from=2024-03-01&date_to=2024-03-31`

**Expected:** Records from March 2024 only

### Test 7.4: Filter by Amount Range

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/records/?amount_min=1000&amount_max=5000`

**Expected:** Records between $1,000 and $5,000

### Test 7.5: Search in Description

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/records/?search=lunch`

**Expected:** Records containing "lunch" in description or notes

### Test 7.6: Combined Filters

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/records/?record_type=expense&category=food&date_from=2024-01-01&ordering=-amount`

**Expected:** Food expenses from 2024, sorted by amount (highest first)

### Test 7.7: Pagination Test

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/records/?page=2&page_size=10`

**Expected:** Second page with 10 records per page

---

## 8. Validation Tests

### Test 8.1: Invalid Amount (Negative)

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/records/`
- **Body:**
```json
{
  "amount": -100,
  "record_type": "income",
  "category": "salary",
  "date": "2024-04-01"
}
```

**Expected (400 Bad Request):**
```json
{
  "amount": ["Amount must be greater than zero"]
}
```

### Test 8.2: Future Date

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/records/`
- **Body:**
```json
{
  "amount": 100,
  "record_type": "income",
  "category": "salary",
  "date": "2025-01-01"
}
```

**Expected (400 Bad Request):**
```json
{
  "date": ["Transaction date cannot be in the future"]
}
```

### Test 8.3: Missing Required Fields

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/records/`
- **Body:**
```json
{
  "record_type": "income"
}
```

**Expected (400 Bad Request):** Multiple field validation errors

### Test 8.4: Category-Type Mismatch

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/records/`
- **Body:**
```json
{
  "amount": 100,
  "record_type": "income",
  "category": "food",
  "date": "2024-04-01"
}
```

**Expected (400 Bad Request):**
```json
{
  "non_field_errors": ["Category 'food' is an expense category. Please use 'expense' as record type..."]
}
```

---

## 9. Token Management Tests

### Test 9.1: Refresh Token

**Request:**
- **Method:** POST
- **URL:** `{{baseUrl}}/api/token/refresh/`
- **Body:**
```json
{
  "refresh": "YOUR_REFRESH_TOKEN_HERE"
}
```

**Expected (200 OK):** New access token

### Test 9.2: Access Protected Resource Without Token

**Request:**
- **Method:** GET
- **URL:** `{{baseUrl}}/api/records/`
- **Authorization:** Remove token or use invalid token

**Expected (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## Testing Checklist

Use this checklist to verify all features:

### Authentication ✅
- [ ] Admin login successful
- [ ] Analyst login successful
- [ ] Viewer login successful
- [ ] Token refresh works
- [ ] Invalid credentials rejected

### User Management (Admin) ✅
- [ ] List all users
- [ ] Create new user
- [ ] Update user details
- [ ] Toggle user status
- [ ] Change password
- [ ] Cannot delete self

### Financial Records ✅
- [ ] List records (paginated)
- [ ] Create income record
- [ ] Create expense record
- [ ] Update own record
- [ ] Delete record (admin only)
- [ ] Restore deleted record (admin only)
- [ ] View single record

### Dashboard Analytics ✅
- [ ] Overall summary
- [ ] Category breakdown
- [ ] Monthly trends
- [ ] Recent activity

### Permissions ✅
- [ ] Viewer can only view
- [ ] Viewer sees only own records
- [ ] Analyst can create records
- [ ] Analyst can update own records
- [ ] Analyst cannot delete
- [ ] Admin has full access

### Filtering ✅
- [ ] Filter by type
- [ ] Filter by category
- [ ] Filter by date range
- [ ] Filter by amount range
- [ ] Search functionality
- [ ] Combined filters
- [ ] Pagination

### Validation ✅
- [ ] Negative amount rejected
- [ ] Future date rejected
- [ ] Missing fields rejected
- [ ] Category-type mismatch rejected
- [ ] Weak password rejected

---

## Expected Results Summary

After completing all tests:

- ✅ **Total API Calls:** ~50-60 requests
- ✅ **Successful Operations:** 95%+ success rate
- ✅ **Permissions Working:** All role restrictions enforced
- ✅ **Validation Working:** All invalid inputs rejected
- ✅ **Data Integrity:** No data corruption or loss

---

## Troubleshooting

### Issue: 401 Unauthorized

**Solution:** Check if token is copied correctly to `accessToken` variable

### Issue: 403 Forbidden

**Solution:** Verify you're logged in with correct role for the operation

### Issue: 404 Not Found

**Solution:** Check URL spelling and ensure record/user ID exists

### Issue: Connection Refused

**Solution:** Ensure Django server is running: `python manage.py runserver`

---

## Export Collection

Once all tests pass:

1. Right-click on collection
2. Select **"Export"**
3. Choose format: **Collection v2.1**
4. Save as: `finance-api-tests.json`

This allows you to share tests or import on another machine!

---

**Testing Complete! 🎉**

Your Finance Data API is fully functional and ready for deployment!
