# 🔐 Authentication & Authorization Roadmap

_Implementation plan for JWT-based authentication and role-based authorization_

---

## 📖 Overview

This roadmap outlines the implementation of a comprehensive authentication and authorization system for the Timeapp backend API. The system will use **JWT tokens in HttpOnly cookies** for secure session management and **role-based access control (RBAC)** for resource protection.

### Key Features
- ✅ **JWT Authentication** – Secure token-based authentication with HttpOnly cookies
- ✅ **User-Specific Routes** – `/me` endpoints that return data for the authenticated user
- ✅ **Role-Based Authorization** – Admin and user-level access control
- ✅ **Resource Ownership** – Users can only access their own resources

### Architecture Alignment
This implementation follows the existing **Vertical Slice Architecture** pattern:
- **Models** – Already exists (User, Employee, Role)
- **DTOs/Schemas** – Request/response models
- **UseCases** – Business logic for authentication/authorization
- **Controllers** – API endpoints
- **Dependencies** – Reusable auth dependencies for FastAPI
- **Tests** – Comprehensive unit and integration tests

---

## 🎯 Implementation Phases

### Phase 1: Authentication Infrastructure
**Goal:** Implement secure JWT-based login with HttpOnly cookies

### Phase 2: User-Specific Routes
**Goal:** Create `/me` endpoints for authenticated users to access their own data

### Phase 3: Authorization & Access Control
**Goal:** Protect existing routes with role-based and ownership-based authorization

---

# Phase 1 – Authentication Infrastructure

## US-0.1: Password Hashing Utilities

**As a** developer  
**I want** secure password hashing and verification utilities  
**So that** user passwords are never stored in plain text

### Acceptance Criteria
- ✅ Hash passwords using bcrypt
- ✅ Verify password against hash
- ✅ Configurable hashing rounds for performance/security trade-off

### Technical Sub-tasks

#### 1. Install Dependencies
```bash
# Add to requirements.txt
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-dotenv==1.0.0  # For environment variables
```

#### 2. Create Password Utilities
- **File**: `backend/app/core/security.py`
- **Functions**:
  - `hash_password(password: str) -> str` – Hash a plain password
  - `verify_password(plain_password: str, hashed_password: str) -> bool` – Verify password
  - **Dependencies**: passlib.context.CryptContext with bcrypt

#### 3. Environment Configuration
- **File**: `backend/.env`
- **Variables**:
  ```
  SECRET_KEY=<random-secret-key>
  ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=30
  ```

#### 4. Configuration Module
- **File**: `backend/app/core/config.py`
- **Class**: `Settings` (Pydantic BaseSettings)
- **Fields**: secret_key, algorithm, access_token_expire_minutes
- Load from environment variables

**Dependencies:** None

---

## US-0.2: JWT Token Generation & Validation

**As a** developer  
**I want** utilities to create and validate JWT tokens  
**So that** I can implement stateless authentication

### Acceptance Criteria
- ✅ Generate JWT tokens with user claims (id, email, role)
- ✅ Validate and decode JWT tokens
- ✅ Handle token expiration
- ✅ Support refresh token flow (optional for Phase 1)

### Technical Sub-tasks

#### 1. JWT Utilities
- **File**: `backend/app/core/security.py` (extend)
- **Functions**:
  - `create_access_token(data: dict, expires_delta: timedelta = None) -> str`
    - Encode user data (id, email, role) into JWT
    - Add expiration claim (exp)
    - Sign with SECRET_KEY
  - `decode_access_token(token: str) -> dict`
    - Decode and validate JWT
    - Verify signature and expiration
    - Return payload or raise exception

#### 2. Token Schema
- **File**: `backend/app/features/auth/shared/auth_dto.py`
- **Classes**:
  - `TokenPayload` – id: int, email: str, role: str, exp: datetime
  - `TokenData` – Optional parsed token data

**Dependencies:** US-0.1 (config)

---

## US-0.3: User Repository Extensions

**As a** developer  
**I want** repository methods to query users for authentication  
**So that** I can validate login credentials

### Acceptance Criteria
- ✅ Find user by email
- ✅ Include related employee and role data
- ✅ Check if user is active

