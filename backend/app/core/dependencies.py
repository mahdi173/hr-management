"""
Authentication and Authorization Dependencies.
Reusable FastAPI dependencies for route protection.
"""
from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from jose import JWTError
from typing import List

from ..database import get_db
from ..repositories.user_repository import UserRepository
from ..models.user import User
from .security import decode_access_token


async def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from JWT cookie.
    
    This dependency extracts the JWT token from the HttpOnly cookie,
    validates it, and returns the corresponding User object.
    
    Args:
        request: FastAPI request object (to access cookies)
        db: Database session
        
    Returns:
        User object for the authenticated user
        
    Raises:
        HTTPException: 401 if token is missing, invalid, or user not found/inactive
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Extract token from cookie
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception
    
    try:
        # Decode and validate JWT token
        payload = decode_access_token(token)
        user_id: int = payload.get("id")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Load user from database with relationships
    user_repo = UserRepository(db)
    user = user_repo.get_user_with_role(user_id)
    
    if user is None:
        raise credentials_exception
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current active user.
    
    This is a wrapper around get_current_user that explicitly checks
    for active status (though get_current_user already does this).
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        Active User object
        
    Raises:
        HTTPException: 403 if user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )
    return current_user


def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Require the current user to be an admin or manager.
    
    Use this dependency for endpoints that should only be accessible
    to users with admin/manager roles.
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        User object if user is admin/manager
        
    Raises:
        HTTPException: 403 if user is not admin/manager
    """
    if not current_user.employee or not current_user.employee.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    if current_user.employee.role.name not in ["Admin", "Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    
    return current_user


def require_manager(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Require the current user to be a manager.
    
    Use this dependency for endpoints that should only be accessible
    to managers (includes Admin role as well).
    
    Args:
        current_user: User from get_current_user dependency
        
    Returns:
        User object if user is manager/admin
        
    Raises:
        HTTPException: 403 if user is not manager/admin
    """
    if not current_user.employee or not current_user.employee.role:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required"
        )
    
    if current_user.employee.role.name not in ["Admin", "Manager"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Manager access required"
        )
    
    return current_user


def require_role(required_roles: List[str]):
    """
    Factory function to create a dependency that requires specific roles.
    
    Usage:
        @router.get("/endpoint", dependencies=[Depends(require_role(["Admin", "Manager"]))])
    
    Args:
        required_roles: List of role names that are allowed
        
    Returns:
        Dependency function that checks for required roles
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if not current_user.employee or not current_user.employee.role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role required: {', '.join(required_roles)}"
            )
        
        if current_user.employee.role.name not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role required: {', '.join(required_roles)}"
            )
        
        return current_user
    
    return role_checker
