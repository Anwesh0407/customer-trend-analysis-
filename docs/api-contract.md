# Amazon Vendor Assist (AVA) — API Contract Specification

All public and internal endpoints in AVA are hosted under `/api/v1` (with `/health` available at the root) and adhere to the Evidence Envelope design pattern.

---

## 1. Evidence Envelope Specification

All analytical, product, review, and recommendation endpoints wrap their payloads inside a standard `EvidenceEnvelope`:

```json
{
  "data": { ... },
  "meta": {
    "generated_at": "2026-10-14T03:00:00Z",
    "sample_size": 32,
    "confidence_level": "medium",
    "data_mode": "demo",
    "sources": ["synthetic_curated"],
    "limitations": [
      "Observational snapshot; not a complete census.",
      "Review counts are observation volume proxies, not unit sales."
    ],
    "warnings": []
  }
}
```

### Metadata Fields
- `generated_at` (`string`, ISO-8601): Server timestamp when the analytical calculation or retrieval completed.
- `sample_size` (`integer`): Number of product or review records included in the calculation.
- `confidence_level` (`string`): Categorical certainty indicator (`low` or `medium`). Strictly capped at `medium` due to observational market sampling.
- `data_mode` (`string`): Runtime mode (`demo` or `production`).
- `sources` (`string[]`): Provenance identifiers contributing to the payload.
- `limitations` (`string[]`): Mandatory legal and analytical disclaimers.
- `warnings` (`string[]`): Triggered alerts, such as small sample size warnings when `sample_size < 5`.

---

## 2. API Endpoints Catalog

### System & Taxonomy

#### `GET /health`
Returns backend health status, database connection state, and uptime.
- **Response:** `{"status": "ok", "app": "AVA", "version": "1.0.0"}`

#### `GET /api/v1/meta`
Returns application metadata, supported categories, data version, and active data mode.

#### `GET /api/v1/categories`
Returns the taxonomy of supported and upcoming marketplace categories.
- **Response:** Array of `Category` objects:
  ```json
  [
    {
      "id": "womens-kurtas",
      "name": "Women's Kurtas & Kurtis",
      "slug": "womens-kurtas-kurtis",
      "is_active": true,
      "product_count": 32,
      "review_count": 2840,
      "median_price": 899.0
    }
  ]
  ```

---

### Niches Management

#### `GET /api/v1/niches?category={category_name}`
Lists pre-configured and custom user-defined niches for a category.

#### `POST /api/v1/niches`
Creates a new custom niche filter.
- **Body:** `NicheCreate` schema (`name`, `category`, `filter_criteria`).

#### `POST /api/v1/niches/preview`
Evaluates a proposed filter against the active catalog and returns the matching listing count.
- **Body:** `NicheFilter` schema (`category`, `price_min`, `price_max`, `materials`, `patterns`, `sizes`).
- **Response:** `{"matching_count": 14, "small_sample_warning": false}`

---

### Products & Catalog

#### `GET /api/v1/products`
Retrieves a paginated list of products matching optional niche or facet filters.
- **Query Params:**
  - `niche_id` (`string`, optional)
  - `category` (`string`, optional)
  - `price_min`, `price_max` (`float`, optional)
  - `material`, `pattern` (`string`, optional)
  - `sort_by` (`string`: `relevance` | `price_asc` | `price_desc` | `rating_desc` | `reviews_desc`)
  - `page` (`integer`, default 1)
  - `page_size` (`integer`, default 20)
- **Response:** `EvidenceEnvelope<ProductListResponse>` with `items`, `total`, `page`, `page_size`.

#### `GET /api/v1/products/{asin}`
Returns the 18 canonical attributes of a specific product listing.
- **Response:** `EvidenceEnvelope<Product>`.

#### `GET /api/v1/products/{asin}/similar`
Returns up to 5 benchmark listings matching price tier and silhouette characteristics.
- **Response:** `EvidenceEnvelope<Product[]>`.

---

### Analytics & Opportunities

#### `GET /api/v1/analytics/summary?niche_id={id}`
Returns aggregated statistical metrics for the active niche:
- Median price, mean price, min/max price.
- Median discount percentage.
- Price band distribution (Budget, Mass, Mid-Premium, Premium).
- Top colours, materials, and silhouettes.
- Size availability distribution (including 3XL+ coverage).
- Leading brands and market concentration.
- **Response:** `EvidenceEnvelope<MarketSummary>`.

#### `GET /api/v1/analytics/opportunities?niche_id={id}`
Returns algorithmic whitespace opportunities (e.g. plus-size demand gap, underserved fabric-price corridor).
- **Response:** `EvidenceEnvelope<OpportunityAnalysis>`.

---

### Reviews (Voice of Customer)

#### `GET /api/v1/reviews?asin={asin}&niche_id={id}`
Lists customer review feedback with pagination and sentiment tags.
- **Response:** `EvidenceEnvelope<ReviewListResponse>`.

#### `GET /api/v1/reviews/summary?niche_id={id}`
Returns VoC diagnostic metrics:
- Net Sentiment score (`-100` to `+100`).
- Sentiment distribution percentages (positive, neutral, negative).
- Macro topic volume drivers (sizing, fabric quality, stitching).
- **Response:** `EvidenceEnvelope<ReviewSummary>`.

---

### Recommendations

#### `GET /api/v1/recommendations?niche_id={id}`
Generates production-ready vendor sourcing blueprints based on deterministic market rules:
- Recommended product concept & silhouette.
- Price sweet spot corridor.
- Technical textile specifications (yarn count, dye grade, seam construction).
- Evidence citations explaining the recommendation rationale.
- **Response:** `EvidenceEnvelope<RecommendationListResponse>`.

---

### AI Assistant (Ask AVA)

#### `GET /api/v1/assistant/status`
Returns AI engine readiness, model configuration (`gemini-2.5-flash` or `demo_engine`), and active tool whitelist.

#### `POST /api/v1/assistant/ask`
Submits a natural language vendor question to the grounded copilot.
- **Body:** `ChatRequest` (`message`, `niche_id`, `history`).
- **Response:** `EvidenceEnvelope<ChatResponse>`:
  - `answer`: Natural language reply strictly verified against grounded telemetry.
  - `evidence_items`: Array of citations with entity names, values, and verification status.
  - `tool_calls`: Audit log of read-only tools invoked to satisfy the query.
