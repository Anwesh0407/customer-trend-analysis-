"""
AVA CSV Source Adapter
Robustly parses CSV files handling Excel BOM (utf-8-sig), ragged rows, and blank lines.
"""

import csv
import os
from typing import List, Dict, Any, Optional
from ava.sources.base import BaseSource
from ava.exceptions import SourceUnavailable
from ava.logging_setup import logger

class CsvSource(BaseSource):
    def __init__(self, file_path: str, source_name: Optional[str] = None):
        super().__init__(source_name or f"csv:{os.path.basename(file_path)}")
        self.file_path = file_path

    def fetch(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        if not os.path.exists(self.file_path):
            raise SourceUnavailable(f"CSV source file not found: {self.file_path}")

        records: List[Dict[str, Any]] = []

        # Read with utf-8-sig to automatically strip Excel BOM
        with open(self.file_path, "r", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.reader(f)
            headers = None

            for row in reader:
                # Skip blank lines
                if not row or not any(cell.strip() for cell in row):
                    continue

                if headers is None:
                    headers = [h.strip() for h in row]
                    continue

                # Handle ragged rows (pad with empty string if too short; truncate if too long)
                padded_row = row + [""] * (len(headers) - len(row))
                record = {headers[i]: padded_row[i].strip() for i in range(len(headers))}
                records.append(record)

                if limit and len(records) >= limit:
                    break

        logger.info(f"Loaded {len(records)} raw rows from CSV source '{self.file_path}'")
        return records

CSVSource = CsvSource
