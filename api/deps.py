"""FastAPI dependency injection utilities."""
from __future__ import annotations

from typing import Any, Dict, Generator, Optional, Tuple
from fastapi import Depends, Query

from ava.config import get_settings
from ava.storage.base import Repository
from ava.storage.sql_repository import SQLAlchemyRepository

_repo_instance: Optional[SQLAlchemyRepository] = None


def get_repo() -> Repository:
    """Returns singleton SQLAlchemyRepository initialized with active database URL."""
    global _repo_instance
    if _repo_instance is None:
        db_url = get_settings().database_url
        _repo_instance = SQLAlchemyRepository(database_url=db_url)
        _repo_instance.init_db()
    return _repo_instance


def get_niche_context(
    niche_id: Optional[str] = Query(None, description="Optional saved Niche ID to scope data to"),
    repo: Repository = Depends(get_repo),
) -> Tuple[Optional[Dict[str, Any]], str]:
    """Resolves niche filters and human-readable name from query parameters."""
    if not niche_id or niche_id in ("all", "default", "none"):
        return None, "All Listings (Whole Category)"

    niche_record = repo.get_niche_by_id(niche_id)
    if niche_record:
        return niche_record.get("filters"), niche_record.get("name", "Saved Niche")

    return None, f"Custom Niche ({niche_id})"
