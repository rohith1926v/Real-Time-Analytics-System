from fastapi import APIRouter

from app.api.v1.endpoints import analytics, dashboard, health

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(analytics.router, tags=["analytics"])
api_router.include_router(dashboard.router, tags=["dashboard"])
