from functools import lru_cache
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class KafkaRuntimeSettings(BaseSettings):
    kafka_bootstrap_servers: str = Field(default="localhost:9092")
    kafka_consumer_group: str = Field(default="streaming-analytics-telemetry-consumers")
    event_rate_per_second: float = Field(default=5.0, ge=0.1, le=500.0)
    anomaly_rate: float = Field(default=0.05, ge=0.0, le=1.0)
    producer_log_level: str = Field(default="INFO")
    consumer_log_level: str = Field(default="INFO")
    producer_client_id: str = Field(default="streaming-analytics-producer")
    consumer_client_id: str = Field(default="streaming-analytics-consumer")
    deadletter_topic: str = Field(default="telemetry.deadletter.events")
    runtime_mode: Literal["producer", "consumer"] | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("kafka_bootstrap_servers")
    @classmethod
    def validate_bootstrap_servers(cls, value: str) -> str:
        servers = [server.strip() for server in value.split(",") if server.strip()]
        if not servers:
            raise ValueError("KAFKA_BOOTSTRAP_SERVERS must define at least one Kafka broker")
        return ",".join(servers)


@lru_cache
def get_settings() -> KafkaRuntimeSettings:
    return KafkaRuntimeSettings()
