# 🏗️ Authentication & Authorization Architecture

Visual overview of the authentication and authorization system architecture.

---

## 🔄 Authentication Flow

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │
       │ 1. POST /auth/login
       │    { email, password }
       ▼
┌─────────────────────────────────────┐
│     Login Controller                │
│  (features/auth/login)              │
└──────┬──────────────────────────────┘
       │
       │ 2. Execute
       ▼
┌─────────────────────────────────────┐
│     Login UseCase                   │
│  - Find user by email               │
│  - Verify password (bcrypt)         │
│  - Load employee & role             │
│  - Create JWT token                 │
└──────┬──────────────────────────────┘
       │
       │ 3. Return (user, token)
       ▼
┌─────────────────────────────────────┐
│     Login Controller                │
│  - Set HttpOnly cookie              │
│  - Return user info                 │
└──────┬──────────────────────────────┘
       │
       │ 4. Response + Set-Cookie
       ▼
┌─────────────┐
│   Client    │
│  (Browser)  │
│  Cookie: JWT│
└─────────────┘
```

---

## 🔐 Authorization Flow (Protected Route)

```
┌─────────────┐
│   Client    │
│  Cookie: JWT│
└──────┬──────┘
       │
       │ 1. GET /shifts/me
       │    Cookie: access_token=<JWT>
       ▼
┌─────────────────────────────────────┐
│  FastAPI Dependency System          │
│  get_current_user()                 │
└──────┬──────────────────────────────┘
       │
       │ 2. Extract JWT from cookie
       ▼
┌─────────────────────────────────────┐
│  Security Module (core/security.py) │
│  decode_access_token()              │
│  - Verify signature                 │
│  - Check expiration                 │
└──────┬──────────────────────────────┘
       │
       │ 3. Valid? Extract user_id
       ▼
┌─────────────────────────────────────┐
│  User Repository                    │
│  get_user_with_role(user_id)        │
│  - Query database                   │
│  - Load user + employee + role      │
└──────┬──────────────────────────────┘
       │
       │ 4. Return User object
       ▼
┌─────────────────────────────────────┐
│  Route Handler                      │
│  def get_my_shifts(                 │
│      current_user: User = Depends() │
│  )                                  │
│  - Access current_user.employee_id  │
│  - Query shifts                     │
└──────┬──────────────────────────────┘
       │
       │ 5. Response
       ▼
┌─────────────┐
│   Client    │
└─────────────┘
```

---

## 📊 Data Model Relationships

```
┌─────────────────┐
│      User       │
│  - id           │
│  - email        │
│  - hashed_pwd   │◄─────────┐
│  - is_active    │          │
│  - employee_id  │──┐       │
└─────────────────┘  │       │
                     │       │
                     │       │ One-to-One
                     │       │
                ┌────▼───────┴────┐
                │    Employee     │
                │  - id           │
                │  - first_name   │
                │  - last_name    │
                │  - email        │
                │  - role_id      │──┐
                │  - is_active    │  │
                └─────────────────┘  │
                                     │
                                     │ Many-to-One
                                     │
                                ┌────▼────────┐
                                │    Role     │
                                │  - id       │
                                │  - name     │
                                │  - perms    │
                                └─────────────┘

JWT Token Contains:
{
  "id": user.id,
  "email": user.email,
  "role": user.employee.role.name,
  "exp": expiration_timestamp
}
```

---

## 🛡️ Authorization Levels

```
┌────────────────────────────────────────────────────┐
│                    ADMIN / MANAGER                 │
│                                                    │
│  ✅ All employee CRUD operations                  │
│  ✅ All schedule/shift management                 │
│  ✅ Approve/reject absences                       │
│  ✅ View all resources                            │
│  ✅ Modify other users' data                      │
└────────────────────────────────────────────────────┘
                       ▲
                       │
                       │ Inherits all permissions
                       │
┌────────────────────────────────────────────────────┐
│                    EMPLOYEE                        │
│                                                    │
│  ✅ View own shifts (/shifts/me)                  │
│  ✅ View own absences (/absences/me)              │
│  ✅ Create own absence requests                   │
│  ✅ View/edit own availabilities                  │
│  ✅ View own work hours                           │
│  ❌ Cannot modify other employees' data           │
│  ❌ Cannot approve absences                       │
│  ❌ Cannot create/edit schedules                  │
└────────────────────────────────────────────────────┘
```

---

## 📁 Module Organization

```
backend/app/
│
├── core/                          # NEW: Cross-cutting concerns
│   ├── config.py                  # Environment configuration
│   ├── security.py                # Password hashing, JWT
│   ├── dependencies.py            # Auth dependencies
│   └── authorization.py           # Resource ownership checks
│
├── features/
│   ├── auth/                      # NEW: Authentication feature
│   │   ├── shared/
│   │   │   └── auth_dto.py        # Login/Token/User DTOs
│   │   ├── login/
│   │   │   ├── login_usecase.py
│   │   │   └── login_controller.py
│   │   ├── logout/
│   │   │   └── logout_controller.py
│   │   └── me/
│   │       └── get_me_controller.py
│   │
│   ├── shifts/
│   │   ├── get_my_shifts/         # NEW: User-specific endpoint
│   │   ├── get_my_hours/          # NEW: User-specific endpoint
│   │   └── ... (existing)
│   │
│   ├── absences/
│   │   ├── get_my_absences/       # NEW: User-specific endpoint
│   │   └── ... (existing + auth)
│   │
│   └── availabilities/
│       ├── get_my_availabilities/ # NEW: User-specific endpoint
│       └── ... (existing + auth)
│
├── repositories/
│   └── user_repository.py         # NEW: User queries
│
└── models/
    └── user.py                     # EXISTING (no changes)
