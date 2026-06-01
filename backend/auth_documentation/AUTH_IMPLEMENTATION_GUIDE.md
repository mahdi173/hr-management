# 🔐 Authentication & Authorization - Quick Implementation Guide

This is a quick reference for implementing the authentication and authorization system. See [AUTH_ROADMAP.md](./AUTH_ROADMAP.md) for full details.

---

## 📁 New File Structure

```
backend/app/
├── core/                           # NEW: Core utilities
│   ├── __init__.py
│   ├── config.py                   # Settings from environment
│   ├── security.py                 # Password hashing, JWT utilities
│   ├── dependencies.py             # Auth dependencies (get_current_user, etc.)
│   └── authorization.py            # Resource ownership validation
│
├── features/
│   └── auth/                       # NEW: Authentication feature
│       ├── __init__.py             # Router export
│       ├── shared/
│       │   └── auth_dto.py         # Login/Token DTOs
│       ├── login/
│       │   ├── login_usecase.py
│       │   └── login_controller.py
│       ├── logout/
│       │   └── logout_controller.py
│       └── me/
│           └── get_me_controller.py
│
├── repositories/
│   └── user_repository.py          # NEW: User queries
│
└── models/
    └── user.py                      # EXISTING (no changes needed)
```

---

## 🔑 Environment Variables

Add to `backend/.env`:

```bash
# JWT Configuration
SECRET_KEY=your-secret-key-min-32-chars-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (existing)
DATABASE_URL=postgresql://...
```

Generate secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## 📦 New Dependencies

Add to `requirements.txt`:

```
passlib[bcrypt]==1.7.4
python-jose[cryptography]==3.3.0
python-dotenv==1.0.0
```

Install:
```bash
pip install passlib[bcrypt] python-jose[cryptography] python-dotenv
```

---

## 🛠️ Key Implementation Snippets

### 1. Configuration (`core/config.py`)

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### 2. Security Utilities (`core/security.py`)

```python
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def decode_access_token(token: str) -> dict:
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
```

### 3. Current User Dependency (`core/dependencies.py`)

```python
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from jose import JWTError
from ..database import get_db
from ..repositories.user_repository import UserRepository
from .security import decode_access_token

async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception
    
    try:
        payload = decode_access_token(token)
        user_id: int = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user_repo = UserRepository(db)
    user = user_repo.get_user_with_role(user_id)
    
    if user is None or not user.is_active:
        raise credentials_exception
    
    return user

def require_admin(current_user = Depends(get_current_user)):
    if not current_user.employee or current_user.employee.role.name not in ["Admin", "Manager"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
```

### 4. Login Controller (`features/auth/login/login_controller.py`)

```python
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from ....database import get_db
from ..shared.auth_dto import LoginRequest, LoginResponse
from .login_usecase import LoginUseCase

router = APIRouter()

@router.post("/login", response_model=LoginResponse)
def login(
    credentials: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    use_case = LoginUseCase(db)
    user, token = use_case.execute(credentials.email, credentials.password)
    
    # Set HttpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set True in production with HTTPS
        samesite="lax",
        max_age=1800  # 30 minutes
    )
    
    return LoginResponse(
        id=user.id,
        email=user.email,
        role=user.employee.role.name if user.employee else "Unknown",
        first_name=user.employee.first_name if user.employee else "",
        last_name=user.employee.last_name if user.employee else ""
    )
```

### 5. Protected Endpoint Example

```python
from fastapi import Depends
from ....core.dependencies import get_current_user, require_admin
from ....models.user import User

# Any authenticated user
@router.get("/shifts/me")
def get_my_shifts(current_user: User = Depends(get_current_user)):
    employee_id = current_user.employee_id
    # ... get shifts for employee_id

# Admin only
@router.post("/employees", dependencies=[Depends(require_admin)])
def create_employee(...):
    # Only admins can access this
    pass

# Resource ownership check
@router.get("/absences/{absence_id}")
def get_absence(
    absence_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    absence = db.query(Absence).filter(Absence.id == absence_id).first()
    
    # Check if user owns resource or is admin
    is_owner = absence.employee_id == current_user.employee_id
    is_admin = current_user.employee.role.name in ["Admin", "Manager"]
    
    if not (is_owner or is_admin):
        raise HTTPException(status_code=403, detail="Access denied")
    
    return absence
```

