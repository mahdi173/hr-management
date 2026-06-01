# ✅ Authentication & Authorization Implementation Checklist

Track your progress through the implementation of the authentication and authorization system.

---

## 📋 Phase 1: Authentication Infrastructure

### US-0.1: Password Hashing Utilities

- [ ] Install dependencies (`passlib`, `python-jose`, `python-dotenv`)
  ```bash
  pip install passlib[bcrypt] python-jose[cryptography] python-dotenv
  ```
- [ ] Update `requirements.txt` with new dependencies
- [ ] Create `.env` file with SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
- [ ] Create `backend/app/core/__init__.py`
- [ ] Create `backend/app/core/config.py` with Settings class
- [ ] Create `backend/app/core/security.py` with:
  - [ ] `hash_password()` function
  - [ ] `verify_password()` function
- [ ] Write unit tests for password hashing
- [ ] ✅ **Verify:** Passwords can be hashed and verified

---

### US-0.2: JWT Token Generation & Validation

- [ ] Extend `backend/app/core/security.py` with:
  - [ ] `create_access_token()` function
  - [ ] `decode_access_token()` function
- [ ] Create `backend/app/features/auth/__init__.py`
- [ ] Create `backend/app/features/auth/shared/__init__.py`
- [ ] Create `backend/app/features/auth/shared/auth_dto.py` with:
  - [ ] `TokenPayload` schema
  - [ ] `TokenData` schema
- [ ] Write unit tests for JWT creation and decoding
- [ ] Write unit test for expired token
- [ ] ✅ **Verify:** JWT tokens can be created and validated

---

### US-0.3: User Repository Extensions

- [ ] Create `backend/app/repositories/user_repository.py`
- [ ] Implement `UserRepository` class extending `BaseRepository[User]`
  - [ ] `get_by_email(email: str)` method
  - [ ] `get_user_with_role(user_id: int)` method (with joinedload)
- [ ] Update `backend/app/repositories/__init__.py` to export `UserRepository`
- [ ] Write unit tests for repository methods
- [ ] ✅ **Verify:** Can query users by email and load with relationships

---

### US-0.4: Login Use Case

- [ ] Update `backend/app/features/auth/shared/auth_dto.py` with:
  - [ ] `LoginRequest` schema (email, password)
  - [ ] `LoginResponse` schema (id, email, role, first_name, last_name)
- [ ] Create `backend/app/features/auth/login/__init__.py`
- [ ] Create `backend/app/features/auth/login/login_usecase.py`
  - [ ] `LoginUseCase` class
  - [ ] `execute()` method with full login logic
- [ ] Create `backend/app/features/auth/login/login_controller.py`
  - [ ] `POST /auth/login` endpoint
  - [ ] Set HttpOnly cookie in response
- [ ] Update `backend/app/features/auth/__init__.py` to create router
- [ ] Register auth router in `backend/app/main.py`
- [ ] Write unit tests for login use case
- [ ] Write integration test for login endpoint (success case)
- [ ] Write integration test for login endpoint (invalid credentials)
- [ ] Write integration test for login endpoint (inactive user)
- [ ] ✅ **Verify:** Can login with valid credentials and receive cookie

**Test manually:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -v  # Check for Set-Cookie header
```

---

### US-0.5: Logout Use Case

- [ ] Create `backend/app/features/auth/logout/__init__.py`
- [ ] Create `backend/app/features/auth/logout/logout_controller.py`
  - [ ] `POST /auth/logout` endpoint
  - [ ] Delete access_token cookie
- [ ] Add logout route to auth router
- [ ] Write integration test for logout endpoint
- [ ] ✅ **Verify:** Logout clears the cookie

**Test manually:**
```bash
curl -X POST http://localhost:8000/auth/logout -c cookies.txt -b cookies.txt -v
```

---

### US-0.6: Get Current User Dependency

- [ ] Create `backend/app/core/dependencies.py`
- [ ] Implement `get_current_user()` dependency function
  - [ ] Extract token from cookies
  - [ ] Decode and validate JWT
  - [ ] Load user from database
  - [ ] Check if user is active
  - [ ] Return User object or raise 401
- [ ] Implement `get_current_active_user()` wrapper (optional)
- [ ] Update `backend/app/core/__init__.py` to export dependencies
- [ ] Write unit tests for dependency
- [ ] ✅ **Verify:** Dependency extracts user from valid cookie

---

### US-0.7: Get Current User Info Endpoint

- [ ] Update `backend/app/features/auth/shared/auth_dto.py` with:
  - [ ] `UserInfoResponse` schema
- [ ] Create `backend/app/features/auth/me/__init__.py`
- [ ] Create `backend/app/features/auth/me/get_me_controller.py`
  - [ ] `GET /auth/me` endpoint
  - [ ] Use `Depends(get_current_user)`
- [ ] Add me route to auth router
- [ ] Write integration test for /auth/me endpoint
- [ ] ✅ **Verify:** Can retrieve current user info with valid cookie

**Test manually:**
```bash
# Login first, save cookie
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  -c cookies.txt