```

---

## 🔑 Endpoint Protection Patterns

### Pattern 1: Require Authentication (Any logged-in user)

```python
from fastapi import Depends
from app.core.dependencies import get_current_user

@router.get("/shifts/me")
def get_my_shifts(current_user: User = Depends(get_current_user)):
    # current_user is automatically injected
    # 401 if not authenticated
    employee_id = current_user.employee_id
    return get_shifts_for_employee(employee_id)
```

### Pattern 2: Require Admin Role

```python
from app.core.dependencies import require_admin

@router.post("/employees", dependencies=[Depends(require_admin)])
def create_employee(data: EmployeeCreate):
    # Only admins can call this
    # 403 if not admin
    return create_employee_logic(data)
```

### Pattern 3: Resource Ownership Check

```python
from app.core.authorization import verify_resource_access

@router.get("/absences/{absence_id}")
def get_absence(
    absence_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    absence = db.query(Absence).filter_by(id=absence_id).first()
    
    # Check if user owns resource OR is admin
    verify_resource_access(current_user, absence.employee_id)
    
    return absence
```

### Pattern 4: Combined (Auth + Admin)

```python
@router.delete("/employees/{id}")
def delete_employee(
    id: int,
    current_user: User = Depends(require_admin)  # Admin required
):
    # Only admins reach here
    return delete_employee_logic(id)
```

---

## 🧪 Testing Strategy

### Unit Tests

```python
# tests/core/test_security.py
def test_hash_password():
    hashed = hash_password("password123")
    assert verify_password("password123", hashed)
    assert not verify_password("wrong", hashed)

def test_create_decode_token():
    data = {"id": 1, "email": "test@example.com"}
    token = create_access_token(data)
    payload = decode_access_token(token)
    assert payload["id"] == 1
```

### Integration Tests

```python
# tests/features/auth/test_login.py
def test_login_success(client, test_user):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.cookies

def test_login_invalid_credentials(client):
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "wrong"
    })
    assert response.status_code == 401

# tests/features/shifts/test_authorization.py
def test_get_my_shifts_authenticated(client, auth_headers):
    response = client.get("/shifts/me", headers=auth_headers)
    assert response.status_code == 200

def test_get_my_shifts_unauthenticated(client):
    response = client.get("/shifts/me")
    assert response.status_code == 401

def test_create_employee_admin_only(client, admin_token, regular_token):
    # Admin can create
    response = client.post("/employees", 
        cookies={"access_token": admin_token},
        json={...}
    )
    assert response.status_code == 201
    
    # Regular user cannot
    response = client.post("/employees", 
        cookies={"access_token": regular_token},
        json={...}
    )
    assert response.status_code == 403
```

---

## 🚀 Frontend Integration

### Login Example (Vue.js)

```javascript
// Login
async function login(email, password) {
  const response = await fetch('http://localhost:8000/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',  // IMPORTANT: Send/receive cookies
    body: JSON.stringify({ email, password })
  });
  
  if (response.ok) {
    const user = await response.json();
    // Cookie is automatically stored by browser
    return user;
  }
  throw new Error('Login failed');
}

// Authenticated request
async function getMyShifts() {
  const response = await fetch('http://localhost:8000/shifts/me', {
    credentials: 'include'  // IMPORTANT: Send cookies
  });
  
  if (response.status === 401) {
    // Redirect to login
    router.push('/login');
    return;
  }
  
  return response.json();
}

// Logout
async function logout() {
  await fetch('http://localhost:8000/auth/logout', {
    method: 'POST',
    credentials: 'include'
  });
  // Cookie is automatically cleared
}
```

### Axios Interceptor

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: true  // Always send cookies
});

// Response interceptor for 401
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      // Redirect to login
      router.push('/login');
    }
    return Promise.reject(error);
  }
);

export default api;
```

---

## 🔒 Security Best Practices

### ✅ Implemented

- **HttpOnly Cookies** – JavaScript cannot access tokens (XSS protection)
- **Secure Flag** – Cookies only sent over HTTPS in production
- **SameSite** – CSRF protection
- **Bcrypt** – Strong password hashing with salt
- **JWT Expiration** – Tokens expire after 30 minutes
- **Password Never Logged** – Sensitive data excluded from logs
- **Role-Based Access** – Least privilege principle
- **Resource Ownership** – Users can only access their data
- **Active User Check** – Inactive accounts cannot authenticate

### 🔜 Future Enhancements

- **Refresh Tokens** – Long-lived sessions with rotation
- **Account Lockout** – After N failed login attempts
- **2FA** – Two-factor authentication
- **Password Requirements** – Complexity rules
- **Password Reset** – Email-based recovery
- **Audit Logging** – Track sensitive operations
- **Rate Limiting** – Prevent brute force attacks

---

## 📝 Migration Path for Existing Routes

### Before (No Auth)

```python
@router.get("/shifts")
def get_shifts(
    employee_id: int = Query(None),
    db: Session = Depends(get_db)
):
    # Anyone can access
    # Anyone can specify any employee_id
    return get_shifts_logic(employee_id, db)
```

### After (With Auth)

```python
@router.get("/shifts")
def get_shifts(
    employee_id: int = Query(None),
    current_user: User = Depends(get_current_user),  # NEW
    db: Session = Depends(get_db)
):
    # Must be authenticated
    
    # If employee_id specified, verify access
    if employee_id:
        verify_resource_access(current_user, employee_id)  # NEW
    
    return get_shifts_logic(employee_id, db)

# New user-specific endpoint
@router.get("/shifts/me")
def get_my_shifts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Automatically uses current user's employee_id
    employee_id = current_user.employee_id
    return get_shifts_logic(employee_id, db)
```

---

**Document Version:** 1.0  
**Last Updated:** June 1, 2026
