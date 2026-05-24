from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class ServiceHealth(BaseModel):
    name: str
    status: str
    detail: str
    category: str
    endpoint: str | None = None
    last_checked: datetime


class MonitoringOverview(BaseModel):
    status: str
    services_total: int
    services_healthy: int
    services_degraded: int
    services_down: int
    total_events: int
    total_predictions: int
    total_alerts: int
    open_incidents: int
    generated_at: datetime
    prometheus_url: str
    grafana_url: str


class PipelineMetrics(BaseModel):
    telemetry_events: int
    analytics_metrics: int
    risk_metrics: int
    feature_snapshots: int
    anomaly_predictions: int
    alerts: int
    incidents: int
    deadletter_events: int
    generated_at: datetime


class ErrorSummary(BaseModel):
    deadletter_events: int
    critical_alerts: int
    failed_services: int
    degraded_services: int
    recent_errors: list[dict[str, Any]] = Field(default_factory=list)
    generated_at: datetime


class MetricsSummary(BaseModel):
    prometheus_available: bool
    scraped_targets_up: int
    scraped_targets_down: int
    key_metrics: dict[str, float]
    generated_at: datetime
