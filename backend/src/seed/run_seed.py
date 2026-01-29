"""Seed reference data (distilleries and whiskies) into the database."""

import asyncio
import json
import uuid
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.engine import AsyncSessionLocal
from src.logging import configure_logging, get_logger
from src.models.distillery import Distillery
from src.models.reference_whisky import ReferenceWhisky

logger = get_logger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"


def load_json(filename: str) -> list[dict[str, Any]]:
    """Load a JSON seed file from the data directory."""
    filepath = DATA_DIR / filename
    with open(filepath) as f:
        data: list[dict[str, Any]] = json.load(f)
        return data


async def seed_distilleries(session: AsyncSession) -> dict[str, uuid.UUID]:
    """Seed distilleries and return slug-to-id mapping."""
    result = await session.execute(select(Distillery.slug))
    existing_slugs = {row[0] for row in result.all()}

    data = load_json("distilleries.json")
    slug_to_id: dict[str, uuid.UUID] = {}
    added = 0

    for entry in data:
        slug = entry["slug"]
        if slug in existing_slugs:
            # Fetch existing ID
            result = await session.execute(
                select(Distillery.id).where(Distillery.slug == slug)
            )
            row = result.one_or_none()
            if row:
                slug_to_id[slug] = row[0]
            continue

        distillery_id = uuid.uuid4()
        slug_to_id[slug] = distillery_id

        distillery = Distillery(
            id=distillery_id,
            slug=slug,
            name=entry["name"],
            region=entry["region"],
            country=entry["country"],
            latitude=entry.get("latitude"),
            longitude=entry.get("longitude"),
            founded=entry.get("founded"),
            owner=entry.get("owner"),
            history=entry.get("history"),
            production_notes=entry.get("production_notes"),
            website=entry.get("website"),
        )
        session.add(distillery)
        added += 1

    await session.flush()
    logger.info("Seeded distilleries", added=added, total=len(data))
    return slug_to_id


async def seed_whiskies(
    session: AsyncSession, slug_to_distillery_id: dict[str, uuid.UUID]
) -> None:
    """Seed reference whiskies."""
    result = await session.execute(select(ReferenceWhisky.slug))
    existing_slugs = {row[0] for row in result.all()}

    data = load_json("whiskies.json")
    added = 0

    for entry in data:
        slug = entry["slug"]
        if slug in existing_slugs:
            continue

        distillery_slug = entry["distillery_slug"]
        distillery_id = slug_to_distillery_id.get(distillery_slug)
        if not distillery_id:
            logger.warning(
                "Distillery not found for whisky, skipping",
                whisky=slug,
                distillery=distillery_slug,
            )
            continue

        whisky = ReferenceWhisky(
            id=uuid.uuid4(),
            slug=slug,
            name=entry["name"],
            distillery_id=distillery_id,
            age_statement=entry.get("age_statement"),
            region=entry["region"],
            country=entry["country"],
            flavor_profile=entry["flavor_profile"],
            description=entry.get("description"),
        )
        session.add(whisky)
        added += 1

    await session.flush()
    logger.info("Seeded whiskies", added=added, total=len(data))


async def run_seed() -> None:
    """Run the full seed process."""
    configure_logging()
    logger.info("Starting seed process")

    async with AsyncSessionLocal() as session:
        try:
            slug_to_id = await seed_distilleries(session)
            await seed_whiskies(session, slug_to_id)
            await session.commit()
            logger.info("Seed process completed successfully")
        except Exception:
            await session.rollback()
            logger.exception("Seed process failed")
            raise


if __name__ == "__main__":
    asyncio.run(run_seed())
