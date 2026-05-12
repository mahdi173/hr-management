from fastapi import APIRouter

from .create_schedule.create_schedule_controller import router as create_router
from .get_schedules.get_schedules_controller import router as get_router
from .update_schedule.update_schedule_controller import router as update_router
from .delete_schedule.delete_schedule_controller import router as delete_router
from .get_schedule_views.get_schedule_views_controller import router as views_router

router = APIRouter(prefix="/api/v1/schedules", tags=["Schedules"])

router.include_router(create_router)
router.include_router(get_router)
router.include_router(update_router)
router.include_router(delete_router)
router.include_router(views_router)
