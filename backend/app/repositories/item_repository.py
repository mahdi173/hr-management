"""Item repository with specific business logic"""

from typing import List, Optional
from sqlalchemy.orm import Session

from ..models import Item
from .base import BaseRepository


class ItemRepository(BaseRepository[Item]):
    """Repository for Item model with custom operations"""

    def __init__(self, db: Session):
        """Initialize item repository with database session"""
        super().__init__(Item, db)

    def get_completed(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """
        Get all completed items
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of completed items
        """
        return (
            self.db.query(self.model)
            .filter(self.model.completed == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_pending(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """
        Get all pending (not completed) items
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of pending items
        """
        return (
            self.db.query(self.model)
            .filter(self.model.completed == False)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_by_title(self, title: str, skip: int = 0, limit: int = 100) -> List[Item]:
        """
        Search items by title (case-insensitive)
        
        Args:
            title: Search term for title
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching items
        """
        return (
            self.db.query(self.model)
            .filter(self.model.title.ilike(f"%{title}%"))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def mark_as_completed(self, id: int) -> Optional[Item]:
        """
        Mark an item as completed
        
        Args:
            id: Item ID
            
        Returns:
            Updated item or None if not found
        """
        return self.update(id, {"completed": True})

    def mark_as_pending(self, id: int) -> Optional[Item]:
        """
        Mark an item as pending (not completed)
        
        Args:
            id: Item ID
            
        Returns:
            Updated item or None if not found
        """
        return self.update(id, {"completed": False})

    def count_completed(self) -> int:
        """
        Count completed items
        
        Returns:
            Number of completed items
        """
        return self.db.query(self.model).filter(self.model.completed == True).count()

    def count_pending(self) -> int:
        """
        Count pending items
        
        Returns:
            Number of pending items
        """
        return self.db.query(self.model).filter(self.model.completed == False).count()
