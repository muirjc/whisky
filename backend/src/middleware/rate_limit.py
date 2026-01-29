"""Simple in-memory rate limiter for auth endpoints."""

import time
from collections import defaultdict
from fastapi import HTTPException, Request, status


class RateLimiter:
    """Token bucket rate limiter keyed by client IP."""

    def __init__(self, max_requests: int = 10, window_seconds: int = 60) -> None:
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = defaultdict(list)

    def _cleanup(self, key: str, now: float) -> None:
        cutoff = now - self.window_seconds
        self._requests[key] = [t for t in self._requests[key] if t > cutoff]

    def check(self, key: str) -> None:
        now = time.monotonic()
        self._cleanup(key, now)
        if len(self._requests[key]) >= self.max_requests:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests. Please try again later.",
            )
        self._requests[key].append(now)


auth_rate_limiter = RateLimiter(max_requests=10, window_seconds=60)


async def rate_limit_auth(request: Request) -> None:
    """Dependency to rate-limit auth endpoints by client IP."""
    client_ip = request.client.host if request.client else "unknown"
    auth_rate_limiter.check(client_ip)
