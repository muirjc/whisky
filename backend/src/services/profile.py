"""User taste profile analysis service."""

import uuid
from collections import Counter
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.bottle import Bottle
from src.schemas.flavor_profile import FlavorProfile
from src.schemas.reference_whisky import ReferenceWhiskyResponse
from src.services.matching import find_similar_whiskies


async def get_taste_profile(
    session: AsyncSession,
    user_id: uuid.UUID,
) -> dict[str, Any]:
    """Analyze user's collection to build a taste profile."""
    result = await session.execute(
        select(Bottle).where(Bottle.user_id == user_id)
    )
    bottles = list(result.scalars().all())

    total = len(bottles)
    bottles_with_profiles = [
        b for b in bottles if b.flavor_profile and any(b.flavor_profile.values())
    ]
    profile_count = len(bottles_with_profiles)

    # Compute average profile
    field_names = FlavorProfile.field_names()
    avg_profile: dict[str, float] = {}
    if profile_count > 0:
        for field in field_names:
            total_val = sum(
                b.flavor_profile.get(field, 0) for b in bottles_with_profiles  # type: ignore[union-attr]
            )
            avg_profile[field] = round(total_val / profile_count, 1)
    else:
        avg_profile = {f: 0.0 for f in field_names}

    # Dominant flavors (sorted by intensity)
    dominant = sorted(avg_profile.items(), key=lambda x: x[1], reverse=True)
    dominant_flavors = [
        {"flavor": name, "average_intensity": val}
        for name, val in dominant
        if val > 0
    ]

    # Region distribution
    region_counts = Counter(b.region for b in bottles)
    region_distribution = dict(region_counts)

    # Recommendations based on average profile
    recommendations = []
    if profile_count > 0:
        int_profile = {k: round(v) for k, v in avg_profile.items()}
        similar = await find_similar_whiskies(session, int_profile, limit=5)
        recommendations = [
            {"whisky": ReferenceWhiskyResponse.model_validate(whisky).model_dump(), "similarity_score": round(score, 3)}
            for whisky, score in similar
        ]

    return {
        "total_bottles": total,
        "bottles_with_profiles": profile_count,
        "average_profile": avg_profile,
        "dominant_flavors": dominant_flavors,
        "region_distribution": region_distribution,
        "recommendations": recommendations,
    }
