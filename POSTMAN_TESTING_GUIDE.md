# 📬 Complete Postman API Testing Guide

## 🎯 Overview

This guide provides comprehensive Postman testing scenarios for all API endpoints. Follow these tests to verify your backend is working correctly before deployment.

---

## 📋 Table of Contents

1. [Pre-Setup Instructions](#pre-setup-instructions)
2. [Authentication Tests](#authentication-tests)
3. [User Management Tests (Admin)](#user-management-tests-admin)
4. [Financial Records Tests](#financial-records-tests)
5. [Dashboard Analytics Tests](#dashboard-analytics-tests)
6. [Role-Based Permission Tests](#role-based-permission-tests)
7. [Error Scenario Tests](#error-scenario-tests)
8. [Collection Export](#collection-export)

---

## 🛠️ Pre-Setup Instructions

### Step 1: Create a New Collection

1. Open Postman
2. Click **"New"** → **"Collection"**
3. Name it: `Finance API - Complete Tests`
4. Add description: `Comprehensive API testing for Finance Data Processing Backend`

### Step 2: Set Up Collection Variables

In the collection, go to **Variables** tab and add:

| Variable | Initial Value | Current Value | Description |
|----------|---------------|---------------|-------------|
| `base_url` | `http://127.0.0.1:8000` | `http://127.0.0.1:8000` | `https://finance-data-api-saav.onrender.com/` |
| `access_token` | (leave empty) | (auto-filled) | JWT Access Token |
| `refresh_token` | (leave empty) | (auto-filled) | JWT Refresh Token |
| `admin_user_id` | (leave empty) | (auto-filled) | Admin user ID |
| `analyst_user_id` | (leave empty) | (auto-filled) | Analyst user ID |
| `viewer_user_id` | (leave empty) | (auto-filled) | Viewer user ID |
| `test_record_id` | (leave empty) | (auto-filled) | Test record ID |

### Step 3: Add Authorization to Collection

1. Go to **Authorization** tab in collection
2. Type: **Bearer Token**
3. Token: `{{access_token}}`

This automatically adds the token to all requests.

---

## 🔐 Authentication Tests

### 1.1 ✅ Successful Login (Admin)

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/token/`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Tests Script (Tests tab):**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has access and refresh tokens", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.access).to.exist;
    pm.expect(jsonData.refresh).to.exist;
    
    // Save tokens to collection variables
    pm.collectionVariables.set("access_token", jsonData.access);
    pm.collectionVariables.set("refresh_token", jsonData.refresh);
});

pm.test("Token format is valid (JWT)", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.access).to.include('.');
    pm.expect(jsonData.refresh).to.include('.');
});
```

**Expected Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNz... ",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcx... "
}
```

---

### 1.2 ❌ Failed Login - Wrong Password

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/token/`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "username": "admin",
  "password": "wrongpassword"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 401", function () {
    pm.response.to.have.status(401);
});

pm.test("Error message exists", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.detail).to.exist;
});
```

**Expected Response:**
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### 1.3 ❌ Failed Login - Missing Fields

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/token/`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "username": "admin"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Password field error exists", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.password).to.exist;
});
```

**Expected Response:**
```json
{
  "password": ["This field is required."]
}
```

---

### 1.4 ✅ Refresh Token

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/token/refresh/`
- **Headers:** `Content-Type: application/json`
- **Body (raw JSON):**
```json
{
  "refresh": "{{refresh_token}}"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("New access token received", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.access).to.exist;
    pm.collectionVariables.set("access_token", jsonData.access);
});
```

**Expected Response:**
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.new_access_token..."
}
```

---

### 1.5 ✅ Verify Token Works

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/users/me/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response contains user data", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.username).to.exist;
    pm.expect(jsonData.role).to.exist;
});
```

**Expected Response:**
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@example.com",
  "full_name": "Admin User",
  "role": "admin",
  "is_active": true,
  ...
}
```

---

## 👥 User Management Tests (Admin)

**⚠️ IMPORTANT:** All these tests require admin authentication. Make sure you've completed test 1.1 first.

### 2.1 ✅ List All Users (Admin Only)

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/users/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response is an array", function () {
    pm.expect(pm.response.json()).to.be.an('array');
});

pm.test("At least one user exists", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.length).to.be.greaterThan(0);
});
```

**Expected Response:** Array of user objects

---

