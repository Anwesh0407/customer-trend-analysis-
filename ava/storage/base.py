"""Repository interface for data persistence."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

from ava.models import Niche, Product, Review


class Repository(ABC):
    """Abstract repository defining storage contract for SQLite and PostgreSQL."""

    @abstractmethod
    def init_db(self) -> None:
        """Initialize database schema/tables."""
        pass

    # Categories
    @abstractmethod
    def save_category(self, category_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_categories(self) -> List[Dict[str, Any]]:
        pass

    # Products
    @abstractmethod
    def save_products(self, products: List[Product]) -> int:
        """Idempotently upsert products. Returns number of records saved/updated."""
        pass

    @abstractmethod
    def get_products(
        self,
        category: Optional[str] = None,
        niche_filter: Optional[Dict[str, Any]] = None,
        sort_by: str = "review_count",
        sort_order: str = "desc",
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[Dict[str, Any]], int]:
        """Query products with optional niche filter and pagination. Returns (items, total_count)."""
        pass

    @abstractmethod
    def get_product_by_asin(self, asin: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_all_products_for_niche(
        self,
        category: Optional[str] = None,
        niche_filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Fetch all product records matching a niche for analytics computation in pandas."""
        pass

    # Reviews
    @abstractmethod
    def save_reviews(self, reviews: List[Review]) -> int:
        """Idempotently upsert reviews."""
        pass

    @abstractmethod
    def get_reviews(
        self,
        asin: Optional[str] = None,
        category: Optional[str] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> Tuple[List[Dict[str, Any]], int]:
        pass

    # Niches
    @abstractmethod
    def save_niche(self, niche: Niche) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_niches(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_niche_by_id(self, niche_id: str) -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_niche(self, niche_id: str) -> bool:
        pass

    # Ingest runs
    @abstractmethod
    def save_ingest_run(self, run_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_ingest_runs(self, limit: int = 10) -> List[Dict[str, Any]]:
        pass

    # Chat logs
    @abstractmethod
    def save_chat_log(self, log_data: Dict[str, Any]) -> None:
        pass

    @abstractmethod
    def get_chat_logs(
        self, session_id: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        pass
