"""
AVA Column Normalization & Alias Mapping
Rule 1: Normalize column names through alias map; track unrecognised columns.
"""

from typing import Dict, Any, Tuple, List

COLUMN_ALIASES = {
    "asin": "asin",
    "product_id": "asin",
    "id": "asin",
    "sku": "asin",
    
    "product_name": "product_name",
    "title": "product_name",
    "name": "product_name",
    "item_name": "product_name",
    
    "category": "category",
    "cat": "category",
    
    "brand": "brand",
    "manufacturer": "brand",
    
    "price": "price",
    "price_inr": "price",
    "selling_price": "price",
    "our_price": "price",
    "deal_price": "price",
    
    "mrp": "mrp",
    "mrp_inr": "mrp",
    "list_price": "mrp",
    "retail_price": "mrp",
    
    "discount_pct": "discount_pct",
    "discount": "discount_pct",
    "discount_percentage": "discount_pct",
    
    "rating": "rating",
    "stars": "rating",
    "review_rating": "rating",
    
    "review_count": "review_count",
    "total_reviews": "review_count",
    "ratings_count": "review_count",
    "num_reviews": "review_count",
    
    "colour": "colour",
    "color": "colour",
    
    "material": "material",
    "fabric": "material",
    
    "pattern": "pattern",
    "design": "pattern",
    
    "sizes": "sizes",
    "size": "sizes",
    "available_sizes": "sizes",
    
    "seller": "seller",
    "sold_by": "seller",
    "merchant": "seller",
    
    "availability": "availability",
    "stock": "availability",
    "stock_status": "availability",
    
    "product_url": "product_url",
    "url": "product_url",
    "link": "product_url",
    
    "source": "source",
    "collected_at": "collected_at"
}

def normalize_columns(row: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    normalized: Dict[str, Any] = {}
    unrecognised: List[str] = []

    for key, value in row.items():
        clean_key = str(key).strip().lower().replace(" ", "_").replace("-", "_")
        if clean_key in COLUMN_ALIASES:
            canon = COLUMN_ALIASES[clean_key]
            # Don't overwrite if already populated with a non-empty value
            if canon not in normalized or normalized[canon] in (None, "", []):
                normalized[canon] = value
        else:
            unrecognised.append(key)

    return normalized, unrecognised
