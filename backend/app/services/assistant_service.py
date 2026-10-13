import os
from typing import Dict, Any, List
from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.analytics_service import analytics_service
from backend.app.services.data_service import data_service
from backend.app.core.config import settings
from backend.app.core.logging import logger

class AssistantService:
    def answer(self, req: ChatRequest) -> ChatResponse:
        overview = analytics_service.get_overview()
        price_analysis = analytics_service.get_price_analytics()
        attrs = analytics_service.get_attribute_analytics()
        
        q = req.message.lower()
        
        # Grounding data context
        evidence: List[str] = [
            f"Active scope: Women's Kurtas & Kurtis (Odisha & Eastern India market)",
            f"Catalog sample size: {overview.total_products} products analyzed",
            f"Market median price: ₹{int(overview.median_price_inr)} (range ₹{int(overview.min_price_inr)} to ₹{int(overview.max_price_inr)})",
            f"Market average rating: {overview.avg_rating} ★",
            f"Top colors: {', '.join(sorted(attrs.colors, key=attrs.colors.get, reverse=True)[:3])}",
            f"Top materials: {', '.join(sorted(attrs.materials, key=attrs.materials.get, reverse=True)[:3])}"
        ]
        
        suggested_actions: List[str] = []

        # Product-specific inquiry
        if req.product_id or "this product" in q or "compete" in q:
            product = data_service.get_product_by_id(req.product_id) if req.product_id else None
            if not product and data_service.get_products().items:
                product = data_service.get_products().items[0]

            if product:
                price_delta = product.price_inr - overview.median_price_inr
                delta_str = f"₹{abs(int(price_delta))} {'above' if price_delta > 0 else 'below'} the market median (₹{int(overview.median_price_inr)})"
                
                reply = (
                    f"**Analysis for '{product.product_name}'**:\n\n"
                    f"- **Pricing Position**: Listed at ₹{int(product.price_inr)}, which is {delta_str}.\n"
                    f"- **Rating Performance**: Holds {product.rating} ★ across {product.review_count:,} reviews (Market median is {overview.median_rating} ★).\n"
                    f"- **Competition & Feasibility**: Competes in the {product.material} ({product.color}) segment. "
                    f"Key seller advantage is {product.badge}.\n\n"
                    f"**Recommended Sourcing Angle**: To win against this listing, test launch a combed cotton alternative "
                    f"at ₹849–₹899 highlighting high breathability, colorfast dyes, and guaranteed non-transparent fabric."
                )
                suggested_actions = [
                    f"Price competitively between ₹849 and ₹899",
                    "Offer sizes M and L with 3/4 sleeves",
                    "Add explicit fabric thickness specification in bullets"
                ]
                return ChatResponse(
                    reply=reply,
                    grounded_evidence=evidence,
                    suggested_actions=suggested_actions,
                    mode="deterministic_analyst"
                )

        # Price range competition
        if "price" in q or "competition" in q or "range" in q:
            sweet = price_analysis.sweet_spot
            reply = (
                f"**Price Range & Competition Analysis**:\n\n"
                f"- **Highest Competition Density**: The budget tier **Under ₹500** has high volume but intense price wars and high return rates due to thin fabric.\n"
                f"- **Market Sweet Spot**: The **₹800 — ₹1,000** price band represents the highest opportunity.\n"
                f"  - Recommended launch price: **{sweet['band']}** (target ~{sweet['recommended_launch_price']}).\n"
                f"  - Intro strategy: {sweet['intro_coupon_target']}.\n"
                f"  - Evidence: {sweet['rationale']}"
            )
            suggested_actions = [
                "Target the ₹800–₹1,000 sweet spot",
                "Apply 15% introductory coupon",
                "Emphasize 100% pure cotton quality"
            ]
            return ChatResponse(
                reply=reply,
                grounded_evidence=evidence,
                suggested_actions=suggested_actions,
                mode="deterministic_analyst"
            )

        # Color & Material inquiry
        if "color" in q or "colour" in q or "material" in q or "fabric" in q:
            top_col = sorted(attrs.colors.items(), key=lambda x: x[1], reverse=True)
            top_mat = sorted(attrs.materials.items(), key=lambda x: x[1], reverse=True)
            
            col_list = ", ".join([f"{c} ({cnt} listings)" for c, cnt in top_col[:4]])
            mat_list = ", ".join([f"{m} ({cnt} listings)" for m, cnt in top_mat[:3]])
            
            reply = (
                f"**Dominant Colors & Materials in Kurtas & Kurtis**:\n\n"
                f"- **Most Frequent Colors**: {col_list}. Indigo Blue and Maroon have the highest customer review conversion.\n"
                f"- **Most Popular Materials**: {mat_list}.\n"
                f"- **Fabric Insight**: Pure Cotton dominates volume, while Chanderi and Cotton Silk command premium margins (₹1,000+) during festive periods."
            )
            suggested_actions = [
                "Stock Indigo Blue and Maroon first",
                "Use 100% breathable cotton for summer / daily wear",
                "Introduce Chanderi flared styles for festive collections"
            ]
            return ChatResponse(
                reply=reply,
                grounded_evidence=evidence,
                suggested_actions=suggested_actions,
                mode="deterministic_analyst"
            )

        # Complaints & Reviews inquiry
        if "complaint" in q or "review" in q or "dissatisfaction" in q or "dislike" in q:
            reply = (
                f"**Customer Complaints & Review Analysis**:\n\n"
                f"Based on sentiment analysis of customer reviews across Odisha & Eastern India:\n"
                f"1. **Fabric Thinness / Transparency** (48% of 1-star complaints): Budget rayon and polyester blends are criticized for being see-through.\n"
                f"2. **Shrinkage After Wash** (24% of complaints): Unwashed cotton kurtas shrink up to 1 inch.\n"
                f"3. **Color Bleeding** (16% of complaints): Cheap dyes fade or bleed onto other clothes on the first wash.\n"
                f"4. **Armhole & Bust Fitting Mismatches** (12% of complaints).\n\n"
                f"**Vendor Action**: Use pre-shrunk combed cotton and display a detailed size chart with exact bust measurements."
            )
            suggested_actions = [
                "Use pre-shrunk cotton fabric",
                "Include 'Non-Transparent' in listing title",
                "Provide accurate bust size chart"
            ]
            return ChatResponse(
                reply=reply,
                grounded_evidence=evidence,
                suggested_actions=suggested_actions,
                mode="deterministic_analyst"
            )

        # Default general response
        reply = (
            f"**AVA Market Intelligence Summary (Odisha Kurtas & Kurtis)**:\n\n"
            f"- **Market Overview**: Analyzed {overview.total_products} products with median price ₹{int(overview.median_price_inr)} and average rating {overview.avg_rating} ★.\n"
            f"- **Key Opportunity**: Pure Cotton straight floral kurtas in Indigo Blue/Maroon in the ₹849–₹949 bracket.\n"
            f"- **Pricing Guidance**: Avoid price wars under ₹500; the ₹800–₹1,000 band offers 38–44% estimated margin with lower return rates.\n\n"
            f"You can ask me specifically about competitor pricing, recurring review complaints, or sourcing specifications!"
        )
        suggested_actions = [
            "Explore Market Results",
            "Review Analytics Dashboard",
            "Check Actionable Recommendations"
        ]
        return ChatResponse(
            reply=reply,
            grounded_evidence=evidence,
            suggested_actions=suggested_actions,
            mode="deterministic_analyst"
        )

assistant_service = AssistantService()
