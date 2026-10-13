"""Analytics and opportunity guardrail tests (Checklist A-01 to A-08, T-01)."""
import pandas as pd
import pytest
from ava.analytics.market import compute_market_analytics
from ava.analytics.opportunities import generate_preliminary_insights


def test_hand_computed_market_analytics():
    # 5 hand-crafted products to verify mathematical accuracy
    data = [
        {"asin": "P1", "price": 400.0, "rating": 4.0, "brand": "BrandA", "discount_pct": 10, "review_count": 100, "sizes": ["M"], "colour": "Blue", "material": "Cotton", "pattern": "Solid"},
        {"asin": "P2", "price": 600.0, "rating": 4.2, "brand": "BrandA", "discount_pct": 20, "review_count": 50, "sizes": ["L"], "colour": "Blue", "material": "Cotton", "pattern": "Printed"},
        {"asin": "P3", "price": 800.0, "rating": 4.4, "brand": "BrandB", "discount_pct": 30, "review_count": 30, "sizes": ["XL"], "colour": "Red", "material": "Rayon", "pattern": "Solid"},
        {"asin": "P4", "price": 1200.0, "rating": 4.6, "brand": "BrandC", "discount_pct": 40, "review_count": 15, "sizes": ["XXL"], "colour": "Green", "material": "Silk", "pattern": "Embroidered"},
        {"asin": "P5", "price": 2500.0, "rating": 4.8, "brand": "BrandD", "discount_pct": 50, "review_count": 5, "sizes": ["3XL"], "colour": "Black", "material": "Georgette", "pattern": "Woven"},
    ]
    df = pd.DataFrame(data)
    summary = compute_market_analytics(df)

    assert summary["sample_size"] == 5
    # Prices: 400, 600, 800, 1200, 2500 -> median is 800
    assert summary["price_metrics"]["median"] == 800.0
    assert summary["price_metrics"]["min"] == 400.0
    assert summary["price_metrics"]["max"] == 2500.0

    # Ratings: 4.0, 4.2, 4.4, 4.6, 4.8 -> median is 4.4
    assert summary["rating_metrics"]["median"] == 4.4

    # Brands: BrandA (2), BrandB (1), BrandC (1), BrandD (1) -> 4 brands
    assert summary["brand_metrics"]["total_brands"] == 4
    assert summary["brand_metrics"]["top_5_share_pct"] == 100.0

    # Review Attention Concentration
    # Total reviews = 100 + 50 + 30 + 15 + 5 = 200. Top 10% (1 listing P1) = 100 reviews = 50%
    assert summary["attention_concentration"]["top_10_pct_review_share"] == 50.0


def test_opportunity_guardrail_suppression():
    # If sample size < 30 (settings.MIN_SAMPLE_SIZE), insights must be suppressed
    small_data = [
        {"asin": f"P{i}", "price": 800.0, "rating": 4.5, "brand": "BrandA", "discount_pct": 20, "review_count": 20, "sizes": ["M"], "colour": "Blue", "material": "Cotton", "pattern": "Solid"}
        for i in range(15)
    ]
    df_small = pd.DataFrame(small_data)
    opps = generate_preliminary_insights(df_small)

    assert opps["insights_suppressed"] is True
    assert opps["insights"] == []
    assert "below minimum statistical threshold" in opps["reason"]


def test_confidence_labels_never_high():
    # Synthesize >= 30 items to trigger insights and check confidence levels
    data = []
    for i in range(35):
        data.append({
            "asin": f"SYN-{i:03d}",
            "price": 850.0 if i < 10 else 1200.0,
            "rating": 4.5 if i < 10 else 3.8,
            "brand": f"Brand_{i % 5}",
            "discount_pct": 65 if i < 8 else 30,
            "review_count": 500 if i == 0 else 10,
            "sizes": ["M", "L", "3XL"] if i < 2 else ["M", "L"],
            "colour": "Navy",
            "material": "Cotton" if i < 8 else "Rayon",
            "pattern": "Solid",
        })
    df = pd.DataFrame(data)
    opps = generate_preliminary_insights(df)

    assert opps["insights_suppressed"] is False
    for insight in opps["insights"]:
        # Rule: Confidence labels only 'very_low', 'low', 'moderate' - NEVER 'high'
        assert insight["confidence"] in ("very_low", "low", "moderate")
        assert insight["confidence"] != "high"
        # Observation and hypothesis both present
        assert "observation" in insight
        assert "hypothesis" in insight
        assert "sample_size" in insight
