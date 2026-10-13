"""
AVA Compliant Public Page Source Adapter
Fetches public non-Amazon product pages complying with robots.txt and rate limits.
Extracts product metadata strictly via schema.org JSON-LD or metadata tags.
Never targets Amazon domains or bypasses anti-bot protection.
"""

import json
import re
from typing import List, Dict, Any, Optional
from ava.sources.base import BaseSource
from ava.http_client import http_client
from ava.exceptions import ComplianceViolation
from ava.logging_setup import logger

class PublicPageSource(BaseSource):
    def __init__(self, urls: List[str]):
        super().__init__("public_web_page")
        self.urls = urls

    def fetch(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        records: List[Dict[str, Any]] = []
        target_urls = self.urls[:limit] if limit else self.urls

        for url in target_urls:
            try:
                resp = http_client.get(url, check_robots=True)
                item = self._extract_json_ld(resp.text, url)
                if item:
                    records.append(item)
            except ComplianceViolation as e:
                logger.warning(f"Compliance stop on {url}: {e}")
                # Partial collection results are saved if a source stops
                break
            except Exception as e:
                logger.error(f"Error fetching public page {url}: {e}")
                continue

        return records

    def _extract_json_ld(self, html: str, url: str) -> Optional[Dict[str, Any]]:
        """Extracts schema.org/Product JSON-LD block from HTML."""
        pattern = re.compile(r'<script[^>]+type=[\'"]application/ld\+json[\'"][^>]*>(.*?)</script>', re.DOTALL | re.IGNORECASE)
        matches = pattern.findall(html)
        for block in matches:
            try:
                data = json.loads(block)
                if isinstance(data, list):
                    for entry in data:
                        if entry.get("@type") == "Product":
                            return self._map_schema_product(entry, url)
                elif isinstance(data, dict):
                    if data.get("@type") == "Product":
                        return self._map_schema_product(data, url)
            except Exception:
                continue
        return None

    def _map_schema_product(self, data: Dict[str, Any], url: str) -> Dict[str, Any]:
        offers = data.get("offers", {})
        price = 0.0
        if isinstance(offers, dict):
            price = float(offers.get("price", 0.0))
        elif isinstance(offers, list) and len(offers) > 0:
            price = float(offers[0].get("price", 0.0))

        return {
            "asin": data.get("sku") or data.get("productID") or data.get("mpn") or "",
            "product_name": data.get("name", ""),
            "brand": data.get("brand", {}).get("name") if isinstance(data.get("brand"), dict) else str(data.get("brand", "Generic")),
            "price": price,
            "product_url": url,
            "source": f"public_web:{url}"
        }
