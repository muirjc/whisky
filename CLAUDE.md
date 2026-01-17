# Whisky Collection Tracker Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-01-17

## Active Technologies

- **Language**: Python 3.11+ (backend), TypeScript 5.x (frontend)
- **Frameworks**: FastAPI (API), SQLAlchemy (ORM), React (frontend), Pydantic (validation)
- **Database**: PostgreSQL
- **Testing**: pytest (backend), Vitest (frontend), Playwright (E2E)
- **Type Checking**: mypy (Python), TypeScript strict mode
- **Linting**: ruff (Python), ESLint (TypeScript)

## Project Structure

```text
backend/
├── src/
│   ├── models/          # SQLAlchemy models, Pydantic schemas
│   ├── services/        # Business logic
│   ├── api/             # FastAPI routes
│   └── seed/            # Reference data seeding
└── tests/
    ├── unit/
    ├── integration/
    └── contract/

frontend/
├── src/
│   ├── components/      # Reusable UI components
│   ├── pages/           # Route-level pages
│   ├── services/        # API client
│   └── hooks/           # Custom React hooks
└── tests/
    ├── unit/
    └── e2e/

data/
├── whiskies.json        # Pre-seeded whisky reference
└── distilleries.json    # Pre-seeded distillery data

specs/
└── 001-whisky-collection-tracker/
    ├── spec.md
    ├── plan.md
    ├── research.md
    ├── data-model.md
    ├── quickstart.md
    └── contracts/
```

## Commands

### Backend
```bash
# Start development server
cd backend && uvicorn src.main:app --reload --port 8000

# Run tests
cd backend && pytest

# Run with coverage
cd backend && pytest --cov=src --cov-report=html

# Type checking
cd backend && mypy src/

# Linting
cd backend && ruff check src/

# Database migrations
cd backend && alembic upgrade head
cd backend && alembic revision --autogenerate -m "description"
```

### Frontend
```bash
# Start development server
cd frontend && npm run dev

# Run tests
cd frontend && npm test

# Type checking
cd frontend && npm run typecheck

# Linting
cd frontend && npm run lint

# E2E tests
cd frontend && npm run test:e2e
```

## Code Style

### Python
- Use type hints on all function signatures
- Use Pydantic models for request/response validation
- Follow layered architecture: api/ → services/ → models/
- Structured JSON logging with correlation IDs
- Minimum 80% test coverage on new code

### TypeScript
- Strict mode enabled
- Components organized by feature
- Custom hooks for reusable logic
- API client services with typed responses

## Constitution Principles

1. **API-First Design**: Design APIs with OpenAPI specs before UI implementation
2. **Test-Driven Development**: Write failing tests first, then implement
3. **Type Safety**: Full type hints (Python), strict mode (TypeScript)
4. **Security by Default**: Validate all input, enforce auth on protected endpoints
5. **Observability**: Structured logging, health checks, correlation IDs

## Recent Changes

### 001-whisky-collection-tracker (2026-01-17)
- Initial feature: Personal whisky collection management
- Technologies added: FastAPI, React, PostgreSQL, SQLAlchemy
- Features: Bottle tracking, flavor profile matching, distillery info

<!-- MANUAL ADDITIONS START -->
<!-- MANUAL ADDITIONS END -->
