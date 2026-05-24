from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict


class RecordResponse(BaseModel):
    id: int
    event_type: str | None = None
    entity_id: str | None = None
    source_topic: str
    timestamp: datetime | None = None
    severity: str | None = None
    risk_score: float | None = None
    ml_risk_score: float | None = None
    raw_payload: dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PredictionResponse(RecordResponse):
    prediction_id: str | None = None
    explanation: str | None = None


class AnalyticsSummaryResponse(BaseModel):
    telemetry_events: int
    analytics_metrics: int
    risk_metrics: int
    feature_snapshots: int
    anomaly_predictions: int
    deadletter_events: int
    high_risk_predictions: int