### Technical Sub-tasks

#### 1. Create User Repository
- **File**: `backend/app/repositories/user_repository.py`
- **Class**: `UserRepository(BaseRepository[User])`
- **Methods**:
  - `get_by_email(email: str) -> Optional[User]`
    - Query user by email
    - Join with Employee and Role for efficient loading
  - `get_user_with_role(user_id: int) -> Optional[User]`
    - Get user with employee and role data loaded

#### 2. Update Repository Index
- **File**: `backend/app/repositories/__init__.py`
- Export `UserRepository`

**Dependencies:** None (User model already exists)

---

## US-0.4: Login Use Case

**As a** user  
**I want** to log in with my email and password  
**So that** I can access the application

### Acceptance Criteria
- ✅ Authenticate user with email and password
- ✅ Return JWT token in HttpOnly cookie
- ✅ Include user info in response (id, email, role)
- ✅ Reject invalid credentials with appropriate error
- ✅ Reject inactive users

### Technical Sub-tasks

#### 1. Login DTOs
- **File**: `backend/app/features/auth/shared/auth_dto.py`
- **Classes**:
  - `LoginRequest` – email: EmailStr, password: str
  - `LoginResponse` – id: int, email: str, role: str, first_name: str, last_name: str

#### 2. Login Use Case
- **File**: `backend/app/features/auth/login/login_usecase.py`
- **Class**: `LoginUseCase`
- **Method**: `execute(email: str, password: str) -> tuple[User, str]`
- **Logic**:
  1. Find user by email using UserRepository
  2. Verify user exists and is active
  3. Verify password using `verify_password()`
  4. Load employee and role data
  5. Create JWT token with user claims (id, email, role)
  6. Return (user, token)
- **Exceptions**:
  - 401 if user not found
  - 401 if password incorrect
  - 403 if user inactive

#### 3. Login Controller
- **File**: `backend/app/features/auth/login/login_controller.py`
- **Endpoint**: `POST /auth/login`
- **Request**: LoginRequest (JSON body)
- **Response**: LoginResponse
- **Cookie**: Set HttpOnly cookie with JWT
  ```python
  response.set_cookie(
      key="access_token",
      value=token,
      httponly=True,
      secure=True,  # HTTPS only in production
      samesite="lax",
      max_age=1800  # 30 minutes
  )
  ```

#### 4. Auth Router
- **File**: `backend/app/features/auth/__init__.py`
- **Export**: `router` with prefix `/auth` and tag `authentication`

#### 5. Register in Main App
- **File**: `backend/app/main.py`
- Import and include auth router

**Dependencies:** US-0.1, US-0.2, US-0.3

---

## US-0.5: Logout Use Case

**As a** logged-in user  
**I want** to log out of the application  
**So that** my session is terminated

### Acceptance Criteria
- ✅ Clear HttpOnly cookie
- ✅ Return success message

### Technical Sub-tasks

#### 1. Logout Controller
- **File**: `backend/app/features/auth/logout/logout_controller.py`
- **Endpoint**: `POST /auth/logout`
- **Response**: `{"message": "Successfully logged out"}`
- **Cookie**: Delete access_token cookie
  ```python
  response.delete_cookie(key="access_token")
  ```

**Dependencies:** US-0.4

---

## US-0.6: Get Current User Dependency

**As a** developer  
**I want** a reusable dependency to extract the current user from JWT  
**So that** I can protect endpoints and access user context

### Acceptance Criteria
- ✅ Extract JWT from HttpOnly cookie
- ✅ Validate and decode token
- ✅ Load user from database
- ✅ Raise 401 if token invalid/expired
- ✅ Raise 403 if user inactive

### Technical Sub-tasks

#### 1. Auth Dependencies
- **File**: `backend/app/core/dependencies.py`
- **Functions**:
  - `get_current_user(request: Request, db: Session = Depends(get_db)) -> User`
    - Extract token from `request.cookies.get("access_token")`
    - Decode token using `decode_access_token()`
    - Query user from database with UserRepository
    - Verify user is active
    - Return User object
  - `get_current_active_user(current_user: User = Depends(get_current_user)) -> User`
    - Wrapper to ensure user is active
    - Raise HTTPException(403) if not active

