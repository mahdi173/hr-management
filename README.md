# MVP Full-Stack Application

A full-stack employee scheduling and time management application with FastAPI backend, Vue.js frontend, and PostgreSQL database, all containerized with Docker.

## 🚀 Features

- **Backend**: FastAPI (Python) with **Vertical Slice Architecture**
- **Frontend**: Vue.js 3 with Vite
- **Database**: PostgreSQL with connection pooling
- **Architecture**: Feature-driven vertical slices (see [VERTICAL_SLICE_ARCHITECTURE.md](backend/VERTICAL_SLICE_ARCHITECTURE.md))
- **Dependency Injection**: FastAPI's dependency system throughout
- **Migrations**: Alembic for database schema management (auto-run on startup)
- **Database Seeding**: Idempotent seed data with existence checks
- **Containerization**: Docker & Docker Compose for easy deployment
- **CRUD Operations**: Complete Create, Read, Update, Delete functionality
- **Modern UI**: Responsive design with gradient styling

## 📋 Prerequisites

- Docker Desktop installed ([Download here](https://www.docker.com/products/docker-desktop))
- Docker Compose (included with Docker Desktop)
- Git (optional, for version control)

## 🏗️ Project Structure

```
.
├── backend/                  # FastAPI backend application
│   ├── alembic/             # Database migration scripts
│   │   ├── versions/        # Migration versions
│   │   └── env.py           # Alembic environment
│   ├── app/
│   │   ├── features/        # VERTICAL SLICE ARCHITECTURE
│   │   │   ├── employees/   # Employee domain features
│   │   │   │   ├── shared/              # Shared DTOs
│   │   │   │   ├── create_employee/     # Feature: Create
│   │   │   │   ├── get_all_employees/   # Feature: List
│   │   │   │   ├── get_one_employee/    # Feature: Get by ID
│   │   │   │   ├── update_employee/     # Feature: Update
│   │   │   │   ├── delete_employee/     # Feature: Delete
│   │   │   │   └── get_employees_by_role/ # Feature: Filter
│   │   │   └── items/       # Item domain features (legacy)
│   │   ├── repositories/    # Data access layer (shared)
│   │   │   ├── base.py      # Base repository
│   │   │   ├── employee_repository.py
│   │   │   └── item_repository.py
│   │   ├── models/          # Database models (shared)
│   │   │   ├── employee.py
│   │   │   ├── role.py
│   │   │   ├── contract_type.py
│   │   │   └── ... (all models)
│   │   ├── __init__.py
│   │   ├── main.py          # Application entry point
│   │   ├── database.py      # Database configuration
│   │   └── seed.py          # Database seeding (idempotent)
│   ├── requirements.txt     # Python dependencies
│   ├── alembic.ini          # Alembic configuration
│   ├── Dockerfile
│   ├── VERTICAL_SLICE_ARCHITECTURE.md  # Architecture documentation
│   └── .dockerignore
│
├── frontend/                # Vue.js frontend application
│   ├── src/
│   │   ├── App.vue          # Main Vue component
│   │   └── main.js          # Application entry point
│   ├── public/
│   ├── index.html
│   ├── package.json         # Node.js dependencies
│   ├── vite.config.js       # Vite configuration
│   ├── Dockerfile
│   └── .dockerignore
│
├── docker-compose.yml       # Docker Compose configuration
├── .env                     # Environment variables
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### 1. Clone or Navigate to Project Directory

```bash
cd "c:\Users\LouisMarriott\Desktop\SDV 2025\TP projet techniqyue"
```

### 2. Start the Application

Run the following command to build and start all services:

```bash
docker-compose up --build
```

This will:
- Build the backend and frontend Docker images
- Create and start all containers
- Set up the SQLite database
- Start the development servers

### 3. Access the Application

Once all services are running:

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)

## 🛠️ Development

### Running in Background

To run containers in detached mode (background):

```bash
docker-compose up -d
```

### Viewing Logs

To view logs from all services:

```bash
docker-compose logs -f
```

To view logs from a specific service:

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Stopping the Application

To stop all running containers:

```bash
docker-compose down
```

To stop and remove all data (including database):

```bash
docker-compose down -v
```

### Rebuilding After Changes

If you make changes to the code:

```bash
docker-compose up --build
```

## 📡 API Endpoints

### Health Check
- `GET /` - Welcome message
- `GET /health` - Check API health status

### Items (CRUD)
- `POST /items/` - Create a new item
- `GET /items/` - Get all items (with pagination)
- `GET /items/{item_id}` - Get a specific item
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

### Items (Filtering & Search)
- `GET /items/filter/completed` - Get all completed items
- `GET /items/filter/pending` - Get all pending items
- `GET /items/search/?title={query}` - Search items by title

### Items (Actions)
- `POST /items/{item_id}/toggle` - Toggle item completion status
- `GET /items/statistics/summary` - Get item statistics (total, completed, pending, completion rate)

### Example API Request

```bash
# Create a new item
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Item",
    "description": "This is a test item",
    "completed": false
  }'

# Get all items
curl "http://localhost:8000/items/"
```

## 🗄️ Database

The application uses PostgreSQL as the database:
- **Image**: PostgreSQL 16 Alpine
- **Connection pooling**: Configured with pool size of 10 and max overflow of 20
- **Persistence**: Data is persisted in a Docker volume named `postgres-data`
- **Migrations**: Alembic is configured for schema migrations
- **Schema**: Automatically created on first run

### Database Credentials (Development)
- **User**: mvp_user
- **Password**: mvp_password
- **Database**: mvp_db
- **Port**: 5432

### Running Migrations

```bash
# Enter the backend container
docker exec -it mvp-backend bash

# Create a new migration
alembic revision --autogenerate -m "description"

# Run migrations
alembicThree-Layer Architecture

The backend implements a clean three-layer architecture with dependency injection:

### 1. Controllers Layer (`app/controllers/`)
**Responsibility**: Handle HTTP requests and responses
- Define API routes and endpoints
- Validate request data using Pydantic schemas
- Return appropriate HTTP responses
- Handle HTTP-specific logic (headers, status codes, etc.)
- **Dependencies**: Services (via dependency injection)

**Example**: `ItemController` handles all `/items/*` endpoints

### 2. Services Layer (`app/services/`)
**Responsibility**: Contain business logic and orchestration
- Implement business rules and validation
- Coordinate between multiple repositories if needed
- Transform data between layers
- Handle complex operations and workflows
- **Dependencies**: Repositories (via dependency injection)

**Key Services**:
- `BaseService`: Generic business operations
- `ItemService`: Item-specific business logic including:
  - Item validation and creation
  - Search and filtering logic
  - Statistics calculation
  - Status management

### 3. Repositories Layer (`app/repositories/`)
**Responsibility**: Data access and persistence
- Execute database queries
- Map between ORM models and Python objects
- Provide data access abstraction
- No business logic - pure data operations
- **Dependencies**: SQLAlchemy models and database session

**Key Repositories**:
- `BaseRepository`: Generic CRUD operations (create, read, update, delete)
- `ItemRepository`: Item-specific queries (search, filter by status, counts)

### Dependency Flow
```
HTTP Request
    ↓
Controller (validates, routes)
    ↓
Service (business logic)
    ↓
Repository (data access)
    ↓
Database
```

### Dependency Injection Example
```python
# In controller
def create_item(
    item: ItemCreate,
    service: ItemService = Depends(get_item_service)  # DI
):
    return service.create_item(item)

# Service gets repository via DI
class ItemService:
    def __init__(self, db: Session):
        self.repository = ItemRepository(db)  # DI
```

### Benefits
- **Separation of Concerns**: Each layer has a single responsibility
- **Testability**: Easy to mock dependencies for unit testing
- **Maintainability**: Changes in one layer don't affect others
- **Reusability**: Services and repositories can be reused across controllers
- **Scalability**: Easy to add new features following the same patterntems
- `get_pending()` - Get all pending items
- `search_by_title()` - Search items by title
- `mark_as_completed()` - Mark item as done
- `mark_as_pending()` - Mark item as not done
- `count_completed()` - Count completed items
- `count_pending()` - Count pending items

## 🔧 Configuration

### Environment Variables

Edit `.env` file to configure:

```env
# Database
POSTGRES_USER=mvp_user
POSTGRES_PASSWORD=mvp_password
POSTGRES_DB=mvp_db
DATABASE_URL=postgresql://mvp_user:mvp_password@postgres:5432/mvp_db

# Backend
BACKEND_PORT=8000

# Frontend
FRONTEND_PORT=3000
VITE_API_URL=http://backend:8000
```

### Ports

Default ports can be changed in `docker-compose.yml`:
- Frontend: `3000`
- Backend: `8000`

## 🐛 Troubleshooting

### Port Already in Use

If ports 3000 or 8000 are already in use, either:
1. Stop the application using those ports
2. Change the ports in `docker-compose.yml`

### Database Issues

If you encounter database issues, reset the database:

```bash
docker-compose down -v
docker-compose up --build
```

### Container Won't Start

Check logs for errors:

```bash
docker-compose logs
```

### Cannot Connect Frontend to Backend

Ensure all services are healthy:

```bash
docker-compose ps
```

## 🧪 Testing

### Test Backend API

Visit the interactive API documentation:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### Test Frontend

Open [http://localhost:3000](http://localhost:3000) in your browser and:
1. Create a new item
2. Mark it as completed
3. Delete it

## 📝 Development Without Docker

### Backend (Local Development)

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Set DATABASE_URL environment variable
$env:DATABASE_URL="postgresql://mvp_user:mvp_password@localhost:5432/mvp_db"

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

**Note**: You'll need a local PostgreSQL instance running on port 5432

### Frontend (Local Development)

```bash
cd frontend
npm install
npm run dev
```

## 🚀 Production Deployment

For production deployment:

1. Update `Dockerfile` configurations for production builds
2. Set secure environment variables (change default passwords!)
3. Use managed PostgreSQL service (AWS RDS, Azure Database, etc.) or configure PostgreSQL with SSL
4. Configure reverse proxy (Nginx) with SSL/TLS
5. Enable HTTPS
6. Set up proper logging and monitoring
7. Configure backup strategy for PostgreSQL
8. Use secrets management (Docker Secrets, Vault, etc.)

## 📚 Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **PostgreSQL**: Robust relational database
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server
- **Alembic**: Database migration tool
- **psycopg2**: PostgreSQL adapter for Python

### Architecture
- **Three-Layer Architecture**: Clean separation with Controllers, Services, and Repositories
- **Dependency Injection**: FastAPI's dependency system throughout all layers
- **Type Safety**: Full typing with Python type hints and Pydantic
- **Generic Base Classes**: Reusable base classes for services and repositories

### Frontend
- **Vue.js 3**: Progressive JavaScript framework
- **Vite**: Next-generation frontend tooling
- **Axios**: Promise-based HTTP client

### DevOps
- **Docker**: Containerization platform
- **Docker Compose**: Multi-container orchestration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 💡 Tips

- The backend automatically reloads when you change Python files
- The frontend has hot-module replacement (HMR) enabled
- Database changes persist between container restarts
- Use `docker-compose down -v` to completely reset the application

## 🆘 Support

For issues and questions:
1. Check the logs: `docker-compose logs`
2. Verify all services are running: `docker-compose ps`
3. Review the API documentation: http://localhost:8000/docs

---

**Happy Coding! 🎉**
