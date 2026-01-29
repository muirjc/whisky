"""User taste profile API routes."""

import uuid
from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_current_user_id
from src.db import get_db
from src.services.profile import get_taste_profile

router = APIRouter()


@router.get("/taste")
async def get_taste_profile_endpoint(
    user_id: uuid.UUID = Depends(get_current_user_id),
    db: AsyncSession = Depends(get_db),
) -> dict[str, Any]:
    """Get the user's taste profile analysis."""
    return await get_taste_profile(db, user_id)
