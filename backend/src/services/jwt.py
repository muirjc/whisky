"""JWT token generation and validation."""

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt

from src.config import get_settings

settings = get_settings()


def create_access_token(user_id: uuid.UUID, email: str) -> tuple[str, int]:
    """Create a JWT access token. Returns (token, expires_in_seconds)."""
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "email": email,
        "exp": expire,
        "type": "access",
    }
    token = jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return token, int(expires_delta.total_seconds())


def create_refresh_token(user_id: uuid.UUID) -> str:
    """Create a JWT refresh token."""
    expires_delta = timedelta(days=settings.refresh_token_expire_days)
    expire = datetime.now(timezone.utc) + expires_delta
    payload: dict[str, Any] = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh",
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict[str, Any] | None:
    """Decode and validate a JWT token. Returns payload or None."""
    try:
        payload: dict[str, Any] = jwt.decode(
            token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        return None


def get_user_id_from_token(token: str, token_type: str = "access") -> uuid.UUID | None:
    """Extract user_id from a valid token of the specified type."""
    payload = decode_token(token)
    if not payload:
        return None
    if payload.get("type") != token_type:
        return None
    sub = payload.get("sub")
    if not sub:
        return None
    try:
        return uuid.UUID(sub)
    except ValueError:
        return None