#### 2. Update Dependency Index
- **File**: `backend/app/core/__init__.py`
- Export dependencies

**Dependencies:** US-0.2, US-0.3

---

## US-0.7: Get Current User Info Endpoint

**As a** logged-in user  
**I want** to retrieve my own user information  
**So that** I can display it in the UI

### Acceptance Criteria
- ✅ Return current user's id, email, role, employee info
- ✅ Require authentication (JWT cookie)

### Technical Sub-tasks

#### 1. User Info DTO
- **File**: `backend/app/features/auth/shared/auth_dto.py`
- **Class**: `UserInfoResponse`
- **Fields**: id, email, is_active, employee (embedded EmployeeResponse)

#### 2. Get Current User Controller
- **File**: `backend/app/features/auth/me/get_me_controller.py`
- **Endpoint**: `GET /auth/me`
- **Response**: UserInfoResponse
- **Dependency**: `current_user: User = Depends(get_current_user)`
- **Logic**: Return current user data with employee and role

**Dependencies:** US-0.6

---

# Phase 2 – User-Specific Routes (`/me` endpoints)

## US-2.1: Get My Shifts Endpoint

**As a** logged-in employee  
**I want** to view my assigned shifts  
**So that** I can see my work schedule

### Acceptance Criteria
- ✅ Return shifts assigned to the current user's employee
- ✅ Support date range filtering
- ✅ Include shift details (schedule, role, hours)

### Technical Sub-tasks

#### 1. Get My Shifts Use Case
- **File**: `backend/app/features/shifts/get_my_shifts/get_my_shifts_usecase.py`
- **Class**: `GetMyShiftsUseCase`
- **Method**: `execute(employee_id: int, start_date: date = None, end_date: date = None) -> List[Shift]`
- **Logic**:
  - Query shifts using ShiftRepository
  - Filter by employee_id (from ShiftAssignment)
  - Apply date range filters if provided
  - Include related data (schedule, role)

#### 2. Get My Shifts Controller
- **File**: `backend/app/features/shifts/get_my_shifts/get_my_shifts_controller.py`
- **Endpoint**: `GET /shifts/me`
- **Query Params**: start_date (optional), end_date (optional)
- **Response**: List[ShiftResponse]
- **Dependency**: `current_user: User = Depends(get_current_user)`
- **Logic**:
  - Verify user has linked employee (`current_user.employee`)
  - Call use case with employee_id
  - Return shift data

**Dependencies:** US-0.6

---

## US-2.2: Get My Absences Endpoint

**As a** logged-in employee  
**I want** to view my absence requests  
**So that** I can track my time off

### Acceptance Criteria
- ✅ Return absences for current user's employee
- ✅ Include status (pending, approved, rejected)
- ✅ Support filtering by status

### Technical Sub-tasks

#### 1. Get My Absences Use Case
- **File**: `backend/app/features/absences/get_my_absences/get_my_absences_usecase.py`
- **Class**: `GetMyAbsencesUseCase`
- **Method**: `execute(employee_id: int, status: str = None) -> List[Absence]`

#### 2. Get My Absences Controller
- **File**: `backend/app/features/absences/get_my_absences/get_my_absences_controller.py`
- **Endpoint**: `GET /absences/me`
- **Query Params**: status (optional)
- **Response**: List[AbsenceResponse]
- **Dependency**: `current_user: User = Depends(get_current_user)`

**Dependencies:** US-0.6

---

## US-2.3: Get My Availabilities Endpoint

**As a** logged-in employee  
**I want** to view my availability settings  
**So that** I can see when I'm available to work

### Acceptance Criteria
- ✅ Return availabilities for current user's employee
- ✅ Include day of week and time ranges

### Technical Sub-tasks

#### 1. Get My Availabilities Controller
- **File**: `backend/app/features/availabilities/get_my_availabilities/get_my_availabilities_controller.py`
- **Endpoint**: `GET /availabilities/me`
- **Response**: List[AvailabilityResponse]
- **Dependency**: `current_user: User = Depends(get_current_user)`
- **Note**: Use existing `get_employee_availabilities` use case, just pass current user's employee_id

