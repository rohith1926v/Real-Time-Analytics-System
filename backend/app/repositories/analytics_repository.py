from sqlalchemy import desc, func, or_, select
from sqlalchemy.orm import Session

from app.db.models import AnalyticsMetric, AnomalyPrediction, DeadLetterEvent, FeatureSnapshot, RiskMetric, TelemetryEvent


class AnalyticsRepository:
    def summary(self, db: Session) -> dict[str, int]:
        return {
            "telemetry_events": db.scalar(select(func.count()).select_from(TelemetryEvent)) or 0,
            "analytics_metrics": db.scalar(select(func.count()).select_from(AnalyticsMetric)) or 0,
            "risk_metrics": db.scalar(select(func.count()).select_from(RiskMetric)) or 0,
            "feature_snapshots": db.scalar(select(func.count()).select_from(FeatureSnapshot)) or 0,
            "anomaly_predictions": db.scalar(select(func.count()).select_from(AnomalyPrediction)) or 0,
            "deadletter_events": db.scalar(select(func.count()).select_from(DeadLetterEvent)) or 0,
            "high_risk_predictions": db.scalar(
                select(func.count()).select_from(AnomalyPrediction).where(AnomalyPrediction.ml_risk_score >= 70)
            )
            or 0,
        }

    def recent_events(self, db: Session, limit: int = 50) -> list[TelemetryEvent]:
        return list(db.scalars(select(TelemetryEvent).order_by(desc(TelemetryEvent.timestamp), desc(TelemetryEvent.id)).limit(limit)))

    def recent_predictions(self, db: Session, limit: int = 50) -> list[AnomalyPrediction]:
        return list(db.scalars(select(AnomalyPrediction).order_by(desc(AnomalyPrediction.timestamp), desc(AnomalyPrediction.id)).limit(limit)))

    def latest_prediction_for_entity(self, db: Session, entity_id: str) -> AnomalyPrediction | None:
        return db.scalars(
            select(AnomalyPrediction)
            .where(AnomalyPrediction.entity_id == entity_id)
            .order_by(desc(AnomalyPrediction.timestamp), desc(AnomalyPrediction.id))
            .limit(1)
        ).first()

    def high_risks(self, db: Session, limit: int = 50) -> list[AnomalyPrediction]:
        return list(
            db.scalars(
                select(AnomalyPrediction)
                .where(or_(AnomalyPrediction.ml_risk_score >= 70, AnomalyPrediction.severity.in_(["high", "critical"])))
                .order_by(desc(AnomalyPrediction.ml_risk_score), desc(AnomalyPrediction.timestamp))
                .limit(limit)
            )
        )

    def average_ml_risk(self, db: Session) -> float:
        return float(db.scalar(select(func.avg(AnomalyPrediction.ml_risk_score))) or 0.0)

    def anomaly_count(self, db: Session) -> int:
        return db.scalar(select(func.count()).select_from(AnomalyPrediction).where(AnomalyPrediction.raw_payload["is_anomaly"].as_boolean() == True)) or 0

    def severity_distribution(self, db: Session) -> list[tuple[str, int]]:
        rows = db.execute(
            select(AnomalyPrediction.severity, func.count())
            .where(AnomalyPrediction.severity.is_not(None))
            .group_by(AnomalyPrediction.severity)
            .order_by(desc(func.count()))
        ).all()
        return [(row[0], int(row[1])) for row in rows]

    def event_type_distribution(self, db: Session) -> list[tuple[str, int]]:
        rows = db.execute(
            select(TelemetryEvent.event_type, func.count())
            .where(TelemetryEvent.event_type.is_not(None))
            .group_by(TelemetryEvent.event_type)
            .order_by(desc(func.count()))
        ).all()
        return [(row[0], int(row[1])) for row in rows]

    def recent_predictions_for_charts(self, db: Session, limit: int = 200) -> list[AnomalyPrediction]:
        return list(db.scalars(select(AnomalyPrediction).order_by(desc(AnomalyPrediction.timestamp), desc(AnomalyPrediction.id)).limit(limit)))

    def recent_events_for_charts(self, db: Session, limit: int = 500) -> list[TelemetryEvent]:
        return list(db.scalars(select(TelemetryEvent).order_by(desc(TelemetryEvent.timestamp), desc(TelemetryEvent.id)).limit(limit)))

    def top_entities(self, db: Session, limit: int = 10) -> list[tuple[str, float, int, str | None]]:
        rows = db.execute(
            select(
                AnomalyPrediction.entity_id,
                func.max(AnomalyPrediction.ml_risk_score),
                func.count(),
                func.max(AnomalyPrediction.severity),
            )
            .where(AnomalyPrediction.entity_id.is_not(None))
            .group_by(AnomalyPrediction.entity_id)
            .order_by(desc(func.max(AnomalyPrediction.ml_risk_score)))
            .limit(limit)
        ).all()
        return [(str(row[0]), float(row[1] or 0.0), int(row[2]), row[3]) for row in rows]
