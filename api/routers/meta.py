"""Meta and health check router."""
from __future__ import annotations

from datetime import datetime, timezone
from fastapi import APIRouter, Depends

from ava.config import get_settings
from ava.storage.base import Repository
from api.deps import get_repo
from api.envelope import DEFAULT_LIMITATIONS
from api.schemas import HealthResponse, MetaResponse

router = APIRouter(tags=["Meta"])


@router.get("/health", response_model=HealthResponse)
def get_health(repo: Repository = Depends(get_repo)) -> HealthResponse:
    # Verify DB connectivity
    db_status = "connected"
    try:
        repo.get_categories()
    except Exception:
        db_status = "error"

    return HealthResponse(
        status="ok" if db_status == "connected" else "degraded",
        version=get_settings().APP_VERSION,
        database=db_status,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@router.get("/meta", response_model=MetaResponse)
def get_metadata(repo: Repository = Depends(get_repo)) -> MetaResponse:
    settings = get_settings()
    prods, total_p = repo.get_products(limit=1)
    revs, total_r = repo.get_reviews(limit=1)

    data_mode = "demo"
    if total_p > 0:
        all_p = repo.get_all_products_for_niche()
        if any("synthetic" in (p.get("source") or "").lower() for p in all_p):
            data_mode = "demo"
        else:
            data_mode = "real"

    return MetaResponse(
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        data_mode=data_mode,
        total_products=total_p,
        total_reviews=total_r,
        active_category="Women's Kurtas & Kurtis",
        limitations=DEFAULT_LIMITATIONS,
    )
