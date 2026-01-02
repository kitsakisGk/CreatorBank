# 🚀 CreatorBank - Quick Reference Guide

## Essential Commands

### Start Development Environment
```bash
# Using Docker (Recommended)
docker-compose up -d

# Manual
cd backend
source venv/bin/activate  # Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

### Access Points
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **pgAdmin**: http://localhost:5050

### Database Operations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# Direct DB access
psql -U postgres -d creatorbank
```

### Testing
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_auth.py -v
```

## API Endpoints Reference

### Authentication
```bash
# Register
POST /api/v1/auth/register
{
  "email": "creator@example.com",
  "password": "securepass123",
  "full_name": "Creator Name"
}

# Login
POST /api/v1/auth/login
Form: username=creator@example.com&password=securepass123

# Get current user
GET /api/v1/auth/me
Headers: Authorization: Bearer <token>

# Refresh token
POST /api/v1/auth/refresh
{"refresh_token": "..."}
```

### User Management
```bash
# Get profile
GET /api/v1/users/profile

# Update profile
PATCH /api/v1/users/profile
{
  "full_name": "New Name",
  "tax_withholding_rate": 35.0
}

# Get stats
GET /api/v1/users/stats
```

### Platforms
```bash
# Get connected platforms
GET /api/v1/platforms/connected

# Connect YouTube
POST /api/v1/platforms/connect/youtube

# Disconnect platform
DELETE /api/v1/platforms/disconnect/{platform_id}

# Sync earnings
POST /api/v1/platforms/sync/{platform_id}
```

### Earnings
```bash
# Get earnings
GET /api/v1/earnings?skip=0&limit=100&platform_id=1

# Get summary
GET /api/v1/earnings/summary
```

### Dashboard
```bash
# Get dashboard data
GET /api/v1/dashboard
```

## File Locations Quick Map

### Need to modify...

**Database models?**
→ `backend/app/models/*.py`

**API endpoints?**
→ `backend/app/api/v1/endpoints/*.py`

**Business logic?**
→ `backend/app/services/*.py`

**Configuration?**
→ `backend/app/core/config.py` or `backend/.env`

**Database schema?**
→ Edit models, then: `alembic revision --autogenerate`

**API schemas?**
→ `backend/app/schemas/*.py`

## Environment Variables

```bash
# Essential
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
SECRET_KEY=your-secret-key
DEBUG=True

# YouTube
YOUTUBE_CLIENT_ID=...
YOUTUBE_CLIENT_SECRET=...

# Banking (later)
STRIPE_SECRET_KEY=...
```

## Database Schema Quick Reference

### Users
- email, hashed_password, full_name
- tier (free, creator, pro, business)
- tax_withholding_rate, tax_savings_balance

### Connected Platforms
- user_id, platform_type
- access_token, refresh_token
- platform_user_id, platform_username

### Earnings
- user_id, platform_id
- amount, currency, earning_date, payout_date
- tax_withheld, is_taxable

### Expenses
- user_id, amount, category
- is_deductible, receipt_url

### Transactions
- user_id, amount, transaction_type
- description, balance_before, balance_after

### Invoices
- user_id, invoice_number, status
- client_name, amount, due_date

## Common Tasks

### Add a new API endpoint
1. Create schema in `schemas/`
2. Add endpoint function in `api/v1/endpoints/`
3. Register in `api/v1/router.py`
4. Test at `/docs`

### Add a new database table
1. Create model in `models/`
2. Import in `models/__init__.py`
3. Generate migration: `alembic revision --autogenerate`
4. Apply: `alembic upgrade head`

### Add a new platform integration
1. Create service in `services/` (copy `youtube_service.py`)
2. Add OAuth endpoints in `platforms.py`
3. Get API credentials from platform
4. Add to `.env`
5. Test OAuth flow

### Add a new business logic service
1. Create file in `services/`
2. Define class with static methods
3. Import in endpoint files
4. Call from API endpoints

## Troubleshooting Quick Fixes

**Import errors?**
```bash
cd backend && source venv/bin/activate && pip install -r requirements.txt
```

**Database errors?**
```bash
docker-compose restart postgres
# or
alembic upgrade head
```

**Port in use?**
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Migration conflicts?**
```bash
alembic downgrade -1
alembic upgrade head
```

## Development Workflow

1. **Make changes** to code
2. **Auto-reload** picks up changes (if using --reload)
3. **Test** at `/docs` or with curl
4. **Run tests**: `pytest`
5. **Commit**: `git add . && git commit -m "message"`

## Testing Workflow

### Test new endpoint
1. Go to http://localhost:8000/docs
2. Find your endpoint
3. Click "Try it out"
4. Fill in parameters
5. Click "Execute"

### Test with curl
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"pass123","full_name":"Test"}'

# Login & save token
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=test@test.com&password=pass123" | jq -r .access_token)

# Use token
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

## Production Checklist (Future)

- [ ] Change SECRET_KEY in production
- [ ] Set DEBUG=False
- [ ] Use production database
- [ ] Enable HTTPS
- [ ] Set up monitoring (Sentry)
- [ ] Configure CORS properly
- [ ] Set up CI/CD
- [ ] Database backups
- [ ] Rate limiting
- [ ] API key management

## Useful SQL Queries

```sql
-- View all users
SELECT id, email, tier, created_at FROM users;

-- View connected platforms
SELECT u.email, cp.platform_type, cp.platform_username
FROM connected_platforms cp
JOIN users u ON cp.user_id = u.id;

-- Total earnings by user
SELECT u.email, SUM(e.amount) as total_earnings
FROM earnings e
JOIN users u ON e.user_id = u.id
GROUP BY u.email;

-- Tax withholdings
SELECT u.email, u.tax_savings_balance, SUM(e.tax_withheld) as total_withheld
FROM users u
LEFT JOIN earnings e ON u.id = e.user_id
GROUP BY u.id;
```

## Links

- [Full Documentation](README.md)
- [Setup Guide](SETUP.md)
- [Getting Started](GETTING_STARTED.md)
- [Project Summary](PROJECT_SUMMARY.md)
- [Product Spec](prompt.md)

---

**Keep this handy!** Bookmark this file for quick reference while developing.
