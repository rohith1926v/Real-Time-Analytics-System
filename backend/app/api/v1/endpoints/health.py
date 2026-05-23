from fastapi import APIRouter, Depends

from app.core.settings import Settings, get_settings
from app.schemas.health import HealthCheckResponse
from app.services.health_service import HealthService

router = APIRouter()


@router.get("", response_model=HealthCheckResponse, summary="Service health check")
async def health_check(settings: Settings = Depends(get_settings)) -> HealthCheckResponse:
    service = HealthService(settings=settings)
    return service.get_status()