# Get current user
curl http://localhost:8000/auth/me -b cookies.txt
```

---

## ✅ Phase 1 Completion Checklist

- [ ] All authentication endpoints working
- [ ] Unit tests passing (>80% coverage)
- [ ] Integration tests passing
- [ ] Can login and receive JWT cookie
- [ ] Can access protected /auth/me endpoint
- [ ] Can logout and clear cookie
- [ ] JWT tokens expire correctly
- [ ] Invalid/expired tokens return 401
- [ ] Documentation updated (OpenAPI)

---

## 📋 Phase 2: User-Specific Routes

### US-2.1: Get My Shifts Endpoint

- [ ] Create `backend/app/features/shifts/get_my_shifts/__init__.py`
- [ ] Create `backend/app/features/shifts/get_my_shifts/get_my_shifts_usecase.py`
  - [ ] `GetMyShiftsUseCase` class
  - [ ] `execute(employee_id, start_date, end_date)` method
- [ ] Create `backend/app/features/shifts/get_my_shifts/get_my_shifts_controller.py`
  - [ ] `GET /shifts/me` endpoint
  - [ ] Use `Depends(get_current_user)`
  - [ ] Extract employee_id from current_user
- [ ] Register route in shifts router
- [ ] Write integration test for /shifts/me
- [ ] ✅ **Verify:** Can retrieve current user's shifts

---

### US-2.2: Get My Absences Endpoint

- [ ] Create `backend/app/features/absences/get_my_absences/__init__.py`
- [ ] Create `backend/app/features/absences/get_my_absences/get_my_absences_usecase.py`
  - [ ] `GetMyAbsencesUseCase` class
  - [ ] `execute(employee_id, status)` method
- [ ] Create `backend/app/features/absences/get_my_absences/get_my_absences_controller.py`
  - [ ] `GET /absences/me` endpoint
  - [ ] Use `Depends(get_current_user)`
- [ ] Register route in absences router
- [ ] Write integration test for /absences/me
- [ ] ✅ **Verify:** Can retrieve current user's absences

---

### US-2.3: Get My Availabilities Endpoint

- [ ] Create `backend/app/features/availabilities/get_my_availabilities/__init__.py`
- [ ] Create `backend/app/features/availabilities/get_my_availabilities/get_my_availabilities_controller.py`
  - [ ] `GET /availabilities/me` endpoint
  - [ ] Use `Depends(get_current_user)`
  - [ ] Reuse existing `get_employee_availabilities` use case
- [ ] Register route in availabilities router
- [ ] Write integration test for /availabilities/me
- [ ] ✅ **Verify:** Can retrieve current user's availabilities

---

### US-2.4: Get My Work Hours Summary

- [ ] Create `backend/app/features/shifts/get_my_hours/__init__.py`
- [ ] Create `backend/app/features/shifts/get_my_hours/get_my_hours_controller.py`
  - [ ] `GET /shifts/me/hours` endpoint
  - [ ] Use `Depends(get_current_user)`
  - [ ] Reuse existing hours calculation logic
- [ ] Register route in shifts router
- [ ] Write integration test for /shifts/me/hours
- [ ] ✅ **Verify:** Can retrieve current user's work hours

---

## ✅ Phase 2 Completion Checklist

- [ ] All `/me` endpoints implemented
- [ ] All endpoints require authentication
- [ ] Integration tests passing
- [ ] Users can only see their own data
- [ ] Proper error handling (no employee linked, etc.)

---

## 📋 Phase 3: Authorization & Access Control

### US-3.1: Role-Based Authorization Dependencies

- [ ] Extend `backend/app/core/dependencies.py` with:
  - [ ] `require_role(required_roles: List[str])` dependency factory
  - [ ] `require_admin()` dependency (shortcut for admin/manager)
  - [ ] `require_manager()` dependency (shortcut for manager)
- [ ] Write unit tests for role dependencies
- [ ] ✅ **Verify:** Role-based dependencies raise 403 for unauthorized roles

---

### US-3.2: Resource Ownership Validation

- [ ] Create `backend/app/core/authorization.py`
- [ ] Implement `verify_resource_access(current_user, resource_employee_id)` function
- [ ] Implement `is_admin_or_manager(user)` helper function
- [ ] Write unit tests for ownership validation
- [ ] ✅ **Verify:** Ownership checks work correctly

---

### US-3.3: Protect Employee Management Endpoints

- [ ] Update `create_employee_controller.py`:
  - [ ] Add `Depends(require_admin)` to endpoint
- [ ] Update `update_employee_controller.py`:
  - [ ] Add `Depends(require_admin)` to endpoint
- [ ] Update `delete_employee_controller.py`:
  - [ ] Add `Depends(require_admin)` to endpoint
- [ ] Update `get_one_employee_controller.py`:
  - [ ] Add ownership check (own record OR admin)
- [ ] Write integration tests:
  - [ ] Admin can create/update/delete employees
  - [ ] Regular user cannot create/update/delete employees
  - [ ] User can view own employee record
  - [ ] User cannot view other employee records (unless admin)
- [ ] ✅ **Verify:** Only admins can manage employees

---

### US-3.4: Protect Absence Management Endpoints

- [ ] Update `approve_absence_controller.py`:
  - [ ] Add `Depends(require_manager)` to endpoint
- [ ] Update `reject_absence_controller.py`:
  - [ ] Add `Depends(require_manager)` to endpoint
- [ ] Update `create_absence_controller.py`:
  - [ ] Add `Depends(get_current_user)` to endpoint
  - [ ] Verify employee_id matches current_user OR user is manager
- [ ] Write integration tests:
  - [ ] Manager can approve/reject absences
  - [ ] Regular user cannot approve/reject absences
  - [ ] User can create own absence
  - [ ] User cannot create absence for another employee
- [ ] ✅ **Verify:** Absence management properly secured

---

### US-3.5: Protect Schedule & Shift Management

- [ ] Update schedule controllers (create, update, delete):
  - [ ] Add `Depends(require_manager)` to all modification endpoints
- [ ] Update shift controllers (create, update, delete, assign, remove):
  - [ ] Add `Depends(require_manager)` to all modification endpoints
  - [ ] Remove manual `manager_id` parameters
  - [ ] Use `current_user` from dependency instead
- [ ] Write integration tests:
  - [ ] Manager can create/update/delete schedules and shifts
  - [ ] Regular user cannot modify schedules or shifts
  - [ ] All users can view schedules (read-only)
- [ ] ✅ **Verify:** Only managers can manage schedules and shifts

---

### US-3.6: Protect Availability Management

- [ ] Update availability controllers (create, update, delete):
  - [ ] Add `Depends(get_current_user)` to endpoints
  - [ ] Add `verify_resource_access()` checks
- [ ] Write integration tests:
  - [ ] User can create/update/delete own availabilities
  - [ ] User cannot modify other employees' availabilities
  - [ ] Manager can modify any employee's availability
- [ ] ✅ **Verify:** Availability management respects ownership

---

### US-3.7: Update Seed Data with Test Users

- [ ] Update `backend/app/seed.py`
- [ ] Add test user accounts:
  - [ ] Admin user (admin@example.com / admin123)
  - [ ] Manager user (manager@example.com / manager123)
  - [ ] Regular employee (employee@example.com / employee123)
- [ ] Link users to employees
- [ ] Hash passwords using `hash_password()`
- [ ] Test seed data loads correctly
- [ ] ✅ **Verify:** Can login with all test accounts

**Test manually:**
```bash
# Test admin login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}' \
  -c admin_cookies.txt

