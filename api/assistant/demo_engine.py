"""Offline-safe deterministic demo fallback engine for Ask AVA."""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from ava.config import get_settings
from ava.storage.base import Repository
from api.assistant.tools import execute_tool
from api.envelope import DEFAULT_LIMITATIONS
from api.schemas import AskQuestionResponse, EvidenceItem


def answer_demo_question(
    question: str,
    repo: Repository,
    niche_filter: Optional[Dict[str, Any]] = None,
    niche_name: str = "All Listings",
    category: Optional[str] = "Women's Kurtas & Kurtis",
    session_id: Optional[str] = None,
) -> AskQuestionResponse:
    q_lower = question.lower().strip()
    prods = repo.get_all_products_for_niche(category=category, niche_filter=niche_filter)
    sample_size = len(prods)
    min_thresh = get_settings().MIN_SAMPLE_SIZE

    evidence: List[EvidenceItem] = []
    estimates: List[str] = []
    follow_ups: List[str] = [
        "What is the most populated price band?",
        "What are the top market opportunities?",
        "Which colours and materials are most common?",
        "What share of listings offer 3XL+ sizes?",
    ]

    # Check for low sample size
    if sample_size < min_thresh:
        answer = (
            f"The current sample size for '{niche_name}' is {sample_size} listings, which is below "
            f"our statistical reliability threshold of {min_thresh}. Empirical insights and distributional metrics "
            f"are suppressed to prevent skewed conclusions. Please select a broader niche or import additional catalog listings."
        )
        return AskQuestionResponse(
            answer=answer,
            evidence=[
                EvidenceItem(
                    metric="sample_size",
                    value=sample_size,
                    sample_size=sample_size,
                    source_tool="get_market_summary",
                    niche=niche_name,
                )
            ],
            estimates_labeled=[],
            limitations=list(DEFAULT_LIMITATIONS),
            follow_up_suggestions=["Switch to 'All Listings' category overview to see full market benchmarks."],
            mode="demo",
            session_id=session_id,
        )

    # 1. Median price / Price distribution
    if any(k in q_lower for k in ["median price", "average price", "price range", "pricing benchmark"]):
        res = execute_tool("get_market_summary", {}, repo, niche_filter, niche_name, category)
        d = res["data"]
        answer = (
            f"Across {d['sample_size']} observed listings in '{niche_name}', the median price is ₹{d['median_price']}. "
            f"Listings range from ₹{d['min_price']} to ₹{d['max_price']}."
        )
        evidence.append(
            EvidenceItem(
                metric="median_price",
                value=f"₹{d['median_price']}",
                sample_size=d["sample_size"],
                source_tool="get_market_summary",
                niche=niche_name,
            )
        )
        return AskQuestionResponse(
            answer=answer,
            evidence=evidence,
            estimates_labeled=[],
            limitations=list(DEFAULT_LIMITATIONS),
            follow_up_suggestions=follow_ups,
            mode="demo",
            session_id=session_id,
        )

    # 2. Most populated price band
    if any(k in q_lower for k in ["most populated", "price band", "popular price", "price distribution"]):
        res = execute_tool("get_price_bands", {}, repo, niche_filter, niche_name, category)
        d = res["data"]
        band = d["most_populated_band"]
        cnt = d["most_populated_count"]
        answer = (
            f"The most populated price band in this niche is ₹{band}, containing {cnt} of {res['sample_size']} listings. "
            f"Vendors heavily target this tier, creating significant competition on catalog visibility."
        )
        evidence.append(
            EvidenceItem(
                metric="most_populated_band",
                value=f"{band} ({cnt} listings)",
                sample_size=res["sample_size"],
                source_tool="get_price_bands",
                niche=niche_name,
            )
        )
        return AskQuestionResponse(
            answer=answer,
            evidence=evidence,
            estimates_labeled=["Hypothesis: Heavy seller clustering in this band indicates proven demand but requires differentiation on fabric."],
            limitations=list(DEFAULT_LIMITATIONS),
            follow_up_suggestions=follow_ups,
            mode="demo",
            session_id=session_id,
        )

    # 3. Brands and leadership
    if any(k in q_lower for k in ["brand", "leader", "competitor"]):
        res = execute_tool("get_brand_and_attribute_counts", {"attribute_type": "brands"}, repo, niche_filter, niche_name, category)
        m_res = execute_tool("get_market_summary", {}, repo, niche_filter, niche_name, category)
        d = res["data"]
        top_b = list(d["top_brands"].keys())[:3]
        top_share = m_res["data"]["top_5_brand_share_pct"]
        answer = (
            f"There are {d['total_brands']} distinct brands observed across {res['sample_size']} listings. "
            f"Leading brands by listing count include {', '.join(top_b)}. "
            f"The top 5 brands account for {top_share}% of observed catalog listings."
        )
        evidence.append(
            EvidenceItem(
                metric="brand_concentration",
                value=f"{top_share}% top 5 share across {d['total_brands']} brands",
                sample_size=res["sample_size"],
                source_tool="get_brand_and_attribute_counts",
                niche=niche_name,
            )
        )
        return AskQuestionResponse(
            answer=answer,
            evidence=evidence,
            estimates_labeled=["Observation: Brand catalog share reflects active listing count, not actual revenue or unit sales."],
            limitations=list(DEFAULT_LIMITATIONS),
            follow_up_suggestions=follow_ups,
            mode="demo",
            session_id=session_id,
        )

    # 4. Colours and materials
    if any(k in q_lower for k in ["colour", "color", "material", "fabric", "pattern"]):
        res = execute_tool("get_brand_and_attribute_counts", {}, repo, niche_filter, niche_name, category)
        d = res["data"]
        top_cols = list(d["top_colours"].keys())[:3]
        top_mats = list(d["top_materials"].keys())[:3]
        answer = (
            f"In this niche (n={res['sample_size']}), the most prominent colours are {', '.join(top_cols)}. "
            f"The predominant materials are {', '.join(top_mats)}, with Cotton maintaining high review ratings."
        )
        evidence.append(
            EvidenceItem(
                metric="top_colours_and_materials",
                value=f"Colours: {', '.join(top_cols)}; Materials: {', '.join(top_mats)}",
                sample_size=res["sample_size"],
                source_tool="get_brand_and_attribute_counts",
                niche=niche_name,
            )
        )
        return AskQuestionResponse(
            answer=answer,
            evidence=evidence,
            estimates_labeled=[],
            limitations=list(DEFAULT_LIMITATIONS),
            follow_up_suggestions=follow_ups,
            mode="demo",
            session_id=session_id,
        )

    # 5. Share of 3XL+ extended sizes
    if any(k in q_lower for k in ["3xl", "extended size", "plus size", "sizes"]):
        res = execute_tool("get_brand_and_attribute_counts", {}, repo, niche_filter, niche_name, category)
        d = res["data"]
        cnt = d["listings_offering_3xl_plus"]
        pct = d["share_offering_3xl_plus_pct"]
        answer = (
            f"Only {cnt} listings ({pct}%) in '{niche_name}' (n={res['sample_size']}) explicitly offer sizes 3XL or larger. "
            f"This represents an underserved product gap in regional ethnic wear merchandising."
        )
        evidence.append(
            EvidenceItem(
                metric="3xl_coverage",
                value=f"{pct}% ({cnt} listings)",
                sample_size=res["sample_size"],
                source_tool="get_brand_and_attribute_counts",
                niche=niche_name,
            )
        )
        return AskQuestionResponse(
            answer=answer,
            evidence=evidence,
            estimates_labeled=["Hypothesis: Sizing coverage gap creates potential for vendors offering verified 3XL+ chest fits."],
            limitations=list(DEFAULT_LIMITATIONS),
            follow_up_suggestions=follow_ups,
            mode="demo",
            session_id=session_id,
        )

    # 6. Customer reviews
    if any(k in q_lower for k in ["review", "rating", "customer feedback"]):
        res = execute_tool("get_review_summary", {}, repo, niche_filter, niche_name, category)
        d = res["data"]
        answer = (
            f"We have collected {d['total_reviews']} customer reviews across {res['sample_size']} listings in '{niche_name}'. "
            f"The average review rating is {d['average_rating']} ★, with {d['coverage_pct']}% of niche products currently having reviews."
        )
        evidence.append(
            EvidenceItem(
                metric="reviews_summary",
                value=f"{d['total_reviews']} reviews, avg {d['average_rating']} ★",
                sample_size=res["sample_size"],
                source_tool="get_review_summary",
                niche=niche_name,
            )
        )
        return AskQuestionResponse(
            answer=answer,
            evidence=evidence,
            estimates_labeled=["Note: Review counts represent customer attention and feedback, not unit sales volumes."],
            limitations=list(DEFAULT_LIMITATIONS),
            follow_up_suggestions=follow_ups,
            mode="demo",
            session_id=session_id,
        )

    # 7. Opportunities
    if any(k in q_lower for k in ["opportunity", "recommend", "insights", "sweet spot"]):
        res = execute_tool("get_opportunities", {}, repo, niche_filter, niche_name, category)
        d = res["data"]
        opps = d.get("insights", [])
        if opps:
            top_titles = [f"{o['title']} ({o['confidence']} confidence)" for o in opps[:3]]
            answer = (
                f"We identified {len(opps)} rule-based opportunities for '{niche_name}' (n={res['sample_size']}): "
                f"{'; '.join(top_titles)}. "
                f"Each recommendation is rule-based and transparent."
            )
        else:
            answer = f"No active opportunities identified for '{niche_name}' with sample size n={res['sample_size']}."

        evidence.append(
            EvidenceItem(
                metric="opportunities_count",
                value=len(opps),
                sample_size=res["sample_size"],
                source_tool="get_opportunities",
                niche=niche_name,
            )
        )
        return AskQuestionResponse(
            answer=answer,
            evidence=evidence,
            estimates_labeled=["Every opportunity is a hypothesis for vendor investigation, never a guarantee of future sales."],
            limitations=list(DEFAULT_LIMITATIONS),
            follow_up_suggestions=follow_ups,
            mode="demo",
            session_id=session_id,
        )

    # 8. Specific ASIN lookup
    asin_match = re.search(r'\b([A-Z0-9]{10}|SYN-[A-Z0-9\-]+)\b', question.upper())
    if asin_match:
        target_asin = asin_match.group(1)
        res = execute_tool("lookup_product_by_asin", {"asin": target_asin}, repo, niche_filter, niche_name, category)
        d = res["data"]
        if d.get("found"):
            p = d["product"]
            answer = (
                f"Product {p['asin']} ('{p['product_name']}') is listed at ₹{p['price']} "
                f"(MRP: ₹{p.get('mrp', 'N/A')}, discount: {p.get('discount_pct', 0)}%) "
                f"with a rating of {p.get('rating', 'unrated')} ★ and {p.get('review_count', 0)} reviews."
            )
            evidence.append(
                EvidenceItem(
                    metric="asin_lookup",
                    value=f"{p['asin']} @ ₹{p['price']}",
                    sample_size=1,
                    source_tool="lookup_product_by_asin",
                    niche=niche_name,
                )
            )
            return AskQuestionResponse(
                answer=answer,
                evidence=evidence,
                estimates_labeled=[],
                limitations=list(DEFAULT_LIMITATIONS),
                follow_up_suggestions=follow_ups,
                mode="demo",
                session_id=session_id,
            )

    # Default fallback overview
    res = execute_tool("get_market_summary", {}, repo, niche_filter, niche_name, category)
    d = res["data"]
    answer = (
        f"In '{niche_name}' (sample size n={d['sample_size']}), the median price is ₹{d['median_price']} "
        f"and median rating is {d['median_rating']} ★ across {d['total_brands']} brands. "
        f"You can ask about price bands, fabric materials, sizing gaps (3XL+), or market opportunities."
    )
    evidence.append(
        EvidenceItem(
            metric="market_overview",
            value=f"Median price ₹{d['median_price']}",
            sample_size=d["sample_size"],
            source_tool="get_market_summary",
            niche=niche_name,
        )
    )
    return AskQuestionResponse(
        answer=answer,
        evidence=evidence,
        estimates_labeled=[],
        limitations=list(DEFAULT_LIMITATIONS),
        follow_up_suggestions=follow_ups,
        mode="demo",
        session_id=session_id,
    )
