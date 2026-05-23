from app.core.settings import Settings
from app.schemas.health import HealthCheckResponse


class HealthService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def get_status(self) -> HealthCheckResponse:
        return HealthCheckResponse(
            status="healthy",
            service=self._settings.project_name,
            environment=self._settings.environment,
            version=self._settings.app_version,
        )
