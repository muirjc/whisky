"""Flavor profile similarity matching service."""

import math
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.reference_whisky import ReferenceWhisky
from src.schemas.flavor_profile import FlavorProfile

# Weights for flavor descriptors (higher = more important for distinguishing)
FLAVOR_WEIGHTS: dict[str, float] = {
    "smoky_peaty": 1.5,
    "fruity": 1.0,
    "sherried": 1.2,
    "spicy": 1.0,
    "floral_grassy": 1.0,
    "maritime": 1.3,
    "honey_sweet": 1.0,
    "vanilla_caramel": 1.0,
    "oak_woody": 1.0,
    "nutty": 0.8,
    "malty_biscuity": 0.8,
    "medicinal_iodine": 1.5,
}


def compute_similarity(
    profile_a: dict[str, int], profile_b: dict[str, int]
) -> float:
    """Compute weighted Euclidean distance similarity score (0-1).

    Score of 1 means identical profiles.
    """
    field_names = FlavorProfile.field_names()
    weighted_sum = 0.0

    for field in field_names:
        a_val = profile_a.get(field, 0)
        b_val = profile_b.get(field, 0)
        weight = FLAVOR_WEIGHTS.get(field, 1.0)
        weighted_sum += weight * ((a_val - b_val) ** 2)

    distance = math.sqrt(weighted_sum)
    # Normalize to 0-1 range (1 = identical)
    return 1.0 / (1.0 + distance)


async def find_similar_whiskies(
    session: AsyncSession,
    flavor_profile: dict[str, int],
    limit: int = 10,
) -> list[tuple[ReferenceWhisky, float]]:
    """Find similar reference whiskies based on flavor profile.

    Returns list of (whisky, similarity_score) tuples, sorted by similarity.
    """
    result = await session.execute(select(ReferenceWhisky))
    all_whiskies = result.scalars().all()

    scored: list[tuple[ReferenceWhisky, float]] = []
    for whisky in all_whiskies:
        score = compute_similarity(flavor_profile, whisky.flavor_profile)
        scored.append((whisky, score))

    # Sort by similarity score descending
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:limit]