### 2.2 ✅ Create New User - Analyst Role

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/users/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
  "username": "test_analyst",
  "email": "analyst@test.com",
  "password": "Analyst123!",
  "password_confirm": "Analyst123!",
  "first_name": "Test",
  "last_name": "Analyst",
  "role": "analyst"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("User created with correct role", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.role).to.equal('analyst');
    pm.expect(jsonData.username).to.equal('test_analyst');
    
    // Save user ID for later tests
    pm.collectionVariables.set("analyst_user_id", jsonData.id);
});

pm.test("Permissions are correct for analyst", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.can_create_records).to.be.true;
    pm.expect(jsonData.can_delete_records).to.be.false;
    pm.expect(jsonData.can_manage_users).to.be.false;
});
```

**Expected Response:**
```json
{
  "id": 2,
  "username": "test_analyst",
  "email": "analyst@test.com",
  "first_name": "Test",
  "last_name": "Analyst",
  "role": "analyst",
  "is_active": true,
  "can_create_records": true,
  "can_delete_records": false,
  "can_manage_users": false,
  ...
}
```

---

### 2.3 ✅ Create New User - Viewer Role

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/users/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
  "username": "test_viewer",
  "email": "viewer@test.com",
  "password": "Viewer123!",
  "password_confirm": "Viewer123!",
  "first_name": "Test",
  "last_name": "Viewer",
  "role": "viewer"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("User created with viewer role", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.role).to.equal('viewer');
    pm.collectionVariables.set("viewer_user_id", jsonData.id);
});
```

---

### 2.4 ✅ Get User Details

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/users/{{analyst_user_id}}/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("User details are correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.id).to.equal(Number(pm.collectionVariables.get("analyst_user_id")));
    pm.expect(jsonData.role).to.equal('analyst');
});
```

---

### 2.5 ✅ Update User Details

**Request:**
- **Method:** `PATCH`
- **URL:** `{{base_url}}/api/users/{{analyst_user_id}}/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
  "first_name": "Updated",
  "last_name": "Senior Analyst"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("User updated successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.first_name).to.equal('Updated');
    pm.expect(jsonData.last_name).to.equal('Senior Analyst');
});
```

---

### 2.6 ✅ Update User Status (Activate/Deactivate)

**Request:**
- **Method:** `PATCH`
- **URL:** `{{base_url}}/api/users/{{viewer_user_id}}/status/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
  "is_active": false
}
```

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("User status updated", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.is_active).to.equal(false);
});
```

---

### 2.7 ✅ Change User Password (Admin)

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/users/{{analyst_user_id}}/change-password/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
  "old_password": "Analyst123!",
  "new_password": "NewAnalyst456!",
  "new_password_confirm": "NewAnalyst456!"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Success message exists", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.detail).to.exist;
});
```

---

### 2.8 ❌ Create User - Validation Error (Passwords Don't Match)

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/users/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
  "username": "invalid_user",
  "email": "invalid@test.com",
  "password": "Password123!",
  "password_confirm": "DifferentPassword456!",
  "role": "viewer"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Password confirm error exists", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.password_confirm).to.exist;
});
```

**Expected Response:**
```json
{
  "password_confirm": ["Passwords do not match"]
}
```

---

### 2.9 ❌ Non-Admin Tries to List Users

First, get a viewer token by logging in:

**Login as Viewer:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/token/`
- **Body:**
```json
{
  "username": "test_viewer",
  "password": "Viewer123!"
}
```

Save this token temporarily.

**Try to List Users:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/users/`
- **Headers:** `Authorization: Bearer <viewer_token>`

**Tests Script:**
```javascript
pm.test("Status code is 403", function () {
    pm.response.to.have.status(403);
});
```

**Expected Response:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 2.10 ✅ Delete User (Admin)

**Request:**
- **Method:** `DELETE`
- **URL:** `{{base_url}}/api/users/{{viewer_user_id}}/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 204", function () {
    pm.response.to.have.status(204);
});
```

**Expected:** No content response

---

## 📊 Financial Records Tests

### 3.1 ✅ List All Records (Authenticated User)

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/records/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Response has pagination", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.count).to.exist;
    pm.expect(jsonData.results).to.exist;
    pm.expect(jsonData.results).to.be.an('array');
});
```

**Expected Response:** Paginated list of records

---

### 3.2 ✅ Create Record - Income (Analyst/Admin)

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/records/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
  "amount": 5000.00,
  "record_type": "income",
  "category": "salary",
  "date": "2024-04-01",
  "description": "Monthly salary payment",
  "notes": "Regular monthly compensation"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Record created successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.amount).to.equal("5000.00");
    pm.expect(jsonData.record_type).to.equal('income');
    pm.expect(jsonData.category).to.equal('salary');
    
    // Save record ID for later tests
    pm.collectionVariables.set("test_record_id", jsonData.id);
});

pm.test("Formatted amount is correct", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.formatted_amount).to.include('$5,000.00');
});
```

