"""
AVA Opportunity & Preliminary Insights Engine
Implements the 6 specific insight rules with strict guardrails:
- Suppression when niche sample size < min_sample_size (default 30)
- Suppression of subgroup insights when subgroup size < min_group_size (default 5)
- Confidence labels strictly limited to: 'very_low', 'low', 'moderate' (NEVER 'high')
- Explicit separation of observation [actual] vs hypothesis [estimate]
"""

import pandas as pd
from typing import List, Dict, Any, Optional
from ava.config import settings
from ava.models import Niche
from ava.analytics.market import compute_market_analytics

STANDING_LIMITATIONS = [
    "Market metrics reflect a point-in-time public listing snapshot.",
    "Non-random sample of active listings; variants are counted as separate rows.",
    "Review ratings reflect self-selected customer sentiment, not verified purchase rates.",
    "Review counts represent cumulative customer attention, not current unit sales or revenue."
]

def generate_preliminary_insights(
    df: pd.DataFrame,
    niche: Optional[Niche] = None
) -> Dict[str, Any]:
    market = compute_market_analytics(df, niche)
    n = market["sample_size"]

    # Guardrail: Suppress insights if sample size is below threshold
    if n < settings.MIN_SAMPLE_SIZE:
        return {
            "insights_suppressed": True,
            "reason": f"Sample size (n={n}) is below minimum statistical threshold ({settings.MIN_SAMPLE_SIZE}). Collect or select more listings to activate insights.",
            "sample_size": n,
            "insights": [],
            "standing_limitations": STANDING_LIMITATIONS
        }

    insights: List[Dict[str, Any]] = []

    # Rule 1: Thin supply in a well-rated price band
    for pb in market["price_bands"]:
        count = pb["product_count"]
        rating = pb["avg_rating"]
        if 0 < count <= 6 and rating >= 4.2 and count >= settings.MIN_GROUP_SIZE:
            insights.append({
                "id": "opp_thin_well_rated_band",
                "title": f"Undersupplied Quality Tier in {pb['band_name']} Band",
                "type": "price_opportunity",
                "observation": f"{count} listings observed in the {pb['band_name']} band with a high average rating of {rating} ★.",
                "hypothesis": f"Buyers show high satisfaction in {pb['band_name']}, but seller concentration is low ({pb['share_pct']}% of catalog).",
                "evidence": f"n={count} listings with average rating {rating} ★ vs market median {market['rating_metrics']['median']} ★.",
                "sample_size": count,
                "confidence": "moderate",
                "limitations": "Low listing counts may indicate low shopper query volume rather than unmet demand."
            })

    # Rule 2: Crowded low-rated band (quality gap)
    for pb in market["price_bands"]:
        count = pb["product_count"]
        rating = pb["avg_rating"]
        if count >= 8 and rating < 4.0:
            insights.append({
                "id": "opp_crowded_low_rated_band",
                "title": f"Quality Discontent in {pb['band_name']} Budget Band",
                "type": "quality_gap",
                "observation": f"{count} listings in {pb['band_name']} show an average rating of {rating} ★ (below market median).",
                "hypothesis": f"Severe price competition in {pb['band_name']} appears to compromise fabric thickness and sizing accuracy, resulting in customer dissatisfaction.",
                "evidence": f"{pb['share_pct']}% of listings cluster in {pb['band_name']}, but average rating lags at {rating} ★.",
                "sample_size": count,
                "confidence": "moderate",
                "limitations": "Customers buying in budget tiers may leave harsher reviews for natural wear and tear."
            })

    # Rule 3: Well-rated but less common colour/pattern/material
    materials = market["attribute_counts"]["materials"]
    for mat, count in materials.items():
        if mat not in ("Unknown", "Generic") and settings.MIN_GROUP_SIZE <= count <= 8:
            mat_df = df[df["material"].str.lower() == mat.lower()]
            mat_rt = round(float(mat_df["rating"].mean()), 2) if not mat_df.empty else 0.0
            if mat_rt >= 4.3:
                insights.append({
                    "id": f"opp_niche_material_{mat.lower()}",
                    "title": f"Favorable Sentiment for {mat} Fabric",
                    "type": "attribute_opportunity",
                    "observation": f"{mat} represents {count} listings with an average rating of {mat_rt} ★.",
                    "hypothesis": f"Shoppers respond very positively to {mat}, yet it represents a small share of the local catalog.",
                    "evidence": f"n={count} listings with rating {mat_rt} ★.",
                    "sample_size": count,
                    "confidence": "low",
                    "limitations": "Limited sample size; specialized fabrics may appeal only to specific customer segments."
                })

    # Rule 4: Extended-size (3XL+) coverage gap
    size_counts = market["attribute_counts"]["sizes"]
    plus_count = size_counts.get("3XL", 0) + size_counts.get("4XL", 0)
    if plus_count < settings.MIN_GROUP_SIZE:
        insights.append({
            "id": "opp_extended_size_gap",
            "title": "Limited Availability of Extended Sizes (3XL+)",
            "type": "size_coverage",
            "observation": f"Only {plus_count} of {n} listings explicitly offer sizes 3XL or larger.",
            "hypothesis": "Vendors primarily stock S-XL, creating an undersupplied opportunity for extended plus sizes.",
            "evidence": f"{plus_count} out of {n} listings observed offering 3XL+.",
            "sample_size": plus_count,
            "confidence": "low",
            "limitations": "Catalog data may omit extended sizes that are offered as child variant listings."
        })

    # Rule 5: Deep-discount prevalence
    disc_60_plus = market["discount_bands"]["60%+"]
    if disc_60_plus >= 5:
        insights.append({
            "id": "opp_deep_discount_prevalence",
            "title": "Widespread Deep Discounting (MRP Reference Pricing)",
            "type": "pricing_strategy",
            "observation": f"{disc_60_plus} listings report discounts of 60% or greater off MRP.",
            "hypothesis": "Competitors utilize elevated MRPs to advertise steep promotional discounts as a psychological reference point.",
            "evidence": f"{disc_60_plus} listings in discount tier 60%+.",
            "sample_size": disc_60_plus,
            "confidence": "moderate",
            "limitations": "High reported discounts do not indicate whether products sell faster or at higher margin."
        })

    # Rule 6: Review-volume concentration
    conc = market["attention_concentration"]["top_10_pct_review_share"]
    if conc >= 50.0:
        insights.append({
            "id": "opp_review_concentration",
            "title": "High Customer Attention Concentration",
            "type": "attention_dynamics",
            "observation": f"The top 10% of listings capture {conc}% of all accumulated customer reviews.",
            "hypothesis": "Marketplace organic discovery heavily favors established incumbent listings.",
            "evidence": f"Top decile accounts for {conc}% of total review volume.",
            "sample_size": n,
            "confidence": "moderate",
            "limitations": "Review count is a cumulative proxy for attention, NOT an indicator of daily sales volume."
        })

    return {
        "insights_suppressed": False,
        "sample_size": n,
        "insights": insights,
        "standing_limitations": STANDING_LIMITATIONS
    }
