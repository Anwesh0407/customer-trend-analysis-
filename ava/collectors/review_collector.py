"""
AVA Review Collector
Stamps and preserves immutable raw review history.
"""

import json
import os
import re
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from ava.sources.base import BaseSource
from ava.logging_setup import logger

class ReviewCollector:
    def __init__(self, raw_dir: str = "data/raw"):
        self.raw_dir = raw_dir
        os.makedirs(self.raw_dir, exist_ok=True)

    def collect(self, source: BaseSource, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        iso_now = datetime.now(timezone.utc).isoformat()
        clean_src = re.sub(r'[^a-zA-Z0-9_\-]', '_', source.source_name)
        out_filename = f"reviews_{clean_src}_{timestamp}.json"
        out_path = os.path.join(self.raw_dir, out_filename)

        logger.info(f"Starting review collection from '{source.source_name}'...")
        raw_items = source.fetch(limit=limit)

        stamped_items: List[Dict[str, Any]] = []
        for item in raw_items:
            entry = dict(item)
            if "source" not in entry or not entry["source"]:
                entry["source"] = source.source_name
            if "collected_at" not in entry or not entry["collected_at"]:
                entry["collected_at"] = iso_now
            stamped_items.append(entry)

        payload = {
            "source": source.source_name,
            "timestamp": iso_now,
            "count": len(stamped_items),
            "items": stamped_items
        }

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        logger.info(f"Saved {len(stamped_items)} raw reviews to '{out_path}'")
        return stamped_items
