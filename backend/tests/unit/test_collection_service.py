"""Unit tests for collection search/filter logic."""

import pytest

from src.schemas.bottle import BottleUpdate
from src.schemas.enums import BottleStatus


class TestBottleUpdate:
    def test_partial_update(self) -> None:
        update = BottleUpdate(name="New Name")
        data = update.model_dump(exclude_unset=True)
        assert data == {"name": "New Name"}

    def test_status_update(self) -> None:
        update = BottleUpdate(status=BottleStatus.OPENED)
        data = update.model_dump(exclude_unset=True)
        assert data["status"] == BottleStatus.OPENED

    def test_empty_update(self) -> None:
        update = BottleUpdate()
        data = update.model_dump(exclude_unset=True)
        assert data == {}
