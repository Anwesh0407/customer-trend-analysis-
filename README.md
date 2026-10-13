# Amazon Vendor Assist (AVA)

> **Tagline:** *Sell smarter. Sell what people want.*  
> An open, compliance-first vendor intelligence and merchandising analytics platform designed for small and regional Indian marketplace apparel vendors.

---

## 🌟 Executive Overview

Amazon Vendor Assist (AVA) bridges the information asymmetry faced by regional Indian manufacturers and apparel sellers. By focusing deeply on a pilot high-velocity category (**Women's Kurtas & Kurtis**), AVA transforms public listing observations into actionable sourcing, sizing, and pricing intelligence.

### Key Capabilities
- **Exact Stitch Prototype Replication:** 8 rich workspaces designed with Hanken Grotesk, JetBrains Mono, and the exact Stitch Design System (`#131921` Navy, `#ff9900` Orange, `#faf8ff` Canvas).
- **Evidence Envelope Architecture:** Every analytical figure returned from the API includes metadata on sample size, confidence rating, generation timestamp, and legal disclaimers. The UI never calculates its own metrics.
- **Compliance-First Ingestion:** Live unauthorized scraping of `amazon.in` is strictly prohibited by domain denylists, `robots.txt` enforcement, and immediate abort guards. Data is ingested through verified offline datasets or official Creator/Vendor APIs.
- **Zero-Hallucination AI Copilot (Ask AVA):** Read-only function calling, server-side prompt injection of niche context, and automated post-generation numeric verification ensuring 0 invented figures.
- **Idempotent CLI Pipeline:** A single unified CLI (`run.py`) handling end-to-end data collection, 12-step cleaning/validation, analytical aggregation, and database loading.

---

## 📁 Repository Layout

```text
Amazon vendor assist project/
├── api/                    # FastAPI application layer
│   ├── assistant/          # Ask AVA engine, tools, prompts, response verifier
│   ├── routers/            # Clean REST API endpoints (/api/v1/...)
│   ├── schemas/            # Request/response contracts & Evidence Envelopes
│   └── main.py             # FastAPI entrypoint
├── ava/                    # Core business logic & analytics library
│   ├── analytics/          # Pandas market aggregations & opportunity scoring
│   ├── collectors/         # Raw data ingestion collectors
│   ├── processing/         # 12-rule parser, validator, deduplicator, cleaner
│   ├── recommendations/    # Rule-based sourcing blueprints & similarity engine
│   ├── sources/            # CSV, JSON, public page, and Creators API adapters
│   └── storage/            # SQLAlchemy repository & Alembic migrations
├── data/
│   ├── sample/             # Curated synthetic dataset (SYN-KUR-001..032)
│   ├── raw/                # Timestamped raw ingestion history (immutable)
│   ├── cleaned/            # Cleaned artifacts & cleaning_report.json
│   └── reports/            # Markdown market summaries & JSON analytics
├── docs/                   # Full documentation & specifications
│   ├── AUDIT_REPORT.md     # Initial blueprint audit
│   ├── STATUS_REPORT.md    # Final 58-point verification matrix (100% PASS)
│   ├── data-dictionary.md  # 18 product & 8 review canonical fields
│   ├── limitations.md      # Ethics, non-random sampling, and disclaimers
│   ├── demo-script.md      # 5-10 minute presentation guide
│   └── api-contract.md     # REST endpoint catalog & envelope specs
├── frontend/               # React 19 + TypeScript + Vite + Tailwind CSS (Stitch UI)
│   ├── src/workspaces/     # 8 dedicated workspaces
│   ├── src/theme/          # Exact Stitch design system tokens
│   └── fixtures/           # Auto-generated offline mock fixtures
├── legacy/                 # Fully isolated historical customer analytics
│   └── customer-shopping/  # Power BI dashboard, SQL queries, Jupyter notebook
├── tests/                  # 44 passing automated tests
│   ├── api/                # Integration tests for REST endpoints
│   ├── assistant/          # Golden question & refusal evaluation suite
│   ├── contract/           # OpenAPI schema & fixture validation
│   └── core/               # Parsing, cleaning, analytics, storage tests
├── docker-compose.yml      # Optional PostgreSQL service configuration
├── run.py                  # Master CLI (collect, clean, analyze, load, pipeline, serve)
└── requirements.txt        # Python dependency manifest
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.12+
- Node.js 18+ & npm

### 2. Backend Setup
```bash
# Set up virtual environment
python3 -m venv backend/.venv
source backend/.venv/bin/activate
pip install -r requirements.txt

# Run the end-to-end data pipeline (collect -> clean -> analyze -> load)
python run.py pipeline

# Start the API server on port 8000
python run.py serve --port 8000
```
- Interactive API Docs: `http://localhost:8000/docs`
- Health Endpoint: `http://localhost:8000/health`

### 3. Frontend Setup
In a new terminal:
```bash
cd frontend
npm install
npm run dev
```
- Access the Application: `http://localhost:5173`

---

## 🧪 Testing & Validation

The codebase includes an exhaustive test suite covering data parsing, cleaning rules, hand-computed analytics math, storage engines, API contracts, and the Ask AVA golden question suite:

```bash
# Run the full test suite (44 tests)
backend/.venv/bin/pytest

# Run frontend build & type check
cd frontend && npm run build
```

---

## 📊 The 8 Integrated Workspaces

1. **Categories Workspace:** Pilot focus on Women's Kurtas & Kurtis with live metric badges; 6 upcoming apparel categories with pilot request CTA.
2. **Define Niche Workspace:** Real-time filter sliders (price corridor, fabric, pattern, sizes) with live sample count preview and small sample warnings (`n < 5`).
3. **Market Results Workspace:** 3-column active facet stack with Grid vs. Dense Table toggle exposing all 18 canonical attributes.
4. **Analytics Workspace:** Bento KPI strip, 4-tier vertical price distribution histogram, horizontal color concentration bars, and strategic hypotheses.
5. **Reviews Workspace:** Net Sentiment score (`+62`), segmented distribution bar (72/18/10), and 3 VoC pillars (Sizing, Fabric, Durability).
6. **Recommendations Workspace:** Vendor sourcing blueprint with recommended price sweet spot (`₹749–₹899`), 30-day demand wave SVG, technical textile specs, and "Why this?" rationale.
7. **Product Details Workspace:** Diagnostic pricing box (Listing vs. Niche Median), 18-attribute specifications grid, and benchmark listings comparison.
8. **Ask AVA Copilot:** Zero-hallucination vendor assistant with live telemetry grounding, read-only tools, numeric response verification, and strict refusal of competitor sales queries.

---

## ⚖️ Ethics, Compliance & Disclaimers

- **Synthetic Demo Data:** All demo products utilize synthetic ASINs (`SYN-KUR-xxx`) and RFC 2606 sanitized URLs (`https://example.com/dp/{asin}`).
- **Observation Proxy:** Review counts represent customer engagement and observation velocity, **not** actual unit sales or competitor turnover.
- **Domain Denylist:** Outbound HTTP requests to Amazon commercial domains are blocked at the networking layer.
- **Isolated Legacy Files:** Historical customer shopping behavior analysis files are quarantined in `legacy/customer-shopping/` with zero runtime dependencies.

For detailed documentation, refer to:
- [Data Dictionary](docs/data-dictionary.md)
- [System Limitations](docs/limitations.md)
- [Demo Presentation Script](docs/demo-script.md)
- [API Contract Specification](docs/api-contract.md)
- [Final Status Report](docs/STATUS_REPORT.md)
