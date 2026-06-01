"""
Logout Controller - API endpoint for user logout.
"""
from fastapi import APIRouter, Response

router = APIRouter()


@router.post(
    "/logout",
    summary="User logout",
    description="Logout user by clearing the JWT cookie.",
    responses={
        200: {"description": "Logout successful"}
    }
)
def logout(response: Response):
    """
    Logout endpoint - clears the JWT cookie.
    
    **Response:**
    - Success message
    - Clears access_token cookie
    """
    # Delete the access_token cookie
    response.delete_cookie(key="access_token")
    
    return {"message": "Successfully logged out"}
