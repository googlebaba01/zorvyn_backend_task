# Manual Testing Checklist

## ✅ Complete Testing Checklist for Finance Data API

Use this checklist to systematically test all features. Mark each item as you complete it.

---

## 📝 Pre-Testing Setup

- [ ] Django server running (`python manage.py runserver`)
- [ ] Sample data populated (`python manage.py populate_sample_data`)
- [ ] Postman opened
- [ ] Collection created: "Finance Data API"
- [ ] Base URL variable set: `http://127.0.0.1:8000`
- [ ] Access token variable created (empty initially)

---

## 🔐 Authentication Tests

### Admin Login
- [ ] POST `/api/token/` with admin credentials
- [ ] Received access and refresh tokens
- [ ] Copied access token to collection variable
- [ ] Verified token works by accessing protected endpoint

### Analyst Login
- [ ] POST `/api/token/` with analyst credentials
- [ ] Received valid token
- [ ] Token has correct permissions

### Viewer Login
- [ ] POST `/api/token/` with viewer credentials
- [ ] Received valid token
- [ ] Token has read-only permissions

### Invalid Login
- [ ] POST `/api/token/` with wrong password → 401 Unauthorized
- [ ] POST `/api/token/` with non-existent username → 401 Unauthorized

---

## 👥 User Management Tests (Admin Only)

### View Users
- [ ] GET `/api/users/` - List all users (should see 3)
- [ ] GET `/api/users/?role=admin` - Filter by role
- [ ] GET `/api/users/?is_active=true` - Filter by status
- [ ] GET `/api/users/1/` - Get single user details

### Create User
- [ ] POST `/api/users/` - Create new analyst user
- [ ] Verify password confirmation validation
- [ ] Verify email uniqueness validation
- [ ] Verify username uniqueness validation
- [ ] Check user appears in list

### Update User
- [ ] PUT `/api/users/{id}/` - Full update
- [ ] PATCH `/api/users/{id}/` - Partial update
- [ ] PATCH `/api/users/{id}/status/` - Toggle active/inactive
- [ ] Try to deactivate own account → Should fail

### Delete User
- [ ] DELETE `/api/users/{id}/` - Delete another user
- [ ] Try to delete own account → Should fail with error
- [ ] Verify deleted user not in list

### Change Password
- [ ] POST `/api/users/{id}/change-password/` - Valid change
- [ ] Old password verification works
- [ ] New passwords match validation
- [ ] Minimum length validation (8 chars)

---

## 💰 Financial Records Tests

### View Records
- [ ] GET `/api/records/` - List all records (paginated)
- [ ] Pagination working (next/previous links)
- [ ] GET `/api/records/{id}/` - Single record details
- [ ] Formatted amounts show correctly (+/- signs)

### Create Income Record
- [ ] POST `/api/records/` - Create income
- [ ] Amount stored as positive
- [ ] Effect amount shows positive
- [ ] Category-type validation works
- [ ] Date validation (no future dates)
- [ ] Created_by automatically set

### Create Expense Record
- [ ] POST `/api/records/` - Create expense
- [ ] Effect amount shows negative
- [ ] All required fields validated
- [ ] Optional fields (notes) work

### Update Records
- [ ] PATCH `/api/records/{id}/` - Update own record (as analyst)
- [ ] Admin can update any record
- [ ] Viewer cannot update → 403 Forbidden
- [ ] Validation errors on invalid data

### Delete Records
- [ ] DELETE `/api/records/{id}/` - Admin can delete
- [ ] Soft delete implemented (record still in DB)
- [ ] is_deleted flag set to True
- [ ] Deleted_at timestamp set
- [ ] Deleted records not shown in normal list

### Restore Records
- [ ] PATCH `/api/records/{id}/restore/` - Admin can restore
- [ ] is_deleted set back to False
- [ ] deleted_at cleared
- [ ] Record visible again in list

---

## 📊 Dashboard Analytics Tests

### Overall Summary
- [ ] GET `/api/dashboard/summary/` - Basic summary
- [ ] total_income calculated correctly
- [ ] total_expense calculated correctly
- [ ] net_balance = income - expense
- [ ] record_count accurate
- [ ] average_income calculated
- [ ] average_expense calculated

### Filtered Summary
- [ ] GET `/api/dashboard/summary/?date_from=2024-01-01` - Date filter
- [ ] GET `/api/dashboard/summary/?record_type=income` - Type filter
- [ ] Filters affect all calculations

### Category Breakdown
- [ ] GET `/api/dashboard/category-breakdown/` - All categories
- [ ] Percentages add up to ~100%
- [ ] total_amount per category correct
- [ ] record_count per category correct
- [ ] average_amount calculated
- [ ] Income and expense categories separate

### Monthly Trends
- [ ] GET `/api/dashboard/monthly-trends/?months=6` - Last 6 months
- [ ] GET `/api/dashboard/monthly-trends/?year=2024` - Specific year
- [ ] Monthly income totals correct
- [ ] Monthly expense totals correct
- [ ] Net calculation (income - expense)
- [ ] Savings rate percentage calculated
- [ ] Sorted chronologically

### Recent Activity
- [ ] GET `/api/dashboard/recent-activity/?limit=10` - Last 10
- [ ] Most recent first
- [ ] All required fields present
- [ ] Formatted amounts display correctly

---

## 🔒 Role-Based Permission Tests

### Viewer Permissions
- [ ] Can view dashboard summary
- [ ] Can view own records only
- [ ] Cannot view other users' records
- [ ] Cannot create records → 403
- [ ] Cannot update records → 403
- [ ] Cannot delete records → 403
- [ ] Cannot manage users → 403

