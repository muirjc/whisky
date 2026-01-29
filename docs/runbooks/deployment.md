# Runbook: Deployment

## Prerequisites

- Docker and Docker Compose installed
- Environment variables configured (see `backend/.env.example` and `frontend/.env.example`)

## Local Development

```bash
# Start PostgreSQL
docker-compose up -d postgres postgres-test

# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
python -m src.seed.run_seed
uvicorn src.main:app --reload --port 8000

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

## Pre-Deployment Checklist

1. All tests pass: `cd backend && pytest --cov=src`
2. Type check passes: `cd backend && mypy src/`
3. Lint passes: `cd backend && ruff check src/`
4. Frontend builds: `cd frontend && npm run build`
5. Frontend lint: `cd frontend && npm run lint`
6. Database migrations are up to date

## Environment Variables

### Backend (required)

- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET_KEY`: Secret for JWT signing (generate with `openssl rand -hex 32`)
- `CORS_ORIGINS`: Allowed frontend origins

### Frontend (required)

- `VITE_API_URL`: Backend API base URL

## Health Checks

- Backend liveness: `GET /health` — returns `{"status": "healthy"}`
- Backend readiness: `GET /ready` — returns `{"status": "ready", "database": "connected"}`
