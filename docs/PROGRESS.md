# AVA MVP Progress Log

## Phase 0: Baseline Discovery (Recorded: 2026-10-14)

### 1. Repository Inventory
- **Current Root Files**:
  - `Customer_Shopping_Behavior_Analysis.ipynb` (Legacy customer transaction notebook)
  - `customer_shopping_behavior.csv` (3,900 rows customer transaction dataset)
  - `customer_behavior_sql_queries.sql` (10 SQL analysis queries)
  - `customer_behavior_dashboard.pbix` (Power BI dashboard)
  - `README.md` (Project overview)
  - `.env.example` (Environment variables template)
  - `.gitignore` (Excludes caches, `.venv`, `node_modules`, `.env`)
- **Current Backend Structure (`backend/`)**:
  - `backend/app/main.py`: FastAPI server mounted at `/api`
  - `backend/app/core/`: `config.py`, `logging.py`
  - `backend/app/api/`: `router.py`, routes for `health`, `categories`, `products`, `analytics`, `reviews`, `recommendations`, `assistant`
  - `backend/app/database/`: `connection.py`, SQLite `ava_local.db`
  - `backend/app/models/`: `product.py` (`ProductModel`, `ReviewModel`, `CollectionRunModel`)
  - `backend/app/schemas/`: `product.py`, `review.py`, `analytics.py`, `recommendation.py`, `chat.py`
  - `backend/app/services/`: `data_service.py`, `analytics_service.py`, `recommendation_service.py`, `assistant_service.py`
  - `backend/app/scraping/`: `collector.py`
  - `backend/app/ml/`: `scoring.py`
  - `backend/requirements.txt`: Python dependencies
  - `backend/tests/test_api.py`: 10 integration tests
- **Current Data Structure (`data/`)**:
  - `data/raw/` (`.gitkeep`)
  - `data/processed/` (`.gitkeep`)
  - `data/sample/`: `generate_sample_data.py`, `sample_kurtas.json`, `sample_kurtas.csv`, `sample_reviews.json`, `sample_reviews.csv`
- **Current Frontend Structure (`frontend/`)**:
  - React 19 + TypeScript + Vite + `@tailwindcss/vite`
  - `frontend/src/App.tsx`: Monolithic view containing 8 tab views + chat drawer
  - `frontend/src/services/api.ts`: API client
  - `frontend/src/types/index.ts`: TypeScript interfaces
  - `frontend/src/index.css`: Tailwind theme styles
- **Current Legacy Analysis (`legacy_analysis/`)**:
  - Contains duplicate copies of the 4 legacy files from initial setup.

### 2. Baseline Test Execution Results
- **Command**: `PYTHONPATH=. backend/.venv/bin/pytest backend/tests/test_api.py`
- **Result**: `10 passed, 1 warning in 0.79s`
- **Frontend Build**: `npm run build` in `frontend/`
- **Result**: `✓ built in 739ms` (0 TypeScript / bundling errors)

### 3. Baseline Observations & Deviations from Target Blueprint
1. **Repository Layout**:
   - The target architecture requires root-level `ava/` (core library), `api/` (FastAPI), `run.py` (CLI), `docker-compose.yml`, `scripts/`, `legacy/customer-shopping/`, and `tests/`. Currently, backend code is nested under `backend/app/`, legacy files sit at both root and `legacy_analysis/`, and `run.py` is absent.
2. **Data Contracts**:
   - The blueprint requires exact 18 fields: `asin, product_name, category, brand, price, mrp, discount_pct, rating, review_count, colour, material, pattern, sizes, seller, availability, product_url, source, collected_at`.
   - Existing code used `price_inr`, `mrp_inr`, `color`, `available_sizes`.
3. **Synthetic Data Policy**:
   - The blueprint strictly mandates clearly synthetic sample data: fake ASINs (e.g. `SYN-KUR-001`), fake brands, `example.com` URLs, `source` containing `synthetic`, and DEMO DATA banners.
   - Existing sample data used Amazon-like ASINs (`B08X1K9P11`) and real `amazon.in` URLs.
4. **Pipeline & CLI**:
   - `run.py` CLI supporting `collect | clean | analyze | load | pipeline | serve` is missing.
   - Separate `data/cleaned/` (`products_clean`, `products_rejected.csv`, `cleaning_report.json`) output is missing.
   - Comprehensive 12-rule data cleaner, parser, deduplicator is missing.
5. **Evidence Envelope & Contracts**:
   - API responses must carry an evidence envelope (`data` + `meta` { `niche`, `sample_size`, `as_of`, `data_mode`, `sources`, `limitations` }).
   - OpenAPI contract must be exported to `docs/openapi.json`.
6. **Ask AVA Architecture**:
   - Needs server-side niche context, fixed read-only function calling whitelist, strict response verifier (comparing numbers in reply against tool outputs), and a ~20 question golden test suite.
7. **Legacy Files**:
   - Legacy customer shopping behavior files must be cleanly moved to `legacy/customer-shopping/` with zero references in AVA runtime code.

---
*Status: Phase 0 complete. Proceeding to Phase 1: Audit Report.*
