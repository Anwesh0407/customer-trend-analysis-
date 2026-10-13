from fastapi import APIRouter
from backend.app.core.config import settings
from backend.app.database.connection import is_postgres_active

router = APIRouter()

@router.get("/health", tags=["Health"])
def get_health():
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "mode": "postgresql" if is_postgres_active else "sample_data_fallback",
        "database_connected": is_postgres_active,
        "gemini_configured": bool(settings.GEMINI_API_KEY)
    }
