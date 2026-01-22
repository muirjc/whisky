"""API module with router configuration."""

from fastapi import APIRouter

from src.api.health import router as health_router

# Create main API router
api_router = APIRouter()

# Include sub-routers
api_router.include_router(health_router, tags=["Health"])

# These will be added as they are implemented:
# api_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
# api_router.include_router(bottles_router, prefix="/bottles", tags=["Bottles"])
# api_router.include_router(wishlist_router, prefix="/wishlist", tags=["Wishlist"])
# api_router.include_router(distilleries_router, prefix="/distilleries", tags=["Distilleries"])
# api_router.include_router(whiskies_router, prefix="/whiskies", tags=["Whiskies"])
# api_router.include_router(profile_router, prefix="/profile", tags=["Profile"])

__all__ = ["api_router"]
