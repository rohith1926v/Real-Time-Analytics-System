from collections import defaultdict, deque
from time import monotonic

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response


class LocalRateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, requests_per_minute: int = 600) -> None:
        super().__init__(app)
        self._requests_per_minute = requests_per_minute
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.url.path in {"/metrics", "/docs", "/redoc"} or request.url.path.endswith("/openapi.json"):
            return await call_next(request)
        client = request.client.host if request.client else "unknown"
        now = monotonic()
        hits = self._hits[client]
        while hits and now - hits[0] > 60:
            hits.popleft()
        if len(hits) >= self._requests_per_minute:
            return Response("Rate limit exceeded", status_code=429, media_type="text/plain")
        hits.append(now)
        return await call_next(request)
