"""API module with router configuration."""

from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.api.bottles import router as bottles_router
from src.api.distilleries import router as distilleries_router
from src.api.health import router as health_router
from src.api.profile import router as profile_router
from src.api.whiskies import router as whiskies_router
from src.api.wishlist import router as wishlist_router

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
api_router.include_router(bottles_router, prefix="/bottles", tags=["Bottles"])
api_router.include_router(wishlist_router, prefix="/wishlist", tags=["Wishlist"])
api_router.include_router(distilleries_router, prefix="/distilleries", tags=["Distilleries"])
api_router.include_router(whiskies_router, prefix="/whiskies", tags=["Whiskies"])
api_router.include_router(profile_router, prefix="/profile", tags=["Profile"])

__all__ = ["api_router"]
