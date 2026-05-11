# Architecture Comparison

## Before: Horizontal Layering

```
app/
├── controllers/           # All controllers together
│   ├── employee_controller.py
│   └── item_controller.py
├── services/             # All services together
│   ├── employee_service.py
│   └── item_service.py
├── dtos/                 # All DTOs together
│   ├── employee_dto.py
│   └── item_dto.py
├── repositories/         # All repositories together
│   ├── employee_repository.py
│   └── item_repository.py
└── models/              # All models together
    ├── employee.py
    └── item.py
```

**Problem**: To implement a feature, you need to touch files in 4-5 different folders.

---

## After: Vertical Slice Architecture

```
app/
├── features/                           # Features organized by domain
│   ├── employees/                     # All employee features
│   │   ├── shared/                    # Shared across employee features
│   │   │   └── employee_dto.py
│   │   ├── create_employee/           # ONE complete feature
│   │   │   ├── usecase.py            # Business logic
│   │   │   └── controller.py          # HTTP endpoint
│   │   ├── get_all_employees/
│   │   │   ├── usecase.py
│   │   │   └── controller.py
│   │   └── ... (other features)
│   └── items/
│       └── ... (similar structure)
│
├── repositories/          # Shared data access (horizontal)
│   ├── employee_repository.py
│   └── item_repository.py
└── models/               # Shared database schema (horizontal)
    ├── employee.py
    └── item.py
```

**Benefit**: Everything for one feature is in one folder. Easy to find, test, and modify.

---

## Request Flow Comparison

### Horizontal (Before)
```
HTTP Request
    ↓
controllers/employee_controller.py
    ↓
services/employee_service.py
    ↓
repositories/employee_repository.py
    ↓
models/employee.py
```

### Vertical Slice (After)
```
HTTP Request
    ↓
features/employees/create_employee/controller.py
    ↓
features/employees/create_employee/usecase.py
    ↓
repositories/employee_repository.py (shared)
    ↓
models/employee.py (shared)
```

**Key Difference**: Feature-specific logic is co-located; only infrastructure layers (repositories, models) are shared.

---

## When to Add New Code

### Adding a New Employee Feature (e.g., "get_inactive_employees")

**Before (Horizontal)**:
1. Add method to `services/employee_service.py`
2. Add method to `repositories/employee_repository.py` (if needed)
3. Add endpoint to `controllers/employee_controller.py`
4. Files scattered across 3 folders

**After (Vertical Slice)**:
1. Create folder: `features/employees/get_inactive_employees/`
2. Create `usecase.py` with business logic
3. Create `controller.py` with HTTP endpoint
4. Register in parent `__init__.py`
5. All code for this feature in ONE folder

---

## File Organization Best Practices

### ✅ Put in `shared/` if:
- Used by **multiple features** in the same domain
- Example: `EmployeeResponse` DTO used by create, update, get_one, get_all

### ✅ Put in feature folder if:
- Used by **only one feature**
- Example: Special validation logic for creating employees

### ✅ Put in `repositories/` if:
- Reusable data access logic
- Example: `get_by_email()`, `get_active_employees()`

### ✅ Put in `models/` if:
- Database schema definition
- Example: `Employee` SQLAlchemy model

---

## Testing Benefits

**Before**: Mock multiple layers
```python
def test_create_employee():
    mock_service = Mock(EmployeeService)
    mock_repo = Mock(EmployeeRepository)
    # Complex setup across layers
```

**After**: Test one use case
```python
def test_create_employee_use_case():
    use_case = CreateEmployeeUseCase(db)
    result = use_case.execute(employee_data)
    # Simple, focused test
```

---

## Migration Path

The old structure (`controllers/`, `services/`, `dtos/`) still exists but is **deprecated**.

**You can safely delete**:
- `app/controllers/` folder
- `app/services/` folder  
- `app/dtos/` folder

**Keep**:
- `app/repositories/` (used by features)
- `app/models/` (used by features)
- `app/database.py`, `app/seed.py`, `app/main.py`

The new vertical slice architecture is **fully functional** and ready to use!