---

## 🔄 Implementation Order

### Phase 1: Authentication (Core)
1. ✅ Install dependencies
2. ✅ Create `core/config.py`
3. ✅ Create `core/security.py`
4. ✅ Create `repositories/user_repository.py`
5. ✅ Create `features/auth/shared/auth_dto.py`
6. ✅ Create `features/auth/login/` (usecase + controller)
7. ✅ Create `features/auth/logout/logout_controller.py`
8. ✅ Create `core/dependencies.py`
9. ✅ Create `features/auth/me/get_me_controller.py`
10. ✅ Register auth router in `main.py`
11. ✅ Test login/logout/me endpoints

### Phase 2: User Routes (/me endpoints)
1. ✅ Create `features/shifts/get_my_shifts/`
2. ✅ Create `features/absences/get_my_absences/`
3. ✅ Create `features/availabilities/get_my_availabilities/`
4. ✅ Create `features/shifts/get_my_hours/`
5. ✅ Update routers to include new endpoints

### Phase 3: Authorization
1. ✅ Create `core/authorization.py`
2. ✅ Add `require_admin()` and `require_manager()` to dependencies
3. ✅ Update all employee endpoints (add `Depends(require_admin)`)
4. ✅ Update absence approval endpoints (add `Depends(require_manager)`)
5. ✅ Update schedule/shift endpoints (add `Depends(require_manager)`)
6. ✅ Update availability endpoints (add ownership checks)
7. ✅ Update seed data with test users
8. ✅ Test all authorization rules

---

## 🧪 Testing Checklist

### Manual Testing with cURL

```bash
# 1. Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example.com","password":"admin123"}' \
  -c cookies.txt

# 2. Get current user (uses cookie)
curl http://localhost:8000/auth/me -b cookies.txt

# 3. Get my shifts
curl http://localhost:8000/shifts/me -b cookies.txt

# 4. Try protected endpoint without auth (should fail)
curl http://localhost:8000/employees

# 5. Try protected endpoint with auth
curl http://localhost:8000/employees -b cookies.txt

# 6. Logout
curl -X POST http://localhost:8000/auth/logout -b cookies.txt -c cookies.txt
```

### Automated Tests

Create tests for:
- ✅ `tests/features/auth/test_login.py`
- ✅ `tests/features/auth/test_me_endpoints.py`
- ✅ `tests/features/*/test_authorization.py` (for each feature)

---

## 🔒 Security Checklist

- [ ] SECRET_KEY is random and not committed to git
- [ ] HttpOnly cookies enabled
- [ ] Secure flag set to True in production
- [ ] CORS configured correctly
- [ ] Passwords hashed with bcrypt
- [ ] JWT tokens expire
- [ ] Inactive users cannot login
- [ ] All sensitive endpoints protected
- [ ] Resource ownership validated
- [ ] Admin routes restricted

---

## 🐛 Common Issues & Solutions

### Issue: "Could not validate credentials"
- Check cookie is being sent (inspect browser DevTools)
- Verify SECRET_KEY matches between token creation and validation
- Check token hasn't expired

### Issue: CORS errors with cookies
- Ensure `allow_credentials=True` in CORS middleware
- Frontend must use `credentials: 'include'` in fetch

### Issue: 403 Forbidden on admin endpoints
- Verify user has correct role assigned
- Check role name matches exactly ("Manager" vs "manager")
- Ensure employee relationship is loaded

### Issue: Cookies not persisting
- Check `httponly`, `secure`, and `samesite` settings
- In development, `secure` should be False (no HTTPS)
- Verify domain/path settings

---

## 📚 Quick Reference: DTOs

```python
# LoginRequest
{
    "email": "user@example.com",
    "password": "password123"
}

# LoginResponse
{
    "id": 1,
    "email": "user@example.com",
    "role": "Manager",
    "first_name": "John",
    "last_name": "Doe"
}

# JWT Token Payload
{
    "id": 1,
    "email": "user@example.com",
    "role": "Manager",
    "exp": 1234567890
}
```

---

**Ready to implement?** Start with Phase 1, Task 1: Install dependencies! 🚀
