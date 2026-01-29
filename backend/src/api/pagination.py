"""Cursor-based pagination utilities."""

import base64
import json
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class CursorParams(BaseModel):
    """Pagination cursor parameters."""

    cursor: str | None = Field(None, description="Pagination cursor from previous response")
    limit: int = Field(20, ge=1, le=100, description="Number of items to return")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response with cursor-based navigation."""

    items: list[T]
    next_cursor: str | None = Field(None, description="Cursor for next page, null if no more")
    has_more: bool = Field(description="Whether there are more items")


def encode_cursor(data: dict[str, Any]) -> str:
    """Encode cursor data to base64 string."""
    json_str = json.dumps(data, default=str)
    return base64.urlsafe_b64encode(json_str.encode()).decode()


def decode_cursor(cursor: str) -> dict[str, Any]:
    """Decode cursor from base64 string."""
    try:
        json_str = base64.urlsafe_b64decode(cursor.encode()).decode()
        return json.loads(json_str)  # type: ignore[no-any-return]
    except Exception:
        return {}


def create_cursor_from_item(item: Any, sort_field: str = "id") -> str:
    """Create cursor from the last item in a result set."""
    cursor_data = {"id": str(getattr(item, "id", None))}

    # Add sort field value if different from id
    if sort_field != "id" and hasattr(item, sort_field):
        value = getattr(item, sort_field)
        cursor_data[sort_field] = str(value) if value is not None else ""

    return encode_cursor(cursor_data)


def get_cursor_value(cursor: str | None, field: str = "id") -> str | None:
    """Extract a value from cursor for use in queries."""
    if not cursor:
        return None
    data = decode_cursor(cursor)
    return data.get(field)
