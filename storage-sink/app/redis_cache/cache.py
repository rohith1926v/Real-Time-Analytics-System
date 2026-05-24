import json
import logging

import redis

from app.config.settings import StorageSinkSettings
from app.schemas.records import StorageRecord
from app.utils.metrics import REDIS_CACHE_ERRORS_TOTAL

logger = logging.getLogger(__name__)


class RedisCache:
    def __init__(self, settings: StorageSinkSettings) -> None:
        self._client = redis.Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True, socket_connect_timeout=3)
        self._available = False

    def initialize(self) -> None:
        try:
            self._client.ping()
            self._available = True
            logger.info("redis_connected")
        except Exception as exc:
            self._available = False
            logger.warning("redis_unavailable action=continue_without_cache reason=%s", exc)

    def update(self, record: StorageRecord) -> None:
        if not self._available:
            return
        try:
            if record.event_type:
                self._client.incr(f"counters:events:{record.event_type}")
            if record.severity:
                self._client.incr(f"counters:severity:{record.severity}")
            if record.record_kind == "prediction" and record.entity_id:
                self._client.set(f"latest:prediction:{record.entity_id}", json.dumps(record.raw_payload, default=str), ex=86400)
            if (record.ml_risk_score or record.risk_score or 0) >= 70:
                key = f"recent:high-risk:{record.entity_id or record.event_id or record.prediction_id or 'unknown'}"
                self._client.set(key, json.dumps(record.raw_payload, default=str), ex=3600)
        except Exception as exc:
            REDIS_CACHE_ERRORS_TOTAL.inc()
            logger.warning("redis_cache_update_failed action=continue reason=%s", exc)
