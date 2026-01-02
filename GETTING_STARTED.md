# 🚀 Getting Started with CreatorBank

Welcome! This guide will help you get CreatorBank up and running quickly.

## 🎯 What We've Built So Far

Your CreatorBank MVP backend is now fully structured with:

### ✅ Complete Backend Architecture
- **FastAPI** application with async/await support
- **PostgreSQL** database with comprehensive schema
- **JWT Authentication** with OAuth2
- **Auto tax savings** logic
- **YouTube API integration** framework
- **RESTful API** with OpenAPI documentation

### ✅ Database Models
- **Users**: Creator accounts with subscription tiers
- **Connected Platforms**: YouTube, TikTok, Instagram, etc.
- **Earnings**: Multi-platform income tracking
- **Expenses**: Business expense tracking with OCR support
- **Transactions**: Bank account transactions
- **Invoices**: Brand deal invoice management
- **Predictions**: ML model outputs for forecasting

### ✅ API Endpoints
- `/api/v1/auth/*` - Registration, login, token refresh
- `/api/v1/users/*` - User profile management
- `/api/v1/platforms/*` - Platform connections (YouTube, etc.)
- `/api/v1/earnings/*` - Earnings tracking and summaries
- `/api/v1/dashboard/*` - Aggregated dashboard data

### ✅ Core Services
- **Tax Service**: Automatic tax withholding calculations
- **YouTube Service**: OAuth flow and earnings fetching
- More platform services ready to be added

### ✅ Development Tools
- Docker Compose setup for local development
- Database migrations with Alembic
- Comprehensive test suite
- API documentation at `/docs`

## 🏃‍♂️ Quick Start (5 Minutes)

### Option 1: Docker (Easiest)

```bash
# Start everything with one command
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Open API docs
# Visit: http://localhost:8000/docs
```

That's it! Your backend is running.

### Option 2: Manual Setup

```bash
# 1. Install dependencies
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 2. Set up environment
cp .env.example .env
# Edit .env with your settings

# 3. Start PostgreSQL and Redis
# (Install separately or use Docker)

# 4. Run migrations
alembic upgrade head

# 5. Start server
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs to see your API!

## 📚 Next Steps

### 1. Test the API (5 minutes)

Open http://localhost:8000/docs and try these in order:

**A. Register a User**
- Click on `POST /api/v1/auth/register`
- Click "Try it out"
- Fill in:
  ```json
  {
    "email": "creator@example.com",
    "password": "securepass123",
    "full_name": "Test Creator"
  }
  ```
- Click "Execute"

**B. Login**
- Click on `POST /api/v1/auth/login`
- Fill in:
  - username: `creator@example.com`
  - password: `securepass123`
- Copy the `access_token` from the response

**C. Get Your Profile**
- Click on `GET /api/v1/auth/me`
- Click "Authorize" button at the top
- Paste your access_token
- Click "Authorize"
- Now try `GET /api/v1/auth/me`

🎉 You're authenticated and can access all endpoints!

### 2. Set Up YouTube API (10 minutes)

To enable YouTube integration:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: "CreatorBank"
3. Enable these APIs:
   - YouTube Data API v3
   - YouTube Analytics API
4. Create OAuth 2.0 credentials:
   - Application type: Web application
   - Authorized redirect URIs: `http://localhost:8000/api/v1/auth/youtube/callback`
5. Copy credentials to `backend/.env`:
   ```
   YOUTUBE_CLIENT_ID=your-client-id
   YOUTUBE_CLIENT_SECRET=your-client-secret
   ```

### 3. Explore the Database (5 minutes)

**Using pgAdmin** (if using Docker):
- Visit: http://localhost:5050
- Login: admin@creatorbank.com / admin
- Add server:
  - Name: CreatorBank
  - Host: postgres
  - Port: 5432
  - Username: postgres
  - Password: postgres
  - Database: creatorbank

**Using psql**:
```bash
psql -U postgres -d creatorbank

# View tables
\dt

# View users
SELECT * FROM users;

# View table structure
\d users
```