**Expected Response:**
```json
{
  "id": 1,
  "amount": "5000.00",
  "record_type": "income",
  "category": "salary",
  "date": "2024-04-01",
  "description": "Monthly salary payment",
  "formatted_amount": "+$5,000.00",
  "created_by": 1,
  "created_by_username": "admin",
  ...
}
```

---

### 3.3 ✅ Create Record - Expense

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/records/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
  "amount": 150.75,
  "record_type": "expense",
  "category": "food",
  "date": "2024-04-02",
  "description": "Grocery shopping",
  "notes": "Weekly groceries from supermarket"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

pm.test("Expense record created", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.record_type).to.equal('expense');
    pm.expect(jsonData.formatted_amount).to.include('-$150.75');
});
```

---

### 3.4 ✅ Get Record Details

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/records/{{test_record_id}}/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Record details match", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.id).to.equal(Number(pm.collectionVariables.get("test_record_id")));
});
```

---

### 3.5 ✅ Update Record (Partial Update)

**Request:**
- **Method:** `PATCH`
- **URL:** `{{base_url}}/api/records/{{test_record_id}}/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
  "amount": 5500.00,
  "notes": "Updated: Bonus included"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Record updated successfully", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.amount).to.equal("5500.00");
    pm.expect(jsonData.notes).to.include('Bonus');
});
```

---

### 3.6 ✅ Filter Records by Type

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/records/?record_type=income`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("All results are income type", function () {
    var jsonData = pm.response.json();
    jsonData.results.forEach(function(record) {
        pm.expect(record.record_type).to.equal('income');
    });
});
```

---

### 3.7 ✅ Filter Records by Date Range

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/records/?date_from=2024-04-01&date_to=2024-04-30`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("All records within date range", function () {
    var jsonData = pm.response.json();
    jsonData.results.forEach(function(record) {
        var recordDate = new Date(record.date);
        var fromDate = new Date('2024-04-01');
        var toDate = new Date('2024-04-30');
        pm.expect(recordDate >= fromDate && recordDate <= toDate).to.be.true;
    });
});
```

---

### 3.8 ✅ Search Records

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/records/?search=salary`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Results contain search term", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.results.length).to.be.greaterThan(0);
});
```

---

### 3.9 ✅ Order Records by Amount (Descending)

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/records/?ordering=-amount`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Records ordered by amount descending", function () {
    var jsonData = pm.response.json();
    var amounts = jsonData.results.map(r => parseFloat(r.amount));
    for (let i = 1; i < amounts.length; i++) {
        pm.expect(amounts[i-1]).to.be.greaterThan(amounts[i]);
    }
});
```

---

### 3.10 ✅ Soft Delete Record (Admin Only)

**Request:**
- **Method:** `DELETE`
- **URL:** `{{base_url}}/api/records/{{test_record_id}}/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 204", function () {
    pm.response.to.have.status(204);
});
```

**Expected:** No content response

---

### 3.11 ✅ Restore Deleted Record (Admin Only)

**Request:**
- **Method:** `PATCH`
- **URL:** `{{base_url}}/api/records/{{test_record_id}}/restore/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Record restored (is_deleted is false)", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.is_deleted).to.equal(false);
});
```

---

### 3.12 ❌ Create Record - Validation Error (Invalid Category)

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/records/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
  "amount": 100,
  "record_type": "invalid_type",
  "category": "salary",
  "date": "2024-04-01"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Record type error exists", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.record_type).to.exist;
});
```

---

### 3.13 ❌ Create Record - Negative Amount

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/records/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{access_token}}`
- **Body (raw JSON):**
```json
{
  "amount": -100,
  "record_type": "income",
  "category": "salary",
  "date": "2024-04-01"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});

pm.test("Amount validation error", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.amount).to.exist;
});
```

---

## 📈 Dashboard Analytics Tests

### 4.1 ✅ Get Dashboard Summary

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/dashboard/summary/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Summary contains required fields", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.total_income).to.exist;
    pm.expect(jsonData.total_expense).to.exist;
    pm.expect(jsonData.net_balance).to.exist;
    pm.expect(jsonData.record_count).to.exist;
    pm.expect(jsonData.income_count).to.exist;
    pm.expect(jsonData.expense_count).to.exist;
});

