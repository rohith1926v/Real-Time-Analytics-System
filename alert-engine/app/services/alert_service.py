import logging

from sqlalchemy.orm import Session

from app.dedup.redis_deduplicator import AlertDeduplicator
from app.elastic.indexer import AlertIndexer
from app.incidents.correlator import IncidentCorrelator
from app.repositories.alert_repository import AlertRepository
from app.rules.rule_engine import AlertRulesEngine

logger = logging.getLogger(__name__)


class AlertProcessingService:
    def __init__(
        self,
        rules: AlertRulesEngine,
        deduplicator: AlertDeduplicator,
        correlator: IncidentCorrelator,
        repository: AlertRepository,
        indexer: AlertIndexer,
    ) -> None:
        self._rules = rules
        self._deduplicator = deduplicator
        self._correlator = correlator
        self._repository = repository
        self._indexer = indexer

    def process(self, session: Session, source_topic: str, payload: dict) -> int:
        emitted = 0
        for alert in self._rules.evaluate(source_topic, payload):
            self._repository.update_dedup_cache(session, alert)
            if not self._deduplicator.should_emit(alert):
                continue
            incident_id = self._correlator.correlate(session, alert)
            alert.incident_id = incident_id
            self._repository.persist_alert(session, alert)
            self._deduplicator.update_live_caches(alert)
            self._indexer.index_alert(alert)
            emitted += 1
            logger.info(
                "alert_generated alert_id=%s severity=%s entity_id=%s incident_id=%s",
                alert.alert_id,
                alert.severity,
                alert.entity_id,
                incident_id,
            )
        return emitted

