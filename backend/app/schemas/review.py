from pydantic import BaseModel
from typing import List, Optional

class ReviewItem(BaseModel):
    review_id: str
    product_id: str
    rating: float
    title: str
    text: str
    date: str
    source: str
    sentiment: str
    collected_at: str

class ReviewInsight(BaseModel):
    positive_drivers: List[str]
    recurring_complaints: List[str]
    sentiment_distribution: dict
    total_reviews_analyzed: int
    avg_rating: float
    samples: List[ReviewItem]