# Test employee login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"employee@example.com","password":"employee123"}' \
  -c employee_cookies.txt
```

---

## ✅ Phase 3 Completion Checklist

- [ ] All endpoints properly protected
- [ ] Role-based access working
- [ ] Resource ownership validation working
- [ ] Admin can access all resources
- [ ] Regular users can only access own resources
- [ ] All integration tests passing
- [ ] Seed data includes test users
- [ ] Manual testing completed

---

## 🧪 Final Testing Checklist

### Functional Testing

- [ ] **Login Flow**
  - [ ] Valid credentials → Success + cookie
  - [ ] Invalid email → 401
  - [ ] Invalid password → 401
  - [ ] Inactive user → 403

- [ ] **Logout Flow**
  - [ ] Logout clears cookie
  - [ ] Cannot access protected routes after logout

- [ ] **Current User**
  - [ ] GET /auth/me returns correct user info
  - [ ] Without cookie → 401

- [ ] **User-Specific Routes**
  - [ ] GET /shifts/me returns only user's shifts
  - [ ] GET /absences/me returns only user's absences
  - [ ] GET /availabilities/me returns only user's availabilities
  - [ ] All require authentication

- [ ] **Admin Routes**
  - [ ] Admin can create/update/delete employees
  - [ ] Regular user cannot create/update/delete employees
  - [ ] Admin can approve/reject absences
  - [ ] Regular user cannot approve/reject absences

- [ ] **Resource Ownership**
  - [ ] User can only edit own availabilities
  - [ ] User can only create own absences
  - [ ] Manager can edit any employee's data

### Security Testing

- [ ] Passwords are hashed in database (never plain text)
- [ ] JWT tokens expire after configured time
- [ ] Expired tokens return 401
- [ ] Invalid tokens return 401
- [ ] Missing tokens return 401
- [ ] HttpOnly cookies prevent JavaScript access
- [ ] CORS configured correctly
- [ ] No sensitive data in logs

### Performance Testing

- [ ] Login response < 500ms
- [ ] Token validation adds minimal overhead
- [ ] Database queries optimized (use joinedload)
- [ ] No N+1 query problems

---

## 📊 Test Coverage Requirements

- [ ] Unit tests: >80% coverage
- [ ] Integration tests: All endpoints covered
- [ ] Security tests: All auth/authz scenarios covered

Run coverage:
```bash
pytest --cov=app --cov-report=html
```

---

## 📝 Documentation Checklist

- [ ] README updated with auth setup instructions
- [ ] OpenAPI docs updated with authentication tag
- [ ] Environment variables documented
- [ ] Test user accounts documented
- [ ] Security best practices documented

---

## 🚀 Pre-Deployment Checklist

- [ ] All tests passing
- [ ] `.env.example` created with template values
- [ ] `.env` added to `.gitignore`
- [ ] SECRET_KEY generated for production (min 32 chars)
- [ ] `secure=True` for cookies in production
- [ ] HTTPS enabled on production server
- [ ] CORS origins configured for production
- [ ] Database backed up before deployment
- [ ] Seed data reviewed (remove/secure test accounts)
- [ ] API documentation published

---

## 🎉 Completion Criteria

**Phase 1 Complete When:**
- ✅ Users can login and receive JWT cookie
- ✅ Users can logout and clear session
- ✅ Users can access /auth/me endpoint
- ✅ All Phase 1 tests passing

**Phase 2 Complete When:**
- ✅ All `/me` endpoints implemented
- ✅ Users can view their own data
- ✅ All Phase 2 tests passing

**Phase 3 Complete When:**
- ✅ All routes properly protected
- ✅ Role-based access working
- ✅ Resource ownership validated
- ✅ All Phase 3 tests passing

**Full Implementation Complete When:**
- ✅ All phases complete
- ✅ All tests passing (unit + integration)
- ✅ Manual testing completed
- ✅ Documentation updated
- ✅ Security checklist complete
- ✅ Ready for production deployment

---

**Good luck with the implementation! 🚀**

Track your progress by checking off items as you complete them.
