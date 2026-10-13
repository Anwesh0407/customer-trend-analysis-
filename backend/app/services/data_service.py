import json
import os
from typing import List, Optional, Dict, Any
from backend.app.schemas.product import ProductResponse, ProductListResponse
from backend.app.schemas.review import ReviewItem
from backend.app.core.logging import logger

DATA_SAMPLE_PRODUCTS = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/sample/sample_kurtas.json"))
DATA_SAMPLE_REVIEWS = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../data/sample/sample_reviews.json"))

class DataService:
    def __init__(self):
        self._products_cache: List[dict] = []
        self._reviews_cache: List[dict] = []
        self._load_cache()

    def _load_cache(self):
        if os.path.exists(DATA_SAMPLE_PRODUCTS):
            try:
                with open(DATA_SAMPLE_PRODUCTS, "r", encoding="utf-8") as f:
                    self._products_cache = json.load(f)
                logger.info(f"Loaded {len(self._products_cache)} sample products into memory cache.")
            except Exception as e:
                logger.error(f"Error loading sample products: {e}")
                self._products_cache = []
        
        if os.path.exists(DATA_SAMPLE_REVIEWS):
            try:
                with open(DATA_SAMPLE_REVIEWS, "r", encoding="utf-8") as f:
                    self._reviews_cache = json.load(f)
                logger.info(f"Loaded {len(self._reviews_cache)} sample reviews into memory cache.")
            except Exception as e:
                logger.error(f"Error loading sample reviews: {e}")
                self._reviews_cache = []

    def get_products(
        self,
        category: Optional[str] = None,
        subcategory: Optional[str] = None,
        location: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        material: Optional[str] = None,
        color: Optional[str] = None,
        search: Optional[str] = None,
        sort: Optional[str] = None,
        page: int = 1,
        page_size: int = 20
    ) -> ProductListResponse:
        items = list(self._products_cache)

        if min_price is not None:
            items = [p for p in items if p["price_inr"] >= min_price]
        if max_price is not None:
            items = [p for p in items if p["price_inr"] <= max_price]
        if material and material.lower() != "all":
            items = [p for p in items if material.lower() in p["material"].lower()]
        if color and color.lower() != "all":
            items = [p for p in items if color.lower() in p["color"].lower()]
        if search:
            q = search.lower()
            items = [
                p for p in items
                if q in p["product_name"].lower()
                or q in p["color"].lower()
                or q in p["material"].lower()
                or q in p["brand"].lower()
            ]

        # Sorting
        if sort == "price_asc":
            items.sort(key=lambda x: x["price_inr"])
        elif sort == "price_desc":
            items.sort(key=lambda x: x["price_inr"], reverse=True)
        elif sort == "rating":
            items.sort(key=lambda x: x["rating"], reverse=True)
        elif sort == "reviews":
            items.sort(key=lambda x: x["review_count"], reverse=True)
        elif sort == "opportunity":
            items.sort(key=lambda x: 1 if x["price_inr"] >= 800 and x["price_inr"] <= 1000 and x["material"] == "Cotton" else 0, reverse=True)

        total = len(items)
        start = (page - 1) * page_size
        end = start + page_size
        paged_items = items[start:end]

        enriched_items = [self._enrich_product(p) for p in paged_items]
        return ProductListResponse(
            total=total,
            page=page,
            page_size=page_size,
            items=enriched_items
        )

    def get_product_by_id(self, asin: str) -> Optional[ProductResponse]:
        for p in self._products_cache:
            if p["asin"] == asin:
                return self._enrich_product(p)
        return None

    def get_reviews(self, product_id: Optional[str] = None) -> List[ReviewItem]:
        if product_id:
            raw = [r for r in self._reviews_cache if r["product_id"] == product_id]
        else:
            raw = self._reviews_cache
        return [ReviewItem(**r) for r in raw]

    def _enrich_product(self, p: dict) -> ProductResponse:
        price = p["price_inr"]
        material = p["material"]
        rating = p["rating"]

        # Rule-based opportunity signals
        if 800 <= price <= 1000 and "cotton" in material.lower() and rating >= 4.2:
            badge = "High Opportunity"
            badge_type = "badge-opportunity"
            opportunity = "High"
            price_pos = "Optimal sweet spot (₹800–₹1,000)"
            competition = "Low"
        elif rating >= 4.3:
            badge = "Rising"
            badge_type = "badge-rising"
            opportunity = "High"
            price_pos = "Above average quality tier"
            competition = "Medium"
        elif p["review_count"] > 2000:
            badge = "Strong Reviews"
            badge_type = "badge-reviews"
            opportunity = "Medium"
            price_pos = "Budget high-volume tier"
            competition = "High"
        else:
            badge = "Standard"
            badge_type = "badge-standard"
            opportunity = "Medium"
            price_pos = "Competitive"
            competition = "Medium"

        sentiment_label = "Positive (82%)" if rating >= 4.2 else "Moderate (65%)" if rating >= 4.0 else "Mixed (52%)"

        return ProductResponse(
            **p,
            badge=badge,
            badge_type=badge_type,
            sentiment=sentiment_label,
            price_position=price_pos,
            rating_position=f"{rating} ★ vs market median 4.2",
            competition=competition,
            opportunity=opportunity
        )

data_service = DataService()
