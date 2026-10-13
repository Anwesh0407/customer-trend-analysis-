"""FastAPI main application entrypoint."""
from __future__ import annotations

import json
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from ava.config import get_settings
from ava.exceptions import AVABaseException
from ava.logging_setup import configure_logging
from api.deps import get_repo
from api.errors import (
    ava_exception_handler,
    generic_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from api.routers import (
    analytics,
    assistant,
    categories,
    meta,
    niches,
    products,
    recommendations,
    reviews,
)

configure_logging()
logger = logging.getLogger("ava.api")
settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AVA (Amazon Vendor Assist) API - Marketplace Intelligence for Local Vendors in Eastern India",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# CORS configuration
allowed_origins = [settings.FRONTEND_URL, "http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(AVABaseException, ava_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Mount API v1 Routers
API_V1_PREFIX = "/api/v1"
app.include_router(meta.router, prefix=API_V1_PREFIX)
app.include_router(categories.router, prefix=API_V1_PREFIX)
app.include_router(niches.router, prefix=API_V1_PREFIX)
app.include_router(products.router, prefix=API_V1_PREFIX)
app.include_router(analytics.router, prefix=API_V1_PREFIX)
app.include_router(reviews.router, prefix=API_V1_PREFIX)
app.include_router(recommendations.router, prefix=API_V1_PREFIX)
app.include_router(assistant.router, prefix=API_V1_PREFIX)

# Backward-compatibility alias (/api)
app.include_router(meta.router, prefix="/api")
app.include_router(categories.router, prefix="/api")
app.include_router(niches.router, prefix="/api")
app.include_router(products.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")
app.include_router(reviews.router, prefix="/api")
app.include_router(recommendations.router, prefix="/api")
app.include_router(assistant.router, prefix="/api")


@app.get("/health")
def root_health():
    return {"status": "ok", "app": "AVA", "version": "0.2.0"}


@app.get("/")
def root_index():
    return {"status": "ok", "app": "Amazon Vendor Assist (AVA)", "docs": "/docs"}


@app.on_event("startup")
def on_startup() -> None:
    logger.info("Initializing AVA database on startup...")
    repo = get_repo()
    repo.init_db()

    # Export OpenAPI specification to docs/openapi.json (Checklist P-07)
    try:
        openapi_schema = app.openapi()
        docs_path = Path("docs")
        docs_path.mkdir(parents=True, exist_ok=True)
        schema_file = docs_path / "openapi.json"
        with open(schema_file, "w", encoding="utf-8") as f:
            json.dump(openapi_schema, f, indent=2)
        logger.info("Exported OpenAPI contract to %s", schema_file)
    except Exception as e:
        logger.warning("Could not export OpenAPI contract on startup: %s", e)
