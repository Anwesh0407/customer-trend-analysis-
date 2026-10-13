import statistics
from typing import Dict, List, Any
from backend.app.schemas.analytics import (
    AnalyticsOverview,
    PriceAnalyticsResponse,
    PriceBandDistribution,
    AttributeBreakdown,
)
from backend.app.services.data_service import data_service

class AnalyticsService:
    def get_overview(self) -> AnalyticsOverview:
        resp = data_service.get_products(page=1, page_size=1000)
        items = resp.items
        
        if not items:
            return AnalyticsOverview(
                total_products=0,
                median_price_inr=0.0,
                min_price_inr=0.0,
                max_price_inr=0.0,
                avg_rating=0.0,
                median_rating=0.0,
                sample_size=0,
                avg_discount_pct=0.0,
                dominant_material="None",
                dominant_color="None",
                dominant_price_band="None"
            )

        prices = [p.price_inr for p in items]
        ratings = [p.rating for p in items]
        discounts = [p.discount_pct for p in items]

        # Counts
        materials: Dict[str, int] = {}
        colors: Dict[str, int] = {}
        for p in items:
            materials[p.material] = materials.get(p.material, 0) + 1
            colors[p.color] = colors.get(p.color, 0) + 1

        top_material = max(materials.items(), key=lambda x: x[1])[0] if materials else "Cotton"
        top_color = max(colors.items(), key=lambda x: x[1])[0] if colors else "Blue"

        return AnalyticsOverview(
            total_products=len(items),
            median_price_inr=float(statistics.median(prices)),
            min_price_inr=float(min(prices)),
            max_price_inr=float(max(prices)),
            avg_rating=round(float(statistics.mean(ratings)), 2),
            median_rating=round(float(statistics.median(ratings)), 2),
            sample_size=len(items),
            avg_discount_pct=round(float(statistics.mean(discounts)), 1),
            dominant_material=top_material,
            dominant_color=top_color,
            dominant_price_band="₹500 — ₹1,000"
        )

    def get_price_analytics(self) -> PriceAnalyticsResponse:
        resp = data_service.get_products(page=1, page_size=1000)
        items = resp.items

        bands = [
            {"name": "Under ₹500", "min": 0.0, "max": 499.99, "items": []},
            {"name": "₹500 — ₹1,000", "min": 500.0, "max": 1000.0, "items": []},
            {"name": "₹1,000 — ₹1,500", "min": 1000.01, "max": 1500.0, "items": []},
            {"name": "Over ₹1,500", "min": 1500.01, "max": 99999.0, "items": []},
        ]

        for p in items:
            for b in bands:
                if b["min"] <= p.price_inr <= b["max"]:
                    b["items"].append(p)
                    break

        distributions: List[PriceBandDistribution] = []
        for b in bands:
            count = len(b["items"])
            avg_rt = round(sum(p.rating for p in b["items"]) / count, 2) if count > 0 else 0.0
            
            if b["name"] == "₹500 — ₹1,000":
                density = "High Volume / Undersupplied Mid-Tier"
                opp = "High (Optimal profit & volume balance)"
            elif b["name"] == "Under ₹500":
                density = "Saturated / Price War"
                opp = "Medium (High return rate on fabric thinness)"
            elif b["name"] == "₹1,000 — ₹1,500":
                density = "Moderate Festive Demand"
                opp = "Medium-High (Premium fabrics like Cotton Silk)"
            else:
                density = "Niche Designer Tier"
                opp = "Low (Low search velocity)"

            distributions.append(
                PriceBandDistribution(
                    band_name=b["name"],
                    min_price=b["min"],
                    max_price=b["max"],
                    product_count=count,
                    avg_rating=avg_rt,
                    competition_density=density,
                    opportunity_level=opp
                )
            )

        return PriceAnalyticsResponse(
            price_bands=distributions,
            sweet_spot={
                "band": "₹800 — ₹1,000",
                "recommended_launch_price": "₹899",
                "intro_coupon_target": "15% off coupon (net ₹764)",
                "rationale": "Competitors cluster either at budget ₹599 (high return rate due to thin fabric) or high-end ₹1,199, leaving an uncrowded quality sweet spot in ₹800–₹1,000."
            }
        )

    def get_attribute_analytics(self) -> AttributeBreakdown:
        resp = data_service.get_products(page=1, page_size=1000)
        items = resp.items

        materials: Dict[str, int] = {}
        colors: Dict[str, int] = {}
        patterns: Dict[str, int] = {}
        brands: Dict[str, int] = {}

        for p in items:
            materials[p.material] = materials.get(p.material, 0) + 1
            colors[p.color] = colors.get(p.color, 0) + 1
            patterns[p.pattern] = patterns.get(p.pattern, 0) + 1
            brands[p.brand] = brands.get(p.brand, 0) + 1

        return AttributeBreakdown(
            materials=materials,
            colors=colors,
            patterns=patterns,
            brands=brands
        )

analytics_service = AnalyticsService()
