"""
Role repository - handles data access for Role model.
"""
from typing import Optional, List
from sqlalchemy.orm import Session

from ..models.role import Role
from .base import BaseRepository


class RoleRepository(BaseRepository[Role]):
    """Repository for Role model with custom queries"""

    def __init__(self, db: Session):
        """Initialize with Role model"""
        super().__init__(Role, db)

    def get_by_name(self, name: str) -> Optional[Role]:
        """
        Get role by name
        
        Args:
            name: Role name
            
        Returns:
            Role instance or None if not found
        """
        return self.db.query(self.model).filter(
            self.model.name == name
        ).first()

    def get_active_roles(self, skip: int = 0, limit: int = 100) -> List[Role]:
        """
        Get all active roles with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active role instances
        """
        return self.db.query(self.model).filter(
            self.model.is_active == True
        ).offset(skip).limit(limit).all()

    def name_exists(self, name: str, exclude_id: Optional[int] = None) -> bool:
        """
        Check if a role name already exists
        
        Args:
            name: Role name to check
            exclude_id: Optional role ID to exclude from check (for updates)
            
        Returns:
            True if name exists, False otherwise
        """
        query = self.db.query(self.model).filter(self.model.name == name)
        if exclude_id:
            query = query.filter(self.model.id != exclude_id)
        return query.first() is not None
