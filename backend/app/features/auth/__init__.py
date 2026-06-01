"""
Authentication feature - Login, logout, and user session management.
"""
from fastapi import APIRouter

# Create auth router
router = APIRouter(prefix="/auth", tags=["authentication"])

# Import and include controllers
from .login.login_controller import router as login_router
from .logout.logout_controller import router as logout_router
from .me.get_me_controller import router as me_router

router.include_router(login_router)
router.include_router(logout_router)
router.include_router(me_router)
