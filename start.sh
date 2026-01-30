#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

DB_CONTAINER="whisky-postgres-dev"
DB_USER="whisky"
DB_PASS="whisky"
DB_NAME="whisky"
DB_PORT=5432

cleanup() {
    echo "Shutting down..."
    kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
    wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
    echo "Done."
}
trap cleanup EXIT INT TERM

# --- Database ---
if docker inspect "$DB_CONTAINER" &>/dev/null; then
    if [ "$(docker inspect -f '{{.State.Running}}' "$DB_CONTAINER")" != "true" ]; then
        echo "Starting existing database container..."
        docker start "$DB_CONTAINER"
    else
        echo "Database container already running."
    fi
else
    echo "Creating database container..."
    docker run -d --name "$DB_CONTAINER" \
        -e POSTGRES_USER="$DB_USER" \
        -e POSTGRES_PASSWORD="$DB_PASS" \
        -e POSTGRES_DB="$DB_NAME" \
        -p "$DB_PORT":5432 \
        --tmpfs /var/lib/postgresql/data \
        postgres:16-alpine
fi

echo "Waiting for database..."
for i in $(seq 1 30); do
    if docker exec "$DB_CONTAINER" pg_isready -U "$DB_USER" &>/dev/null; then
        echo "Database ready."
        break
    fi
    if [ "$i" -eq 30 ]; then
        echo "ERROR: Database failed to start." >&2
        exit 1
    fi
    sleep 1
done

# --- Migrations ---
echo "Running migrations..."
cd "$BACKEND_DIR"
.venv/bin/alembic upgrade head

# --- Seed data (idempotent) ---
echo "Seeding reference data..."
.venv/bin/python3 -m src.seed.run_seed 2>&1 | tail -3

# --- Backend ---
echo "Starting backend on http://localhost:8000 ..."
.venv/bin/uvicorn src.main:app --reload --port 8000 &
BACKEND_PID=$!

# --- Frontend ---
echo "Starting frontend on http://localhost:5173 ..."
cd "$FRONTEND_DIR"
npm run dev &
FRONTEND_PID=$!

echo ""
echo "==================================="
echo "  Whisky Collection Tracker"
echo "==================================="
echo "  Frontend: http://localhost:5173"
echo "  Backend:  http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo "==================================="
echo "  Press Ctrl+C to stop"
echo ""

wait
