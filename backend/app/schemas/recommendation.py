from pydantic import BaseModel
from typing import List, Optional

class SourcingSpec(BaseModel):
    fabric: str
    test_range: str
    colors: str
    priority_sizes: str

class RecommendationItem(BaseModel):
    id: str
    title: str
    badge: str
    confidence_pct: int
    what_observed: str
    why_it_matters: str
    evidence_sample_size: str
    what_to_do: str
    limitations: str
    sourcing_specs: Optional[SourcingSpec] = None
    estimated_margin: Optional[str] = None

class RecommendationResponse(BaseModel):
    total_recommendations: int
    items: List[RecommendationItem]
