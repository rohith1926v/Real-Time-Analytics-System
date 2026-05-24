from datetime import datetime

from sqlalchemy import DateTime, Float, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class StoredRecordMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    event_type: Mapped[str | None] = mapped_column(String(128))
    entity_id: Mapped[str | None] = mapped_column(String(255))
    source_topic: Mapped[str] = mapped_column(String(255))
    timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    severity: Mapped[str | None] = mapped_column(String(64))
    raw_payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class TelemetryEvent(Base, StoredRecordMixin):
    __tablename__ = "telemetry_events"
    event_id: Mapped[str | None] = mapped_column(String(128))
    risk_score: Mapped[float | None] = mapped_column(Float)

    __table_args__ = (
        UniqueConstraint("source_topic", "event_id", name="uq_telemetry_events_source_event"),
        Index("ix_telemetry_events_timestamp", "timestamp"),
        Index("ix_telemetry_events_event_type", "event_type"),
        Index("ix_telemetry_events_entity_id", "entity_id"),
        Index("ix_telemetry_events_severity", "severity"),
        Index("ix_telemetry_events_source_topic", "source_topic"),
    )


class AnalyticsMetric(Base, StoredRecordMixin):
    __tablename__ = "analytics_metrics"
    event_id: Mapped[str | None] = mapped_column(String(128))
    risk_score: Mapped[float | None] = mapped_column(Float)

    __table_args__ = (
        Index("ix_analytics_metrics_timestamp", "timestamp"),
        Index("ix_analytics_metrics_event_type", "event_type"),
        Index("ix_analytics_metrics_entity_id", "entity_id"),
        Index("ix_analytics_metrics_severity", "severity"),
        Index("ix_analytics_metrics_source_topic", "source_topic"),
    )


class RiskMetric(Base, StoredRecordMixin):
    __tablename__ = "risk_metrics"
    event_id: Mapped[str | None] = mapped_column(String(128))
    risk_score: Mapped[float | None] = mapped_column(Float)

    __table_args__ = (
        Index("ix_risk_metrics_timestamp", "timestamp"),
        Index("ix_risk_metrics_event_type", "event_type"),
        Index("ix_risk_metrics_entity_id", "entity_id"),
        Index("ix_risk_metrics_severity", "severity"),
        Index("ix_risk_metrics_source_topic", "source_topic"),
    )


class FeatureSnapshot(Base, StoredRecordMixin):
    __tablename__ = "feature_snapshots"
    event_id: Mapped[str | None] = mapped_column(String(128))
    risk_score: Mapped[float | None] = mapped_column(Float)

    __table_args__ = (
        Index("ix_feature_snapshots_timestamp", "timestamp"),
        Index("ix_feature_snapshots_event_type", "event_type"),
        Index("ix_feature_snapshots_entity_id", "entity_id"),
        Index("ix_feature_snapshots_severity", "severity"),
        Index("ix_feature_snapshots_source_topic", "source_topic"),
    )


class AnomalyPrediction(Base, StoredRecordMixin):
    __tablename__ = "anomaly_predictions"
    prediction_id: Mapped[str | None] = mapped_column(String(128))
    ml_risk_score: Mapped[float | None] = mapped_column(Float)
    explanation: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        UniqueConstraint("prediction_id", name="uq_anomaly_predictions_prediction_id"),
        Index("ix_anomaly_predictions_timestamp", "timestamp"),
        Index("ix_anomaly_predictions_event_type", "event_type"),
        Index("ix_anomaly_predictions_entity_id", "entity_id"),
        Index("ix_anomaly_predictions_severity", "severity"),
        Index("ix_anomaly_predictions_source_topic", "source_topic"),
    )


class DeadLetterEvent(Base, StoredRecordMixin):
    __tablename__ = "deadletter_events"
    event_id: Mapped[str | None] = mapped_column(String(128))
    reason: Mapped[str | None] = mapped_column(Text)

    __table_args__ = (
        Index("ix_deadletter_events_timestamp", "timestamp"),
        Index("ix_deadletter_events_event_type", "event_type"),
        Index("ix_deadletter_events_entity_id", "entity_id"),
        Index("ix_deadletter_events_severity", "severity"),
        Index("ix_deadletter_events_source_topic", "source_topic"),
    )


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    alert_id: Mapped[str] = mapped_column(String(128), unique=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    severity: Mapped[str] = mapped_column(String(32))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    source_event_id: Mapped[str | None] = mapped_column(String(128))
    entity_id: Mapped[str | None] = mapped_column(String(255))
    event_type: Mapped[str | None] = mapped_column(String(128))
    source_topic: Mapped[str] = mapped_column(String(255))
    anomaly_score: Mapped[float | None] = mapped_column(Float)
    ml_risk_score: Mapped[float | None] = mapped_column(Float)
    correlation_id: Mapped[str] = mapped_column(String(255))
    incident_id: Mapped[str | None] = mapped_column(String(128))
    explanation: Mapped[str] = mapped_column(Text)
    recommended_action: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32))
    tags: Mapped[list] = mapped_column(JSON)
    raw_payload: Mapped[dict] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_alerts_severity", "severity"),
        Index("ix_alerts_timestamp", "timestamp"),
        Index("ix_alerts_incident_id", "incident_id"),
        Index("ix_alerts_entity_id", "entity_id"),
        Index("ix_alerts_status", "status"),
    )


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(128), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    severity: Mapped[str] = mapped_column(String(32))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    related_alerts: Mapped[list] = mapped_column(JSON)
    entity_ids: Mapped[list] = mapped_column(JSON)
    status: Mapped[str] = mapped_column(String(32))
    event_count: Mapped[int] = mapped_column(Integer)
    escalation_level: Mapped[int] = mapped_column(Integer)
    resolution_notes: Mapped[str | None] = mapped_column(Text)
    raw_payload: Mapped[dict] = mapped_column(JSON)

    __table_args__ = (
        Index("ix_incidents_severity", "severity"),
        Index("ix_incidents_updated_at", "updated_at"),
        Index("ix_incidents_status", "status"),
    )


class IncidentAlertLink(Base):
    __tablename__ = "incident_alert_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    incident_id: Mapped[str] = mapped_column(String(128))
    alert_id: Mapped[str] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        UniqueConstraint("incident_id", "alert_id", name="uq_incident_alert_link"),
        Index("ix_incident_alert_links_incident_id", "incident_id"),
    )


class AlertDedupCache(Base):
    __tablename__ = "alert_dedup_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    dedup_key: Mapped[str] = mapped_column(String(512), unique=True)
    alert_id: Mapped[str | None] = mapped_column(String(128))
    entity_id: Mapped[str | None] = mapped_column(String(255))
    counter: Mapped[int] = mapped_column(Integer)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_alert_dedup_cache_dedup_key", "dedup_key"),
        Index("ix_alert_dedup_cache_entity_id", "entity_id"),
    )
