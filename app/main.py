import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.v1.endpoints import health
from app.api.v1.router import api_router
from app.core.config import get_settings
from app.core.exceptions import LLMProviderError, LLMTimeoutError
from app.core.logging import configure_logging
from app.services.llm import get_llm_provider

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    configure_logging(settings.log_level, secrets=[settings.gemini_api_key])
    if not settings.is_test:
        get_llm_provider(settings)
    logger.info("Starting %s env=%s", settings.app_name, settings.app_env)
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(
        title="Interview Copilot API",
        version="0.1.0",
        lifespan=lifespan,
    )

    application.include_router(health.router)
    application.include_router(api_router, prefix="/api/v1")

    @application.get("/")
    def root() -> dict[str, str]:
        return {
            "service": "interview-copilot-api",
            "health": "/health",
            "docs": "/docs",
            "interview_answer": "/api/v1/interview/answer",
        }

    @application.exception_handler(LLMTimeoutError)
    async def llm_timeout_handler(_request: Request, exc: LLMTimeoutError) -> JSONResponse:
        logger.warning("LLM timeout: %s", exc)
        return JSONResponse(status_code=502, content={"detail": str(exc)})

    @application.exception_handler(LLMProviderError)
    async def llm_provider_handler(_request: Request, exc: LLMProviderError) -> JSONResponse:
        logger.warning("LLM provider error: %s", exc)
        return JSONResponse(status_code=502, content={"detail": str(exc)})

    @application.exception_handler(Exception)
    async def unhandled_error_handler(_request: Request, exc: Exception) -> JSONResponse:
        logger.exception("Unhandled error", exc_info=exc)
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred."},
        )

    application.state.settings = settings
    return application


app = create_app()
