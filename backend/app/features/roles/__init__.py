from fastapi import APIRouter

from .create_role import router as create_role_router
from .get_all_roles import router as get_all_roles_router
from .get_one_role import router as get_one_role_router
from .update_role import router as update_role_router

router = APIRouter(prefix="/roles", tags=["Roles"])

router.include_router(create_role_router)
router.include_router(get_all_roles_router)
router.include_router(get_one_role_router)
router.include_router(update_role_router)
