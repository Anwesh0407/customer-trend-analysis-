from pydantic import BaseModel, Field
from typing import List, Optional

class ProductBase(BaseModel):
    asin: str = Field(..., description="Amazon Standard Identification Number or unique product ID")
    product_name: str
    category: str
    subcategory: str
    brand: str
    price_inr: float
    mrp_inr: float
    discount_pct: int
    rating: float
    review_count: int
    color: str
    material: str
    pattern: str
    available_sizes: List[str]
    seller: str
    availability: str
    product_url: str
    source: str
    collected_at: str

class ProductResponse(ProductBase):
    badge: Optional[str] = None
    badge_type: Optional[str] = None
    sentiment: Optional[str] = None
    price_position: Optional[str] = None
    rating_position: Optional[str] = None
    competition: Optional[str] = None
    opportunity: Optional[str] = None

class ProductListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ProductResponse]
