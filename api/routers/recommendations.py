"""Recommendations router for transparent, rule-based vendor guidance."""
from __future__ import annotations

import pandas as pd
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, Query

from ava.config import get_settings
from ava.recommendations.rules import generate_recommendations
from ava.storage.base import Repository
from api.deps import get_niche_context, get_repo
from api.envelope import EvidenceEnvelope, create_envelope
from api.schemas import RecommendationCard, RecommendationListData

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.get("", response_model=EvidenceEnvelope[RecommendationListData])
def get_recommendations_list(
    category: Optional[str] = Query(None, description="Category filter"),
    niche_ctx=Depends(get_niche_context),
    repo: Repository = Depends(get_repo),
) -> Dict[str, Any]:
    niche_filter, niche_name = niche_ctx
    prods = repo.get_all_products_for_niche(category=category, niche_filter=niche_filter)
    sample_size = len(prods)
    min_thresh = get_settings().MIN_SAMPLE_SIZE

    if sample_size < min_thresh:
        data = RecommendationListData(
            cards=[],
            suppressed=True,
            reason=f"Recommendations are suppressed because sample size (n={sample_size}) is below minimum threshold ({min_thresh}). Collect or select more listings.",
        )
    else:
        df = pd.DataFrame(prods)
        raw_cards = generate_recommendations(df, niche=None)
        cards = []
        for c in raw_cards:
            thresholds_dict = {}
            if isinstance(c.get("threshold_values"), dict):
                thresholds_dict = c["threshold_values"]
            else:
                thresholds_dict = {"rule_threshold": str(c.get("threshold_values", ""))}

            cards.append(
                RecommendationCard(
                    rule_name=c.get("rule_name", "RuleEngine"),
                    type=c.get("id", "opportunity"),
                    thresholds=thresholds_dict,
                    evidence=c.get("computed_evidence", ""),
                    sample_size=c.get("sample_size", sample_size),
                    confidence=c.get("confidence", "low"),
                    limitations=c.get("limitations", ""),
                    why_this=c.get("why_this", ""),
                    suggested_action=c.get("recommended_action", "Worth investigating."),
                )
            )
        data = RecommendationListData(cards=cards, suppressed=False)

    data_mode = "demo"
    if prods and all("synthetic" not in (p.get("source") or "").lower() for p in prods):
        data_mode = "real"

    sources = list({p.get("source", "unknown") for p in prods})

    return create_envelope(
        data=data.model_dump(),
        niche=niche_name,
        sample_size=sample_size,
        data_mode=data_mode,
        sources=sources,
    )
