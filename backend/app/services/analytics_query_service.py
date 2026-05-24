from elasticsearch import Elasticsearch
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.repositories.analytics_repository import AnalyticsRepository


class AnalyticsQueryService:
    def __init__(self, repository: AnalyticsRepository | None = None) -> None:
        self._repository = repository or AnalyticsRepository()

    def summary(self, db: Session) -> dict[str, int]:
        return self._repository.summary(db)

    def recent_events(self, db: Session, limit: int) -> list:
        return self._repository.recent_events(db, limit)

    def recent_predictions(self, db: Session, limit: int) -> list:
        return self._repository.recent_predictions(db, limit)

    def latest_prediction(self, db: Session, entity_id: str):
        return self._repository.latest_prediction_for_entity(db, entity_id)

    def high_risks(self, db: Session, limit: int) -> list:
        return self._repository.high_risks(db, limit)

    def search_events(self, query: str, limit: int = 25) -> list[dict]:
        try:
            client = Elasticsearch(settings.elasticsearch_host, request_timeout=2)
            if not client.ping():
                return []
            response = client.search(
                index="telemetry-events,analytics-events,ml-predictions",
                size=limit,
                query={"query_string": {"query": query, "default_field": "*"}},
                sort=[{"timestamp": {"order": "desc", "unmapped_type": "date"}}],
            )
            return [hit["_source"] for hit in response["hits"]["hits"]]
        except Exception:
            return []

