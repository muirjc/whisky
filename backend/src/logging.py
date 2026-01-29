"""Structured JSON logging with correlation IDs."""

import logging
import sys
import uuid
from contextvars import ContextVar
from typing import Any

import structlog

from src.config import get_settings

# Context variable for correlation ID
correlation_id_ctx: ContextVar[str] = ContextVar("correlation_id", default="")


def get_correlation_id() -> str:
    """Get current correlation ID or generate new one."""
    cid = correlation_id_ctx.get()
    if not cid:
        cid = str(uuid.uuid4())
        correlation_id_ctx.set(cid)
    return cid


def set_correlation_id(cid: str) -> None:
    """Set correlation ID for current context."""
    correlation_id_ctx.set(cid)


def add_correlation_id(
    logger: logging.Logger, method_name: str, event_dict: dict[str, Any]
) -> dict[str, Any]:
    """Add correlation ID to log event."""
    event_dict["correlation_id"] = get_correlation_id()
    return event_dict


def configure_logging() -> None:
    """Configure structured logging for the application."""
    settings = get_settings()

    # Set log level
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            add_correlation_id,  # type: ignore[list-item]
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )

    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


def get_logger(name: str = __name__) -> structlog.BoundLogger:
    """Get a configured logger instance."""
    return structlog.get_logger(name)  # type: ignore[no-any-return]