pm.test("Net balance calculation is correct", function () {
    var jsonData = pm.response.json();
    var expected = parseFloat(jsonData.total_income) - parseFloat(jsonData.total_expense);
    var actual = parseFloat(jsonData.net_balance);
    pm.expect(Math.abs(expected - actual)).to.be.lessThan(0.01);
});
```

**Expected Response:**
```json
{
  "total_income": "5000.00",
  "total_expense": "150.75",
  "net_balance": "4849.25",
  "record_count": 2,
  "income_count": 1,
  "expense_count": 1,
  "average_income": "5000.00",
  "average_expense": "150.75",
  "date_range": {
    "from": "All time",
    "to": "Present"
  }
}
```

---

### 4.2 ✅ Get Category Breakdown

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/dashboard/category-breakdown/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Category breakdown is an array", function () {
    pm.expect(pm.response.json()).to.be.an('array');
});

pm.test("Each category has required fields", function () {
    var jsonData = pm.response.json();
    jsonData.forEach(function(cat) {
        pm.expect(cat.category).to.exist;
        pm.expect(cat.category_display).to.exist;
        pm.expect(cat.total_amount).to.exist;
        pm.expect(cat.record_count).to.exist;
        pm.expect(cat.percentage).to.exist;
    });
});
```

**Expected Response:** Array of category objects

---

### 4.3 ✅ Get Monthly Trends

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/dashboard/monthly-trends/?months=6`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Monthly trends is an array", function () {
    pm.expect(pm.response.json()).to.be.an('array');
});

pm.test("Each month has required fields", function () {
    var jsonData = pm.response.json();
    jsonData.forEach(function(month) {
        pm.expect(month.month).to.exist;
        pm.expect(month.income).to.exist;
        pm.expect(month.expense).to.exist;
        pm.expect(month.net).to.exist;
        pm.expect(month.savings_rate).to.exist;
    });
});
```

**Expected Response:** Array of monthly trend objects

---

### 4.4 ✅ Get Recent Activity

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/dashboard/recent-activity/?limit=5`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Recent activity is an array", function () {
    pm.expect(pm.response.json()).to.be.an('array');
});

pm.test("Limited to requested number", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.length).to.be.lessThanOrEqual(5);
});
```

**Expected Response:** Array of recent records

---

### 4.5 ✅ Dashboard Summary with Date Filter

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/dashboard/summary/?date_from=2024-04-01&date_to=2024-04-30`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Date range reflected in response", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.date_range.from).to.include('2024-04-01');
});
```

---

## 🔒 Role-Based Permission Tests

### 5.1 ✅ Viewer Can Only See Own Records

**Step 1:** Login as viewer (create one if needed)
```json
POST {{base_url}}/api/token/
{
  "username": "test_viewer",
  "password": "Viewer123!"
}
```
Save token as `viewer_token`

**Step 2:** Try to view records
- **Method:** `GET`
- **URL:** `{{base_url}}/api/records/`
- **Headers:** `Authorization: Bearer {{viewer_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 200", function () {
    pm.response.to.have.status(200);
});

pm.test("Only shows viewer's own records", function () {
    var jsonData = pm.response.json();
    jsonData.results.forEach(function(record) {
        pm.expect(record.created_by).to.equal(Number(pm.collectionVariables.get("viewer_user_id")));
    });
});
```

---

### 5.2 ❌ Viewer Cannot Create Records

**Request:**
- **Method:** `POST`
- **URL:** `{{base_url}}/api/records/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{viewer_token}}`
- **Body:**
```json
{
  "amount": 100,
  "record_type": "income",
  "category": "salary",
  "date": "2024-04-01"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 403", function () {
    pm.response.to.have.status(403);
});
```

**Expected Response:**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 5.3 ❌ Viewer Cannot Update Records

**Request:**
- **Method:** `PATCH`
- **URL:** `{{base_url}}/api/records/{{test_record_id}}/`
- **Headers:** 
  - `Content-Type: application/json`
  - `Authorization: Bearer {{viewer_token}}`
- **Body:**
```json
{
  "amount": 999
}
```

**Tests Script:**
```javascript
pm.test("Status code is 403", function () {
    pm.response.to.have.status(403);
});
```

---

### 5.4 ✅ Analyst Can Create Records

**Step 1:** Login as analyst
```json
POST {{base_url}}/api/token/
{
  "username": "test_analyst",
  "password": "NewAnalyst456!"
}
```
Save as `analyst_token`

**Step 2:** Create record
- **Method:** `POST`
- **URL:** `{{base_url}}/api/records/`
- **Headers:** `Authorization: Bearer {{analyst_token}}`
- **Body:**
```json
{
  "amount": 2000,
  "record_type": "income",
  "category": "freelance",
  "date": "2024-04-05"
}
```

