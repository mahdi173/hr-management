"""Item controller with API endpoints"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..services.item_service import ItemService


# Create router for item endpoints
router = APIRouter(prefix="/items", tags=["items"])


# Dependency injection for ItemService
def get_item_service(db: Session = Depends(get_db)) -> ItemService:
    """
    Dependency to get item service instance
    
    Args:
        db: Database session from dependency
        
    Returns:
        ItemService instance
    """
    return ItemService(db)


@router.post("/", response_model=schemas.Item, status_code=201)
def create_item(
    item: schemas.ItemCreate,
    service: ItemService = Depends(get_item_service)
):
    """
    ## Create a New Item
    
    Create a new todo item with the following information:
    * **title**: Item title (required)
    * **description**: Detailed description (optional)
    * **completed**: Completion status (default: false)
    
    **Returns:** The created item with auto-generated ID and timestamps
    """
    return service.create_item(item)


@router.get("/", response_model=List[schemas.Item])
def get_items(
    skip: int = 0,
    limit: int = 100,
    service: ItemService = Depends(get_item_service)
):
    """
    ## Get All Items
    
    Retrieve a list of all todo items with pagination support.
    
    **Parameters:**
    * **skip**: Number of items to skip (for pagination)
    * **limit**: Maximum number of items to return (max: 100)
    
    **Returns:** List of items
    """
    return service.get_all(skip=skip, limit=limit)


@router.get("/{item_id}", response_model=schemas.Item)
def get_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
):
    """
    ## Get Specific Item
    
    Retrieve details of a specific item by its ID.
    
    **Parameters:**
    * **item_id**: The unique identifier of the item
    
    **Returns:** Item details
    
    **Raises:**
    * **404**: Item not found
    """
    item = service.get_by_id(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.put("/{item_id}", response_model=schemas.Item)
def update_item(
    item_id: int,
    item: schemas.ItemCreate,
    service: ItemService = Depends(get_item_service)
):
    """
    ## Update an Item
    
    Update an existing item's information.
    
    **Parameters:**
    * **item_id**: The unique identifier of the item to update
    * **item**: Updated item data
    
    **Returns:** The updated item
    
    **Raises:**
    * **404**: Item not found
    """
    updated_item = service.update_item(item_id, item)
    if updated_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_item


@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    service: ItemService = Depends(get_item_service)
):
    """
    ## Delete an Item
    
    Permanently delete an item from the database.
    
    **Parameters:**
    * **item_id**: The unique identifier of the item to delete
    
    **Returns:** Success message
    
    **Raises:**
    * **404**: Item not found
    """
    success = service.delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


@router.get("/filter/completed", response_model=List[schemas.Item])
def get_completed_items(
    skip: int = 0,
    limit: int = 100,
    service: ItemService = Depends(get_item_service)
):
    """
    ## Get Completed Items
    
    Retrieve all completed items.
    
    **Parameters:**
    * **skip**: Number of items to skip (for pagination)
    * **limit**: Maximum number of items to return (max: 100)
    
    **Returns:** List of completed items
    """
    return service.get_completed_items(skip=skip, limit=limit)


@router.get("/filter/pending", response_model=List[schemas.Item])
def get_pending_items(
    skip: int = 0,
    limit: int = 100,
    service: ItemService = Depends(get_item_service)
):
    """
    ## Get Pending Items
    
    Retrieve all pending (not completed) items.
    
    **Parameters:**
    * **skip**: Number of items to skip (for pagination)
    * **limit**: Maximum number of items to return (max: 100)
    
    **Returns:** List of pending items
    """
    return service.get_pending_items(skip=skip, limit=limit)


@router.get("/search/", response_model=List[schemas.Item])
def search_items(
    title: str,
    skip: int = 0,
    limit: int = 100,
    service: ItemService = Depends(get_item_service)
):
    """
    ## Search Items by Title
    
    Search for items by title (case-insensitive partial match).
    
    **Parameters:**
    * **title**: Search term for title
    * **skip**: Number of items to skip (for pagination)
    * **limit**: Maximum number of items to return (max: 100)
    
    **Returns:** List of matching items
    """
    return service.search_items_by_title(title, skip=skip, limit=limit)


@router.post("/{item_id}/toggle", response_model=schemas.Item)
def toggle_item_completion(
    item_id: int,
    service: ItemService = Depends(get_item_service)
):
    """
    ## Toggle Item Completion
    
    Toggle the completion status of an item.
    
    **Parameters:**
    * **item_id**: The unique identifier of the item
    
    **Returns:** Updated item
    
    **Raises:**
    * **404**: Item not found
    """
    item = service.toggle_item_completion(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/statistics/summary", response_model=dict)
def get_statistics(service: ItemService = Depends(get_item_service)):
    """
    ## Get Item Statistics
    
    Get summary statistics about items.
    
    **Returns:** Statistics including total, completed, pending, and completion rate
    """
    return service.get_statistics()
