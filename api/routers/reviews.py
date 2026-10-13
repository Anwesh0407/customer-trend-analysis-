"""Reviews router for customer feedback and coverage analysis."""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query

from ava.analytics.reviews import compute_reviews_summary
from ava.models import Review
from ava.storage.base import Repository
from api.deps import get_niche_context, get_repo
from api.envelope import EvidenceEnvelope, create_envelope
from api.schemas import ReviewListResponse, ReviewResponse, ReviewSummaryData

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/summary", response_model=EvidenceEnvelope[ReviewSummaryData])
def get_reviews_summary(
    category: Optional[str] = Query(None, description="Category filter"),
    asin: Optional[str] = Query(None, description="Specific ASIN filter"),
    niche_ctx=Depends(get_niche_context),
    repo: Repository = Depends(get_repo),
) -> Dict[str, Any]:
    niche_filter, niche_name = niche_ctx
    niche_prods = repo.get_all_products_for_niche(category=category, niche_filter=niche_filter)
    sample_size = len(niche_prods)
    niche_asins = [p["asin"] for p in niche_prods]

    if asin:
        clean_asin = asin.strip().upper()
        raw_revs, _ = repo.get_reviews(asin=clean_asin, limit=1000)
    else:
        raw_revs, _ = repo.get_reviews(category=category, limit=1000)

    # Convert to Review models
    reviews = []
    for r in raw_revs:
        try:
            reviews.append(
                Review(
                    review_id=r["review_id"],
                    product_id=r["product_id"],
                    rating=int(r["rating"]),
                    review_title=r.get("review_title") or "",
                    review_text=r.get("review_text") or "",
                    review_date=r.get("review_date") or "",
                    source=r.get("source", "synthetic"),
                    collected_at=r.get("collected_at") or "",
                )
            )
        except Exception:
            pass

    summary = compute_reviews_summary(
        reviews,
        niche_asins=niche_asins if not asin else [clean_asin],
    )

    data = ReviewSummaryData(
        total_reviews=summary["total_reviews"],
        average_rating=summary["average_rating"],
        rating_distribution={str(k): v for k, v in summary["rating_distribution"].items()},
        coverage_pct=summary["niche_coverage_pct"],
        sentiment_badge="planned",
        note="Review sentiment analysis is a planned future capability.",
    )

    data_mode = "demo"
    if reviews and all("synthetic" not in r.source.lower() for r in reviews):
        data_mode = "real"

    sources = list({r.source for r in reviews}) or ["synthetic_review"]

    return create_envelope(
        data=data.model_dump(),
        niche=niche_name,
        sample_size=sample_size,
        data_mode=data_mode,
        sources=sources,
    )


@router.get("", response_model=EvidenceEnvelope[ReviewListResponse])
def list_reviews(
    asin: Optional[str] = Query(None, description="Optional product ASIN"),
    category: Optional[str] = Query(None, description="Category filter"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    niche_ctx=Depends(get_niche_context),
    repo: Repository = Depends(get_repo),
) -> Dict[str, Any]:
    niche_filter, niche_name = niche_ctx
    clean_asin = asin.strip().upper() if asin else None

    # Fetch reviews
    raw_revs, total = repo.get_reviews(
        asin=clean_asin,
        category=category,
        limit=limit,
        offset=offset,
    )

    # Filter to niche products if scoped to niche
    if niche_filter and not clean_asin:
        niche_prods = repo.get_all_products_for_niche(category=category, niche_filter=niche_filter)
        niche_asins = {p["asin"] for p in niche_prods}
        raw_revs = [r for r in raw_revs if r.get("product_id") in niche_asins]
        total = len(raw_revs)

    items = [ReviewResponse(**r) for r in raw_revs]
    data = ReviewListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )

    data_mode = "demo"
    if items and all("synthetic" not in r.source.lower() for r in items):
        data_mode = "real"

    sources = list({r.source for r in items}) or ["synthetic_review"]

    return create_envelope(
        data=data.model_dump(),
        niche=niche_name,
        sample_size=total,
        data_mode=data_mode,
        sources=sources,
    )
