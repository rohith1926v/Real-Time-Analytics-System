from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.logging import configure_logging
from app.core.settings import settings


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

    application.include_router(api_router, prefix=settings.api_v1_prefix)
    return application


app = create_application()