**Dependencies:** US-0.6

---

## US-2.4: Get My Work Hours Summary

**As a** logged-in employee  
**I want** to view my total work hours  
**So that** I can track my time worked

### Acceptance Criteria
- ✅ Calculate total hours from assigned shifts
- ✅ Support date range filtering
- ✅ Return summary by week/month

### Technical Sub-tasks

#### 1. Get My Hours Controller
- **File**: `backend/app/features/shifts/get_my_hours/get_my_hours_controller.py`
- **Endpoint**: `GET /shifts/me/hours`
- **Query Params**: start_date, end_date
- **Response**: HoursSummaryResponse
- **Dependency**: `current_user: User = Depends(get_current_user)`
- **Note**: Reuse existing hours calculation logic from `get_hours` feature

**Dependencies:** US-0.6

---

# Phase 3 – Authorization & Access Control

## US-3.1: Role-Based Authorization Dependencies

**As a** developer  
**I want** reusable dependencies for role-based authorization  
**So that** I can restrict endpoints to specific roles

### Acceptance Criteria
- ✅ Verify user has required role
- ✅ Support admin-only endpoints
- ✅ Support manager-level endpoints

### Technical Sub-tasks

#### 1. Role Authorization Dependencies
- **File**: `backend/app/core/dependencies.py` (extend)
- **Functions**:
  - `require_role(required_roles: List[str])`
    - Returns a dependency function
    - Verifies current_user.employee.role.name in required_roles
    - Raises HTTPException(403) if unauthorized
  - `require_admin(current_user: User = Depends(get_current_user)) -> User`
    - Shortcut for admin-only endpoints
    - Verifies role is "Manager" or "Admin"
  - `require_manager(current_user: User = Depends(get_current_user)) -> User`
    - For manager-level permissions

**Dependencies:** US-0.6

---

## US-3.2: Resource Ownership Validation

**As a** developer  
**I want** utilities to verify resource ownership  
**So that** users can only access their own resources

### Acceptance Criteria
- ✅ Verify employee owns a resource
- ✅ Allow admin override (admins can access all resources)
- ✅ Raise 403 for unauthorized access

### Technical Sub-tasks

#### 1. Ownership Utilities
- **File**: `backend/app/core/authorization.py`
- **Functions**:
  - `verify_resource_access(current_user: User, resource_employee_id: int) -> bool`
    - Return True if:
      - current_user.employee_id == resource_employee_id OR
      - current_user.employee.role.name in ["Admin", "Manager"]
    - Raise HTTPException(403) if False
  - `is_admin_or_manager(user: User) -> bool`
    - Helper to check admin privileges

**Dependencies:** US-0.6

---

## US-3.3: Protect Employee Management Endpoints

**As a** manager  
**I want** employee CRUD endpoints restricted to managers  
**So that** regular employees cannot modify employee data

### Acceptance Criteria
- ✅ Only managers can create/update/delete employees
- ✅ All users can view employee list (read-only)
- ✅ Users can view their own employee details

### Technical Sub-tasks

#### 1. Update Employee Controllers
- **Files**:
  - `backend/app/features/employees/create_employee/create_employee_controller.py`
  - `backend/app/features/employees/update_employee/update_employee_controller.py`
  - `backend/app/features/employees/delete_employee/delete_employee_controller.py`
- **Add Dependency**: `current_user: User = Depends(require_admin)`

#### 2. Update Get Employee Endpoint
- **File**: `backend/app/features/employees/get_one_employee/get_one_employee_controller.py`
- **Add Logic**: Verify user is admin OR requesting their own employee record

**Dependencies:** US-3.1

---

## US-3.4: Protect Absence Management Endpoints

**As a** system  
**I want** absence approval restricted to managers  
**So that** only authorized personnel can approve time off

### Acceptance Criteria
- ✅ Employees can create/view their own absences
- ✅ Only managers can approve/reject absences
- ✅ Employees cannot approve their own absences

### Technical Sub-tasks

#### 1. Update Absence Controllers
- **Files**:
  - `backend/app/features/absences/approve_absence/approve_absence_controller.py`
  - `backend/app/features/absences/reject_absence/reject_absence_controller.py`
