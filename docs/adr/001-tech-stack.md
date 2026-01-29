# ADR-001: Technology Stack Selection

**Status**: Accepted
**Date**: 2026-01-17
**Context**: Choosing the technology stack for the Whisky Collection Tracker web application.

## Decision

- **Backend**: Python 3.11+ with FastAPI, SQLAlchemy (async), PostgreSQL
- **Frontend**: TypeScript 5.x with React 18, Vite
- **Auth**: JWT tokens with bcrypt password hashing

## Rationale

### FastAPI over Django/Flask

- Native async support for database operations (SQLAlchemy async)
- Automatic OpenAPI/Swagger documentation aligns with API-First constitution principle
- Pydantic integration provides type-safe request/response validation
- High performance for API-heavy workloads

### PostgreSQL over SQLite

- JSONB columns for flexible flavor profile storage without schema migration per field
- Full-text search capabilities for distillery/bottle search
- Production-grade concurrency for multi-user data isolation
- UUID primary key support

### React over Vue/Svelte

- Mature ecosystem with extensive TypeScript support
- Large component library ecosystem for future extensibility
- Team familiarity and hiring pool considerations

### Separate Frontend/Backend over Monolith

- Enables independent deployment and scaling
- Aligns with API-First constitution principle
- Allows frontend to be replaced without backend changes
- Parallel development by different team members

## Consequences

- Requires Docker for local PostgreSQL development
- Two separate build/deploy pipelines needed
- CORS configuration required for cross-origin requests
- More complex local setup compared to a monolith
