# Runbook: Database Migration

## Prerequisites

- PostgreSQL running (via `docker-compose up -d postgres`)
- Backend virtualenv activated
- `DATABASE_URL` environment variable set

## Running Migrations

```bash
cd backend
alembic upgrade head
```

## Creating a New Migration

```bash
cd backend
alembic revision --autogenerate -m "description of change"
```

Review the generated file in `backend/alembic/versions/` before applying.

## Rolling Back

```bash
# Roll back one revision
cd backend
alembic downgrade -1

# Roll back to specific revision
alembic downgrade <revision_id>
```

## Troubleshooting

- **Connection refused**: Ensure PostgreSQL is running on the correct port (5432 for dev, 5433 for test)
- **Migration conflicts**: If two migrations target the same revision, resolve by rebasing one with `alembic merge`
- **Data loss risk**: Always back up production data before running destructive migrations (column drops, table drops)
