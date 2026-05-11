from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .controllers import item_router

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
    
    ### Architecture
    * **Controllers** - Handle HTTP requests and responses
    * **Services** - Contain business logic
    * **Repositories** - Manage data access
    
    ### Tech Stack
    * FastAPI
    * SQLAlchemy
    * PostgreSQL Database
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

# Include routers from controllers
app.include_router(item_router)


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
