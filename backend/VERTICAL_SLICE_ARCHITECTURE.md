# Vertical Slice Architecture

This backend follows the **Vertical Slice Architecture** pattern, which organizes code by feature rather than by technical layer.

## 📁 Project Structure

```
backend/app/
├── features/                    # All features organized vertically
│   ├── employees/              # Employee domain
│   │   ├── shared/             # Shared DTOs/types for employee features
│   │   │   ├── __init__.py
│   │   │   └── employee_dto.py
│   │   ├── create_employee/    # Feature: Create employee
│   │   │   ├── __init__.py
│   │   │   ├── usecase.py      # Business logic
│   │   │   └── controller.py   # HTTP endpoint
│   │   ├── get_all_employees/  # Feature: List employees
│   │   │   ├── __init__.py
│   │   │   ├── usecase.py
│   │   │   └── controller.py
│   │   ├── get_one_employee/   # Feature: Get employee by ID
│   │   │   ├── __init__.py
│   │   │   ├── usecase.py
│   │   │   └── controller.py
│   │   ├── update_employee/    # Feature: Update employee
│   │   │   ├── __init__.py
│   │   │   ├── usecase.py
│   │   │   └── controller.py
│   │   ├── delete_employee/    # Feature: Delete employee
│   │   │   ├── __init__.py
│   │   │   ├── usecase.py
│   │   │   └── controller.py
│   │   └── get_employees_by_role/  # Feature: Filter by role
│   │       ├── __init__.py
│   │       ├── usecase.py
│   │       └── controller.py
│   │
│   └── items/                  # Item domain (legacy)
│       ├── shared/             # Shared DTOs/types for item features
│       │   ├── __init__.py
│       │   └── item_dto.py
│       ├── create_item/
│       ├── get_all_items/
│       ├── get_one_item/
│       ├── update_item/
│       └── delete_item/
│
├── models/                     # Database models (shared)
├── repositories/               # Data access layer (shared)
├── database.py                 # Database configuration
├── seed.py                     # Database seeding
└── main.py                     # Application entry point
```

## 🏗️ Architecture Principles

### Vertical Slices
Each feature is self-contained with:
- **Use Case** (`usecase.py`): Business logic for that specific feature
- **Controller** (`controller.py`): HTTP endpoint handling
- **Shared DTOs**: Data Transfer Objects shared across related features

### Horizontal Layers (Shared)
Some layers remain horizontal as they're shared infrastructure:
- **Models**: Database schema (SQLAlchemy) - shared by all features
- **Repositories**: Data access layer - reusable query logic

### Benefits

1. **Feature Isolation**: Each feature is independent and can be developed/tested separately
2. **Easier Navigation**: Find all code for a feature in one place
3. **Reduced Coupling**: Features don't depend on each other
4. **Scalability**: Easy to add new features without impacting existing ones
5. **Team Collaboration**: Different developers can work on different features with minimal conflicts

## 📝 Adding a New Feature

To add a new feature (e.g., `get_active_employees`):

1. **Create feature folder**:
   ```
   features/employees/get_active_employees/
   ```

2. **Create use case** (`usecase.py`):
   ```python
   from sqlalchemy.orm import Session
   from ...repositories.employee_repository import EmployeeRepository
   
   class GetActiveEmployeesUseCase:
       def __init__(self, db: Session):
           self.repository = EmployeeRepository(db)
       
       def execute(self, skip: int = 0, limit: int = 100):
           return self.repository.get_active_employees(skip, limit)
   ```

3. **Create controller** (`controller.py`):
   ```python
   from fastapi import APIRouter, Depends
   from ....database import get_db
   from ..shared import EmployeeResponse
   from .usecase import GetActiveEmployeesUseCase
   
   router = APIRouter()
   
   @router.get("/active", response_model=List[EmployeeResponse])
   def get_active_employees(db: Session = Depends(get_db)):
       use_case = GetActiveEmployeesUseCase(db)
       return use_case.execute()
   ```

4. **Register in parent `__init__.py`**:
   ```python
   from .get_active_employees.controller import router as get_active_router
   router.include_router(get_active_router)
   ```

## 🔄 Request Flow

```
HTTP Request
    ↓
Controller (HTTP handling, validation)
    ↓
Use Case (Business logic)
    ↓
Repository (Data access)
    ↓
Model (Database)
```

## 🎯 When to Use Shared vs Feature-Specific

### Shared (`features/employees/shared/`)
- DTOs used by **multiple features** in the same domain
- Example: `EmployeeResponse` used by get_one, get_all, create, update

### Feature-Specific
- DTOs unique to **one feature**
- Specialized business logic
- Example: If `create_employee` needs a special validation DTO

## 🧪 Testing

Test each feature independently:
```python
def test_create_employee():
    use_case = CreateEmployeeUseCase(db)
    result = use_case.execute(employee_data)
    assert result.email == employee_data.email
```

## 🚀 Migration from Old Structure

The old structure (controllers, services, dtos) is **deprecated** but still exists for reference:
- ~~`app/controllers/`~~ → `app/features/*/*/controller.py`
- ~~`app/services/`~~ → `app/features/*/*/usecase.py`
- ~~`app/dtos/`~~ → `app/features/*/shared/*.py`

These folders can be safely deleted once you're comfortable with the new structure.
