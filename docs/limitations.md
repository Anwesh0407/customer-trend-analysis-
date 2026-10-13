# Amazon Vendor Assist (AVA) — System Limitations & Data Disclaimers

This document transparently outlines the analytical scope, data boundaries, compliance invariants, and operational limitations of the AVA platform.

---

## 1. Non-Random Snapshot Limitations

Marketplace data analyzed by AVA represents point-in-time observational snapshots of publicly accessible search result listings within the pilot taxonomy ("Women's Kurtas & Kurtis").
- **Observational, Not Censused:** Search ranking algorithms, geo-targeted inventory availability, and promotional rotations mean that listings retrieved in any given snapshot reflect algorithmic relevance rather than an exhaustive census of all products ever listed.
- **Survivor & Visibility Bias:** Higher-ranked and active items are systematically over-represented compared to dormant or out-of-stock listings.

---

## 2. No Competitor Sales or Private Financial Data

AVA explicitly does **not** provide, estimate, or fabricate private vendor or marketplace financial data:
- **No Unit Sales:** AVA does not claim to know the number of units sold for any competitor listing.
- **No Revenue or GMV:** Competitor sales turnover, gross merchandise value (GMV), profit margins, or ad spend are completely inaccessible from public listings.
- **Refusal Guarantee:** The AI assistant (Ask AVA) is governed by strict system prompts and tool whitelists that unconditionally refuse queries soliciting competitor sales volumes, private turnover, or vendor margins.

---

## 3. Review Counts Are Not Unit Sales (Engagement Proxy Only)

- **Review Rate Variance:** On major marketplaces like Amazon, the review-to-purchase ratio typically varies between 0.5% and 3.0% depending on subcategory, brand reputation, price point, and customer demographics.
- **Observation Proxy:** In AVA, `review_count` is treated strictly as an **observation volume proxy** for customer engagement, product longevity, and relative market attention. It must never be multiplied by an arbitrary conversion constant to claim actual sales.

---

## 4. Synthetic Sample Data & Demo Environment Disclaimers

To enable fully reproducible, safe testing and demonstration without violating marketplace terms or publishing copyrighted assets:
- **Synthetic ASINs:** All demo product records use synthetic identifiers prefixed with `SYN-` (e.g., `SYN-KUR-001` through `SYN-KUR-032`).
- **Sanitized URLs:** Product URLs link to RFC 2606 reserved domains (`https://example.com/dp/{asin}`).
- **Visual Banners:** All UI workspaces display persistent `DEMO DATA` and `OBSERVATION PROXY` badges.
- **Single Source of Truth:** Synthetic distributions are statistically calibrated against realistic apparel market dynamics (cotton dominance, ₹600–₹1,200 sweet spot, 3XL size supply gap) to provide actionable merchandising heuristics.

---

## 5. Domain Blocking & Compliance Invariants

- **Domain Denylist:** `ava.http_client` hard-blocks outbound HTTP requests to `amazon.in`, `amazon.com`, `media-amazon.com`, and related domains.
- **No Unauthorized Live Scraping:** The system relies strictly on authorized ingestion sources: offline CSV/JSON imports, official Creator/Vendor APIs, and public pages complying with `robots.txt`.
- **Immediate Abort:** If any collector encounters an HTTP `401`, `403`, or CAPTCHA challenge, ingestion halts immediately without brute-force retries.

---

## 6. AI Assistant Grounding & Zero Hallucination Protocol

The Ask AVA copilot operates under the following verifiable guardrails:
1. **Tool-Grounded Context:** The assistant only accesses data through read-only analytic tools (`get_niche_summary`, `get_top_products`, `get_opportunities`, `get_review_summary`).
2. **Numeric Verification Filter:** An automated post-generation verifier extracts all numerical figures (percentages, prices, listing counts) from the LLM response and validates them against the tool telemetry envelope. If an ungrounded or invented metric is detected, the response is rejected and replaced with verified fallback analytics.
3. **Small Sample Size Suppression:** When a defined niche contains fewer than 5 listings, automated opportunity scoring and high-confidence recommendations are suppressed, alerting the vendor that sample density is insufficient for statistically valid deductions.
4. **Confidence Ceiling:** Because data is observational, confidence levels in AVA are capped at `Medium` or `Low`—never `High`—to remind vendors that market experimentation remains essential.
