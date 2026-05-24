import time
from collections.abc import Callable

from fastapi import Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from starlette.middleware.base import BaseHTTPMiddleware

HTTP_REQUESTS_TOTAL = Counter("http_requests_total", "Total HTTP requests", ["method", "path", "status"])
HTTP_REQUEST_DURATION_SECONDS = Histogram("http_request_duration_seconds", "HTTP request latency", ["method", "path"])
ACTIVE_WEBSOCKET_CONNECTIONS = Gauge("active_websocket_connections", "Active dashboard and alert WebSocket connections", ["stream"])
DASHBOARD_WEBSOCKET_MESSAGES_TOTAL = Counter("dashboard_websocket_messages_total", "Dashboard WebSocket messages sent")
ALERT_WEBSOCKET_MESSAGES_TOTAL = Counter("alert_websocket_messages_total", "Alert WebSocket messages sent")


class PrometheusMetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path == "/metrics":
            return await call_next(request)
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start
        path = request.scope.get("route").path if request.scope.get("route") else request.url.path
        HTTP_REQUESTS_TOTAL.labels(request.method, path, str(response.status_code)).inc()
        HTTP_REQUEST_DURATION_SECONDS.labels(request.method, path).observe(duration)
        return response


def metrics_response() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