- **Add Dependency**: `current_user: User = Depends(require_manager)`

#### 2. Update Create Absence Controller
- **File**: `backend/app/features/absences/create_absence/create_absence_controller.py`
- **Add Dependency**: `current_user: User = Depends(get_current_user)`
- **Add Logic**: Verify employee_id matches current_user.employee_id (or user is manager)

**Dependencies:** US-3.1, US-3.2

---

## US-3.5: Protect Schedule & Shift Management

**As a** manager  
**I want** schedule and shift management restricted to managers  
**So that** only authorized personnel can modify work schedules

### Acceptance Criteria
- ✅ Only managers can create/update/delete schedules
- ✅ Only managers can create/update/delete shifts
- ✅ Only managers can assign employees to shifts
- ✅ All employees can view schedules (read-only)

### Technical Sub-tasks

#### 1. Update Schedule Controllers
- **Files**:
  - `backend/app/features/schedules/create_schedule/create_schedule_controller.py`
  - `backend/app/features/schedules/update_schedule/update_schedule_controller.py`
  - `backend/app/features/schedules/delete_schedule/delete_schedule_controller.py`
- **Add Dependency**: `current_user: User = Depends(require_manager)`

#### 2. Update Shift Controllers
- **Files**:
  - `backend/app/features/shifts/create_shift/create_shift_controller.py`
  - `backend/app/features/shifts/update_shift/update_shift_controller.py`
  - `backend/app/features/shifts/delete_shift/delete_shift_controller.py`
  - `backend/app/features/shifts/assign_employee/assign_employee_controller.py`
  - `backend/app/features/shifts/remove_assignment/remove_assignment_controller.py`
- **Add Dependency**: `current_user: User = Depends(require_manager)`
- **Remove**: Manual manager_id parameter (use current_user instead)

**Dependencies:** US-3.1

---

## US-3.6: Protect Availability Management

**As a** system  
**I want** availability management properly secured  
**So that** users can only modify their own availability

### Acceptance Criteria
- ✅ Employees can create/update/delete their own availabilities
- ✅ Managers can modify any employee's availability
- ✅ Users cannot modify other employees' availability

### Technical Sub-tasks

#### 1. Update Availability Controllers
- **Files**:
  - `backend/app/features/availabilities/create_availability/create_availability_controller.py`
  - `backend/app/features/availabilities/update_availability/update_availability_controller.py`
  - `backend/app/features/availabilities/delete_availability/delete_availability_controller.py`
- **Add Dependency**: `current_user: User = Depends(get_current_user)`
- **Add Logic**: Use `verify_resource_access()` to check ownership or admin status

**Dependencies:** US-3.2

---

## US-3.7: Update Seed Data with Test Users

**As a** developer  
**I want** seed data to include test users with hashed passwords  
**So that** I can test authentication in development

### Acceptance Criteria
- ✅ Create admin user (admin@example.com)
- ✅ Create manager user (manager@example.com)
- ✅ Create regular employee user (employee@example.com)
- ✅ Link users to employees
- ✅ Use properly hashed passwords

### Technical Sub-tasks

#### 1. Update Seed Script
- **File**: `backend/app/seed.py`
- **Add**: User creation with hashed passwords
- **Test Accounts**:
  ```python
  {
    "email": "admin@example.com",
    "password": "admin123",  # Hashed in code
    "role": "Manager"
  },
  {
    "email": "employee@example.com",
    "password": "employee123",
    "role": "Employee"
  }
  ```

**Dependencies:** US-0.1

---

# 📊 Implementation Summary

## Phase 1: Authentication Infrastructure
| Task | Estimated Effort | Dependencies |
|------|-----------------|--------------|
| US-0.1: Password Hashing | 2 hours | None |
| US-0.2: JWT Utilities | 3 hours | US-0.1 |
| US-0.3: User Repository | 2 hours | None |
| US-0.4: Login Use Case | 4 hours | US-0.1, US-0.2, US-0.3 |
| US-0.5: Logout Use Case | 1 hour | US-0.4 |
| US-0.6: Current User Dependency | 3 hours | US-0.2, US-0.3 |
| US-0.7: Get Current User Info | 2 hours | US-0.6 |
| **Total Phase 1** | **17 hours** | |

