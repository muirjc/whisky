# Quickstart: Whisky Collection Tracker

**Date**: 2026-01-17
**Feature**: 001-whisky-collection-tracker

## Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Docker (optional, for containerized development)

## Quick Setup

### 1. Clone and Setup Environment

```bash
# Clone repository
git clone <repository-url>
cd whisky-collection-tracker

# Create Python virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Database Setup

```bash
# Start PostgreSQL (if using Docker)
docker run -d \
  --name whisky-postgres \
  -e POSTGRES_USER=whisky \
  -e POSTGRES_PASSWORD=whisky \
  -e POSTGRES_DB=whisky \
  -p 5432:5432 \
  postgres:15

# Or configure your existing PostgreSQL instance
```

### 3. Environment Configuration

Create `.env` file in `backend/`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://whisky:whisky@localhost:5432/whisky

# Auth
JWT_SECRET_KEY=your-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# App
DEBUG=true
LOG_LEVEL=DEBUG
CORS_ORIGINS=http://localhost:5173
```

Create `.env` file in `frontend/`:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

### 4. Database Migration and Seeding

```bash
cd backend

# Run migrations
alembic upgrade head

# Seed reference data (distilleries and whiskies)
python -m src.seed.run_seed
```

### 5. Start Development Servers

Terminal 1 - Backend:
```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

### 6. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (Swagger UI)
- **Health Check**: http://localhost:8000/api/v1/health

## Running Tests

### Backend Tests

```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test types
pytest tests/unit/
pytest tests/integration/
pytest tests/contract/

# Run type checking
mypy src/

# Run linter
ruff check src/
```

### Frontend Tests

```bash
cd frontend

# Run unit tests
npm run test

# Run with coverage
npm run test:coverage

# Run E2E tests (requires backend running)
npm run test:e2e

# Run type checking
npm run typecheck

# Run linter
npm run lint
```

## Development Workflow

### Adding a New Feature

1. **Create feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Write failing tests first** (TDD)
   ```bash
   # Backend: Create test in tests/unit/ or tests/integration/
   # Frontend: Create test in tests/unit/ or tests/e2e/
   ```

3. **Implement the feature**
   - Backend: Models in `src/models/`, services in `src/services/`, routes in `src/api/`
   - Frontend: Components in `src/components/`, pages in `src/pages/`

4. **Run tests and checks**
   ```bash
   # Backend
   pytest && mypy src/ && ruff check src/

   # Frontend
   npm run test && npm run typecheck && npm run lint
   ```

5. **Create pull request**

### Database Migrations

```bash
cd backend

# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### API Contract Updates

When modifying API endpoints:

1. Update `specs/001-whisky-collection-tracker/contracts/openapi.yaml`
2. Regenerate frontend API client (if using code generation)
3. Update backend route implementations
4. Update integration tests

## Project Structure Reference

```
whisky-collection-tracker/
├── backend/
│   ├── src/
│   │   ├── api/           # FastAPI routes
│   │   │   ├── auth.py
│   │   │   ├── bottles.py
│   │   │   ├── distilleries.py
│   │   │   ├── whiskies.py
│   │   │   ├── wishlist.py
│   │   │   └── profile.py
│   │   ├── models/        # SQLAlchemy + Pydantic
│   │   │   ├── user.py
│   │   │   ├── bottle.py
│   │   │   ├── distillery.py
│   │   │   ├── whisky.py
│   │   │   └── wishlist.py
│   │   ├── services/      # Business logic
│   │   │   ├── auth.py
│   │   │   ├── bottle.py
│   │   │   ├── matching.py
│   │   │   └── profile.py
│   │   ├── seed/          # Reference data seeding
│   │   └── main.py        # FastAPI app entry
│   ├── tests/
│   ├── alembic/           # Database migrations
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/    # Reusable UI
│   │   ├── pages/         # Route pages
│   │   ├── services/      # API client
│   │   └── hooks/         # Custom hooks
│   └── tests/
├── data/
│   ├── distilleries.json  # Seed data
│   └── whiskies.json      # Seed data
└── specs/
    └── 001-whisky-collection-tracker/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        ├── quickstart.md (this file)
        └── contracts/
```

## Troubleshooting

### Database Connection Issues

```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Test connection
psql postgresql://whisky:whisky@localhost:5432/whisky -c "SELECT 1"
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # Backend
lsof -i :5173  # Frontend

# Kill process
kill -9 <PID>
```

### Missing Dependencies

```bash
# Backend
pip install -r requirements.txt -r requirements-dev.txt

# Frontend
npm install
```

### Type Errors

```bash
# Backend: Check mypy output
mypy src/ --show-error-codes

# Frontend: Check TypeScript output
npm run typecheck
```

## Useful Commands Reference

| Task | Command |
|------|---------|
| Start backend | `cd backend && uvicorn src.main:app --reload` |
| Start frontend | `cd frontend && npm run dev` |
| Run all backend tests | `cd backend && pytest` |
| Run all frontend tests | `cd frontend && npm test` |
| Check backend types | `cd backend && mypy src/` |
| Check frontend types | `cd frontend && npm run typecheck` |
| Lint backend | `cd backend && ruff check src/` |
| Lint frontend | `cd frontend && npm run lint` |
| Create migration | `cd backend && alembic revision --autogenerate -m "msg"` |
| Apply migrations | `cd backend && alembic upgrade head` |
| Seed database | `cd backend && python -m src.seed.run_seed` |
| View API docs | Open http://localhost:8000/docs |
