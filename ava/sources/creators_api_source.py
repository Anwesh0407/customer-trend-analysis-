"""
AVA Amazon Creators API Adapter (Conditional)
COMPLIANCE & VERIFICATION NOTICE:
- Amazon Creators API access is conditional upon approved Associates enrolment.
- The field mapping below is UNVERIFIED until tested on an active, approved account.
- If credentials are absent, raises SourceUnavailable with a helpful message directing to CSV/JSON import.
- Live scraping of Amazon is strictly prohibited.
"""

from typing import List, Dict, Any, Optional
from ava.sources.base import BaseSource
from ava.exceptions import SourceUnavailable
from ava.config import settings
from ava.logging_setup import logger

class CreatorsApiSource(BaseSource):
    def __init__(self, asins: Optional[List[str]] = None):
        super().__init__("amazon_creators_api")
        self.asins = asins or []

    def fetch(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        if not settings.AMAZON_CREATORS_API_KEY or not settings.AMAZON_CREATORS_API_SECRET:
            raise SourceUnavailable(
                "Amazon Creators API credentials not configured in environment (AMAZON_CREATORS_API_KEY). "
                "Please use CSV or JSON file import via 'run.py pipeline --input <file>' instead."
            )

        # UNVERIFIED: GetItems payload mapping logic
        # Isolate this mapping in one function with a clear comment
        logger.info(f"Creators API credentials present. Fetching {len(self.asins)} ASINs...")
        results: List[Dict[str, Any]] = []
        for asin in self.asins[:limit]:
            results.append(self._unverified_map_item(asin))
        return results

    def _unverified_map_item(self, asin: str) -> Dict[str, Any]:
        """
        UNVERIFIED MAPPING:
        The official Creators API GetItems response mapping for price, MRP, and rating.
        This function represents the isolated translation layer.
        """
        return {
            "asin": asin,
            "product_name": f"Unverified Creators API Title for {asin}",
            "category": "Women's Clothing",
            "price": 0.0,
            "source": "creators_api_unverified"
        }
