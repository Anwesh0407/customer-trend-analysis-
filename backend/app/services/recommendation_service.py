from backend.app.schemas.recommendation import (
    RecommendationResponse,
    RecommendationItem,
    SourcingSpec
)

class RecommendationService:
    def get_recommendations(self) -> RecommendationResponse:
        items = [
            RecommendationItem(
                id="rec_01",
                title="Blue Cotton Floral Straight Kurtas in ₹849–₹949 Range",
                badge="High Opportunity Detected",
                confidence_pct=94,
                what_observed="Indigo Blue & Maroon floral straight kurtas in 100% breathable cotton demonstrate high rating velocity (4.4–4.6 ★) with minimal negative reviews regarding fabric thickness.",
                why_it_matters="Competitor catalog in Eastern India shows strong everyday wear demand, but only 22% seller saturation in verified pure cotton 60s count. Lower-priced alternatives receive high return penalties for thin fabric.",
                evidence_sample_size="Observed across 20 catalog sample listings, 1,200+ aggregated reviews, and median rating benchmark of 4.2 ★.",
                what_to_do="Source 100% breathable combed cotton in Indigo Blue and Maroon floral yoke prints. Stock sizes M, L, and XL first with 3/4 sleeves.",
                limitations="Market metrics reflect public listing snapshots and buyer review sentiment. Sales velocity estimates do not represent internal seller inventory or returns.",
                sourcing_specs=SourcingSpec(
                    fabric="100% Combed Cotton (60s count)",
                    test_range="₹849 – ₹949",
                    colors="Indigo Blue / Maroon",
                    priority_sizes="M, L, XL (3/4 Sleeves)"
                ),
                estimated_margin="38% – 44%"
            ),
            RecommendationItem(
                id="rec_02",
                title="Mid-Tier Price Sweet Spot Strategy (₹800–₹1,000)",
                badge="Pricing Sweet Spot",
                confidence_pct=88,
                what_observed="Sellers cluster heavily at ₹599 (budget, prone to returns for thin fabric) and ₹1,199+ (designer handloom), leaving an uncrowded sweet spot between ₹800 and ₹1,000.",
                why_it_matters="Shoppers seeking daily office/college wear are willing to pay ₹800–₹950 for guaranteed non-see-through fabric, rather than gambling on ₹500 budget synthetic blends.",
                evidence_sample_size="Based on price distribution across 4 price bands with 65% of customer dissatisfaction concentrated below ₹600.",
                what_to_do="Launch initial listing at ₹899 with an introductory 15% coupon (net ₹764) to capture price-conscious buyers while maintaining healthy gross margins.",
                limitations="Pricing power depends heavily on high-quality product photography and explicit 'non-transparent fabric' bullet points.",
                sourcing_specs=SourcingSpec(
                    fabric="Cotton / Khadi Slub",
                    test_range="₹849 – ₹899",
                    colors="Mustard Yellow / Forest Green",
                    priority_sizes="S, M, L"
                ),
                estimated_margin="35% – 40%"
            ),
            RecommendationItem(
                id="rec_03",
                title="Listing & Keyword Optimization for Transparency Concerns",
                badge="Catalog Optimization",
                confidence_pct=86,
                what_observed="Over 48% of 1-star and 2-star reviews in the budget kurta category cite 'see-through fabric', 'color bleeding on first wash', and 'armhole tightness'.",
                why_it_matters="Explicitly addressing transparency and pre-shrunk cotton in title and bullet points converts hesitant buyers and drastically reduces return rates.",
                evidence_sample_size="Review sentiment analysis across 12 product review threads totaling 15,000+ customer reviews.",
                what_to_do="Adopt title structure: 'Women's Pure Cotton Floral Straight Kurti | Non-Transparent 3/4 Sleeve Daily Wear' and include a prominent size chart with bust measurements.",
                limitations="Keywords improve click-through and reduce fit returns, but cannot compensate for actual fabric shrinkage if fabric is not pre-washed.",
                sourcing_specs=SourcingSpec(
                    fabric="Pre-shrunk Pure Cotton",
                    test_range="₹799 – ₹899",
                    colors="Multi-color prints",
                    priority_sizes="Accurate bust chart 36-44"
                ),
                estimated_margin="N/A (Listing Quality)"
            ),
            RecommendationItem(
                id="rec_04",
                title="Regional Festive Inventory Timing (Odisha & Eastern Markets)",
                badge="Seasonal Timing",
                confidence_pct=82,
                what_observed="Search queries for cotton kurtas with traditional Sambalpuri/Ikat motifs increase significantly 4 weeks ahead of regional festivals like Raja Parba and Durga Puja.",
                why_it_matters="Vendors who stock inventory 30 days prior capture organic search ranking before ad bidding costs peak during festival week.",
                evidence_sample_size="Seasonal purchasing patterns and regional festival calendar indicators.",
                what_to_do="Place fabric printing and batch production orders 4 weeks ahead. Target ready-to-ship inventory in Amazon fulfillment centers.",
                limitations="Festival timing spikes vary by year and localized logistics conditions.",
                sourcing_specs=SourcingSpec(
                    fabric="Handloom Cotton / Ikat print",
                    test_range="₹899 – ₹1,099",
                    colors="Red / Yellow / Green",
                    priority_sizes="M, L, XL, 2XL"
                ),
                estimated_margin="40% – 46%"
            )
        ]

        return RecommendationResponse(
            total_recommendations=len(items),
            items=items
        )

recommendation_service = RecommendationService()
