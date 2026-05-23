from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SparkStreamingSettings(BaseSettings):
    app_name: str = Field(default="StreamingAnalyticsStructuredStreaming")
    kafka_bootstrap_servers: str = Field(default="streaming-analytics-kafka:29092", validation_alias="SPARK_KAFKA_BOOTSTRAP_SERVERS")
    checkpoint_root: str = Field(default="/opt/spark/checkpoints", validation_alias="SPARK_CHECKPOINT_ROOT")
    starting_offsets: str = Field(default="latest", validation_alias="SPARK_STARTING_OFFSETS")
    max_offsets_per_trigger: int = Field(default=5000, ge=1, validation_alias="SPARK_MAX_OFFSETS_PER_TRIGGER")
    trigger_processing_time: str = Field(default="15 seconds", validation_alias="SPARK_TRIGGER_PROCESSING_TIME")
    watermark_delay: str = Field(default="2 minutes", validation_alias="SPARK_WATERMARK_DELAY")
    spark_log_level: str = Field(default="WARN", validation_alias="SPARK_LOG_LEVEL")

    enriched_events_topic: str = Field(default="analytics.enriched.events")
    window_metrics_topic: str = Field(default="analytics.window.metrics")
    risk_metrics_topic: str = Field(default="analytics.risk.metrics")
    feature_engineering_topic: str = Field(default="analytics.feature.engineering")

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
            raise ValueError("SPARK_KAFKA_BOOTSTRAP_SERVERS must define at least one broker")
        return ",".join(servers)


@lru_cache
def get_settings() -> SparkStreamingSettings:
    return SparkStreamingSettings()
