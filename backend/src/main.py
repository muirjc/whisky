"""FastAPI application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import api_router
from src.config import get_settings
from src.logging import configure_logging, get_logger

settings = get_settings()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup and shutdown events."""
    # Startup
    configure_logging()
    logger.info("Starting Whisky Collection Tracker API")
    yield
    # Shutdown
    logger.info("Shutting down Whisky Collection Tracker API")


app = FastAPI(
    title="Whisky Collection Tracker API",
    description=(
        "API for managing personal whisky collections, discovering similar whiskies "
        "based on flavor profiles, and exploring distillery information."
    ),
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint with API information."""
    return {
        "name": "Whisky Collection Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
    }
