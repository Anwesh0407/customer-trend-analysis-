"""Pydantic schemas for the AVA OpenAPI contract."""
from __future__ import annotations

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

# -----------------
# 1. Meta & Health
# -----------------
class HealthResponse(BaseModel):
    status: str = Field(default="ok")
    version: str = Field(default="0.2.0")
    database: str = Field(default="connected")
    timestamp: str


class MetaResponse(BaseModel):
    app_name: str
    version: str
    environment: str
    data_mode: str
    total_products: int
    total_reviews: int
    active_category: str
    limitations: List[str]


# -----------------
# 2. Categories
# -----------------
class CategoryResponse(BaseModel):
    id: str
    name: str
    display_name: str
    description: Optional[str] = None
    is_active: bool = True
    product_count: int = 0
    last_updated: Optional[str] = None
    data_mode: str = "demo"


# -----------------
# 3. Niches
# -----------------
class NicheCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Human readable niche name")
    category: str = Field(default="Women's Kurtas & Kurtis")
    filters: Dict[str, Any] = Field(default_factory=dict, description="Filter rules dictionary")
    description: Optional[str] = None


class NicheUpdate(BaseModel):
    name: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None
    description: Optional[str] = None


class NicheResponse(BaseModel):
    id: str
    name: str
    category: str
    filters: Dict[str, Any]
    description: Optional[str] = None
    sample_size: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


class NichePreviewRequest(BaseModel):
    category: Optional[str] = "Women's Kurtas & Kurtis"
    filters: Dict[str, Any] = Field(default_factory=dict)


class NichePreviewResponse(BaseModel):
    sample_size: int
    below_threshold: bool
    threshold: int = 30
    warning: Optional[str] = None


# -----------------
# 4. Products
# -----------------
class ProductResponse(BaseModel):
    asin: str
    product_name: str
    category: str
    brand: Optional[str] = None
    price: Optional[float] = None
    mrp: Optional[float] = None
    discount_pct: Optional[float] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    colour: Optional[str] = None
    material: Optional[str] = None
    pattern: Optional[str] = None
    sizes: List[str] = Field(default_factory=list)
    seller: Optional[str] = None
    availability: str = "in_stock"
    product_url: Optional[str] = None
    source: str = "synthetic"
    collected_at: Optional[str] = None
    updated_at: Optional[str] = None
    # Derived niche positioning
    percentile_in_niche: Optional[Dict[str, Any]] = None
    quality_flags: List[str] = Field(default_factory=list)


class ProductListResponse(BaseModel):
    items: List[ProductResponse]
    total: int
    limit: int
    offset: int


class SimilarProductItem(BaseModel):
    asin: str
    product_name: str
    brand: Optional[str] = None
    price: Optional[float] = None
    mrp: Optional[float] = None
    discount_pct: Optional[float] = None
    rating: Optional[float] = None
    review_count: Optional[int] = None
    colour: Optional[str] = None
    material: Optional[str] = None
    similarity_reason: str


class SimilarProductsResponse(BaseModel):
    asin: str
    similar_items: List[SimilarProductItem]


# -----------------
# 5. Analytics
# -----------------
class PriceMetrics(BaseModel):
    min: float
    q1: float
    median: float
    q3: float
    max: float
    n: int


class PriceBandItem(BaseModel):
    band_name: str
    min_price: float
    max_price: float
    product_count: int
    avg_rating: float
    share_pct: float


class RatingMetrics(BaseModel):
    median: float
    mean: float
    n: int


class BrandMetrics(BaseModel):
    total_brands: int
    top_5_share_pct: float
    top_brands: Dict[str, int]
    n: int


class AttributeCounts(BaseModel):
    colours: Dict[str, int]
    materials: Dict[str, int]
    patterns: Dict[str, int]
    sizes: Dict[str, int]


class AttentionConcentration(BaseModel):
    top_10_pct_review_share: float
    note: str = "Attention concentration proxy only. Review counts are not sales counts."


class MarketSummaryData(BaseModel):
    sample_size: int
    price_metrics: PriceMetrics
    price_bands: List[PriceBandItem]
    rating_metrics: RatingMetrics
    discount_bands: Dict[str, int]
    brand_metrics: BrandMetrics
    attribute_counts: AttributeCounts
    completeness: Dict[str, float]
    attention_concentration: AttentionConcentration


class OpportunityItem(BaseModel):
    id: str
    title: str
    type: str
    observation: str
    hypothesis: str
    evidence: str
    sample_size: int
    confidence: str
    limitations: str
    why_this: Optional[str] = None


class OpportunitiesData(BaseModel):
    insights_suppressed: bool
    reason: Optional[str] = None
    sample_size: int
    insights: List[OpportunityItem]
    standing_limitations: List[str]


# -----------------
# 6. Reviews
# -----------------
class ReviewResponse(BaseModel):
    review_id: str
    product_id: str
    rating: int
    review_title: Optional[str] = None
    review_text: Optional[str] = None
    review_date: Optional[str] = None
    source: str = "synthetic"
    collected_at: Optional[str] = None


class ReviewSummaryData(BaseModel):
    total_reviews: int
    average_rating: float
    rating_distribution: Dict[str, int]
    coverage_pct: float
    sentiment_badge: str = "planned"
    note: str = "Review sentiment analysis is a planned future capability."


class ReviewListResponse(BaseModel):
    items: List[ReviewResponse]
    total: int
    limit: int
    offset: int


# -----------------
# 7. Recommendations
# -----------------
class RecommendationCard(BaseModel):
    rule_name: str
    type: str
    thresholds: Dict[str, Any]
    evidence: str
    sample_size: int
    confidence: str  # strictly 'very_low', 'low', 'moderate'
    limitations: str
    why_this: str
    suggested_action: str


class RecommendationListData(BaseModel):
    cards: List[RecommendationCard]
    suppressed: bool = False
    reason: Optional[str] = None


# -----------------
# 8. Assistant (Ask AVA)
# -----------------
class AskQuestionRequest(BaseModel):
    question: str = Field(..., min_length=2, max_length=1000)
    niche_id: Optional[str] = None
    session_id: Optional[str] = None


class EvidenceItem(BaseModel):
    metric: str
    value: Any
    sample_size: int
    source_tool: str
    niche: str


class AskQuestionResponse(BaseModel):
    answer: str
    evidence: List[EvidenceItem]
    estimates_labeled: List[str]
    limitations: List[str]
    follow_up_suggestions: List[str]
    mode: str = Field(default="demo", description="gemini | demo")
    session_id: Optional[str] = None


class AssistantStatusResponse(BaseModel):
    mode: str
    gemini_available: bool
    model: str
    sample_questions: List[str]
