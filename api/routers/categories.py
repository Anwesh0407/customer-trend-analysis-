"""Categories router."""
from __future__ import annotations

from typing import List
from fastapi import APIRouter, Depends

from ava.storage.base import Repository
from api.deps import get_repo
from api.schemas import CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=List[CategoryResponse])
def list_categories(repo: Repository = Depends(get_repo)) -> List[CategoryResponse]:
    categories = repo.get_categories()
    all_prods = repo.get_all_products_for_niche()

    result: List[CategoryResponse] = []
    for cat in categories:
        cat_name = cat.get("name")
        matching = [p for p in all_prods if p.get("category") == cat_name]
        p_count = len(matching)

        mode = "demo"
        if matching:
            if all("synthetic" not in (p.get("source") or "").lower() for p in matching):
                mode = "real"

        last_updated = cat.get("updated_at")
        if matching:
            dates = [p.get("collected_at") for p in matching if p.get("collected_at")]
            if dates:
                last_updated = max(dates)

        result.append(
            CategoryResponse(
                id=cat["id"],
                name=cat["name"],
                display_name=cat["display_name"],
                description=cat.get("description"),
                is_active=cat.get("is_active", True),
                product_count=p_count,
                last_updated=last_updated,
                data_mode=mode,
            )
        )
    return result
