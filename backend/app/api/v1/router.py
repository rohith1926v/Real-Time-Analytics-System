from fastapi import APIRouter

from app.api.v1.endpoints import alerts, analytics, dashboard, health, monitoring, threat_intel

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(analytics.router, tags=["analytics"])
api_router.include_router(dashboard.router, tags=["dashboard"])
api_router.include_router(alerts.router, tags=["alerts"])
api_router.include_router(monitoring.router, tags=["monitoring"])
api_router.include_router(threat_intel.router, tags=["threat-intelligence"])