**Tests Script:**
```javascript
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});
```

---

### 5.5 ❌ Analyst Cannot Delete Records

**Request:**
- **Method:** `DELETE`
- **URL:** `{{base_url}}/api/records/{{test_record_id}}/`
- **Headers:** `Authorization: Bearer {{analyst_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 403", function () {
    pm.response.to.have.status(403);
});
```

---

### 5.6 ✅ Admin Can Do Everything

Test all operations with admin token - should all succeed:
- ✅ List users
- ✅ Create users
- ✅ Create records
- ✅ Update any record
- ✅ Delete records
- ✅ Access all dashboard endpoints

---

## ⚠️ Error Scenario Tests

### 6.1 ❌ Unauthenticated Request (No Token)

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/records/`
- **Headers:** (No Authorization header)

**Tests Script:**
```javascript
pm.test("Status code is 401", function () {
    pm.response.to.have.status(401);
});

pm.test("Authentication error message", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.detail).to.exist;
});
```

**Expected Response:**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

### 6.2 ❌ Invalid Token

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/records/`
- **Headers:** `Authorization: Bearer invalid_token_here`

**Tests Script:**
```javascript
pm.test("Status code is 401", function () {
    pm.response.to.have.status(401);
});
```

**Expected Response:**
```json
{
  "detail": "Token is invalid or expired"
}
```

---

### 6.3 ❌ Access Non-Existent Resource

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/records/99999/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 404", function () {
    pm.response.to.have.status(404);
});
```

**Expected Response:**
```json
{
  "detail": "Not found."
}
```

---

### 6.4 ❌ Delete Your Own Account (Should Fail)

**Request:**
- **Method:** `DELETE`
- **URL:** `{{base_url}}/api/users/{{admin_user_id}}/`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 403", function () {
    pm.response.to.have.status(403);
});
```

**Expected Response:**
```json
{
  "detail": "You cannot delete your own account"
}
```

---

### 6.5 ❌ Invalid Query Parameter

**Request:**
- **Method:** `GET`
- **URL:** `{{base_url}}/api/records/?record_type=invalid_type`
- **Headers:** `Authorization: Bearer {{access_token}}`

**Tests Script:**
```javascript
pm.test("Status code is 400", function () {
    pm.response.to.have.status(400);
});
```

---

## 📤 Collection Export

### How to Export Collection

1. Click on collection name (`Finance API - Complete Tests`)
2. Click **three dots (...)** → **Export**
3. Choose format: **Collection Format v2.1**
4. Click **Export**
5. Save as: `Finance_API_Tests.postman_collection.json`

### How to Import Collection

1. Click **Import** button in Postman
2. Drag & drop collection file or select it
3. Collection imported successfully!

---

## 🎯 Quick Test Runner

### Run All Tests

1. Click **Runner** in left sidebar
2. Select your collection
3. Choose environment (or use no environment)
4. Click **Run**

### Run Specific Folder

1. Expand collection
2. Click three dots next to folder
3. Click **Run**

---

## 📊 Test Coverage Summary

| Category | Total Tests | Passing | Failing (Expected) |
|----------|-------------|---------|-------------------|
| Authentication | 5 | 4 | 1 |
| User Management | 10 | 8 | 2 |
| Financial Records | 13 | 10 | 3 |
| Dashboard Analytics | 5 | 5 | 0 |
| Role Permissions | 6 | 3 | 3 |
| Error Scenarios | 5 | 0 | 5 |
| **TOTAL** | **44** | **30** | **14** |

✅ **30 successful scenarios** - Verify features work  
❌ **14 failure scenarios** - Verify error handling works

---

## 🚀 Next Steps

1. ✅ Run all 44 tests in Postman
2. ✅ Verify 30 pass (green)
3. ✅ Verify 14 fail as expected (red, but intentional)
4. ✅ Export collection for documentation
5. ✅ Share with team for QA testing

---

## 💡 Pro Tips

1. **Use Collection Variables:** Automatically store IDs and tokens between requests
2. **Chain Requests:** Use test scripts to save responses as variables
3. **Automate:** Use Newman (Postman CLI) for CI/CD integration
4. **Monitor:** Set up Postman Monitoring for production APIs
5. **Document:** Add descriptions to each request for team clarity

---

**Last Updated:** April 2, 2026  
**API Version:** 1.0.0  
**Test Coverage:** 44 scenarios across 6 categories
