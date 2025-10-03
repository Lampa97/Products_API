# Products API

A comprehensive REST API service built with FastAPI, PostgreSQL, and Redis that provides user authentication, product management, role-based access control, and automated external API synchronization.

## Features

- **User Authentication**: JWT-based authentication with email/password
- **Role-based Access Control**: Admin and regular user roles
- **Product Management**: Full CRUD operations for products
- **External API Sync**: Automated synchronization with external product APIs every 30 minutes
- **Background Tasks**: Celery-based task queue with Redis broker
- **Database Migrations**: Alembic for schema management
- **API Documentation**: Auto-generated Swagger UI and ReDoc
- **Docker Support**: Complete containerized development environment

## Tech Stack

- **Backend**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+ with SQLAlchemy 2.0 (async)
- **Cache/Broker**: Redis 7+
- **Task Queue**: Celery
- **Authentication**: JWT with python-jose
- **Validation**: Pydantic
- **Migrations**: Alembic
- **HTTP Client**: httpx (async)
- **Containerization**: Docker & Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd Products_API
   ```

2. **Start the development environment**:

   ```bash
   # Windows PowerShell
   .\start-dev.ps1
   
   # Windows Command Prompt / Linux / macOS
   ./start-dev.sh
   ```

3. **Wait for all services to be healthy** (check logs):

   ```bash
   docker-compose logs -f
   ```

4. **Access the application**:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Alternative API Docs: http://localhost:8000/redoc

### Manual Docker Commands

If you prefer to run commands manually:

```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down

# Stop and remove all data (careful!)
docker-compose down -v
```

## API Endpoints

### Authentication

```bash
# Register a new user
POST /auth/register
{
  "email": "user@example.com",
  "password": "securepassword",
  "role": "user"  # Optional, defaults to "user"
}

# Login
POST /auth/login
{
  "email": "user@example.com",
  "password": "securepassword"
}

# Get current user info
GET /auth/me
Headers: Authorization: Bearer <token>
```

### Products

```bash
# Get all products (paginated)
GET /products?skip=0&limit=100

# Get product by ID
GET /products/{product_id}

# Create product (admin only)
POST /products
Headers: Authorization: Bearer <admin_token>
{
  "name": "New Product",
  "description": "Product description",
  "price": 99.99,
  "category": "Electronics"
}

# Update product (admin only)
PUT /products/{product_id}
Headers: Authorization: Bearer <admin_token>

# Delete product (admin only)
DELETE /products/{product_id}
Headers: Authorization: Bearer <admin_token>
```

### External API Sync

```bash
# Manual sync trigger (admin only)
POST /sync/trigger
Headers: Authorization: Bearer <admin_token>

# Get sync status
GET /sync/status
Headers: Authorization: Bearer <admin_token>
```

## Development

### Local Development (without Docker)

1. **Install dependencies**:
   ```bash
   pip install uv
   uv sync
   ```

2. **Set up environment variables**:
   ```bash
   # Copy and edit environment file
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Start PostgreSQL and Redis** (via Docker):

   ```bash
   docker run -d --name postgres -p 5432:5432 -e POSTGRES_PASSWORD=password postgres:15-alpine
   docker run -d --name redis -p 6379:6379 redis:7-alpine
   ```

4. **Run database migrations**:

   ```bash
   uv run alembic upgrade head
   ```

5. **Start the application**:

   ```bash
   # API server
   uv run uvicorn main:app --reload

   # In another terminal - Celery worker
   uv run python celery_worker.py

   # In another terminal - Celery beat (scheduler)
   uv run python celery_beat.py
   ```

### Database Migrations

```bash
# Create a new migration
uv run alembic revision --autogenerate -m "Description of changes"

# Apply migrations
uv run alembic upgrade head

# View migration history
uv run alembic history

# Rollback to previous migration
uv run alembic downgrade -1
```

### Testing API with curl

```bash
# Register admin user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123", "role": "admin"}'

# Login and get token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@example.com", "password": "admin123"}'

# Use token to create product (replace <token> with actual token)
curl -X POST "http://localhost:8000/products" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"name": "Test Product", "description": "A test product", "price": 29.99, "category": "Test"}'
```

## Configuration

The application uses environment variables for configuration. Key settings:

- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: JWT secret key
- `EXTERNAL_API_PROVIDER`: External API provider (e.g., "dummyjson")
- `EXTERNAL_API_URL`: External API endpoint
- `BACKEND_CORS_ORIGINS`: Allowed CORS origins

### External API Providers

The system supports multiple external API providers through a flexible adapter pattern:

- **DummyJSON**: `EXTERNAL_API_PROVIDER=dummyjson` (default)
- **Custom Provider**: Implement the `ExternalAPIProvider` interface

## Architecture

```
├── app/
│   ├── core/           # Core configuration and settings
│   ├── db/             # Database connection and setup
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas for validation
│   ├── services/       # Business logic and external services
│   ├── routers/        # FastAPI route handlers
│   └── tasks/          # Celery background tasks
├── alembic/            # Database migrations
├── docker-compose.yml  # Development environment
└── main.py            # FastAPI application entry point
```

## Automatic Synchronization

The system automatically synchronizes products from external APIs every 30 minutes using Celery Beat. The sync process:

1. Fetches products from the configured external API
2. Updates existing products based on `external_id`
3. Creates new products if they don't exist
4. Logs the sync results

## Troubleshooting

### Common Issues

1. **Port already in use**: Change ports in `docker-compose.yml`
2. **Database connection failed**: Ensure PostgreSQL is running and accessible
3. **Redis connection failed**: Ensure Redis is running
4. **Migration errors**: Check database permissions and connection

### Logs

```bash
# View all service logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f api
docker-compose logs -f celery-worker
docker-compose logs -f celery-beat
```

### Health Checks

The application includes health check endpoints:

- API Health: `GET /health`
- Service status: Check Docker container health
