"""Authentication API routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.api.deps import get_current_user
from src.middleware.rate_limit import rate_limit_auth
from src.models.user import User
from src.schemas.auth import (
    AuthResponse,
    ChangePasswordRequest,
    LoginRequest,
    PasswordResetRequest,
    RegisterRequest,
    UserResponse,
)
from src.services.auth import (
    authenticate_user,
    create_user,
    get_user_by_email,
    hash_password,
    validate_password_strength,
    verify_password,
)
from src.services.jwt import (
    create_access_token,
    create_refresh_token,
    get_user_id_from_token,
)
from src.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(rate_limit_auth)])
async def register(
    request: RegisterRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    """Register a new user."""
    # Validate password strength
    error = validate_password_strength(request.password)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    # Check if email already exists
    existing = await get_user_by_email(db, request.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = await create_user(db, request.email, request.password)
    token, expires_in = create_access_token(user.id, user.email)

    logger.info("User registered", user_id=str(user.id), email=user.email)

    return AuthResponse(
        access_token=token,
        expires_in=expires_in,
        user=UserResponse(id=user.id, email=user.email, created_at=user.created_at),
    )


@router.post("/login", response_model=AuthResponse, dependencies=[Depends(rate_limit_auth)])
async def login(
    request: LoginRequest,
    db: AsyncSession = Depends(get_db),
) -> AuthResponse:
    """Login with email and password."""
    user = await authenticate_user(db, request.email, request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token, expires_in = create_access_token(user.id, user.email)

    logger.info("User logged in", user_id=str(user.id))

    return AuthResponse(
        access_token=token,
        expires_in=expires_in,
        user=UserResponse(id=user.id, email=user.email, created_at=user.created_at),
    )


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(
    current_user: User = Depends(get_current_user),
) -> None:
    """Logout the current user (client should discard token)."""
    logger.info("User logged out", user_id=str(current_user.id))


@router.post("/refresh", response_model=AuthResponse)
async def refresh_token(
    current_user: User = Depends(get_current_user),
) -> AuthResponse:
    """Refresh access token."""
    token, expires_in = create_access_token(current_user.id, current_user.email)

    return AuthResponse(
        access_token=token,
        expires_in=expires_in,
        user=UserResponse(
            id=current_user.id,
            email=current_user.email,
            created_at=current_user.created_at,
        ),
    )


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Change the current user's password."""
    # Verify current password
    if not verify_password(request.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Current password is incorrect",
        )

    # Validate new password
    error = validate_password_strength(request.new_password)
    if error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    current_user.password_hash = hash_password(request.new_password)
    await db.flush()

    logger.info("Password changed", user_id=str(current_user.id))


@router.post("/password/reset", status_code=status.HTTP_202_ACCEPTED, dependencies=[Depends(rate_limit_auth)])
async def request_password_reset(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db),
) -> dict[str, str]:
    """Request a password reset (always returns 202 to prevent email enumeration)."""
    # In a production app, this would send an email
    user = await get_user_by_email(db, request.email)
    if user:
        logger.info("Password reset requested", user_id=str(user.id))
    return {"message": "If the email exists, a reset link has been sent"}
