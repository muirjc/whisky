"""Comprehensive error handling middleware."""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from src.logging import get_logger

logger = get_logger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    """Register global error handlers on the FastAPI app."""

    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(
        request: Request, exc: IntegrityError
    ) -> JSONResponse:
        logger.warning("Database integrity error", error=str(exc.orig))
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "A resource with the given data already exists"},
        )

    @app.exception_handler(ValueError)
    async def value_error_handler(
        request: Request, exc: ValueError
    ) -> JSONResponse:
        logger.warning("Value error", error=str(exc))
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error("Unhandled exception", error=str(exc), exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An internal server error occurred"},
        )
