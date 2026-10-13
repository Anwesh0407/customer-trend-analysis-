from fastapi import APIRouter, Query
from typing import Optional
from backend.app.schemas.review import ReviewInsight
from backend.app.services.data_service import data_service

router = APIRouter()

@router.get("/reviews", response_model=ReviewInsight, tags=["Reviews"])
def get_reviews(product_id: Optional[str] = Query(None, description="Optional product ASIN filter")):
    reviews = data_service.get_reviews(product_id=product_id)
    
    pos = sum(1 for r in reviews if r.sentiment == "positive")
    neu = sum(1 for r in reviews if r.sentiment == "neutral")
    neg = sum(1 for r in reviews if r.sentiment == "negative")
    total = len(reviews)
    
    avg_rating = round(sum(r.rating for r in reviews) / total, 2) if total > 0 else 0.0

    return ReviewInsight(
        positive_drivers=[
            "Breathable pure cotton comfort in hot/humid weather",
            "Authentic Sambalpuri & Ikat handloom motifs",
            "Vibrant colorfast dyes on navy & maroon items",
            "Functional pockets on daily-wear straight kurtis"
        ],
        recurring_complaints=[
            "Thin, see-through fabric on budget rayon (<₹600)",
            "Shrinkage of up to 1 inch after machine wash",
            "Color bleeding on unbranded synthetic dyes",
            "Tightness around armholes and inaccurate bust sizing"
        ],
        sentiment_distribution={
            "positive_pct": round(pos / total * 100, 1) if total else 0,
            "neutral_pct": round(neu / total * 100, 1) if total else 0,
            "negative_pct": round(neg / total * 100, 1) if total else 0
        },
        total_reviews_analyzed=total,
        avg_rating=avg_rating,
        samples=reviews[:10]
    )
