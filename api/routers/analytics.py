"""Analytics router for market summary and opportunity preliminary insights."""
from __future__ import annotations

import pandas as pd
from typing import Any, Dict, Optional
from fastapi import APIRouter, Depends, Query

from ava.analytics.market import compute_market_analytics
from ava.analytics.opportunities import generate_preliminary_insights
from ava.storage.base import Repository
from api.deps import get_niche_context, get_repo
from api.envelope import EvidenceEnvelope, create_envelope
from api.schemas import MarketSummaryData, OpportunitiesData

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary", response_model=EvidenceEnvelope[MarketSummaryData])
def get_analytics_summary(
    category: Optional[str] = Query(None, description="Category filter"),
    niche_ctx=Depends(get_niche_context),
    repo: Repository = Depends(get_repo),
) -> Dict[str, Any]:
    niche_filter, niche_name = niche_ctx
    prods = repo.get_all_products_for_niche(category=category, niche_filter=niche_filter)
    sample_size = len(prods)

    df = pd.DataFrame(prods) if prods else pd.DataFrame(columns=["asin", "price", "rating", "brand", "discount_pct", "sizes", "review_count"])
    market_summary = compute_market_analytics(df, niche=None)

    data_mode = "demo"
    if prods and all("synthetic" not in (p.get("source") or "").lower() for p in prods):
        data_mode = "real"

    sources = list({p.get("source", "unknown") for p in prods})

    return create_envelope(
        data=market_summary,
        niche=niche_name,
        sample_size=sample_size,
        data_mode=data_mode,
        sources=sources,
    )


@router.get("/opportunities", response_model=EvidenceEnvelope[OpportunitiesData])
def get_analytics_opportunities(
    category: Optional[str] = Query(None, description="Category filter"),
    niche_ctx=Depends(get_niche_context),
    repo: Repository = Depends(get_repo),
) -> Dict[str, Any]:
    niche_filter, niche_name = niche_ctx
    prods = repo.get_all_products_for_niche(category=category, niche_filter=niche_filter)
    sample_size = len(prods)

    df = pd.DataFrame(prods) if prods else pd.DataFrame(columns=["asin", "price", "rating", "brand", "discount_pct", "sizes", "review_count", "material", "pattern", "colour"])
    opps = generate_preliminary_insights(df, niche=None)

    data_mode = "demo"
    if prods and all("synthetic" not in (p.get("source") or "").lower() for p in prods):
        data_mode = "real"

    sources = list({p.get("source", "unknown") for p in prods})

    return create_envelope(
        data=opps,
        niche=niche_name,
        sample_size=sample_size,
        data_mode=data_mode,
        sources=sources,
    )
