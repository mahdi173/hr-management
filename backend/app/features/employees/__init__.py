"""Employee features - Vertical slice architecture"""

from .create_employee.create_employee_controller import router as create_employee_router
from .get_all_employees.get_all_employees_controller import router as get_all_employees_router
from .get_one_employee.get_one_employee_controller import router as get_one_employee_router
from .update_employee.update_employee_controller import router as update_employee_router
from .delete_employee.delete_employee_controller import router as delete_employee_router
from .get_employees_by_role.get_employees_by_role_controller import router as get_employees_by_role_router

# Combine all employee routers into one
from fastapi import APIRouter

router = APIRouter(prefix="/employees", tags=["employees"])

# Include all feature routes
router.include_router(create_employee_router)
router.include_router(get_all_employees_router)
router.include_router(get_one_employee_router)
router.include_router(update_employee_router)
router.include_router(delete_employee_router)
router.include_router(get_employees_by_role_router)

__all__ = ["router"]
