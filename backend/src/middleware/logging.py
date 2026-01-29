"""Request/response logging middleware."""

import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from src.logging import get_logger, set_correlation_id

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware that logs request/response details with correlation IDs."""

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Set correlation ID from header or generate new one
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        set_correlation_id(correlation_id)

        start_time = time.perf_counter()

        logger.info(
            "Request started",
            method=request.method,
            path=str(request.url.path),
            query=str(request.query_params),
        )

        response = await call_next(request)

        duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

        logger.info(
            "Request completed",
            method=request.method,
            path=str(request.url.path),
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        response.headers["X-Correlation-ID"] = correlation_id
        return response
