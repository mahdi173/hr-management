"""CRUD operations using repository layer"""

from sqlalchemy.orm import Session
from . import schemas
from .repositories import ItemRepository


def get_item_repository(db: Session) -> ItemRepository:
    """Get item repository instance"""
    return ItemRepository(db)


def get_item(db: Session, item_id: int):
    """Get item by ID"""
    repo = get_item_repository(db)
    return repo.get_by_id(item_id)


def get_items(db: Session, skip: int = 0, limit: int = 100):
    """Get all items with pagination"""
    repo = get_item_repository(db)
    return repo.get_all(skip=skip, limit=limit)


def create_item(db: Session, item: schemas.ItemCreate):
    """Create a new item"""
    repo = get_item_repository(db)
    return repo.create(item.model_dump())


def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    """Update an existing item"""
    repo = get_item_repository(db)
    return repo.update(item_id, item.model_dump())


def delete_item(db: Session, item_id: int):
    """Delete an item"""
    repo = get_item_repository(db)
    return repo.delete(item_id)


# Additional repository methods exposed
def get_completed_items(db: Session, skip: int = 0, limit: int = 100):
    """Get completed items"""
    repo = get_item_repository(db)
    return repo.get_completed(skip=skip, limit=limit)


def get_pending_items(db: Session, skip: int = 0, limit: int = 100):
    """Get pending items"""
    repo = get_item_repository(db)
    return repo.get_pending(skip=skip, limit=limit)


def search_items_by_title(db: Session, title: str, skip: int = 0, limit: int = 100):
    """Search items by title"""
    repo = get_item_repository(db)
    return repo.search_by_title(title, skip=skip, limit=limit)

