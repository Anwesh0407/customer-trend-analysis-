# Amazon Vendor Assist (AVA) — Demo Script & Presentation Guide

This guide provides a structured 5-to-10 minute presentation walkthrough of AVA, demonstrating all 8 workspaces, data evidence envelopes, and AI copilot guardrails.

---

## Preparation & Launch

1. **Start Backend & Seed Database:**
   ```bash
   python run.py pipeline
   python run.py serve --port 8000
   ```
2. **Start Frontend:**
   ```bash
   cd frontend && npm run dev
   ```
3. **Open Browser:** Navigate to `http://localhost:5173`.

---

## 1. Categories Workspace (Market Scope)
- **What to show:**
  - Active Pilot Hero Card: **"Women's Kurtas & Kurtis"** with live metrics (32 Listings Analyzed, ₹899 Median Price, 2,840 VoC Reviews).
  - Upcoming category tiles (Sarees, Men's Kurtas, Western Tops, Dupattas) marked `Coming Soon` with Category Expansion Pilot request banner.
- **What to say:**
  > *"AVA is designed for small and regional Indian marketplace vendors. Instead of overwhelming sellers with shallow generic scrapers, AVA focuses deeply on a high-velocity pilot category—Women's Kurtas & Kurtis—uncovering high-margin sourcing niches using verified marketplace observations."*

---

## 2. Define Niche Workspace (Targeted Slicing)
- **What to show:**
  - Live interactive filters: Price Range (`₹500` - `₹1,200`), Fabric (`Pure Cotton`), Pattern (`Straight`).
  - Real-time sample count preview badge showing matching listings.
  - Threshold guardrail: Adjusting filters to an overly narrow range triggers the small sample warning (< 5 listings).
- **What to say:**
  > *"Sellers can define their manufacturing constraints. AVA immediately validates statistical density—if a niche has fewer than 5 listings, AVA alerts the seller that sample size is too low to guarantee reliable commercial conclusions."*

---

## 3. Market Results Workspace (Catalog & Benchmarks)
- **What to show:**
  - Left column: Active Facet Stack with badge counts.
  - Right column: Grid vs. Table view toggle.
  - Individual product cards: Highlighting price in INR, discount badge, star rating, verified canonical sizes (`XS` to `3XL`), and `DEMO DATA` badge.
  - Click on any product card (e.g. `SYN-KUR-001`) to inspect it.
- **What to say:**
  > *"Here vendors benchmark their catalog against live listings. Notice the Table view, which exposes all 18 canonical attributes parsed and cleaned by our pipeline, including standardized size ladders."*

---

## 4. Analytics Workspace (Market Dynamics)
- **What to show:**
  - 4-Card Bento Strip: Median Price (`₹899`), Median Discount (`45%`), Leading Brand Share (`18%`), Total Reviews Cataloged (`2,840`).
  - Vertical Price Distribution Histogram: Visualizing the 4 market tiers (Budget <₹500, Mass ₹500–₹999, Mid-Premium ₹1,000–₹1,499, Premium ₹1,500+).
  - Horizontal Color Concentration Bars: Navy Blue, Mustard Yellow, and Sage Green leading.
  - Hypotheses & Merchandising Insights card.
- **What to say:**
  > *"AVA's analytics engine runs centralized statistical calculations on verified data. The Mass segment between ₹500 and ₹999 accounts for 56% of total market activity, identifying the primary volume corridor for new entrants."*

---

## 5. Reviews Workspace (Voice of Customer Diagnostics)
- **What to show:**
  - Top Net Sentiment Score Card: `+62 Net Sentiment`.
  - Segmented sentiment distribution bar (72% Positive, 18% Neutral, 10% Negative).
  - 3 Core Feedback Pillar Cards: Sizing & Fit Accuracy, Fabric Breathability & Shrinkage, Stitching & Hemming Durability.
  - "Sourcing Edge" highlights for vendor mill negotiations.
- **What to say:**
  > *"Instead of simplistic star averages, AVA synthesizes customer sentiment into actionable manufacturing specifications. Notice the negative sentiment on synthetic blends regarding post-wash shrinkage—this directly informs our cotton sourcing rule."*

---

## 6. Recommendations Workspace (Vendor Sourcing Blueprint)
- **What to show:**
  - Primary Sourcing Spec: Navy Blue Cotton Straight Kurta.
  - Recommended Price Corridor: `₹749 – ₹899` with expected gross margin guidance.
  - 30-Day Demand Trend Wave SVG sparkline.
  - Technical Textile Sourcing Specs: 60s combed cotton, reactive vat dyeing, French seams, and mandatory 3XL size inclusion.
  - "Why this?" rationale card with clickable citations.
- **What to say:**
  > *"AVA turns raw market intelligence into a production-ready sourcing spec. We highlight the 3XL size gap: 42% of customer queries search for extended sizes, but only 19% of competitor listings offer them."*

---

## 7. Product Details Workspace (Deep Diagnostic)
- **What to show:**
  - Price Diagnostic Box: Listing Price (`₹799`) vs. Niche Median (`₹899`) — ₹100 below median.
  - 4 Tabs: Canonical Specifications (18 fields grid), Size Availability Matrix, Customer Reviews list, Similar Benchmark Listings.
  - Click on a benchmark card to switch context instantly.
- **What to say:**
  > *"Vendors can conduct SKU-level diagnostics before setting prices. The diagnostic box shows exactly where a listing sits relative to its competitive cohort."*

---

## 8. Ask AVA Workspace (Zero-Hallucination AI Copilot)
- **What to show:**
  - Telemetry Grounded Scope Box in left sidebar showing Active Niche, Sample Size, Data Mode, and Tool Verifier status.
  - **Prompt 1 (Median Price):**
    - Input: *"What is the median price for kurtas in this niche?"*
    - Response: Answers `₹899` with citation to the verified evidence envelope.
  - **Prompt 2 (Size Opportunity):**
    - Input: *"What share of listings offer 3XL or larger sizes?"*
    - Response: Identifies that only 19% of listings provide 3XL, highlighting the plus-size supply deficit.
  - **Prompt 3 (Compliance Refusal Test):**
    - Input: *"How many units did Anouk sell last month?"*
    - Response: The assistant immediately refuses: *"I cannot provide competitor sales volumes or private transaction figures..."*
- **What to say:**
  > *"Ask AVA is governed by strict read-only function calling and post-generation numeric verification. It never hallucinates figures, never estimates private competitor sales, and grounds every answer in verifiable evidence."*
