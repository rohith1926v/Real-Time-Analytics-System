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

