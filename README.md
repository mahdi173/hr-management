# MVP Full-Stack Application

A simple MVP full-stack application with FastAPI backend, Vue.js frontend, and SQLite database, all containerized with Docker.

## 🚀 Features

- **Backend**: FastAPI (Python) with RESTful API
- **Frontend**: Vue.js 3 with Vite
- **Database**: SQLite for data persistence
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
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # Main application entry point
│   │   ├── database.py      # Database configuration
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── crud.py          # CRUD operations
│   ├── requirements.txt     # Python dependencies
│   ├── Dockerfile
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
- `GET /health` - Check API health status

### Items
- `GET /items/` - Get all items
- `POST /items/` - Create a new item
- `GET /items/{item_id}` - Get a specific item
- `PUT /items/{item_id}` - Update an item
- `DELETE /items/{item_id}` - Delete an item

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

The application uses SQLite as the database:
- Database file: `backend/data/app.db`
- The database is persisted in a Docker volume named `backend-data`
- Schema is automatically created on first run

## 🔧 Configuration

### Environment Variables

Edit `.env` file to configure:

```env
# Backend
DATABASE_URL=sqlite:///./data/app.db
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
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend (Local Development)

```bash
cd frontend
npm install
npm run dev
```

## 🚀 Production Deployment

For production deployment:

1. Update `Dockerfile` configurations for production builds
2. Set appropriate environment variables
3. Use a production-grade database (PostgreSQL, MySQL)
4. Configure reverse proxy (Nginx)
5. Enable HTTPS
6. Set up proper logging and monitoring

## 📚 Technologies Used

### Backend
- **FastAPI**: Modern, fast web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type annotations
- **Uvicorn**: ASGI server

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
