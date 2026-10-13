"""
Machine Learning and Opportunity Scoring Module for AVA
Provides clean interface isolating rule-based scoring and future trained ML models.
"""

from typing import Dict, Any, List

class BaseOpportunityModel:
    """Interface for opportunity scoring models."""
    def score_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError

class RuleBasedOpportunityModel(BaseOpportunityModel):
    """
    Transparent rule-based scoring module.
    Evaluates price competitiveness, rating velocity, and material demand.
    Does not claim statistical causation; generates actionable baseline confidence.
    """
    def score_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        price = float(product.get("price_inr", 0))
        rating = float(product.get("rating", 0))
        reviews = int(product.get("review_count", 0))
        material = str(product.get("material", "")).lower()

        score = 50.0  # Baseline

        # Sweet spot price scoring (₹800 - ₹1,000)
        if 800 <= price <= 1000:
            score += 25.0
        elif 500 <= price < 800:
            score += 10.0
        elif price < 500:
            # Low price has return penalty
            score -= 10.0

        # Quality rating
        if rating >= 4.3:
            score += 15.0
        elif rating >= 4.0:
            score += 5.0
        elif rating < 3.8:
            score -= 15.0

        # Proven review volume
        if reviews >= 1000:
            score += 10.0

        # High-demand natural fabrics
        if "cotton" in material or "khadi" in material:
            score += 10.0

        score = max(0.0, min(100.0, score))

        if score >= 80:
            level = "High"
            badge = "High Opportunity"
        elif score >= 65:
            level = "Medium-High"
            badge = "Rising"
        elif score >= 50:
            level = "Medium"
            badge = "Standard"
        else:
            level = "Low"
            badge = "High Competition"

        return {
            "score": round(score, 1),
            "opportunity_level": level,
            "badge": badge,
            "model_version": "v1.0-rule-based-baseline"
        }

opportunity_model = RuleBasedOpportunityModel()
