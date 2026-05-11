"""Shifts feature module - Combines all shift-related routers"""

from fastapi import APIRouter

from .create_shift.create_shift_controller import router as create_shift_router
from .get_shifts.get_shifts_controller import router as get_shifts_router
from .update_shift.update_shift_controller import router as update_shift_router
from .assign_employee.assign_employee_controller import router as assign_employee_router
from .remove_assignment.remove_assignment_controller import router as remove_assignment_router
from .get_hours.get_hours_controller import router as get_hours_router


# Combine all shift routers
router = APIRouter(prefix="/api/v1", tags=["shifts"])

# Include all feature routers
router.include_router(create_shift_router)
router.include_router(get_shifts_router)
router.include_router(update_shift_router)
router.include_router(assign_employee_router)
router.include_router(remove_assignment_router)
router.include_router(get_hours_router)
