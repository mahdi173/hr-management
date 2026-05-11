"""
Employee repository - handles data access for Employee model.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import and_

from ..models.employee import Employee
from .base import BaseRepository


class EmployeeRepository(BaseRepository[Employee]):
    """Repository for Employee model with custom queries"""

    def __init__(self, db: Session):
        """Initialize with Employee model"""
        super().__init__(Employee, db)

    def get_by_email(self, email: str) -> Optional[Employee]:
        """
        Get employee by email address
        
        Args:
            email: Employee's email address
            
        Returns:
            Employee instance or None if not found
        """
        return self.db.query(self.model).filter(
            self.model.email == email
        ).first()

    def get_active_employees(self, skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Get all active employees with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active employee instances
        """
        return self.db.query(self.model).filter(
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def get_by_role(self, role_id: int, skip: int = 0, limit: int = 100) -> List[Employee]:
        """
        Get employees by role ID
        
        Args:
            role_id: ID of the role
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of employee instances with the specified role
        """
        return self.db.query(self.model).filter(
            self.model.role_id == role_id
        ).offset(skip).limit(limit).all()

    def soft_delete(self, id: int) -> Optional[Employee]:
        """
        Soft delete an employee by setting is_active to False
        
        Args:
            id: Employee ID
            
        Returns:
            Updated employee instance or None if not found
        """
        employee = self.get_by_id(id)
        if employee:
            employee.is_active = False
            self.db.commit()
            self.db.refresh(employee)
        return employee

    def count_active(self) -> int:
        """
        Count the number of active employees
        
        Returns:
            Number of active employees
        """
        return self.db.query(self.model).filter(
            self.model.is_active == True
        ).count()

    def email_exists(self, email: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if an email already exists (useful for validation during updates)
        
        Args:
            email: Email address to check
            exclude_id: Optional employee ID to exclude from check (for updates)
            
        Returns:
            True if email exists, False otherwise
        """
        query = self.db.query(self.model).filter(self.model.email == email)
        if exclude_id:
            query = query.filter(self.model.id != exclude_id)
        return query.first() is not None
