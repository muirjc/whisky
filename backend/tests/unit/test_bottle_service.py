"""Unit tests for bottle service."""

import pytest

from src.schemas.bottle import BottleCreate
from src.schemas.enums import BottleStatus
from src.schemas.flavor_profile import FlavorProfile


class TestBottleCreate:
    def test_valid_bottle(self) -> None:
        bottle = BottleCreate(
            name="Lagavulin 16",
            distillery_name="Lagavulin",
            region="Islay",
            country="Scotland",
        )
        assert bottle.name == "Lagavulin 16"
        assert bottle.status == BottleStatus.SEALED

    def test_with_all_fields(self) -> None:
        bottle = BottleCreate(
            name="Lagavulin 16",
            distillery_name="Lagavulin",
            region="Islay",
            country="Scotland",
            age_statement=16,
            size_ml=700,
            abv=43.0,
            rating=5,
            flavor_profile=FlavorProfile(smoky_peaty=5, maritime=4),
            tasting_notes="Intense peat smoke",
            status=BottleStatus.OPENED,
        )
        assert bottle.age_statement == 16
        assert bottle.rating == 5

    def test_invalid_rating(self) -> None:
        with pytest.raises(Exception):
            BottleCreate(
                name="Test",
                distillery_name="Test",
                region="Islay",
                country="Scotland",
                rating=6,
            )

    def test_invalid_abv(self) -> None:
        with pytest.raises(Exception):
            BottleCreate(
                name="Test",
                distillery_name="Test",
                region="Islay",
                country="Scotland",
                abv=101,
            )


class TestFlavorProfile:
    def test_default_values(self) -> None:
        fp = FlavorProfile()
        assert fp.smoky_peaty == 0
        assert fp.fruity == 0

    def test_to_vector(self) -> None:
        fp = FlavorProfile(smoky_peaty=5, fruity=3)
        vec = fp.to_vector()
        assert vec[0] == 5
        assert vec[1] == 3
        assert len(vec) == 12

    def test_from_dict(self) -> None:
        fp = FlavorProfile.from_dict({"smoky_peaty": 4, "fruity": 2})
        assert fp.smoky_peaty == 4
        assert fp.fruity == 2

    def test_from_empty_dict(self) -> None:
        fp = FlavorProfile.from_dict(None)
        assert fp.smoky_peaty == 0
