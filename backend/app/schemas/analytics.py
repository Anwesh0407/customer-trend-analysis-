from pydantic import BaseModel
from typing import Dict, List, Optional

class AnalyticsOverview(BaseModel):
    total_products: int
    median_price_inr: float
    min_price_inr: float
    max_price_inr: float
    avg_rating: float
    median_rating: float
    sample_size: int
    avg_discount_pct: float
    dominant_material: str
    dominant_color: str
    dominant_price_band: str

class PriceBandDistribution(BaseModel):
    band_name: str
    min_price: float
    max_price: float
    product_count: int
    avg_rating: float
    competition_density: str
    opportunity_level: str

class PriceAnalyticsResponse(BaseModel):
    price_bands: List[PriceBandDistribution]
    sweet_spot: Dict[str, str]

class AttributeBreakdown(BaseModel):
    materials: Dict[str, int]
    colors: Dict[str, int]
    patterns: Dict[str, int]
    brands: Dict[str, int]
