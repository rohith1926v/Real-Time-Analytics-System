import json
import logging
import signal
from types import FrameType

from confluent_kafka import Consumer
from sqlalchemy.orm import sessionmaker

from app.config.settings import StorageSinkSettings
from app.config.topics import STORAGE_INPUT_TOPICS, TELEMETRY_DEADLETTER_EVENTS
from app.elastic.indexer import ElasticsearchIndexer
from app.redis_cache.cache import RedisCache
from app.repositories.postgres_repository import PostgresStorageRepository
from app.services.record_mapper import map_payload_to_record
from app.utils.retry import retry_with_backoff
from app.utils.metrics import POSTGRES_WRITE_ERRORS_TOTAL, RECORDS_PERSISTED_TOTAL

logger = logging.getLogger(__name__)


class StorageSinkConsumer:
    def __init__(
        self,
        settings: StorageSinkSettings,
        session_factory: sessionmaker,
        repository: PostgresStorageRepository,
        indexer: ElasticsearchIndexer,
        cache: RedisCache,
    ) -> None:
        self._settings = settings
        self._session_factory = session_factory
        self._repository = repository
        self._indexer = indexer
        self._cache = cache
        self._consumer: Consumer | None = None
        self._running = True

    def run(self) -> None:
        self._register_shutdown_handlers()
        self._consumer = retry_with_backoff(self._create_consumer, logger, "Kafka storage sink consumer connection")
        logger.info("subscribing_storage_sink topics=%s group=%s", STORAGE_INPUT_TOPICS, self._settings.kafka_consumer_group)
        self._consumer.subscribe(list(STORAGE_INPUT_TOPICS))

        while self._running:
            message = self._consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                logger.error("kafka_storage_sink_error error=%s", message.error())
                continue
            self._handle_message(message.topic(), message.value())

        logger.info("closing_storage_sink_consumer")
        self._consumer.close()

    def _create_consumer(self) -> Consumer:
        consumer = Consumer(
            {
                "bootstrap.servers": self._settings.kafka_bootstrap_servers,
                "group.id": self._settings.kafka_consumer_group,
                "client.id": self._settings.consumer_client_id,
                "auto.offset.reset": "earliest",
                "enable.auto.commit": True,
            }
        )
        metadata = consumer.list_topics(timeout=10)
        logger.info("kafka_connected brokers=%s", len(metadata.brokers))
        return consumer

    def _handle_message(self, topic: str, payload: bytes | None) -> None:
        try:
            if payload is None:
                raise ValueError("Kafka message payload is empty")
            parsed = json.loads(payload.decode("utf-8"))
            record = map_payload_to_record(topic, parsed)
        except Exception as exc:
            logger.warning("storage_sink_malformed topic=%s reason=%s", topic, exc)
            record = map_payload_to_record(
                TELEMETRY_DEADLETTER_EVENTS,
                {"source_topic": topic, "reason": str(exc), "payload": payload.decode("utf-8", errors="replace") if payload else None},
            )

        try:
            with self._session_factory() as session:
                self._repository.persist(session, record)
                session.commit()
            RECORDS_PERSISTED_TOTAL.labels(record.record_kind).inc()
        except Exception:
            POSTGRES_WRITE_ERRORS_TOTAL.inc()
            raise

        self._indexer.index(record)
        self._cache.update(record)
        logger.info(
            "record_persisted kind=%s topic=%s entity_id=%s event_type=%s",
            record.record_kind,
            topic,
            record.entity_id,
            record.event_type,
        )

    def _register_shutdown_handlers(self) -> None:
        def shutdown_handler(signum: int, _frame: FrameType | None) -> None:
            logger.info("received_shutdown_signal signal=%s", signum)
            self._running = False

        signal.signal(signal.SIGTERM, shutdown_handler)
        signal.signal(signal.SIGINT, shutdown_handler)
