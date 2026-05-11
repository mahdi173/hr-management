"""Base service class with common business logic patterns"""

from typing import Generic, TypeVar, Type
from sqlalchemy.orm import Session

from ..repositories.base import BaseRepository

# Type variable for repository
RepositoryType = TypeVar("RepositoryType", bound=BaseRepository)


class BaseService(Generic[RepositoryType]):
    """Base service providing common business logic operations"""

    def __init__(self, repository: RepositoryType):
        """
        Initialize service with repository
        
        Args:
            repository: Repository instance for data access
        """
        self.repository = repository

    def get_by_id(self, id: int):
        """
        Get a single record by ID
        
        Args:
            id: Primary key value
            
        Returns:
            Model instance or None if not found
        """
        return self.repository.get_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 100):
        """
        Get all records with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of model instances
        """
        return self.repository.get_all(skip=skip, limit=limit)

    def create(self, obj_in: dict):
        """
        Create a new record with validation
        
        Args:
            obj_in: Dictionary of model attributes
            
        Returns:
            Created model instance
        """
        # Business logic can be added here before creating
        return self.repository.create(obj_in)

    def update(self, id: int, obj_in: dict):
        """
        Update an existing record with validation
        
        Args:
            id: Primary key value
            obj_in: Dictionary of attributes to update
            
        Returns:
            Updated model instance or None if not found
        """
        # Business logic can be added here before updating
        return self.repository.update(id, obj_in)

    def delete(self, id: int) -> bool:
        """
        Delete a record by ID
        
        Args:
            id: Primary key value
            
        Returns:
            True if deleted, False if not found
        """
        # Business logic can be added here before deleting
        return self.repository.delete(id)

    def exists(self, id: int) -> bool:
        """
        Check if a record exists
        
        Args:
            id: Primary key value
            
        Returns:
            True if exists, False otherwise
        """
        return self.repository.exists(id)

    def count(self) -> int:
        """
        Get total count of records
        
        Returns:
            Total number of records
        """
        return self.repository.count()
