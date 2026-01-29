"""Authentication Pydantic schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    """User registration request."""

    email: EmailStr
    password: str = Field(min_length=8, description="Minimum 8 characters")


class LoginRequest(BaseModel):
    """User login request."""

    email: EmailStr
    password: str


class ChangePasswordRequest(BaseModel):
    """Change password request."""

    current_password: str
    new_password: str = Field(min_length=8, description="Minimum 8 characters")


class PasswordResetRequest(BaseModel):
    """Password reset request."""

    email: EmailStr


class UserResponse(BaseModel):
    """User information response."""

    id: uuid.UUID
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    """Authentication response with token."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponse
