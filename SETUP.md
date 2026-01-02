# CreatorBank Setup Guide

Complete setup instructions for getting CreatorBank running locally.

## Prerequisites

### Required Software

1. **Python 3.11+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Verify: `python --version`

2. **PostgreSQL 14+**
   - Download from [postgresql.org](https://www.postgresql.org/download/)
   - Or use Docker (recommended for development)

3. **Redis 7+**
   - Download from [redis.io](https://redis.io/download)
   - Or use Docker (recommended for development)

4. **Git**
   - Download from [git-scm.com](https://git-scm.com/downloads/)

5. **Docker & Docker Compose** (Optional but recommended)
   - Download from [docker.com](https://www.docker.com/products/docker-desktop)

## Quick Start with Docker (Recommended)

The easiest way to get started is using Docker Compose:

```bash
# Start all services (PostgreSQL, Redis, Backend)
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down

# Stop and remove data
docker-compose down -v
```

Services will be available at:
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050 (admin@creatorbank.com / admin)
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Manual Setup (Without Docker)

### 1. Install PostgreSQL

#### Windows
```bash
# Download installer from postgresql.org
# Or use Chocolatey:
choco install postgresql

# Create database
createdb creatorbank
```

#### macOS
```bash
brew install postgresql@14
brew services start postgresql@14
createdb creatorbank
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb creatorbank
```

### 2. Install Redis

#### Windows
```bash
# Download from https://github.com/microsoftarchive/redis/releases
# Or use Chocolatey:
choco install redis-64
```

#### macOS
```bash
brew install redis
brew services start redis
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

### 3. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env with your settings
# At minimum, verify DATABASE_URL is correct

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload
```

The backend will be running at http://localhost:8000

### 4. Verify Installation

Open http://localhost:8000/docs in your browser. You should see the FastAPI interactive documentation.

Test the health endpoint:
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

## Configuration

### Environment Variables

Edit `backend/.env` with your configuration:

```bash
# Application
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/creatorbank

# YouTube API (Get from Google Cloud Console)
YOUTUBE_CLIENT_ID=your-youtube-client-id
YOUTUBE_CLIENT_SECRET=your-youtube-client-secret
YOUTUBE_REDIRECT_URI=http://localhost:8000/api/v1/auth/youtube/callback

# Other platform APIs (optional for MVP)
TIKTOK_CLIENT_KEY=
INSTAGRAM_APP_ID=
PATREON_CLIENT_ID=
TWITCH_CLIENT_ID=

# Banking (for later phases)
STRIPE_SECRET_KEY=
```

### Getting YouTube API Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable these APIs:
   - YouTube Data API v3
   - YouTube Analytics API
   - YouTube Reporting API
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/api/v1/auth/youtube/callback`
5. Copy Client ID and Client Secret to `.env`

## Database Migrations

### Create a New Migration

After modifying models:

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```bash
alembic upgrade head
```

### Rollback Migration

```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>
```

### View Migration History

```bash
alembic history
alembic current
```

## Testing the API

### 1. Register a User

```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "creator@example.com",
    "password": "securepassword123",
    "full_name": "Test Creator"
  }'
```

### 2. Login

```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=creator@example.com&password=securepassword123"
```

Save the `access_token` from the response.

### 3. Get User Profile

```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Get Dashboard

```bash
curl -X GET "http://localhost:8000/api/v1/dashboard" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Development Workflow

### Running the Backend

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload --log-level debug
```

The `--reload` flag automatically restarts the server when code changes.

### Database Management

#### Using pgAdmin

1. Open http://localhost:5050
2. Login with admin@creatorbank.com / admin
3. Add server:
   - Host: postgres (or localhost if not using Docker)
   - Port: 5432
   - Username: postgres
   - Password: postgres
   - Database: creatorbank

#### Using psql

```bash
# Connect to database
psql -U postgres -d creatorbank

# View tables
\dt

# View table schema
\d users

# Query data
SELECT * FROM users;
```

### Redis Management

#### Using redis-cli

```bash
# Connect to Redis
redis-cli

# View all keys
KEYS *

# Get a value
GET key_name

# Clear all data
FLUSHALL
```

## Troubleshooting

### Database Connection Issues

**Error**: `could not connect to server`

**Solution**:
1. Verify PostgreSQL is running: `pg_isready`
2. Check DATABASE_URL in `.env`
3. Ensure database exists: `createdb creatorbank`

### Import Errors

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solution**:
1. Make sure you're in the `backend` directory
2. Virtual environment is activated
3. Dependencies are installed: `pip install -r requirements.txt`

### Migration Issues

**Error**: `alembic: command not found`

**Solution**:
```bash
pip install alembic
```

**Error**: `Target database is not up to date`

**Solution**:
```bash
alembic upgrade head
```

### Port Already in Use

**Error**: `Address already in use`

**Solution**:
```bash
# Find process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

## Next Steps

1. **Connect YouTube Account**: Implement YouTube OAuth flow
2. **Add Test Data**: Create sample earnings for testing
3. **Build Frontend**: Start React application
4. **Deploy**: Set up production environment

## Production Deployment

(Coming soon: AWS deployment guide, Docker production setup, CI/CD pipeline)

## Support

Having issues? Check:
1. This setup guide
2. README.md
3. API documentation: http://localhost:8000/docs
4. Create an issue on GitHub

---

Happy coding! 🚀
