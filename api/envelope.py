"""Evidence envelope for all analytic and intelligence responses.

Enforces transparency by requiring every analytic output to declare:
- Niche context
- Sample size (n)
- Snapshot timestamp (as_of)
- Data mode (demo | real | mixed)
- Underlying sources
- Standing limitations
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")

DEFAULT_LIMITATIONS: List[str] = [
    "Market metrics reflect a point-in-time public catalog snapshot.",
    "Non-random sample of active listings; variants are counted as separate rows.",
    "Review ratings reflect self-selected customer sentiment, not verified purchase rates.",
    "Review counts represent cumulative customer attention, not current unit sales or revenue.",
]


class EvidenceMeta(BaseModel):
    niche: str = Field(default="All Listings (Whole Category)")
    sample_size: int = Field(default=0, description="Total listings observed in this sample (n)")
    as_of: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    data_mode: str = Field(default="demo", description="demo | real | mixed")
    sources: List[str] = Field(default_factory=lambda: ["synthetic_curated"])
    limitations: List[str] = Field(default_factory=lambda: list(DEFAULT_LIMITATIONS))


class EvidenceEnvelope(BaseModel, Generic[T]):
    data: T
    meta: EvidenceMeta


def create_envelope(
    data: Any,
    niche: str = "All Listings (Whole Category)",
    sample_size: int = 0,
    data_mode: str = "demo",
    sources: Optional[List[str]] = None,
    limitations: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Utility to build standard evidence envelope dict."""
    return {
        "data": data,
        "meta": {
            "niche": niche,
            "sample_size": sample_size,
            "as_of": datetime.now(timezone.utc).isoformat(),
            "data_mode": data_mode,
            "sources": sources or ["synthetic_curated"],
            "limitations": limitations or DEFAULT_LIMITATIONS,
        },
    }
