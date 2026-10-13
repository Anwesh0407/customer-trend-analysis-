"""
AVA JSON Source Adapter
Parses standard JSON arrays, JSON Lines (.jsonl), and wrapped object envelopes (e.g. {"items": [...]}).
"""

import json
import os
from typing import List, Dict, Any, Optional
from ava.sources.base import BaseSource
from ava.exceptions import SourceUnavailable
from ava.logging_setup import logger

class JsonSource(BaseSource):
    def __init__(self, file_path: str, source_name: Optional[str] = None):
        super().__init__(source_name or f"json:{os.path.basename(file_path)}")
        self.file_path = file_path

    def fetch(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        if not os.path.exists(self.file_path):
            raise SourceUnavailable(f"JSON source file not found: {self.file_path}")

        records: List[Dict[str, Any]] = []

        with open(self.file_path, "r", encoding="utf-8-sig", errors="replace") as f:
            content = f.read().strip()

        if not content:
            return []

        # 1. Try standard JSON array or wrapped object
        try:
            data = json.loads(content)
            if isinstance(data, list):
                records = [item for item in data if isinstance(item, dict)]
            elif isinstance(data, dict):
                # Wrapped object envelope: check common keys
                for key in ["items", "products", "data", "results"]:
                    if key in data and isinstance(data[key], list):
                        records = [item for item in data[key] if isinstance(item, dict)]
                        break
                if not records:
                    records = [data]
        except json.JSONDecodeError:
            # 2. Try JSON Lines
            for line in content.splitlines():
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    if isinstance(obj, dict):
                        records.append(obj)
                except json.JSONDecodeError:
                    continue

        if limit:
            records = records[:limit]

        logger.info(f"Loaded {len(records)} raw items from JSON source '{self.file_path}'")
        return records

JSONSource = JsonSource
