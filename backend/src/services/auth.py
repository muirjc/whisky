"""Authentication service for user registration and login."""

import re

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_strength(password: str) -> str | None:
    """Validate password meets requirements. Returns error message or None."""
    if len(password) < 8:
        return "Password must be at least 8 characters"
    if not re.search(r"[a-zA-Z]", password):
        return "Password must contain at least one letter"
    if not re.search(r"\d", password):
        return "Password must contain at least one number"
    return None


async def get_user_by_email(session: AsyncSession, email: str) -> User | None:
    """Get a user by email address."""
    result = await session.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def create_user(session: AsyncSession, email: str, password: str) -> User:
    """Create a new user with hashed password."""
    user = User(
        email=email,
        password_hash=hash_password(password),
    )
    session.add(user)
    await session.flush()
    return user


async def authenticate_user(
    session: AsyncSession, email: str, password: str
) -> User | None:
    """Authenticate a user by email and password. Returns User or None."""
    user = await get_user_by_email(session, email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
