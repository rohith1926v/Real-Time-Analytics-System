import argparse
import logging

from app.config.settings import get_settings
from app.consumers.telemetry_consumer import TelemetryConsumer
from app.producers.telemetry_producer import TelemetryProducer
from app.utils.logging import configure_logging
from app.utils.metrics import start_metrics_server


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Kafka telemetry runtime")
    parser.add_argument("mode", choices=["producer", "consumer"], help="Runtime mode to execute")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = get_settings()
    log_level = settings.producer_log_level if args.mode == "producer" else settings.consumer_log_level
    configure_logging(log_level)

    logger = logging.getLogger(__name__)
    start_metrics_server(settings.producer_metrics_port if args.mode == "producer" else settings.consumer_metrics_port)
    logger.info("Starting Kafka telemetry runtime mode=%s", args.mode)

    if args.mode == "producer":
        TelemetryProducer(settings).run()
        return

    TelemetryConsumer(settings).run()


if __name__ == "__main__":
    main()