### Analyst Permissions
- [ ] Can view dashboard summary
- [ ] Can view all records
- [ ] Can create records
- [ ] Can update own records
- [ ] Cannot update others' records → 403
- [ ] Cannot delete records → 403
- [ ] Cannot manage users → 403

### Admin Permissions
- [ ] Can view dashboard summary
- [ ] Can view all records
- [ ] Can create records
- [ ] Can update any record
- [ ] Can delete any record
- [ ] Can restore deleted records
- [ ] Can manage users
- [ ] Can toggle user status

---

## 🔍 Filtering & Search Tests

### Type Filtering
- [ ] `?record_type=income` - Income only
- [ ] `?record_type=expense` - Expense only

### Category Filtering
- [ ] `?category=salary` - Single category
- [ ] `?category=salary&category=freelance` - Multiple categories

### Date Range Filtering
- [ ] `?date_from=2024-01-01` - From date
- [ ] `?date_to=2024-12-31` - To date
- [ ] `?date_from=2024-03-01&date_to=2024-03-31` - Range

### Amount Range Filtering
- [ ] `?amount_min=1000` - Minimum amount
- [ ] `?amount_max=5000` - Maximum amount
- [ ] `?amount_min=500&amount_max=2000` - Range

### User Filtering
- [ ] `?created_by=1` - By specific user
- [ ] `?is_mine=true` - Current user's records only

### Search
- [ ] `?search=lunch` - Search in description
- [ ] `?search=project` - Search in notes
- [ ] Case-insensitive search works

### Combined Filters
- [ ] Multiple filters work together
- [ ] `?record_type=expense&category=food&date_from=2024-01-01`

### Ordering
- [ ] `?ordering=-amount` - Descending by amount
- [ ] `?ordering=date` - Ascending by date
- [ ] `?ordering=-created_at` - Newest first

### Pagination
- [ ] Default page size (20 items)
- [ ] `?page=2` - Second page
- [ ] Next/Previous links work
- [ ] Count field accurate

---

## ⚠️ Validation Tests

### Amount Validation
- [ ] Negative amount → 400 error
- [ ] Zero amount → 400 error
- [ ] Very large amount (>999B) → 400 error
- [ ] Decimal places handled correctly

### Date Validation
- [ ] Future date → 400 error
- [ ] Invalid date format → 400 error
- [ ] Null date → Uses default (today)

### Required Fields
- [ ] Missing amount → 400 error
- [ ] Missing record_type → 400 error
- [ ] Missing category → 400 error
- [ ] All required fields enforced

### Category-Type Matching
- [ ] Income type with expense category → 400 error
- [ ] Expense type with income category → 400 error
- [ ] Correct combinations accepted

### String Lengths
- [ ] Description >200 chars → 400 error
- [ ] Notes >2000 chars → 400 error
- [ ] Username <3 chars → 400 error

### Password Validation
- [ ] Password <8 chars → 400 error
- [ ] Password mismatch → 400 error
- [ ] Common passwords rejected

---

## 🔄 Token Management Tests

### Token Refresh
- [ ] POST `/api/token/refresh/` with valid refresh token
- [ ] Received new access token
- [ ] New token works for API calls

### Token Expiration
- [ ] Wait for token to expire (60 minutes)
- [ ] Expired token → 401 Unauthorized
- [ ] Must login again

### Invalid Tokens
- [ ] Malformed token → 401 Unauthorized
- [ ] Random string as token → 401
- [ ] Expired refresh token → 401

---

## 🎯 Edge Cases & Special Scenarios

### Empty States
- [ ] No records in database → Empty array returned
- [ ] No users except admin → List shows only admin
- [ ] Date range with no data → Zeros in summary

### Large Datasets
- [ ] 100+ records → Pagination works
- [ ] Many users → List paginated
- [ ] Performance acceptable

### Concurrent Operations
- [ ] Two users creating records simultaneously → Both succeed
- [ ] Update while another deletes → Proper locking

### Soft Delete Behavior
- [ ] Deleted records excluded from summaries
- [ ] Deleted records excluded from analytics
- [ ] Can filter to show only deleted: `?is_deleted=true`

---

## 📈 Performance Checks

- [ ] API response time < 500ms for most endpoints
- [ ] Paginated responses load quickly
- [ ] Complex aggregations (dashboard) < 1 second
- [ ] No N+1 query issues (check Django logs)

---

## 🛡️ Security Verification

- [ ] Cannot access API without token → 401
- [ ] Inactive user cannot login → Token not issued
- [ ] SQL injection attempts fail (ORM protects)
- [ ] XSS attempts in text fields sanitized
- [ ] CORS headers configured correctly

---

## ✅ Final Verification

### All Features Working
- [ ] Authentication ✅
- [ ] User management ✅
- [ ] Financial records CRUD ✅
- [ ] Dashboard analytics ✅
- [ ] Filtering & search ✅
- [ ] Role-based permissions ✅
- [ ] Validation ✅
- [ ] Error handling ✅

### Documentation
- [ ] README.md reviewed
- [ ] API documentation checked
- [ ] All endpoints documented in Swagger
- [ ] Code comments clear

### Ready for Submission
- [ ] All tests passing
- [ ] No console errors
- [ ] Sample data loads correctly
- [ ] Deployment guide tested
- [ ] GitHub repository prepared

---

## 📊 Test Summary

**Total Tests:** ~100  
**Passed:** _____  
**Failed:** _____  
**Blocked:** _____  

**Test Duration:** _____ minutes

**Issues Found:**
1. _________________________________
2. _________________________________
3. _________________________________

**Overall Status:** ⬜ Pass / ⬜ Fail

---

**Tester:** _________________  
**Date:** _________________  
**Environment:** Local Development

---

**Next Steps:**
- [ ] Fix any failed tests
- [ ] Document known issues
- [ ] Prepare for deployment
- [ ] Update documentation if needed
