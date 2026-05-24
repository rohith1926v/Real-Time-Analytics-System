from datetime import UTC, datetime
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field

Severity = Literal["info", "low", "medium", "high", "critical"]
Status = Literal["open", "acknowledged", "investigating", "resolved"]


class AlertEvent(BaseModel):
    alert_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    severity: Severity
    title: str
    description: str
    source_event_id: str | None = None
    entity_id: str
    event_type: str
    source_topic: str
    anomaly_score: float | None = None
    ml_risk_score: float | None = None
    correlation_id: str
    incident_id: str | None = None
    explanation: str
    recommended_action: str
    status: Status = "open"
    tags: list[str]
    raw_payload: dict[str, Any]


class IncidentEvent(BaseModel):
    incident_id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    severity: Severity
    title: str
    description: str
    related_alerts: list[str]
    entity_ids: list[str]
    status: Status = "open"
    event_count: int = 1
    escalation_level: int = 0
    resolution_notes: str | None = None
    raw_payload: dict[str, Any]

