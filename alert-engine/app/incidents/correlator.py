from datetime import UTC, datetime, timedelta

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.config.settings import AlertEngineSettings
from app.db.models import Incident, IncidentAlertLink
from app.schemas.alerts import AlertEvent
from app.utils.metrics import INCIDENTS_CREATED_TOTAL

SEVERITY_RANK = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


class IncidentCorrelator:
    def __init__(self, settings: AlertEngineSettings) -> None:
        self._settings = settings

    def correlate(self, session: Session, alert: AlertEvent) -> str:
        window_start = datetime.now(UTC) - timedelta(seconds=self._settings.incident_window_seconds)
        incident = session.scalars(
            select(Incident)
            .where(Incident.status != "resolved")
            .where(Incident.updated_at >= window_start)
            .where(Incident.raw_payload["correlation_id"].as_string() == alert.correlation_id)
            .order_by(desc(Incident.updated_at))
            .limit(1)
        ).first()

        if incident is None:
            incident = Incident(
                incident_id=f"inc-{alert.alert_id}",
                severity=alert.severity,
                title=f"Incident: {alert.title}",
                description=alert.explanation,
                related_alerts=[alert.alert_id],
                entity_ids=[alert.entity_id],
                status="open",
                event_count=1,
                escalation_level=SEVERITY_RANK[alert.severity],
                raw_payload={"correlation_id": alert.correlation_id, "timeline": [alert.model_dump(mode="json")]},
            )
            session.add(incident)
            INCIDENTS_CREATED_TOTAL.inc()
        else:
            related_alerts = list(incident.related_alerts or [])
            entity_ids = list(incident.entity_ids or [])
            timeline = list((incident.raw_payload or {}).get("timeline", []))
            if alert.alert_id not in related_alerts:
                related_alerts.append(alert.alert_id)
            if alert.entity_id not in entity_ids:
                entity_ids.append(alert.entity_id)
            timeline.append(alert.model_dump(mode="json"))
            incident.related_alerts = related_alerts
            incident.entity_ids = entity_ids
            incident.event_count += 1
            incident.updated_at = datetime.now(UTC)
            incident.escalation_level = max(incident.escalation_level, SEVERITY_RANK[alert.severity])
            incident.severity = self._escalate(incident.severity, alert.severity, incident.event_count)
            incident.description = alert.explanation
            incident.raw_payload = {"correlation_id": alert.correlation_id, "timeline": timeline[-50:]}

        session.flush()
        session.add(IncidentAlertLink(incident_id=incident.incident_id, alert_id=alert.alert_id))
        return incident.incident_id

    @staticmethod
    def _escalate(current: str, incoming: str, count: int) -> str:
        severity = current if SEVERITY_RANK[current] >= SEVERITY_RANK[incoming] else incoming
        if severity == "medium" and count >= 3:
            return "high"
        if severity == "high" and count >= 3:
            return "critical"
        return severity
