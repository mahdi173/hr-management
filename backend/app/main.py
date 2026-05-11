from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

# OpenAPI and Swagger configuration
app = FastAPI(
    title="MVP Todo API",
    description="""
    ## Simple Todo API with FastAPI
    
    This API allows you to manage todo items with full CRUD operations.
    
    ### Features
    * **Create** new items
    * **Read** all items or specific items
    * **Update** existing items
    * **Delete** items
    
    ### Tech Stack
    * FastAPI
    * SQLAlchemy
    * SQLite Database
    * Pydantic for validation
    """,
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support",
        "url": "http://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check and status endpoints",
        },
        {
            "name": "items",
            "description": "Operations with todo items. CRUD functionality for managing items.",
        },
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080", "http://frontend:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["health"])
def read_root():
    """
    ## Root Endpoint
    
    Welcome message for the API.
    """
    return {"message": "Welcome to the MVP API"}


@app.get("/health", tags=["health"])
def health_check():
    """
    ## Health Check
    
    Returns the health status of the API.
    
    **Returns:**
    * status: "healthy" if the service is running
    """
    return {"status": "healthy"}


# Items endpoints
@app.post("/items/", response_model=schemas.Item, status_code=201, tags=["items"])
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    ## Create a New Item
    
    Create a new todo item with the following information:
    * **title**: Item title (required)
    * **description**: Detailed description (optional)
    * **completed**: Completion status (default: false)
    
    **Returns:** The created item with auto-generated ID and timestamps
    """
    return crud.create_item(db=db, item=item)


@app.get("/items/", response_model=List[schemas.Item], tags=["items"])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    ## Get All Items
    
    Retrieve a list of all todo items with pagination support.
    
    **Parameters:**
    * **skip**: Number of items to skip (for pagination)
    * **limit**: Maximum number of items to return (max: 100)
    
    **Returns:** List of items
    """
    items = crud.get_items(db, skip=skip, limit=limit)
    return items


@app.get("/items/{item_id}", response_model=schemas.Item, tags=["items"])
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    ## Get Specific Item
    
    Retrieve details of a specific item by its ID.
    
    **Parameters:**
    * **item_id**: The unique identifier of the item
    
    **Returns:** Item details
    
    **Raises:**
    * **404**: Item not found
    """
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.put("/items/{item_id}", response_model=schemas.Item, tags=["items"])
def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
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
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@app.delete("/items/{item_id}", tags=["items"])
def delete_item(item_id: int, db: Session = Depends(get_db)):
    """
    ## Delete an Item
    
    Permanently delete an item from the database.
    
    **Parameters:**
    * **item_id**: The unique identifier of the item to delete
    
    **Returns:** Success message
    
    **Raises:**
    * **404**: Item not found
    """
    success = crud.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}


@app.get("/items/filter/completed", response_model=List[schemas.Item], tags=["items"])
def get_completed_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    ## Get Completed Items
    
    Retrieve all completed items.
    
    **Parameters:**
    * **skip**: Number of items to skip (for pagination)
    * **limit**: Maximum number of items to return (max: 100)
    
    **Returns:** List of completed items
    """
    return crud.get_completed_items(db, skip=skip, limit=limit)


@app.get("/items/filter/pending", response_model=List[schemas.Item], tags=["items"])
def get_pending_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    ## Get Pending Items
    
    Retrieve all pending (not completed) items.
    
    **Parameters:**
    * **skip**: Number of items to skip (for pagination)
    * **limit**: Maximum number of items to return (max: 100)
    
    **Returns:** List of pending items
    """
    return crud.get_pending_items(db, skip=skip, limit=limit)


@app.get("/items/search/", response_model=List[schemas.Item], tags=["items"])
def search_items(title: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    ## Search Items by Title
    
    Search for items by title (case-insensitive partial match).
    
    **Parameters:**
    * **title**: Search term for title
    * **skip**: Number of items to skip (for pagination)
    * **limit**: Maximum number of items to return (max: 100)
    
    **Returns:** List of matching items
    """
    return crud.search_items_by_title(db, title=title, skip=skip, limit=limit)
