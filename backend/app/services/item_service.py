"""Item service with business logic for item management"""

from typing import List, Optional
from sqlalchemy.orm import Session

from ..models import Item
from ..schemas import ItemCreate
from ..repositories.item_repository import ItemRepository
from .base import BaseService


class ItemService(BaseService[ItemRepository]):
    """Service for managing items with business logic"""

    def __init__(self, db: Session):
        """
        Initialize item service with database session
        
        Args:
            db: Database session
        """
        repository = ItemRepository(db)
        super().__init__(repository)
        self.db = db

    def create_item(self, item_data: ItemCreate) -> Item:
        """
        Create a new item with business validation
        
        Args:
            item_data: Item creation data
            
        Returns:
            Created item instance
        """
        # Business logic: validate title length, format, etc.
        item_dict = item_data.model_dump()
        
        # Additional business rules can be added here
        # For example: check for duplicates, validate business constraints, etc.
        
        return self.create(item_dict)

    def update_item(self, item_id: int, item_data: ItemCreate) -> Optional[Item]:
        """
        Update an existing item with business validation
        
        Args:
            item_id: Item ID
            item_data: Updated item data
            
        Returns:
            Updated item or None if not found
        """
        # Business logic before updating
        item_dict = item_data.model_dump()
        
        return self.update(item_id, item_dict)

    def delete_item(self, item_id: int) -> bool:
        """
        Delete an item with business validation
        
        Args:
            item_id: Item ID
            
        Returns:
            True if deleted, False if not found
        """
        # Business logic: check if item can be deleted
        # For example: check if item is referenced elsewhere
        
        return self.delete(item_id)

    def get_completed_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """
        Get all completed items
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of completed items
        """
        return self.repository.get_completed(skip=skip, limit=limit)

    def get_pending_items(self, skip: int = 0, limit: int = 100) -> List[Item]:
        """
        Get all pending items
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of pending items
        """
        return self.repository.get_pending(skip=skip, limit=limit)

    def search_items_by_title(self, title: str, skip: int = 0, limit: int = 100) -> List[Item]:
        """
        Search items by title with business logic
        
        Args:
            title: Search term
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of matching items
        """
        # Business logic: sanitize search term, validate length, etc.
        if not title or len(title.strip()) < 1:
            return []
        
        return self.repository.search_by_title(title.strip(), skip=skip, limit=limit)

    def toggle_item_completion(self, item_id: int) -> Optional[Item]:
        """
        Toggle item completion status
        
        Args:
            item_id: Item ID
            
        Returns:
            Updated item or None if not found
        """
        item = self.get_by_id(item_id)
        if not item:
            return None
        
        # Toggle the completed status
        new_status = not item.completed
        return self.update(item_id, {"completed": new_status})

    def mark_as_completed(self, item_id: int) -> Optional[Item]:
        """
        Mark an item as completed
        
        Args:
            item_id: Item ID
            
        Returns:
            Updated item or None if not found
        """
        return self.repository.mark_as_completed(item_id)

    def mark_as_pending(self, item_id: int) -> Optional[Item]:
        """
        Mark an item as pending
        
        Args:
            item_id: Item ID
            
        Returns:
            Updated item or None if not found
        """
        return self.repository.mark_as_pending(item_id)

    def get_statistics(self) -> dict:
        """
        Get item statistics
        
        Returns:
            Dictionary with statistics
        """
        total = self.count()
        completed = self.repository.count_completed()
        pending = self.repository.count_pending()
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "completion_rate": round((completed / total * 100) if total > 0 else 0, 2)
        }