## Phase 2: User-Specific Routes
| Task | Estimated Effort | Dependencies |
|------|-----------------|--------------|
| US-2.1: Get My Shifts | 3 hours | US-0.6 |
| US-2.2: Get My Absences | 2 hours | US-0.6 |
| US-2.3: Get My Availabilities | 1 hour | US-0.6 |
| US-2.4: Get My Work Hours | 2 hours | US-0.6 |
| **Total Phase 2** | **8 hours** | |

## Phase 3: Authorization & Access Control
| Task | Estimated Effort | Dependencies |
|------|-----------------|--------------|
| US-3.1: Role Authorization | 3 hours | US-0.6 |
| US-3.2: Resource Ownership | 2 hours | US-0.6 |
| US-3.3: Protect Employees | 2 hours | US-3.1 |
| US-3.4: Protect Absences | 2 hours | US-3.1, US-3.2 |
| US-3.5: Protect Schedules/Shifts | 3 hours | US-3.1 |
| US-3.6: Protect Availabilities | 2 hours | US-3.2 |
| US-3.7: Seed Test Users | 1 hour | US-0.1 |
| **Total Phase 3** | **15 hours** | |

## **Grand Total: ~40 hours**

---

# 🧪 Testing Strategy

## Unit Tests
- ✅ Password hashing and verification
- ✅ JWT token creation and validation
- ✅ User repository methods
- ✅ Login use case (valid/invalid credentials)
- ✅ Authorization dependencies
- ✅ Resource ownership validation

## Integration Tests
- ✅ Login endpoint (POST /auth/login)
- ✅ Logout endpoint (POST /auth/logout)
- ✅ Get current user (GET /auth/me)
- ✅ All `/me` endpoints with valid JWT
- ✅ Protected endpoints with/without authentication
- ✅ Protected endpoints with insufficient permissions
- ✅ Resource ownership validation

## Test Coverage Goals
- Minimum 80% code coverage
- All error cases tested (401, 403, 404)
- Edge cases (expired tokens, inactive users, etc.)

---

# 🔒 Security Considerations

## Best Practices Implemented
✅ **HttpOnly Cookies** – Prevents XSS attacks  
✅ **Secure Flag** – HTTPS-only cookies in production  
✅ **SameSite** – CSRF protection  
✅ **Bcrypt Hashing** – Industry-standard password hashing  
✅ **JWT Expiration** – Tokens expire after 30 minutes  
✅ **Active User Check** – Inactive users cannot authenticate  
✅ **Role-Based Access** – Principle of least privilege  
✅ **Resource Ownership** – Users can only access their own data  

## Future Enhancements (Out of Scope)
- ⬜ Refresh token rotation
- ⬜ Account lockout after failed login attempts
- ⬜ Two-factor authentication (2FA)
- ⬜ Password complexity requirements
- ⬜ Password reset flow
- ⬜ Email verification
- ⬜ Audit logging for sensitive operations

---

# 📝 API Documentation Updates

Update OpenAPI documentation in `main.py`:

```python
openapi_tags=[
    # ... existing tags ...
    {
        "name": "authentication",
        "description": "User authentication and authorization - login, logout, and current user info",
    },
]
```

---

# 🚀 Deployment Checklist

Before deploying to production:

- [ ] Set strong `SECRET_KEY` in production environment
- [ ] Enable `secure=True` for cookies (HTTPS only)
- [ ] Configure appropriate `ACCESS_TOKEN_EXPIRE_MINUTES`
- [ ] Review and update CORS settings
- [ ] Remove or secure test user accounts
- [ ] Enable HTTPS on frontend and backend
- [ ] Test all authentication flows in staging environment
- [ ] Review and test all authorization rules
- [ ] Run full test suite
- [ ] Update API documentation

---

# 📚 Additional Resources

- **FastAPI Security**: https://fastapi.tiangolo.com/tutorial/security/
- **JWT Best Practices**: https://tools.ietf.org/html/rfc8725
- **OWASP Authentication**: https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html

---

**Document Version:** 1.0  
**Last Updated:** June 1, 2026  
**Status:** Ready for Implementation
