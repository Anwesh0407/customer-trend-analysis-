# Amazon Vendor Assist (AVA) — Data Dictionary

This document defines the canonical schema, attribute specifications, validation rules, and allowable ranges for all data entities handled by the AVA pipeline, database, analytics engine, and API.

---

## 1. Product Attributes (Canonical 18 Fields)

Every product record in AVA strictly conforms to the following 18 canonical attributes. No ad-hoc fields are permitted in the core storage layer.

| # | Attribute Name | Data Type | Nullable | Default | Description & Constraints | Example Value |
|---|---|---|:---:|:---:|---|---|
| 1 | `asin` | `VARCHAR(32)` | No | — | Unique 10-character alphanumeric identifier. In synthetic demo mode, prefixed with `SYN-` (e.g. `SYN-KUR-001`). Primary key. | `"SYN-KUR-001"` |
| 2 | `product_name` | `VARCHAR(512)` | No | — | Canonical title of the product listing. Stripped of excess whitespace and control characters. Must be 3–512 characters. | `"Anouk Floral Straight Pure Cotton Kurta"` |
| 3 | `category` | `VARCHAR(128)` | No | — | Marketplace category node. Currently scoped to pilot category: `"Women's Kurtas & Kurtis"`. | `"Women's Kurtas & Kurtis"` |
| 4 | `brand` | `VARCHAR(128)` | No | — | Normalized brand or label name. Cleaned of "Visit the X Store" or promotional prefixes. | `"Anouk"` |
| 5 | `price` | `FLOAT` | No | — | Current selling price in Indian Rupees (INR). Must be positive (> 0) and realistically capped (<= ₹50,000 for apparel). Parsed from currency symbols (`₹`, `Rs.`). | `799.0` |
| 6 | `mrp` | `FLOAT` | Yes | `None` | Maximum Retail Price / List Price in INR. Must be `>= price`. If `mrp < price`, it is invalidated to `null` and flagged. | `1599.0` |
| 7 | `discount_pct` | `FLOAT` | Yes | `None` | Derived discount percentage: `round((mrp - price) / mrp * 100, 1)`. Recomputed by pipeline; if source differs by > 2%, computed value is used and logged. | `50.0` |
| 8 | `rating` | `FLOAT` | Yes | `None` | Average customer star rating. Normalized to 1-decimal float within `[1.0, 5.0]`. Parsed from strings like `"4.2 out of 5 stars"`. | `4.2` |
| 9 | `review_count` | `INTEGER` | No | `0` | Total number of customer ratings/reviews received. Non-negative integer. Parsed from numbers, commas, or abbreviations (e.g. `"1.2K"` -> `1200`). | `480` |
| 10 | `colour` | `VARCHAR(64)` | Yes | `None` | Primary dominant garment colour or shade. | `"Navy Blue"` |
| 11 | `material` | `VARCHAR(64)` | Yes | `None` | Primary fabric composition (e.g., `"Pure Cotton"`, `"Chanderi Silk"`, `"Rayon"`, `"Linen"`). | `"Pure Cotton"` |
| 12 | `pattern` | `VARCHAR(64)` | Yes | `None` | Silhouette or surface design motif (e.g., `"Straight"`, `"Anarkali"`, `"A-Line"`, `"Floral Print"`). | `"Straight"` |
| 13 | `sizes` | `JSON` | No | `[]` | Array of available size options, normalized to canonical size ladder: `["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL", "6XL"]`. Free size is mapped to `["Free Size"]`. | `["S", "M", "L", "XL", "2XL"]` |
| 14 | `seller` | `VARCHAR(128)` | Yes | `None` | Merchant of record or distributor name. | `"RetailNet India"` |
| 15 | `availability` | `VARCHAR(64)` | No | `"In Stock"` | Stock status enumeration: `"In Stock"`, `"Out of Stock"`, `"Limited Stock"`. Normalized from marketplace badges. | `"In Stock"` |
| 16 | `product_url` | `VARCHAR(1024)` | No | — | Canonical product URL. In demo mode, sanitized to RFC 2606 domain (`https://example.com/dp/{asin}`). | `"https://example.com/dp/SYN-KUR-001"` |
| 17 | `source` | `VARCHAR(64)` | No | — | Ingestion provenance identifier (e.g. `"synthetic_curated"`, `"csv_import"`, `"creators_api"`). | `"synthetic_curated"` |
| 18 | `collected_at` | `TIMESTAMP` | No | — | ISO-8601 UTC timestamp of record ingestion/extraction. | `"2026-10-14T03:00:00Z"` |

---

## 2. Review Attributes (8 Fields)

Customer reviews provide qualitative Voice of Customer (VoC) feedback for product diagnostic workflows.

| # | Attribute Name | Data Type | Nullable | Default | Description & Constraints | Example Value |
|---|---|---|:---:|:---:|---|---|
| 1 | `review_id` | `VARCHAR(64)` | No | — | Stable deterministic unique identifier. If missing from source, generated as SHA-256 hash of `(asin + review_date + title + body)`. Primary key. | `"rev_syn_001_1"` |
| 2 | `asin` | `VARCHAR(32)` | No | — | Foreign key referencing `products.asin`. Orphan reviews with non-existent ASINs are rejected by the pipeline. | `"SYN-KUR-001"` |
| 3 | `rating` | `INTEGER` | No | — | Discrete star rating integer from 1 to 5 (`1 <= rating <= 5`). | `5` |
| 4 | `title` | `VARCHAR(256)` | Yes | `None` | Headline or summary text of the review. | `"Exceptional stitching and breathable cotton"` |
| 5 | `body` | `TEXT` | Yes | `None` | Full review narrative text. Cleaned of control characters and HTML tags. | `"The fitting is true to size and fabric did not shrink after washing."` |
| 6 | `verified_purchase` | `BOOLEAN` | No | `False` | Boolean indicator whether the review is an Amazon Verified Purchase. | `True` |
| 7 | `review_date` | `TIMESTAMP` | Yes | `None` | Date when the customer submitted the review. | `"2026-09-15T10:30:00Z"` |
| 8 | `source` | `VARCHAR(64)` | No | — | Ingestion provenance identifier. | `"synthetic_curated"` |

---

## 3. Data Integrity & Validation Invariants

1. **Price Validation:**
   - `price > 0`
   - `mrp is None or mrp >= price`
   - If source data specifies `mrp < price`, the record is not dropped; instead, `mrp` is nulled, `discount_pct` is nulled, and a data-quality flag is recorded in `cleaning_report.json`.
2. **ASIN Validation:**
   - Must match regex `^(SYN-[A-Z0-9-]+|[A-Z0-9]{10})$`. Invalid ASIN formats are dropped to `products_rejected.csv`.
3. **Deduplication Priority:**
   - When multiple records have the same `asin`, the record with the most recent `collected_at` timestamp is retained.
   - If timestamps match, the record with higher field completeness (fewer null attributes) is chosen.
4. **Canonical Size Order:**
   - Sizes are deduplicated and ordered strictly according to the canonical sequence:
     `XS < S < M < L < XL < 2XL < 3XL < 4XL < 5XL < 6XL`.
