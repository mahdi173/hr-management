from fastapi import APIRouter

from .create_absence.create_absence_controller import router as create_router
from .approve_absence.approve_absence_controller import router as approve_router
from .reject_absence.reject_absence_controller import router as reject_router
from .get_absences.get_absences_controller import router as get_router

router = APIRouter(prefix="/absences", tags=["Absences"])

router.include_router(create_router)
router.include_router(approve_router)
router.include_router(reject_router)
router.include_router(get_router)