### 4. Run Tests (2 minutes)

```bash
cd backend

# Create test database
createdb creatorbank_test

# Run tests
pytest -v

# Run with coverage
pytest --cov=app --cov-report=html
```

## 🎯 Development Workflow

### Making Database Changes

1. **Edit models** in `backend/app/models/`
2. **Generate migration**:
   ```bash
   alembic revision --autogenerate -m "Add new field"
   ```
3. **Review migration** in `backend/alembic/versions/`
4. **Apply migration**:
   ```bash
   alembic upgrade head
   ```

### Adding New API Endpoints

1. **Create schema** in `backend/app/schemas/`
2. **Add endpoint** in `backend/app/api/v1/endpoints/`
3. **Register route** in `backend/app/api/v1/router.py`
4. **Test** at http://localhost:8000/docs

### Adding Platform Integrations

1. **Create service** in `backend/app/services/` (see `youtube_service.py`)
2. **Add OAuth endpoints** in `backend/app/api/v1/endpoints/platforms.py`
3. **Get API credentials** from platform
4. **Add to `.env`**

## 📖 Key Files to Know

```
backend/
├── app/
│   ├── main.py                    # ⭐ FastAPI app entry point
│   ├── core/
│   │   ├── config.py             # ⭐ Configuration settings
│   │   └── security.py           # JWT and password hashing
│   ├── models/                   # ⭐ Database models
│   │   ├── user.py
│   │   ├── platform.py
│   │   └── ...
│   ├── api/v1/endpoints/         # ⭐ API endpoints
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   └── ...
│   ├── services/                 # ⭐ Business logic
│   │   ├── tax_service.py
│   │   └── youtube_service.py
│   └── schemas/                  # Pydantic schemas
├── .env                          # ⭐ Environment variables
└── requirements.txt              # Python dependencies
```

## 🎨 What to Build Next

### Week 1-2: Complete YouTube Integration
- [ ] Finish YouTube OAuth callback
- [ ] Fetch real earnings data
- [ ] Store in database
- [ ] Display in dashboard

### Week 3-4: Tax Features
- [ ] Add tax dashboard endpoint
- [ ] Quarterly tax calculator
- [ ] Export tax report to CSV
- [ ] Email quarterly reminders

### Week 5-6: Expense Tracking
- [ ] Receipt upload endpoint
- [ ] OCR integration (Google Vision)
- [ ] AI categorization
- [ ] Export for accountant

### Week 7-8: Frontend
- [ ] React app setup
- [ ] Login/Register pages
- [ ] Dashboard UI
- [ ] Connect platforms UI
- [ ] Earnings charts

## 🐛 Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in backend/ and venv is activated
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### Database connection errors
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Or if running manually:
pg_isready
```

### Port 8000 already in use
```bash
# Kill the process
# macOS/Linux:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 📚 Learning Resources

### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

### SQLAlchemy
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)
- [Async SQLAlchemy](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)

### Platform APIs
- [YouTube Data API](https://developers.google.com/youtube/v3)
- [YouTube Analytics API](https://developers.google.com/youtube/analytics)
- [TikTok Creator API](https://developers.tiktok.com/)
- [Instagram Graph API](https://developers.facebook.com/docs/instagram-api/)

## 💬 Questions?

- Check [SETUP.md](SETUP.md) for detailed setup instructions
- Read [README.md](README.md) for project overview
- Review [prompt.md](prompt.md) for product specifications

## 🎉 You're Ready!

You now have a solid foundation for CreatorBank. The backend architecture is complete and ready for you to:

1. **Connect real platforms** (YouTube, TikTok, etc.)
2. **Build the frontend** (React dashboard)
3. **Add ML features** (income forecasting)
4. **Launch MVP** (beta users!)

**Happy building! 🚀**

Remember: You're building something that will help 500 million creators worldwide manage their finances better. That's huge!

---

*Questions or stuck? The code is well-documented - check the docstrings in each file.*
