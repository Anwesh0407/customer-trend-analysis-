"""
AVA Niche Filtering Engine
A single, shared filter implementation over product collections (pandas DataFrame).
"""

import pandas as pd
from typing import List, Optional, Any, Dict
from ava.models import Niche, Product

def filter_products_by_niche(df: pd.DataFrame, niche: Optional[Niche] = None) -> pd.DataFrame:
    if df.empty or niche is None:
        return df

    filtered = df.copy()

    # Category filter
    if niche.category and "category" in filtered.columns:
        filtered = filtered[filtered["category"].str.lower() == niche.category.lower()]

    # Price bounds
    if niche.min_price is not None and "price" in filtered.columns:
        filtered = filtered[filtered["price"] >= niche.min_price]
    if niche.max_price is not None and "price" in filtered.columns:
        filtered = filtered[filtered["price"] <= niche.max_price]

    # Brands include filter
    if niche.brands and "brand" in filtered.columns:
        b_lower = [b.lower() for b in niche.brands if b]
        if b_lower:
            filtered = filtered[filtered["brand"].str.lower().isin(b_lower)]

    # Colours filter
    if niche.colours and "colour" in filtered.columns:
        c_lower = [c.lower() for c in niche.colours if c]
        if c_lower:
            filtered = filtered[filtered["colour"].str.lower().isin(c_lower)]

    # Materials filter
    if niche.materials and "material" in filtered.columns:
        m_lower = [m.lower() for m in niche.materials if m]
        if m_lower:
            pattern = "|".join(m_lower)
            filtered = filtered[filtered["material"].str.lower().str.contains(pattern, na=False)]

    # Patterns filter
    if niche.patterns and "pattern" in filtered.columns:
        p_lower = [p.lower() for p in niche.patterns if p]
        if p_lower:
            filtered = filtered[filtered["pattern"].str.lower().isin(p_lower)]

    # Min Rating
    if niche.min_rating is not None and "rating" in filtered.columns:
        filtered = filtered[filtered["rating"] >= niche.min_rating]

    # Min Reviews
    if niche.min_reviews is not None and "review_count" in filtered.columns:
        filtered = filtered[filtered["review_count"] >= niche.min_reviews]

    # Free-text Keyword
    if niche.keyword and "product_name" in filtered.columns:
        kw = niche.keyword.lower().strip()
        filtered = filtered[
            filtered["product_name"].str.lower().str.contains(kw, na=False) |
            filtered["brand"].str.lower().str.contains(kw, na=False) |
            filtered["material"].str.lower().str.contains(kw, na=False)
        ]

    return filtered


def apply_niche_filter(
    products: List[Dict[str, Any]],
    niche_filter: Optional[Any] = None,
) -> List[Dict[str, Any]]:
    """Applies niche filters to a list of product dictionaries."""
    if not products or not niche_filter:
        return products

    if isinstance(niche_filter, dict):
        niche_obj = Niche(
            id="temp",
            name="temp",
            category=niche_filter.get("category", "Women's Kurtas & Kurtis"),
            min_price=niche_filter.get("min_price"),
            max_price=niche_filter.get("max_price"),
            brands=niche_filter.get("brands", []),
            colours=niche_filter.get("colours", []),
            materials=niche_filter.get("materials", []),
            patterns=niche_filter.get("patterns", []),
            sizes=niche_filter.get("sizes", []),
            min_rating=niche_filter.get("min_rating"),
            min_reviews=niche_filter.get("min_reviews"),
            keyword=niche_filter.get("keyword"),
        )
    else:
        niche_obj = niche_filter

    df = pd.DataFrame(products)
    filtered_df = filter_products_by_niche(df, niche_obj)
    return filtered_df.to_dict(orient="records")
