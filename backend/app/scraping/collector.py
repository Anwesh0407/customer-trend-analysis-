"""
Modular Data Collection & Ingestion Pipeline for Amazon Vendor Assist (AVA)
Designed for compliance, rate limiting, and safe import of marketplace data.
"""

import json
import csv
import os
import time
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from backend.app.core.logging import logger

class BaseCollector:
    """Abstract base class for all data collectors and adapters."""
    def collect(self) -> List[Dict[str, Any]]:
        raise NotImplementedError

class LocalFileCollector(BaseCollector):
    """
    Imports and validates raw/sample JSON or CSV files into cleaned records.
    Ensures safe fallback without violating marketplace robots.txt or terms.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path

    def collect(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.file_path):
            logger.warning(f"File not found: {self.file_path}")
            return []

        cleaned: List[Dict[str, Any]] = []
        if self.file_path.endswith(".json"):
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                cleaned = [self._clean_product(item) for item in data]
        elif self.file_path.endswith(".csv"):
            with open(self.file_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cleaned.append(self._clean_product(row))
        
        # Deduplicate by ASIN
        deduped = {}
        for item in cleaned:
            asin = item.get("asin")
            if asin and asin not in deduped:
                deduped[asin] = item

        logger.info(f"Imported and deduplicated {len(deduped)} products from {self.file_path}")
        return list(deduped.values())

    def _clean_product(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        """Standardizes product records against the AVA schema."""
        sizes = raw.get("available_sizes", [])
        if isinstance(sizes, str):
            sizes = [s.strip() for s in sizes.split(",") if s.strip()]

        price = float(raw.get("price_inr", 0.0))
        mrp = float(raw.get("mrp_inr", price))
        discount = int(raw.get("discount_pct", int(((mrp - price) / mrp * 100)) if mrp > price else 0))

        return {
            "asin": str(raw.get("asin", "")),
            "product_name": str(raw.get("product_name", "")),
            "category": str(raw.get("category", "Women's Clothing")),
            "subcategory": str(raw.get("subcategory", "Kurtas & Kurtis")),
            "brand": str(raw.get("brand", "Generic")),
            "price_inr": price,
            "mrp_inr": mrp,
            "discount_pct": discount,
            "rating": float(raw.get("rating", 0.0)),
            "review_count": int(raw.get("review_count", 0)),
            "color": str(raw.get("color", "Multicolor")),
            "material": str(raw.get("material", "Cotton")),
            "pattern": str(raw.get("pattern", "Straight")),
            "available_sizes": sizes,
            "seller": str(raw.get("seller", "Unknown")),
            "availability": str(raw.get("availability", "In Stock")),
            "product_url": str(raw.get("product_url", "")),
            "source": str(raw.get("source", "file_import")),
            "collected_at": raw.get("collected_at", datetime.now(timezone.utc).isoformat())
        }

class CompliantAPIScraperAdapter(BaseCollector):
    """
    Adapter stub for authorized marketplace APIs (e.g. SP-API or licensed marketplace providers).
    Enforces strict rate-limiting, respects access policies, never bypasses anti-bot systems.
    """
    def __init__(self, api_key: Optional[str] = None, rate_limit_delay: float = 2.0):
        self.api_key = api_key
        self.rate_limit_delay = rate_limit_delay

    def collect(self) -> List[Dict[str, Any]]:
        if not self.api_key:
            logger.info("No authorized API credentials configured. Yielding to local collector.")
            return []
        
        # Polite rate-limiting placeholder
        time.sleep(self.rate_limit_delay)
        return []
