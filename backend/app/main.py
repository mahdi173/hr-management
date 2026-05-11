from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from .models import Base
from .database import engine
from .features.employees import router as employees_router
from .features.roles import router as roles_router
from .features.absences import router as absences_router
from .features.schedules import router as schedules_router
from .features.contract_types import router as contract_types_router
from .features.availabilities import router as availabilities_router
from .features.shifts import router as shifts_router
from .seed import seed_database

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create database tables (auto-migrate)
logger.info("🔄 Checking database schema...")
Base.metadata.create_all(bind=engine)
logger.info("✅ Database schema is up to date")

# Seed database with initial data
logger.info("🌱 Seeding database...")
try:
    seed_database()
except Exception as e:
    logger.warning(f"⚠️  Database seeding skipped or failed: {e}")

# OpenAPI and Swagger configuration
app = FastAPI(
    title="Timeapp API",
    description="""
    ## Employee Scheduling & Time Management API
    
    This API provides comprehensive employee and schedule management capabilities.
    
    ### Features
    * **Employee Management** - Create, read, update, and delete employee profiles
    * **Role Management** - Define and assign roles to employees
    * **Contract Types** - Manage different employment arrangements
    * **Schedule Management** - Create and manage work schedules
    * **Availability Tracking** - Track employee availability
    * **Absence Management** - Handle employee absences
    
    ### Architecture
    * **Vertical Slices** - Features organized by business capability
    * **Use Cases** - Encapsulate business logic for each feature
    * **Repositories** - Manage data access
    * **Models** - Database schema definitions
    
    ### Tech Stack
    * FastAPI
    * SQLAlchemy
    * PostgreSQL Database
    * Pydantic for validation
    * Alembic for migrations
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
            "name": "employees",
            "description": "Employee management operations - CRUD functionality for managing employee profiles",
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

# Include feature routers (vertical slice architecture)
app.include_router(employees_router)
app.include_router(roles_router)
app.include_router(absences_router)
app.include_router(schedules_router)
app.include_router(contract_types_router)
app.include_router(availabilities_router)
app.include_router(shifts_router)


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
