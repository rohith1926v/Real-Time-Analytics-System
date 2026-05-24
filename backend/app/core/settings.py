from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_csv_origins(value: str) -> List[str]:
    origins = [origin.strip() for origin in value.split(",")]
    return [origin for origin in origins if origin]


class Settings(BaseSettings):
    project_name: str = "Real-Time Streaming Analytics Platform"
    app_version: str = "0.1.0"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    backend_cors_origins_raw: str = Field(
        default="http://localhost:5173",
        validation_alias="BACKEND_CORS_ORIGINS",
        description="Comma-separated CORS origins loaded from BACKEND_CORS_ORIGINS.",
    )
    log_level: str = "INFO"
    database_url: str = "sqlite+pysqlite:///./analytics.db"
    elasticsearch_host: str = "http://localhost:9200"
    redis_url: str = "redis://localhost:6379/0"
    prometheus_url: str = "http://localhost:9090"
    grafana_url: str = "http://localhost:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("backend_cors_origins_raw", mode="before")
    @classmethod
    def validate_cors_origins_raw(cls, value: str) -> str:
        if not isinstance(value, str):
            raise TypeError("BACKEND_CORS_ORIGINS must be a comma-separated string")

        if not _parse_csv_origins(value):
            raise ValueError("BACKEND_CORS_ORIGINS must define at least one origin")

        return value

    @property
    def cors_origins(self) -> List[str]:
        return _parse_csv_origins(self.backend_cors_origins_raw)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
