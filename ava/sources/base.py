"""
AVA Base Source Adapter
"""

from typing import List, Dict, Any, Optional

class BaseSource:
    """Abstract base class for all data sources."""
    def __init__(self, source_name: str):
        self.source_name = source_name

    def fetch(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        raise NotImplementedError
