"""
User Repository - Data access layer for User model.
Handles user queries for authentication and authorization.
"""
from typing import Optional
from sqlalchemy.orm import Session, joinedload
from .base import BaseRepository
from ..models.user import User
from ..models.employee import Employee
from ..models.role import Role


class UserRepository(BaseRepository[User]):
    """Repository for User model with authentication-specific queries"""
    
    def __init__(self, db: Session):
        super().__init__(User, db)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """
        Get a user by email address.
        Includes employee and role relationships for efficiency.
        
        Args:
            email: User's email address
            
        Returns:
            User object if found, None otherwise
        """
        return (
            self.db.query(User)
            .options(
                joinedload(User.employee).joinedload(Employee.role)
            )
            .filter(User.email == email)
            .first()
        )
    
    def get_user_with_role(self, user_id: int) -> Optional[User]:
        """
        Get a user by ID with employee and role relationships loaded.
        Optimized for authentication/authorization checks.
        
        Args:
            user_id: User's ID
            
        Returns:
            User object with relationships loaded, None if not found
        """
        return (
            self.db.query(User)
            .options(
                joinedload(User.employee).joinedload(Employee.role)
            )
            .filter(User.id == user_id)
            .first()
        )
    
    def get_active_users(self):
        """
        Get all active users.
        
        Returns:
            List of active User objects
        """
        return self.db.query(User).filter(User.is_active == True).all()
