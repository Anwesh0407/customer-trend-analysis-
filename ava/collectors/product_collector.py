"""
AVA Product Collector
Executes raw collection from sources, stamps provenance (source + collected_at),
and preserves immutable raw history in data/raw/products_<source>_<timestamp>.json.
"""

import json
import os
import re
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from ava.sources.base import BaseSource
from ava.logging_setup import logger

class ProductCollector:
    def __init__(self, raw_dir: str = "data/raw"):
        self.raw_dir = raw_dir
        os.makedirs(self.raw_dir, exist_ok=True)

    def collect(self, source: BaseSource, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        iso_now = datetime.now(timezone.utc).isoformat()
        clean_src = re.sub(r'[^a-zA-Z0-9_\-]', '_', source.source_name)
        out_filename = f"products_{clean_src}_{timestamp}.json"
        out_path = os.path.join(self.raw_dir, out_filename)

        logger.info(f"Starting product collection from '{source.source_name}'...")
        is_partial = False
        try:
            raw_items = source.fetch(limit=limit)
        except Exception as e:
            logger.warning(f"Collection from '{source.source_name}' encountered partial error: {e}")
            raw_items = []
            is_partial = True

        stamped_items: List[Dict[str, Any]] = []
        for item in raw_items:
            entry = dict(item)
            if "source" not in entry or not entry["source"]:
                entry["source"] = source.source_name
            if "collected_at" not in entry or not entry["collected_at"]:
                entry["collected_at"] = iso_now
            stamped_items.append(entry)

        # Save immutable raw history (D-03, D-04)
        payload = {
            "source": source.source_name,
            "timestamp": iso_now,
            "count": len(stamped_items),
            "status": "partial" if is_partial else "completed",
            "items": stamped_items
        }

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        logger.info(f"Saved {len(stamped_items)} raw items to '{out_path}' (status={payload['status']})")
        return stamped_items
