"""
Login Use Case - Handles user authentication logic.
"""
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import Tuple

from ....core.security import verify_password, create_access_token
from ....core.config import settings
from ....repositories.user_repository import UserRepository
from ....models.user import User


class LoginUseCase:
    """Use case for user login authentication"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repository = UserRepository(db)
    
    def execute(self, email: str, password: str) -> Tuple[User, str]:
        """
        Authenticate a user and create an access token.
        
        Args:
            email: User's email address
            password: User's plain text password
            
        Returns:
            Tuple of (User object, JWT token string)
            
        Raises:
            HTTPException: 401 if credentials invalid, 403 if user inactive
        """
        # Find user by email
        user = self.user_repository.get_by_email(email)
        
        # Check if user exists
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Verify password
        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        
        # Check if user is active
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Get role name from employee relationship
        role_name = "Unknown"
        if user.employee and user.employee.role:
            role_name = user.employee.role.name
        
        # Create JWT token with user claims
        token_data = {
            "id": user.id,
            "email": user.email,
            "role": role_name
        }
        
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data=token_data,
            expires_delta=access_token_expires
        )
        
        return user, access_token
