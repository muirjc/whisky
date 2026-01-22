"""Health check endpoints for liveness and readiness probes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db

router = APIRouter()


@router.get("/health")
async def health_check() -> dict[str, str]:
    """Liveness check - returns 200 if the service is running."""
    return {"status": "healthy"}


@router.get("/ready")
async def readiness_check(db: AsyncSession = Depends(get_db)) -> dict[str, str]:
    """Readiness check - verifies database connectivity."""
    try:
        # Execute a simple query to verify database connection
        await db.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}",
        )
