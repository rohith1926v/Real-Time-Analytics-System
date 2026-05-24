from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StorageRecord(BaseModel):
    source_topic: str
    raw_payload: dict[str, Any]
    record_kind: Literal["telemetry", "analytics", "risk", "feature", "prediction", "deadletter"]
    event_id: str | None = None
    prediction_id: str | None = None
    event_type: str | None = None
    entity_id: str | None = None
    timestamp: datetime | None = None
    risk_score: float | None = None
    ml_risk_score: float | None = None
    severity: str | None = None
    explanation: str | None = None
    reason: str | None = None

    model_config = ConfigDict(extra="ignore")

    @field_validator("timestamp", mode="before")
    @classmethod
    def parse_timestamp(cls, value: Any) -> datetime | None:
        if value is None or isinstance(value, datetime):
            return value
        if isinstance(value, str):
            normalized = value.replace("Z", "+00:00")
            try:
                return datetime.fromisoformat(normalized)
            except ValueError:
                return None
        return None

    @property
    def timestamp_or_created(self) -> datetime:
        return self.timestamp or datetime.now(UTC)

