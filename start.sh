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

BACKEND_PID=""
FRONTEND_PID=""

cleanup() {
    echo "Shutting down..."
    [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null || true
    [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null || true
    wait 2>/dev/null || true
    echo "Done."
}
trap cleanup EXIT INT TERM

# --- Database ---
# Check if container exists and is running
if docker inspect "$DB_CONTAINER" &>/dev/null; then
    if [ "$(docker inspect -f '{{.State.Running}}' "$DB_CONTAINER")" = "true" ]; then
        echo "Database container already running."
    else
        echo "Starting existing database container..."
        docker start "$DB_CONTAINER" >/dev/null
    fi
else
    # Remove any orphaned volume
    docker volume rm "${DB_CONTAINER}-data" 2>/dev/null || true

    echo "Creating database container..."
    docker run -d --name "$DB_CONTAINER" \
        -e POSTGRES_USER="$DB_USER" \
        -e POSTGRES_PASSWORD="$DB_PASS" \
        -e POSTGRES_DB="$DB_NAME" \
        -p "$DB_PORT":5432 \
        -v "${DB_CONTAINER}-data:/var/lib/postgresql/data" \
        postgres:15-alpine >/dev/null
fi

# Wait for PostgreSQL to accept connections
echo "Waiting for database..."
sleep 2  # Give container time to initialize
for i in $(seq 1 30); do
    if docker exec "$DB_CONTAINER" pg_isready -U "$DB_USER" &>/dev/null; then
        # Verify we can actually connect with password
        if docker exec "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1" &>/dev/null; then
            echo "Database ready."
            break
        fi
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
