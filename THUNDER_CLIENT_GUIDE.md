# Thunder Client Testing Guide - NGO Fund Backend

## Setup Instructions

### 1. Import Collection and Environment
1. Open Thunder Client in VS Code
2. Click "Collections" → "Import" → Select `thunder-client-collection.json`
3. Click "Env" → "Import" → Select `thunder-client-environment.json`
4. Set environment to "NGO Fund Development"

### 2. Start Django Server
```bash
cd /home/don/Projects/Solvit-Africa/NGO_Fund_Backend
python manage.py runserver
```

## Available Endpoints

### Base URL: `http://127.0.0.1:8000`

### Authentication Endpoints

#### 1. Register User (All Types Allowed)
- **URL:** `POST /api/accounts/user/`
- **Body:**
```json
{
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe", 
  "password": "SecurePass123!",
  "re_password": "SecurePass123!",
  "phone_number": "+254712345678",
  "user_type": "DONOR"
}
```
- **User Types:** `ADMIN`, `FINANCE`, `AUDITOR`, `DONOR`
- **DONOR:** Active immediately, can login right away
- **Others:** Created as inactive, need admin approval
- **Phone Format:** Exactly 15 characters (e.g., +254712345678)

#### 2. Login User
- **URL:** `POST /api/accounts/login/`
- **Body:**
```json
{
  "email": "donor@example.com",
  "password": "SecurePass123!"
}
```
- **Response:** Returns `access` and `refresh` tokens
- **Note:** Copy the `access` token to `access_token` environment variable

### User Management Endpoints

#### 3. Get User Profile
- **URL:** `GET /api/accounts/user/profile/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Description:** Get current user's profile

#### 4. List All Users (Admin Only)
- **URL:** `GET /api/accounts/user/`
- **Headers:** `Authorization: Bearer {{admin_token}}`
- **Permission:** Requires ADMIN user type

#### 5. Get User Detail
- **URL:** `GET /api/accounts/user/{user_id}/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Note:** Replace `{user_id}` with actual UUID

#### 6. Update User
- **URL:** `PUT /api/accounts/user/{user_id}/`
- **Headers:** `Authorization: Bearer {{access_token}}`
- **Body:**
```json
{
  "first_name": "Jane",
  "last_name": "Smith",
  "phone_number": "+254712345679"
}
```

#### 7. Delete User
- **URL:** `DELETE /api/accounts/user/{user_id}/`
- **Headers:** `Authorization: Bearer {{access_token}}`

## Testing Workflow

### Step 1: Create Test Users
1. **Register Donor:**
   - Use "Register User" request
   - Set `user_type` to `DONOR`
   - User becomes active immediately

2. **Register Other User Types:**
   - Use "Register User" request
   - Set `user_type` to `ADMIN`, `FINANCE`, or `AUDITOR`
   - Users are created but inactive, need admin approval

3. **Create Superuser (via Django Admin):**
   ```bash
   python manage.py createsuperuser
   ```

### Step 2: Authentication Flow
1. **Login as Donor:**
   - Use "Login User" request
   - Copy `access` token to environment variable

2. **Login as Admin:**
   - Use "Login User" with admin credentials
   - Copy `access` token to `admin_token` environment variable

### Step 3: Test Protected Endpoints
1. **Test Profile Access:**
   - Use "Get User Profile" with donor token

2. **Test Admin Access:**
   - Use "List All Users" with admin token
   - Should return all users

3. **Test User CRUD:**
   - Get user detail
   - Update user information
   - Delete user (if needed)

## User Registration & Approval Flow

### DONOR Users (Self-Registration)
- Can register directly via API
- Become active immediately
- Can login and access system right away

### ADMIN/FINANCE/AUDITOR Users (Admin Approval Required)
- Can register via API
- Account created successfully but inactive (`is_active=False`)
- Receive message: "Account created successfully. Please wait for admin approval before you can login."
- Cannot login until admin approves them
- Admin must approve them using "Approve selected pending users" action

### Admin Approval Process
1. Login to Django Admin: `http://127.0.0.1:8000/admin/`
2. Go to Users section
3. Select pending users (inactive users)
4. Choose "Approve selected pending users" from Actions dropdown
5. Click "Go" to activate selected users

## Sample Test Data

### Donor User
```json
{
  "email": "donor@ngofund.com",
  "first_name": "Alice",
  "last_name": "Johnson",
  "password": "DonorPass123!",
  "re_password": "DonorPass123!",
  "phone_number": "+254701234567",
  "user_type": "DONOR"
}
```

### Finance User
```json
{
  "email": "finance@ngofund.com",
  "first_name": "Bob",
  "last_name": "Wilson",
  "password": "FinancePass123!",
  "re_password": "FinancePass123!",
  "phone_number": "+254702234567",
  "user_type": "FINANCE"
}
```

### Auditor User
```json
{
  "email": "auditor@ngofund.com",
  "first_name": "Carol",
  "last_name": "Davis",
  "password": "AuditorPass123!",
  "re_password": "AuditorPass123!",
  "phone_number": "+254703234567",
  "user_type": "AUDITOR"
}
```

## Expected Responses

### Successful DONOR Registration
```json
{
  "id": "uuid-string",
  "email": "donor@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+254712345678",
  "is_active": true,
  "user_type": "DONOR",
  "message": "Account created successfully. You can now login."
}
```

### Successful Non-DONOR Registration
```json
{
  "id": "uuid-string",
  "email": "admin@example.com",
  "first_name": "Admin",
  "last_name": "User",
  "phone_number": "+254712345679",
  "is_active": false,
  "user_type": "ADMIN",
  "message": "Account created successfully. Please wait for admin approval before you can login."
}
```

### Successful Login
```json
{
  "access": "jwt-access-token",
  "refresh": "jwt-refresh-token"
}
```

### User Profile
```json
{
  "id": "uuid-string",
  "email": "donor@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "phone_number": "+254712345678",
  "is_active": true,
  "user_type": "DONOR"
}
```

## Common Issues & Solutions

### 1. Phone Number Validation
- **Error:** Phone number must be exactly 15 characters
- **Solution:** Use format like `+254712345678` (country code + number)

### 2. Password Mismatch
- **Error:** "Password and Confirm Password does not match"
- **Solution:** Ensure `password` and `re_password` are identical

### 3. Authentication Required
- **Error:** 401 Unauthorized
- **Solution:** Include `Authorization: Bearer {token}` header

### 4. Permission Denied
- **Error:** 403 Forbidden
- **Solution:** Use admin token for admin-only endpoints

### 6. Inactive User Login Attempt
- **Error:** Login fails for inactive users
- **Solution:** Admin must approve the user account first using Django Admin

### 7. Database Connection

Make sure your `.env` file contains:
```
DEV_DB_NAME=ngofund_db
DEV_DB_USER=don
DEV_DB_PASSWORD=Tresor92@
```

## Database Setup

If you haven't set up the database yet:
```bash
# Create database
mysql -u root -p
CREATE DATABASE ngofund_db;

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```