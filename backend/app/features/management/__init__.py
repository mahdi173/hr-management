from fastapi import APIRouter
from .alert_controller import router as alerts_router
from .analytics_controller import router as analytics_router
from .recommendation_controller import router as recommendation_router

router = APIRouter()
router.include_router(alerts_router)
router.include_router(analytics_router)
router.include_router(recommendation_router)
