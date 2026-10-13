"""
AVA Similar Products Benchmark
Finds competitor products in the same category with matching material or pattern
within a configurable price tolerance band (+/- 25%).
"""

import pandas as pd
from typing import List, Dict, Any, Optional

def find_similar_products(
    target_product: Dict[str, Any],
    df: pd.DataFrame,
    price_tolerance: float = 0.25,
    limit: int = 5
) -> List[Dict[str, Any]]:
    if df.empty:
        return []

    target_asin = target_product.get("asin")
    target_price = float(target_product.get("price", 0.0))
    target_mat = str(target_product.get("material", "")).lower()
    target_pat = str(target_product.get("pattern", "")).lower()

    # Filter out self
    pool = df[df["asin"] != target_asin].copy()
    if pool.empty:
        return []

    # Price window
    min_p = target_price * (1 - price_tolerance)
    max_p = target_price * (1 + price_tolerance)
    pool = pool[(pool["price"] >= min_p) & (pool["price"] <= max_p)]

    # Match material or pattern
    matched = pool[
        pool["material"].str.lower().str.contains(target_mat, na=False) |
        (pool["pattern"].str.lower() == target_pat)
    ]

    if matched.empty:
        # Fallback to nearest price products
        pool["price_diff"] = (pool["price"] - target_price).abs()
        similar = pool.sort_values(by="price_diff").head(limit)
    else:
        matched["price_diff"] = (matched["price"] - target_price).abs()
        similar = matched.sort_values(by="price_diff").head(limit)

    results: List[Dict[str, Any]] = []
    for _, row in similar.iterrows():
        p_dict = row.to_dict()
        results.append(p_dict)

    return results
