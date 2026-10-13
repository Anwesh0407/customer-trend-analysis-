"""Products router with niche scoping, percentiles, and similarity benchmark."""
from __future__ import annotations

import pandas as pd
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query

from ava.storage.base import Repository
from ava.recommendations.similarity import find_similar_products
from api.deps import get_niche_context, get_repo
from api.envelope import EvidenceEnvelope, create_envelope
from api.schemas import (
    ProductListResponse,
    ProductResponse,
    SimilarProductItem,
    SimilarProductsResponse,
)

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=EvidenceEnvelope[ProductListResponse])
def list_products(
    category: Optional[str] = Query(None, description="Category filter"),
    sort_by: str = Query("review_count", description="Field to sort by: price, rating, review_count, discount_pct"),
    sort_order: str = Query("desc", description="asc or desc"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    niche_ctx=Depends(get_niche_context),
    repo: Repository = Depends(get_repo),
) -> Dict[str, Any]:
    niche_filter, niche_name = niche_ctx
    all_niche_items = repo.get_all_products_for_niche(category=category, niche_filter=niche_filter)
    sample_size = len(all_niche_items)

    reverse = sort_order.lower() == "desc"
    def sort_key(x):
        val = x.get(sort_by)
        if val is None:
            return -1e9 if reverse else 1e9
        return val

    sorted_items = sorted(all_niche_items, key=sort_key, reverse=reverse)
    paged = sorted_items[offset : offset + limit]

    prod_responses = [ProductResponse(**p) for p in paged]
    data = ProductListResponse(
        items=prod_responses,
        total=sample_size,
        limit=limit,
        offset=offset,
    )

    data_mode = "demo"
    if all_niche_items and all("synthetic" not in (p.get("source") or "").lower() for p in all_niche_items):
        data_mode = "real"

    sources = list({p.get("source", "unknown") for p in all_niche_items})

    return create_envelope(
        data=data.model_dump(),
        niche=niche_name,
        sample_size=sample_size,
        data_mode=data_mode,
        sources=sources,
    )


@router.get("/{asin}", response_model=EvidenceEnvelope[ProductResponse])
def get_product(
    asin: str,
    niche_ctx=Depends(get_niche_context),
    repo: Repository = Depends(get_repo),
) -> Dict[str, Any]:
    clean_asin = asin.strip().upper()
    product = repo.get_product_by_asin(clean_asin)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ASIN '{clean_asin}' not found.")

    niche_filter, niche_name = niche_ctx
    all_prods = repo.get_all_products_for_niche(category=product.get("category"), niche_filter=niche_filter)
    sample_size = len(all_prods)

    # Compute percentiles within niche
    percentiles: Dict[str, Any] = {}
    quality_flags: List[str] = []

    if sample_size > 1:
        df = pd.DataFrame(all_prods)
        p_price = product.get("price")
        if p_price is not None and "price" in df.columns:
            prices = df["price"].dropna()
            if not prices.empty:
                percentiles["price_percentile"] = round(float((prices < p_price).mean()) * 100, 1)

        p_rating = product.get("rating")
        if p_rating is not None and "rating" in df.columns:
            ratings = df["rating"].dropna()
            if not ratings.empty:
                percentiles["rating_percentile"] = round(float((ratings < p_rating).mean()) * 100, 1)

    # Data quality flags
    if not product.get("mrp"):
        quality_flags.append("MRP absent or unverified")
    if product.get("discount_pct", 0) and product.get("discount_pct", 0) >= 60:
        quality_flags.append("Deep promotional discount (>=60% off MRP)")
    if (product.get("review_count") or 0) < 10:
        quality_flags.append("Low review sample (<10 ratings)")

    product["percentile_in_niche"] = percentiles
    product["quality_flags"] = quality_flags

    prod_response = ProductResponse(**product)
    data_mode = "demo" if "synthetic" in (product.get("source") or "").lower() else "real"

    return create_envelope(
        data=prod_response.model_dump(),
        niche=niche_name,
        sample_size=sample_size,
        data_mode=data_mode,
        sources=[product.get("source", "file")],
    )


@router.get("/{asin}/similar", response_model=EvidenceEnvelope[SimilarProductsResponse])
def get_similar_products(
    asin: str,
    limit: int = Query(5, ge=1, le=20),
    repo: Repository = Depends(get_repo),
) -> Dict[str, Any]:
    clean_asin = asin.strip().upper()
    product = repo.get_product_by_asin(clean_asin)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ASIN '{clean_asin}' not found.")

    all_prods = repo.get_all_products_for_niche(category=product.get("category"))
    df = pd.DataFrame(all_prods)

    similar = find_similar_products(product, df, limit=limit)
    items = []
    for s in similar:
        mat_match = str(s.get("material", "")).lower() == str(product.get("material", "")).lower()
        pat_match = str(s.get("pattern", "")).lower() == str(product.get("pattern", "")).lower()
        reason_parts = []
        if mat_match and s.get("material"):
            reason_parts.append(f"Matching material ({s['material']})")
        if pat_match and s.get("pattern"):
            reason_parts.append(f"Matching pattern ({s['pattern']})")
        if not reason_parts:
            reason_parts.append(f"Comparable price point within ±25%")

        items.append(
            SimilarProductItem(
                asin=s["asin"],
                product_name=s["product_name"],
                brand=s.get("brand"),
                price=s.get("price"),
                mrp=s.get("mrp"),
                discount_pct=s.get("discount_pct"),
                rating=s.get("rating"),
                review_count=s.get("review_count"),
                colour=s.get("colour"),
                material=s.get("material"),
                similarity_reason="; ".join(reason_parts),
            )
        )

    res = SimilarProductsResponse(asin=clean_asin, similar_items=items)
    data_mode = "demo" if any("synthetic" in (p.get("source") or "").lower() for p in all_prods) else "real"

    return create_envelope(
        data=res.model_dump(),
        niche="Whole Category Benchmark",
        sample_size=len(all_prods),
        data_mode=data_mode,
        sources=[product.get("source", "file")],
    )
