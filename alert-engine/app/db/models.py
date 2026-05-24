from datetime import UTC, datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    alert_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    source_event_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    entity_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    event_type: Mapped[str | None] = mapped_column(String(128), nullable=True)
    source_topic: Mapped[str] = mapped_column(String(255), nullable=False)
    anomaly_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    ml_risk_score: Mapped[float | None] = mapped_column(Float, nullable=True)
    correlation_id: Mapped[str] = mapped_column(String(255), nullable=False)
    incident_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_action: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="open", nullable=False)
    tags: Mapped[list] = mapped_column(JSONB, nullable=False)
    raw_payload: Mapped[dict] = mapped_column(JSONB, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    __table_args__ = (
        Index("ix_alerts_severity", "severity"),
        Index("ix_alerts_timestamp", "timestamp"),
        Index("ix_alerts_incident_id", "incident_id"),
        Index("ix_alerts_entity_id", "entity_id"),
        Index("ix_alerts_status", "status"),
    )


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    severity: Mapped[str] = mapped_column(String(32), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    related_alerts: Mapped[list] = mapped_column(JSONB, nullable=False)
    entity_ids: Mapped[list] = mapped_column(JSONB, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="open", nullable=False)
    event_count: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    escalation_level: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    resolution_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_payload: Mapped[dict] = mapped_column(JSONB, nullable=False)

    __table_args__ = (
        Index("ix_incidents_severity", "severity"),
        Index("ix_incidents_updated_at", "updated_at"),
        Index("ix_incidents_status", "status"),
    )


class IncidentAlertLink(Base):
    __tablename__ = "incident_alert_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[str] = mapped_column(String(128), ForeignKey("incidents.incident_id"), nullable=False)
    alert_id: Mapped[str] = mapped_column(String(128), ForeignKey("alerts.alert_id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    __table_args__ = (
        UniqueConstraint("incident_id", "alert_id", name="uq_incident_alert_link"),
        Index("ix_incident_alert_links_incident_id", "incident_id"),
    )


class AlertDedupCache(Base):
    __tablename__ = "alert_dedup_cache"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dedup_key: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    alert_id: Mapped[str | None] = mapped_column(String(128), nullable=True)
    entity_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    counter: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    __table_args__ = (
        Index("ix_alert_dedup_cache_dedup_key", "dedup_key"),
        Index("ix_alert_dedup_cache_entity_id", "entity_id"),
    )

