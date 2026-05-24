from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.logging import configure_logging
from app.core.metrics import PrometheusMetricsMiddleware, metrics_response
from app.core.settings import settings
from app.db.session import initialize_database


def create_application() -> FastAPI:
    configure_logging(settings.log_level)

    application = FastAPI(
        title=settings.project_name,
        version=settings.app_version,
        description="Foundation API for the Real-Time Streaming Analytics Platform.",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(PrometheusMetricsMiddleware)

    application.add_api_route("/metrics", metrics_response, methods=["GET"], include_in_schema=False)

    application.include_router(api_router, prefix=settings.api_v1_prefix)

    @application.on_event("startup")
    def initialize_local_database() -> None:
        initialize_database()

    return application


app = create_application()
