from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.db.session import get_db
from app.schemas.monitoring import ErrorSummary, MetricsSummary, MonitoringOverview, PipelineMetrics, ServiceHealth
from app.services.monitoring_service import MonitoringService

router = APIRouter()
service = MonitoringService(settings)


@router.get("/monitoring/overview", response_model=MonitoringOverview)
def monitoring_overview(db: Annotated[Session, Depends(get_db)]) -> MonitoringOverview:
    return service.overview(db)


@router.get("/monitoring/services", response_model=list[ServiceHealth])
def monitoring_services(db: Annotated[Session, Depends(get_db)]) -> list[ServiceHealth]:
    return service.services(db)


@router.get("/monitoring/pipeline", response_model=PipelineMetrics)
def monitoring_pipeline(db: Annotated[Session, Depends(get_db)]) -> PipelineMetrics:
    return service.pipeline(db)


@router.get("/monitoring/errors", response_model=ErrorSummary)
def monitoring_errors(db: Annotated[Session, Depends(get_db)]) -> ErrorSummary:
    return service.errors(db)


@router.get("/monitoring/metrics-summary", response_model=MetricsSummary)
def monitoring_metrics_summary() -> MetricsSummary:
    return service.metrics_summary()
