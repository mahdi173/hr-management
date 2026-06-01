"""
Login Controller - API endpoint for user authentication.
"""
from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from ....database import get_db
from ..shared.auth_dto import LoginRequest, LoginResponse
from .login_usecase import LoginUseCase


router = APIRouter()


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="User login",
    description="Authenticate user with email and password. Returns user info and sets HttpOnly cookie with JWT token.",
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials"},
        403: {"description": "User account inactive"}
    }
)
def login(
    credentials: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
) -> LoginResponse:
    """
    Login endpoint - authenticates user and sets JWT cookie.
    
    **Request Body:**
    - **email**: User's email address
    - **password**: User's password
    
    **Response:**
    - User information (id, email, role, name)
    - Sets HttpOnly cookie with JWT token (access_token)
    
    **Errors:**
    - 401: Invalid email or password
    - 403: User account is inactive
    """
    # Execute login use case
    use_case = LoginUseCase(db)
    user, token = use_case.execute(credentials.email, credentials.password)
    
    # Set HttpOnly cookie with JWT token
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # Set to True in production with HTTPS
        samesite="lax",
        max_age=1800  # 30 minutes in seconds
    )
    
    # Return user information
    return LoginResponse(
        id=user.id,
        email=user.email,
        role=user.employee.role.name if user.employee and user.employee.role else "Unknown",
        first_name=user.employee.first_name if user.employee else "",
        last_name=user.employee.last_name if user.employee else ""
    )
