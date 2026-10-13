"""Niches router for filter management and preview."""
from __future__ import annotations

import uuid
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from ava.config import get_settings
from ava.models import Niche
from ava.storage.base import Repository
from api.deps import get_repo
from api.schemas import (
    NicheCreate,
    NichePreviewRequest,
    NichePreviewResponse,
    NicheResponse,
    NicheUpdate,
)

router = APIRouter(prefix="/niches", tags=["Niches"])


@router.get("", response_model=List[NicheResponse])
def list_niches(
    category: Optional[str] = Query(None, description="Category name"),
    repo: Repository = Depends(get_repo),
) -> List[NicheResponse]:
    records = repo.get_niches(category=category)
    result = []
    for r in records:
        # compute sample size for each niche
        prods = repo.get_all_products_for_niche(category=r.get("category"), niche_filter=r.get("filters"))
        result.append(
            NicheResponse(
                id=r["id"],
                name=r["name"],
                category=r["category"],
                filters=r.get("filters", {}),
                description=r.get("description"),
                sample_size=len(prods),
                created_at=r.get("created_at"),
                updated_at=r.get("updated_at"),
            )
        )
    return result


@router.post("", response_model=NicheResponse, status_code=status.HTTP_201_CREATED)
def create_niche(payload: NicheCreate, repo: Repository = Depends(get_repo)) -> NicheResponse:
    niche_id = f"niche_{uuid.uuid4().hex[:8]}"
    niche = Niche(
        id=niche_id,
        name=payload.name,
        category=payload.category,
        filters=payload.filters,
        description=payload.description,
    )
    saved = repo.save_niche(niche)
    prods = repo.get_all_products_for_niche(category=saved["category"], niche_filter=saved.get("filters"))
    return NicheResponse(
        id=saved["id"],
        name=saved["name"],
        category=saved["category"],
        filters=saved.get("filters", {}),
        description=saved.get("description"),
        sample_size=len(prods),
        created_at=saved.get("created_at"),
        updated_at=saved.get("updated_at"),
    )


@router.get("/{niche_id}", response_model=NicheResponse)
def get_niche(niche_id: str, repo: Repository = Depends(get_repo)) -> NicheResponse:
    n = repo.get_niche_by_id(niche_id)
    if not n:
        raise HTTPException(status_code=404, detail=f"Niche with id '{niche_id}' not found.")
    prods = repo.get_all_products_for_niche(category=n["category"], niche_filter=n.get("filters"))
    return NicheResponse(
        id=n["id"],
        name=n["name"],
        category=n["category"],
        filters=n.get("filters", {}),
        description=n.get("description"),
        sample_size=len(prods),
        created_at=n.get("created_at"),
        updated_at=n.get("updated_at"),
    )


@router.put("/{niche_id}", response_model=NicheResponse)
def update_niche(niche_id: str, payload: NicheUpdate, repo: Repository = Depends(get_repo)) -> NicheResponse:
    existing = repo.get_niche_by_id(niche_id)
    if not existing:
        raise HTTPException(status_code=404, detail=f"Niche with id '{niche_id}' not found.")

    updated_name = payload.name if payload.name is not None else existing["name"]
    updated_filters = payload.filters if payload.filters is not None else existing.get("filters", {})
    updated_desc = payload.description if payload.description is not None else existing.get("description")

    niche = Niche(
        id=niche_id,
        name=updated_name,
        category=existing["category"],
        filters=updated_filters,
        description=updated_desc,
    )
    saved = repo.save_niche(niche)
    prods = repo.get_all_products_for_niche(category=saved["category"], niche_filter=saved.get("filters"))
    return NicheResponse(
        id=saved["id"],
        name=saved["name"],
        category=saved["category"],
        filters=saved.get("filters", {}),
        description=saved.get("description"),
        sample_size=len(prods),
        created_at=saved.get("created_at"),
        updated_at=saved.get("updated_at"),
    )


@router.delete("/{niche_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_niche(niche_id: str, repo: Repository = Depends(get_repo)):
    success = repo.delete_niche(niche_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Niche with id '{niche_id}' not found.")
    return None


@router.post("/preview", response_model=NichePreviewResponse)
def preview_niche(payload: NichePreviewRequest, repo: Repository = Depends(get_repo)) -> NichePreviewResponse:
    """Live preview of sample size before saving a niche."""
    prods = repo.get_all_products_for_niche(category=payload.category, niche_filter=payload.filters)
    sample_size = len(prods)
    min_thresh = get_settings().MIN_SAMPLE_SIZE
    below = sample_size < min_thresh
    warning = None
    if below:
        warning = f"Sample size (n={sample_size}) is below statistical reliability threshold ({min_thresh}). Insights may be suppressed."

    return NichePreviewResponse(
        sample_size=sample_size,
        below_threshold=below,
        threshold=min_thresh,
        warning=warning,
    )
