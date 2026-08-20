"""Main FastAPI application entrypoint for Bhoomi API (SIH25076)."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import api_v1_router
from app.core.config import get_settings
from app.core.errors import register_error_handlers

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("bhoomi.api")

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan context manager for startup and shutdown events."""
    logger.info("Starting Bhoomi Advisory API...")
    logger.info(f"Feature Flag - LAND_API_MODE: {settings.LAND_API_MODE}")
    logger.info(f"Feature Flag - DIAGNOSIS_MODEL: {settings.DIAGNOSIS_MODEL}")
    logger.info(f"Confidence Gate Threshold: {settings.CONFIDENCE_GATE}")
    logger.info(f"RAG Relevance Cutoff: {settings.RAG_RELEVANCE_THRESHOLD}")
    yield
    logger.info("Shutting down Bhoomi Advisory API...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "Bhoomi — AI-Powered Farmer Companion (SIH25076).\n\n"
        "A voice-first, multimodal advisory backend treating every farm as a continuous living case file.\n"
        "Enforces the hard rules: Never answer below confidence gate; Never fabricate on no-retrieval."
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Open in development for Flutter mobile + Vite portals
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Custom Error Envelope Handlers
register_error_handlers(app)

# Mount API v1 Routers
app.include_router(api_v1_router, prefix=settings.API_V1_STR)


@app.get(
    "/",
    tags=["Root & Health"],
    summary="Root API greeting and metadata",
)
async def root() -> dict[str, str]:
    return {
        "app": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs",
        "contract": "SIH25076",
        "motto": "Every number inspectable; escalate, don't guess.",
    }


@app.get(
    "/health",
    tags=["Root & Health"],
    status_code=status.HTTP_200_OK,
    summary="Health check probe",
)
async def health_check() -> dict[str, str]:
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
        "database": "fallback_in_memory_or_postgres",
    }
