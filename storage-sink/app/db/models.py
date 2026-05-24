from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class StoredRecordMixin:
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    entity_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_topic: Mapped[str] = mapped_column(String(255), nullable=False)
    timestamp: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    severity: Mapped[str | None] = mapped_column(String(64), nullable=True)
    raw_payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)


class TelemetryEvent(Base, StoredRecordMixin):
    __tablename__ = "telemetry_events"
    event_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)

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
    event_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        Index("ix_analytics_metrics_timestamp", "timestamp"),
        Index("ix_analytics_metrics_event_type", "event_type"),
        Index("ix_analytics_metrics_entity_id", "entity_id"),
        Index("ix_analytics_metrics_severity", "severity"),
        Index("ix_analytics_metrics_source_topic", "source_topic"),
    )


class RiskMetric(Base, StoredRecordMixin):
    __tablename__ = "risk_metrics"
    event_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        Index("ix_risk_metrics_timestamp", "timestamp"),
        Index("ix_risk_metrics_event_type", "event_type"),
        Index("ix_risk_metrics_entity_id", "entity_id"),
        Index("ix_risk_metrics_severity", "severity"),
        Index("ix_risk_metrics_source_topic", "source_topic"),
    )


class FeatureSnapshot(Base, StoredRecordMixin):
    __tablename__ = "feature_snapshots"
    event_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)

    __table_args__ = (
        Index("ix_feature_snapshots_timestamp", "timestamp"),
        Index("ix_feature_snapshots_event_type", "event_type"),
        Index("ix_feature_snapshots_entity_id", "entity_id"),
        Index("ix_feature_snapshots_severity", "severity"),
        Index("ix_feature_snapshots_source_topic", "source_topic"),
    )


class AnomalyPrediction(Base, StoredRecordMixin):
    __tablename__ = "anomaly_predictions"
    prediction_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    ml_risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)

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
    event_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        Index("ix_deadletter_events_timestamp", "timestamp"),
        Index("ix_deadletter_events_event_type", "event_type"),
        Index("ix_deadletter_events_entity_id", "entity_id"),
        Index("ix_deadletter_events_severity", "severity"),
        Index("ix_deadletter_events_source_topic", "source_topic"),
    )

