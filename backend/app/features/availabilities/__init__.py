"""Availabilities Feature Package"""

from fastapi import APIRouter

from .create_availability import router as create_availability_router
from .get_employee_availabilities import router as get_employee_availabilities_router
from .get_one_availability import router as get_one_availability_router
from .update_availability import router as update_availability_router
from .delete_availability import router as delete_availability_router

router = APIRouter(tags=["Availabilities"])

router.include_router(create_availability_router)
router.include_router(get_employee_availabilities_router)
router.include_router(get_one_availability_router)
router.include_router(update_availability_router)
router.include_router(delete_availability_router)
