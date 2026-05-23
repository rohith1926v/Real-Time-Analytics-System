from datetime import UTC, datetime

from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    status: str = Field(examples=["healthy"])
    service: str
    environment: str
    version: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
