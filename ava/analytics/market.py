"""
AVA Market Analytics Engine
Calculates observations and distributional statistics in pandas.
Ensures parity across SQLite and PostgreSQL and enforces sample size reporting (n).
"""

import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
from ava.models import Niche
from ava.analytics.niche_filter import filter_products_by_niche

PRICE_BANDS = [
    {"name": "0-499", "min": 0.0, "max": 499.99},
    {"name": "500-999", "min": 500.0, "max": 999.99},
    {"name": "1000-1499", "min": 1000.0, "max": 1499.99},
    {"name": "1500-1999", "min": 1500.0, "max": 1999.99},
    {"name": "2000-2999", "min": 2000.0, "max": 2999.99},
    {"name": "3000+", "min": 3000.0, "max": 999999.0}
]

def compute_market_analytics(df: pd.DataFrame, niche: Optional[Niche] = None) -> Dict[str, Any]:
    filtered = filter_products_by_niche(df, niche)
    n = len(filtered)

    if n == 0:
        return {
            "sample_size": 0,
            "price_metrics": {"min": 0, "q1": 0, "median": 0, "q3": 0, "max": 0, "n": 0},
            "price_bands": [],
            "rating_metrics": {"median": 0, "mean": 0, "n": 0},
            "discount_bands": {},
            "brand_metrics": {"total_brands": 0, "top_5_share": 0.0, "counts": {}, "n": 0},
            "attribute_counts": {"colours": {}, "materials": {}, "patterns": {}, "sizes": {}},
            "completeness": {},
            "attention_concentration": {"top_10_pct_review_share": 0.0, "note": "Attention concentration proxy only, not sales counts."}
        }

    # 1. Price Metrics
    prices = filtered["price"].dropna()
    p_min = float(prices.min()) if not prices.empty else 0.0
    p_max = float(prices.max()) if not prices.empty else 0.0
    p_q1 = float(prices.quantile(0.25)) if not prices.empty else 0.0
    p_median = float(prices.median()) if not prices.empty else 0.0
    p_q3 = float(prices.quantile(0.75)) if not prices.empty else 0.0

    # 2. Price Bands
    price_bands_result = []
    for pb in PRICE_BANDS:
        b_df = filtered[(filtered["price"] >= pb["min"]) & (filtered["price"] <= pb["max"])]
        b_count = len(b_df)
        b_avg_rating = round(float(b_df["rating"].mean()), 2) if b_count > 0 and not b_df["rating"].dropna().empty else 0.0
        price_bands_result.append({
            "band_name": pb["name"],
            "min_price": pb["min"],
            "max_price": pb["max"],
            "product_count": b_count,
            "avg_rating": b_avg_rating,
            "share_pct": round((b_count / n) * 100, 1)
        })

    # 3. Rating Metrics
    ratings = filtered["rating"].dropna()
    r_med = round(float(ratings.median()), 2) if not ratings.empty else 0.0
    r_mean = round(float(ratings.mean()), 2) if not ratings.empty else 0.0

    # 4. Discount Bands
    discounts = filtered["discount_pct"].dropna()
    disc_bands = {
        "0-19%": int((discounts < 20).sum()),
        "20-39%": int(((discounts >= 20) & (discounts < 40)).sum()),
        "40-59%": int(((discounts >= 40) & (discounts < 60)).sum()),
        "60%+": int((discounts >= 60).sum())
    }

    # 5. Brand Metrics
    brands = filtered["brand"].value_counts().to_dict()
    top_5_count = sum(list(brands.values())[:5])
    top_5_share = round((top_5_count / n) * 100, 1) if n > 0 else 0.0

    # 6. Attributes Counts
    colours = filtered["colour"].value_counts().to_dict()
    materials = filtered["material"].value_counts().to_dict()
    patterns = filtered["pattern"].value_counts().to_dict()

    # Sizes count
    all_sizes: Dict[str, int] = {}
    for s_val in filtered["sizes"]:
        if isinstance(s_val, list):
            for s in s_val:
                all_sizes[s] = all_sizes.get(s, 0) + 1
        elif isinstance(s_val, str) and s_val:
            for s in s_val.split(","):
                clean_s = s.strip()
                if clean_s:
                    all_sizes[clean_s] = all_sizes.get(clean_s, 0) + 1

    # 7. Completeness per field
    completeness = {}
    for col in filtered.columns:
        valid_cnt = int(filtered[col].replace(["", "Unknown", None], np.nan).dropna().count())
        completeness[col] = round((valid_cnt / n) * 100, 1)

    # 8. Review Attention Concentration (Top 10% listings' share of total reviews)
    rev_counts = filtered["review_count"].dropna().sort_values(ascending=False)
    total_reviews = float(rev_counts.sum())
    if total_reviews > 0:
        top_10_pct_n = max(1, int(np.ceil(len(rev_counts) * 0.10)))
        top_10_reviews = float(rev_counts.iloc[:top_10_pct_n].sum())
        conc_share = round((top_10_reviews / total_reviews) * 100, 1)
    else:
        conc_share = 0.0

    return {
        "sample_size": n,
        "price_metrics": {
            "min": round(p_min, 2),
            "q1": round(p_q1, 2),
            "median": round(p_median, 2),
            "q3": round(p_q3, 2),
            "max": round(p_max, 2),
            "n": n
        },
        "price_bands": price_bands_result,
        "rating_metrics": {
            "median": r_med,
            "mean": r_mean,
            "n": len(ratings)
        },
        "discount_bands": disc_bands,
        "brand_metrics": {
            "total_brands": len(brands),
            "top_5_share_pct": top_5_share,
            "top_brands": dict(list(brands.items())[:5]),
            "n": n
        },
        "attribute_counts": {
            "colours": colours,
            "materials": materials,
            "patterns": patterns,
            "sizes": all_sizes
        },
        "completeness": completeness,
        "attention_concentration": {
            "top_10_pct_review_share": conc_share,
            "note": "Attention concentration proxy only. Review counts are not sales counts."
        }
    }
