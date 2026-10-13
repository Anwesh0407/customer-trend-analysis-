"""Consistent error formatting and exception handlers."""
from __future__ import annotations

from datetime import datetime, timezone
import logging
from typing import Any, Dict, Optional
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from ava.exceptions import AVABaseException, SourceUnavailable

logger = logging.getLogger("ava.api.errors")


def create_error_response(
    detail: str,
    code: str = "ERROR",
    status_code: int = 400,
    extra: Optional[Dict[str, Any]] = None,
) -> JSONResponse:
    content = {
        "error": {
            "code": code,
            "message": detail,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    }
    if extra:
        content["error"]["details"] = extra
    return JSONResponse(status_code=status_code, content=content)


async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    return create_error_response(
        detail=str(exc.detail),
        code=f"HTTP_{exc.status_code}",
        status_code=exc.status_code,
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()
    clean_errors = []
    for err in errors:
        clean_errors.append({
            "loc": err.get("loc"),
            "msg": err.get("msg"),
            "type": err.get("type"),
        })
    return create_error_response(
        detail="Validation error in request payload or query parameters.",
        code="VALIDATION_ERROR",
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        extra={"validation_errors": clean_errors},
    )


async def ava_exception_handler(request: Request, exc: AVABaseException) -> JSONResponse:
    status_code = status.HTTP_400_BAD_REQUEST
    if isinstance(exc, SourceUnavailable):
        status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    return create_error_response(
        detail=str(exc),
        code=exc.__class__.__name__,
        status_code=status_code,
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled server exception: %s", exc)
    return create_error_response(
        detail="An internal server error occurred. Please verify backend logs.",
        code="INTERNAL_SERVER_ERROR",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )
