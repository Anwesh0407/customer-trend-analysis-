"""
AVA Canonical Data Models
Single source of truth for entity validation (Pydantic v2).
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, field_validator

CANONICAL_SIZES = ["XS", "S", "M", "L", "XL", "XXL", "3XL", "4XL", "5XL", "6XL", "Free Size"]
VALID_AVAILABILITIES = ["in_stock", "limited", "out_of_stock", "unknown"]

class Product(BaseModel):
    asin: str = Field(..., description="10-character alphanumeric ASIN or synthetic identifier")
    product_name: str = Field(..., min_length=1, description="Product title/name")
    category: str = Field(default="Women's Kurtas & Kurtis")
    brand: str = Field(default="Generic")
    price: float = Field(..., ge=0.0, description="Current selling price in INR")
    mrp: Optional[float] = Field(default=None, description="Maximum Retail Price in INR")
    discount_pct: Optional[int] = Field(default=None, ge=0, le=100)
    rating: Optional[float] = Field(default=None, ge=1.0, le=5.0)
    review_count: Optional[int] = Field(default=None, ge=0)
    colour: Optional[str] = Field(default="Unknown")
    material: Optional[str] = Field(default="Unknown")
    pattern: Optional[str] = Field(default="Unknown")
    sizes: List[str] = Field(default_factory=list)
    seller: Optional[str] = Field(default="Unknown")
    availability: str = Field(default="in_stock")
    product_url: str = Field(...)
    source: str = Field(...)
    collected_at: Union[str, datetime] = Field(...)

    @field_validator("collected_at")
    @classmethod
    def serialize_collected_at(cls, v: Any) -> str:
        if isinstance(v, datetime):
            return v.isoformat()
        return str(v)

    @field_validator("availability")
    @classmethod
    def validate_availability(cls, v: str) -> str:
        clean = v.lower().strip()
        if clean in VALID_AVAILABILITIES:
            return clean
        if "stock" in clean and "out" not in clean:
            return "in_stock"
        if "out" in clean:
            return "out_of_stock"
        return "unknown"

class Review(BaseModel):
    review_id: str = Field(..., description="Stable SHA-256 hash identifier")
    product_id: str = Field(..., description="ASIN of reviewed product")
    rating: int = Field(..., ge=1, le=5, description="Integer rating from 1 to 5")
    review_title: str = Field(default="")
    review_text: str = Field(default="")
    review_date: Optional[Union[str, datetime]] = Field(default=None)
    source: str = Field(default="synthetic")
    collected_at: Union[str, datetime] = Field(...)

    @field_validator("review_date", "collected_at")
    @classmethod
    def serialize_dates(cls, v: Any) -> str:
        if isinstance(v, datetime):
            return v.isoformat()
        return str(v)

    @field_validator("rating")
    @classmethod
    def validate_rating_int(cls, v: Any) -> int:
        return int(round(float(v)))

class Niche(BaseModel):
    id: str = Field(...)
    name: str = Field(...)
    category: str = Field(default="Women's Kurtas & Kurtis")
    filters: Dict[str, Any] = Field(default_factory=dict)
    description: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    brands: List[str] = Field(default_factory=list)
    colours: List[str] = Field(default_factory=list)
    materials: List[str] = Field(default_factory=list)
    patterns: List[str] = Field(default_factory=list)
    sizes: List[str] = Field(default_factory=list)
    min_rating: Optional[float] = None
    min_reviews: Optional[int] = None
    keyword: Optional[str] = None
    is_default: bool = False

class CleaningReport(BaseModel):
    timestamp: str
    source_file: str
    rows_in: int
    rows_out: int
    duplicates_removed: int
    rejected_counts: Dict[str, int] = Field(default_factory=dict)
    data_quality_notes: Dict[str, int] = Field(default_factory=dict)
    missing_counts_per_field: Dict[str, int] = Field(default_factory=dict)
    unrecognised_columns: List[str] = Field(default_factory=list)

    @property
    def rows_rejected(self) -> int:
        return sum(self.rejected_counts.values())
