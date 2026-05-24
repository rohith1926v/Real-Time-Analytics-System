from typing import Any

from app.config.topics import (
    ANALYTICS_ENRICHED_EVENTS,
    ANALYTICS_FEATURE_ENGINEERING,
    ANALYTICS_RISK_METRICS,
    ANALYTICS_WINDOW_METRICS,
    ML_ANOMALY_PREDICTIONS,
    TELEMETRY_DEADLETTER_EVENTS,
)
from app.schemas.records import StorageRecord


def map_payload_to_record(source_topic: str, payload: dict[str, Any]) -> StorageRecord:
    record_kind = _record_kind(source_topic)
    timestamp = payload.get("timestamp") or payload.get("event_timestamp") or payload.get("window_start") or payload.get("calculated_at")
    event_type = payload.get("event_type") or payload.get("metric_type") or payload.get("feature_name") or record_kind
    entity_id = payload.get("entity_id") or payload.get("user_id") or payload.get("source_ip") or payload.get("endpoint") or payload.get("anomaly_type")
    severity = payload.get("severity")
    if not severity and payload.get("risk_level"):
        severity = payload.get("risk_level")

    return StorageRecord(
        source_topic=source_topic,
        raw_payload=payload,
        record_kind=record_kind,
        event_id=_string_or_none(payload.get("event_id") or payload.get("source_event_id")),
        prediction_id=_string_or_none(payload.get("prediction_id")),
        event_type=_string_or_none(event_type),
        entity_id=_string_or_none(entity_id),
        timestamp=timestamp,
        risk_score=_float_or_none(payload.get("risk_score") or payload.get("risk_score_moving_average")),
        ml_risk_score=_float_or_none(payload.get("ml_risk_score")),
        severity=_string_or_none(severity),
        explanation=_string_or_none(payload.get("explanation")),
        reason=_string_or_none(payload.get("reason")),
    )


def _record_kind(source_topic: str) -> str:
    if source_topic == ML_ANOMALY_PREDICTIONS:
        return "prediction"
    if source_topic == TELEMETRY_DEADLETTER_EVENTS:
        return "deadletter"
    if source_topic == ANALYTICS_RISK_METRICS:
        return "risk"
    if source_topic == ANALYTICS_FEATURE_ENGINEERING:
        return "feature"
    if source_topic in {ANALYTICS_ENRICHED_EVENTS, ANALYTICS_WINDOW_METRICS}:
        return "analytics"
    return "telemetry"


def _string_or_none(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _float_or_none(value: Any) -> float | None:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None

