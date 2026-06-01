"""
Get Current User Controller - API endpoint to retrieve current user information.
"""
from fastapi import APIRouter, Depends

from ....core.dependencies import get_current_user
from ....models.user import User
from ..shared.auth_dto import UserInfoResponse


router = APIRouter()


@router.get(
    "/me",
    response_model=UserInfoResponse,
    summary="Get current user",
    description="Get information about the currently authenticated user.",
    responses={
        200: {"description": "Current user information"},
        401: {"description": "Not authenticated"}
    }
)
def get_me(current_user: User = Depends(get_current_user)) -> UserInfoResponse:
    """
    Get current user endpoint - returns authenticated user's information.
    
    Requires authentication via JWT cookie.
    
    **Response:**
    - User information (id, email, role, employee details)
    
    **Errors:**
    - 401: Not authenticated or invalid token
    """
    return UserInfoResponse(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        employee_id=current_user.employee_id,
        first_name=current_user.employee.first_name if current_user.employee else None,
        last_name=current_user.employee.last_name if current_user.employee else None,
        role=current_user.employee.role.name if current_user.employee and current_user.employee.role else None
    )
