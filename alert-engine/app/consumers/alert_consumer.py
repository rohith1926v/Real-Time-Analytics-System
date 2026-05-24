import json
import logging
import signal
from types import FrameType

from confluent_kafka import Consumer
from sqlalchemy.orm import sessionmaker

from app.config.settings import AlertEngineSettings
from app.config.topics import ALERT_INPUT_TOPICS
from app.services.alert_service import AlertProcessingService
from app.utils.retry import retry_with_backoff

logger = logging.getLogger(__name__)


class AlertEngineConsumer:
    def __init__(self, settings: AlertEngineSettings, session_factory: sessionmaker, service: AlertProcessingService) -> None:
        self._settings = settings
        self._session_factory = session_factory
        self._service = service
        self._consumer: Consumer | None = None
        self._running = True

    def run(self) -> None:
        self._register_shutdown_handlers()
        self._consumer = retry_with_backoff(self._create_consumer, logger, "Kafka alert-engine consumer connection")
        logger.info("subscribing_alert_engine topics=%s group=%s", ALERT_INPUT_TOPICS, self._settings.consumer_group)
        self._consumer.subscribe(list(ALERT_INPUT_TOPICS))

        while self._running:
            message = self._consumer.poll(timeout=1.0)
            if message is None:
                continue
            if message.error():
                logger.error("alert_engine_kafka_error error=%s", message.error())
                continue
            self._handle_message(message.topic(), message.value())

        logger.info("closing_alert_engine_consumer")
        self._consumer.close()

    def _create_consumer(self) -> Consumer:
        consumer = Consumer(
            {
                "bootstrap.servers": self._settings.kafka_bootstrap_servers,
                "group.id": self._settings.consumer_group,
                "client.id": "streaming-analytics-alert-engine",
                "auto.offset.reset": "earliest",
                "enable.auto.commit": True,
            }
        )
        metadata = consumer.list_topics(timeout=10)
        logger.info("alert_engine_kafka_connected brokers=%s", len(metadata.brokers))
        return consumer

    def _handle_message(self, topic: str, payload: bytes | None) -> None:
        try:
            if payload is None:
                return
            parsed = json.loads(payload.decode("utf-8"))
            with self._session_factory() as session:
                count = self._service.process(session, topic, parsed)
                session.commit()
            if count:
                logger.info("alerts_persisted count=%s source_topic=%s", count, topic)
        except Exception:
            logger.exception("alert_engine_message_failed topic=%s", topic)

    def _register_shutdown_handlers(self) -> None:
        def shutdown_handler(signum: int, _frame: FrameType | None) -> None:
            logger.info("received_shutdown_signal signal=%s", signum)
            self._running = False

        signal.signal(signal.SIGTERM, shutdown_handler)
        signal.signal(signal.SIGINT, shutdown_handler)

