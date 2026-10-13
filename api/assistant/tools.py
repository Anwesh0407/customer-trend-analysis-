"""Whitelist of read-only analytic tools available to Ask AVA.

All numbers served to Gemini or the demo engine originate from these verified functions.
"""
from __future__ import annotations

import pandas as pd
from typing import Any, Dict, List, Optional

from ava.analytics.market import compute_market_analytics
from ava.analytics.opportunities import generate_preliminary_insights
from ava.analytics.reviews import compute_reviews_summary
from ava.models import Review
from ava.storage.base import Repository

TOOL_DEFINITIONS = [
    {
        "name": "get_market_summary",
        "description": "Fetch overall market metrics for the current niche: sample size (n), median price, quartiles, median rating, top 5 brand share, and review attention concentration.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "get_price_bands",
        "description": "Fetch distribution of listings across price bands (0-499, 500-999, 1000-1499, 1500-1999, 2000-2999, 3000+) including product counts, share %, and average rating per band.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "get_brand_and_attribute_counts",
        "description": "Fetch brand counts, leader brands, and listing counts for colours, materials, patterns, and sizes (including 3XL+ extended sizes).",
        "parameters": {
            "type": "object",
            "properties": {
                "attribute_type": {
                    "type": "string",
                    "description": "Specific attribute to query: 'colours', 'materials', 'patterns', 'sizes', 'brands', or 'all'",
                    "enum": ["colours", "materials", "patterns", "sizes", "brands", "all"],
                }
            },
        },
    },
    {
        "name": "get_opportunities",
        "description": "Fetch rule-based market preliminary insights: undersupplied price bands, quality gaps, fabric sentiment, extended size coverage, discount prevalence, or review concentration.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "get_review_summary",
        "description": "Fetch review metrics: total reviews collected, average star rating, rating distribution (1-5 stars), and percentage of niche listings with reviews.",
        "parameters": {
            "type": "object",
            "properties": {
                "asin": {
                    "type": "string",
                    "description": "Optional specific product ASIN to inspect reviews for.",
                }
            },
        },
    },
    {
        "name": "lookup_product_by_asin",
        "description": "Fetch full product details for a specific 10-character ASIN: title, brand, price, mrp, discount, rating, review count, colour, material, and availability.",
        "parameters": {
            "type": "object",
            "properties": {
                "asin": {
                    "type": "string",
                    "description": "The exact 10-character ASIN of the product.",
                }
            },
            "required": ["asin"],
        },
    },
]


def execute_tool(
    tool_name: str,
    args: Dict[str, Any],
    repo: Repository,
    niche_filter: Optional[Dict[str, Any]] = None,
    niche_name: str = "All Listings",
    category: Optional[str] = "Women's Kurtas & Kurtis",
) -> Dict[str, Any]:
    """Executes a whitelisted tool and returns structured data with sample sizes."""
    prods = repo.get_all_products_for_niche(category=category, niche_filter=niche_filter)
    sample_size = len(prods)
    df = pd.DataFrame(prods) if prods else pd.DataFrame()

    if tool_name == "get_market_summary":
        summary = compute_market_analytics(df, niche=None)
        return {
            "tool": tool_name,
            "niche": niche_name,
            "sample_size": sample_size,
            "data": {
                "sample_size": summary["sample_size"],
                "median_price": summary["price_metrics"]["median"],
                "min_price": summary["price_metrics"]["min"],
                "max_price": summary["price_metrics"]["max"],
                "median_rating": summary["rating_metrics"]["median"],
                "mean_rating": summary["rating_metrics"]["mean"],
                "top_5_brand_share_pct": summary["brand_metrics"]["top_5_share_pct"],
                "total_brands": summary["brand_metrics"]["total_brands"],
                "attention_concentration_pct": summary["attention_concentration"]["top_10_pct_review_share"],
            },
        }

    elif tool_name == "get_price_bands":
        summary = compute_market_analytics(df, niche=None)
        bands = summary["price_bands"]
        most_populated = max(bands, key=lambda b: b["product_count"]) if bands else None
        return {
            "tool": tool_name,
            "niche": niche_name,
            "sample_size": sample_size,
            "data": {
                "price_bands": bands,
                "most_populated_band": most_populated["band_name"] if most_populated else None,
                "most_populated_count": most_populated["product_count"] if most_populated else 0,
            },
        }

    elif tool_name == "get_brand_and_attribute_counts":
        summary = compute_market_analytics(df, niche=None)
        attrs = summary["attribute_counts"]
        brands = summary["brand_metrics"]["top_brands"]
        total_brands = summary["brand_metrics"]["total_brands"]
        plus_sizes_count = attrs["sizes"].get("3XL", 0) + attrs["sizes"].get("4XL", 0)
        plus_share_pct = round((plus_sizes_count / sample_size) * 100, 1) if sample_size > 0 else 0.0

        return {
            "tool": tool_name,
            "niche": niche_name,
            "sample_size": sample_size,
            "data": {
                "total_brands": total_brands,
                "top_brands": brands,
                "top_colours": dict(list(attrs["colours"].items())[:5]),
                "top_materials": dict(list(attrs["materials"].items())[:5]),
                "top_patterns": dict(list(attrs["patterns"].items())[:5]),
                "sizes": attrs["sizes"],
                "listings_offering_3xl_plus": plus_sizes_count,
                "share_offering_3xl_plus_pct": plus_share_pct,
            },
        }

    elif tool_name == "get_opportunities":
        opps = generate_preliminary_insights(df, niche=None)
        return {
            "tool": tool_name,
            "niche": niche_name,
            "sample_size": sample_size,
            "data": opps,
        }

    elif tool_name == "get_review_summary":
        target_asin = args.get("asin")
        clean_asin = target_asin.strip().upper() if target_asin else None

        if clean_asin:
            raw_revs, _ = repo.get_reviews(asin=clean_asin, limit=500)
            target_asins = [clean_asin]
        else:
            raw_revs, _ = repo.get_reviews(category=category, limit=500)
            target_asins = [p["asin"] for p in prods]

        rev_objs = []
        for r in raw_revs:
            try:
                rev_objs.append(
                    Review(
                        review_id=r["review_id"],
                        product_id=r["product_id"],
                        rating=int(r["rating"]),
                        review_title=r.get("review_title") or "",
                        review_text=r.get("review_text") or "",
                        review_date=r.get("review_date") or "",
                        source=r.get("source", "file"),
                        collected_at=r.get("collected_at") or "",
                    )
                )
            except Exception:
                pass

        rev_summary = compute_reviews_summary(rev_objs, niche_asins=target_asins)
        return {
            "tool": tool_name,
            "niche": niche_name,
            "sample_size": sample_size,
            "data": {
                "total_reviews": rev_summary["total_reviews"],
                "average_rating": rev_summary["average_rating"],
                "rating_distribution": rev_summary["rating_distribution"],
                "coverage_pct": rev_summary["niche_coverage_pct"],
                "products_with_reviews": rev_summary["products_with_reviews_count"],
            },
        }

    elif tool_name == "lookup_product_by_asin":
        asin = args.get("asin", "").strip().upper()
        prod = repo.get_product_by_asin(asin)
        if not prod:
            return {
                "tool": tool_name,
                "niche": niche_name,
                "sample_size": sample_size,
                "data": {"found": False, "asin": asin, "message": f"Product with ASIN {asin} was not found in the catalog."},
            }
        return {
            "tool": tool_name,
            "niche": niche_name,
            "sample_size": sample_size,
            "data": {"found": True, "product": prod},
        }

    else:
        raise ValueError(f"Unknown tool '{tool_name}'")
