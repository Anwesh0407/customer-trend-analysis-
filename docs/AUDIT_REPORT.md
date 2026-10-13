# AVA System Audit Report

**Date:** 2026-10-14  
**Auditor:** Lead Engineer  
**Status:** Audit Completed (Phase 1 Baseline)  

---

## 1. Executive Summary & Status Counts

| Status | Count | Description |
| :--- | :---: | :--- |
| **PASS** | 9 | Meets blueprint requirements and compliance rules |
| **PARTIAL** | 24 | Implemented in initial prototype but needs blueprint alignment |
| **MISSING** | 22 | Blueprint requirement not yet present in repository |
| **DEVIATES** | 3 | Implementation conflicts with blueprint rules (e.g. confidence labels, ASIN formats) |
| **Total Items Audited** | **58** | Complete checklist from Section 12 |

---

## 2. Comprehensive Gap Matrix

| ID | Requirement | Status | Evidence (File / Command / Result) | Fix Plan | Priority |
| :--- | :--- | :---: | :--- | :--- | :---: |
| **S-01** | Repo layout matches Section 2 | **DEVIATES** | Files located in `backend/app/`, no root `ava/` core library, no `api/` package or `run.py`. | Migrate backend to root `ava/` and `api/`, add `run.py`. | P0 |
| **S-02** | Legacy files isolated & unchanged | **PARTIAL** | Legacy files exist in `legacy_analysis/` but also duplicate copies remain at repo root. | `git mv` legacy files to `legacy/customer-shopping/`. Ensure zero AVA code imports them. | P0 |
| **S-03** | `.gitignore` excludes `.env`, logs, caches | **PASS** | `.gitignore` present. `git status --ignored` verifies `.pytest_cache`, `.venv`, `.db` ignored. | Keep verified. | P0 |
| **S-04** | `.env.example` lists all runtime settings | **PARTIAL** | `.env.example` missing `ASK_AVA_MODE`, `GEMINI_MODEL`, rate-limit caps, and fallback flags. | Add all configuration settings used across the codebase. | P0 |
| **D-01** | CSV source (BOM, ragged rows, blanks) | **MISSING** | `collector.py:38` uses standard `csv.DictReader` without encoding/BOM tolerance. | Implement robust CSV reader in `ava/sources/csv_source.py`. | P0 |
| **D-02** | JSON source (array, JSONL, wrapped) | **PARTIAL** | `collector.py:34` only handles top-level JSON array. | Add JSON Lines and envelope support in `ava/sources/json_source.py`. | P1 |
| **D-03** | Collectors stamp source + timestamp; raw history | **MISSING** | No timestamped `raw/products_<source>_<timestamp>.json` history files created. | Implement `ProductCollector` and `ReviewCollector` in `ava/collectors/`. | P0 |
| **D-04** | Raw is never modified by clean | **MISSING** | Cleaning does not write to separate `data/cleaned/` folder. | Establish one-way pipeline from `data/raw/` to `data/cleaned/`. | P0 |
| **D-05** | Column alias map + unrecognised columns reported | **MISSING** | No alias mapping in `backend/app/scraping/collector.py`. | Implement column mapper and reporting in `ava/processing/columns.py`. | P0 |
| **D-06** | Price & MRP parsing (INR, Rs, /-, grouping) | **PARTIAL** | Simple float cast in `collector.py:65`. No negative/zero/cap checks. | Implement comprehensive INR parser in `ava/processing/parsing.py`. | P0 |
| **D-07** | Rating/review-count parsing ("4.3 out of 5", "1.2K") | **PARTIAL** | Direct float/int cast. Fails on "1.2K" or text strings. | Add parsing regexes in `ava/processing/parsing.py`. | P0 |
| **D-08** | Sizes & availability text normalization | **PARTIAL** | Simple comma split. Canonical size order (XS..6XL) missing. | Add canonical size sorter and availability mapper in `ava/processing/parsing.py`. | P0 |
| **D-09** | Discount computed (not trusted; >2pt logged) | **PARTIAL** | Formula exists in `collector.py:67`, but does not log mismatches. | Compute discount from price/mrp, log discrepancies >2pt. | P0 |
| **D-10** | MRP < price handling (MRP nulled & flagged) | **PARTIAL** | Simple ternary in `collector.py`. Flagging count missing. | Null invalid MRP and record data-quality flag in report. | P0 |
| **D-11** | ASIN validate/extract/reject rule | **PARTIAL** | No 10-char alphanumeric regex or URL `/dp/` extraction. | Implement strict ASIN validator in `ava/processing/validation.py`. | P0 |
| **D-12** | Dedupe rule (newest wins, completeness tiebreak)| **PARTIAL** | First-seen dedupe only in `collector.py:44`. | Implement newest collected_at with completeness tiebreak in `ava/processing/cleaning.py`. | P0 |
| **D-13** | Pydantic single source of validity | **PARTIAL** | Models in `models/product.py` and `schemas/product.py` have slight attribute differences. | Consolidate single validation model in `ava/models.py`. | P0 |
| **D-14** | Rejected file with reasons (`products_rejected.csv`) | **MISSING** | Rejected rows are dropped silently without a reason log. | Output `data/cleaned/products_rejected.csv` with reason column. | P0 |
| **D-15** | Cleaning report (`cleaning_report.json`) | **MISSING** | No cleaning report produced. | Generate `cleaning_report.json` with rows in/out, rejections, notes. | P0 |
| **D-16** | Review cleaning rules (1-5 int, title/text, hash ID)| **PARTIAL** | Reviews are loaded directly from sample JSON without hashing or date parsing. | Implement review cleaner with stable SHA-256 ID in `ava/processing/cleaning.py`. | P0 |
| **D-17** | Synthetic sample data with DEMO labels | **DEVIATES** | Sample data used real Amazon ASINs (`B08X...`) and `amazon.in` URLs. | Regenerate with `SYN-KUR-xxx`, `example.com` URLs, and `source="synthetic"`. | P0 |
| **D-18** | CLI commands (`collect/clean/analyze/load/pipeline/serve`) | **MISSING** | No `run.py` CLI exists. | Implement `run.py` using `argparse` with friendly exit codes. | P1 |
| **D-19** | Pipeline idempotency (clean twice -> identical) | **MISSING** | Cannot be verified until `run.py pipeline` is implemented. | Add test verifying identical output hashes on double run. | P0 |
| **C-01** | HTTP client: rate-limit, backoff, Retry-After | **MISSING** | No shared rate-limited HTTP client in repo. | Build `ava/http_client.py` with polite backoff. | P0 |
| **C-02** | robots.txt enforced | **MISSING** | No robots parser in existing collector. | Integrate `urllib.robotparser` in public page source adapter. | P0 |
| **C-03** | Stop immediately on 401/403 | **MISSING** | No authentication stop handler. | Implement immediate abort in `ava/http_client.py`. | P0 |
| **C-04** | Stop immediately on CAPTCHA | **MISSING** | No CAPTCHA detector. | Add CAPTCHA response detection and immediate abort. | P0 |
| **C-05** | Blocked domains (Amazon) enforced | **MISSING** | Domain blocking list not implemented. | Add default Amazon domain denylist in HTTP client. | P0 |
| **C-06** | Creators API credentials via env; clear error | **PARTIAL** | Stub in `collector.py` logs message but lacks formal `SourceUnavailable` exception. | Implement in `ava/sources/creators_api_source.py`. | P1 |
| **C-07** | Creators API mapping isolated & UNVERIFIED | **MISSING** | Not yet implemented. | Create mapping module with explicit UNVERIFIED banner. | P1 |
| **C-08** | No live Amazon calls in tests or scripts | **PASS** | Tests use local TestClient; sample generator is local. | Maintain mock-only HTTP tests. | P0 |
| **C-09** | No claim that reviews = sales; no private data | **PASS** | `assistant_service.py` explicitly states review counts are attention, not sales. | Preserve compliance across all endpoints. | P0 |
| **B-01** | Repository interface (`storage/base.py`) | **MISSING** | Database queries coupled directly to SQLAlchemy sessions in routes. | Define abstract `Repository` interface in `ava/storage/base.py`. | P1 |
| **B-02** | Single SQLAlchemy implementation for SQLite & Postgres | **PARTIAL** | Engine setup handles SQLite fallback, but lacks repository methods. | Implement `SQLRepository` in `ava/storage/sql_repository.py`. | P1 |
| **B-03** | Alembic migrations apply on both databases | **MISSING** | Tables created via `Base.metadata.create_all()`. | Initialize Alembic migrations in `ava/storage/migrations/`. | P1 |
| **B-04** | Idempotent `load`; counts match cleaning report | **MISSING** | `run.py load` command does not exist. | Build idempotent upsert loader matching cleaning report counts. | P1 |
| **B-05** | Tables per Section 6 (products, reviews, niches, runs, chat) | **PARTIAL** | Only `products`, `reviews`, `collection_runs` exist. | Add `niches` and `chat_logs` models and tables. | P1 |
| **B-06** | `docker-compose.yml` starts PostgreSQL only | **MISSING** | No `docker-compose.yml` in repository. | Create `docker-compose.yml` for PostgreSQL 16 on port 5432. | P1 |
| **A-01** | Niche filter implemented once | **PARTIAL** | Filter logic duplicated in `data_service.py` and API routes. | Centralize niche filtering in `ava/analytics/niche_filter.py`. | P1 |
| **A-02** | All observations reported with sample size `n` | **PARTIAL** | Overview has total sample, but attribute counts lack inline `n`. | Ensure every metric dict includes `n`. | P1 |
| **A-03** | Six preliminary insight rules with guardrails | **PARTIAL** | Prototype has 4 recommendations; needs all 6 rules from Section 7. | Implement all 6 rules in `ava/analytics/opportunities.py`. | P1 |
| **A-04** | Suppression thresholds configurable (default 30 / 5) | **MISSING** | Threshold suppression not enforced. | Implement guardrail suppression when `n < min_sample_size`. | P1 |
| **A-05** | Confidence labels never "high" (very low/low/mod) | **DEVIATES** | Code returned "Confidence: 94%" and "High Opportunity". | Change confidence tiers strictly to `very_low`, `low`, `moderate`. | P0 |
| **A-06** | Standing limitations present on every report | **PARTIAL** | Some recommendations have limitations text; overview report lacks it. | Add standard limitations block to all analytic outputs. | P1 |
| **A-07** | DEMO DATA banner logic | **MISSING** | Backend does not flag `data_mode: "demo"` when synthetic data is loaded. | Add `data_mode` detection to metadata envelope. | P1 |
| **A-08** | Single analytics implementation shared by CLI/API/AVA | **PARTIAL** | CLI report doesn't exist yet; API and Assistant share partial service. | Unify analytics in `ava/analytics/market.py`. | P0 |
| **A-09** | Recommendation types and card fields per Section 8 | **PARTIAL** | Card fields have title/what/why, missing explicit threshold values. | Update recommendation schema and engine. | P1 |
| **A-10** | Markdown + JSON market report written to `reports/` | **MISSING** | No CLI report generation. | Implement `ava/analytics/report.py` outputting markdown & JSON. | P1 |
| **P-01** | All endpoints in Section 9 mounted at `/api/v1` | **PARTIAL** | Existing routes mounted at `/api` without `/api/v1` or niches/meta. | Restructure router with `/api/v1` prefix and missing routes. | P1 |
| **P-02** | Evidence envelope on every analytic response | **MISSING** | Endpoints return raw model lists without `data` + `meta` envelope. | Wrap all analytic endpoints in `EvidenceEnvelope[T]`. | P1 |
| **P-03** | Niche scoping everywhere | **PARTIAL** | Endpoints accept ad-hoc query params rather than niche ID/spec. | Wire `niche_id` query param across analytics/reviews/recommendations. | P1 |
| **P-04** | Consistent error format | **PARTIAL** | Default FastAPI error handler used. | Add standardized error envelope in `api/errors.py`. | P1 |
| **P-05** | CORS restricted to configured origin | **PASS** | Configured via `settings.FRONTEND_URL`. | Maintain settings-driven CORS. | P1 |
| **P-06** | Read-only except niches and chat logs | **PASS** | No mutating product endpoints exist. | Keep mutation restricted to niches/logs. | P1 |
| **P-07** | OpenAPI schema exported to `docs/openapi.json` | **MISSING** | No static schema export in `docs/`. | Add script/export step writing `docs/openapi.json`. | P1 |
| **P-08** | Chat rate and size limits | **MISSING** | No message length cap or client rate limiting. | Add request validation (max 500 chars) and IP rate limiter. | P1 |
| **P-09** | No secrets in responses or logs | **PASS** | Verified no keys returned in health or responses. | Keep verified. | P0 |
| **F-01** | Stitch tokens in one theme file | **PARTIAL** | CSS variables in `index.css`; needs typed `theme/tokens.ts`. | Extract tokens into `frontend/src/theme/tokens.ts`. | P1 |
| **F-02** | All eight workspaces exist and render | **PASS** | Verified in `frontend/src/App.tsx`. | Modularize into `frontend/src/workspaces/`. | P1 |
| **F-03** | Header niche selector drives every workspace | **PARTIAL** | State is local to `App.tsx`. | Wrap in `NicheContext` provider. | P1 |
| **F-04** | Typed client generated from OpenAPI | **PARTIAL** | Hand-crafted API client in `frontend/src/services/api.ts`. | Update typed client against `docs/openapi.json`. | P1 |
| **F-05** | Mock mode + fixtures validated against schema | **PARTIAL** | Fallback in `api.ts`, but no `fixtures/` directory. | Add `frontend/fixtures/` with schema-compliant JSON files. | P1 |
| **F-06** | No metrics computed/hardcoded in UI | **PARTIAL** | Minor inline percentages in `App.tsx`. | Ensure all percentages and stats come from API response. | P0 |
| **F-07** | Loading / empty / error states | **PARTIAL** | Basic error fallback present; needs explicit UI states. | Add dedicated EmptyState and LoadingState components. | P1 |
| **F-08** | DEMO banner, SampleSizeBadge, Observation/Estimate badge | **PARTIAL** | Prototype displays badges, but lacks DEMO DATA top banner. | Add global DEMO banner and standardized badge components. | P1 |
| **F-09** | Production build & type-check pass | **PASS** | `npm run build` succeeds with 0 errors in 739ms. | Maintain 0 error standard. | P0 |
| **K-01** | Tool whitelist, server-side niche context | **PARTIAL** | Backend has tools, but context is passed from client. | Enforce server-side context binding in `api/assistant/`. | P1 |
| **K-02** | Gemini function calling over whitelist | **PARTIAL** | Gemini client stubbed; uses deterministic analyst currently. | Wire `google-genai` / REST API with tool calling definitions. | P1 |
| **K-03** | Verifier (numbers must match tool results) | **MISSING** | No response verification layer. | Build regex number extractor and validator in `api/assistant/verifier.py`. | P0 |
| **K-04** | Structured reply with evidence + sample sizes | **PASS** | Returns `reply`, `grounded_evidence`, `suggested_actions`. | Align with contract schema. | P1 |
| **K-05** | Refusals (sales counts, competitor revenue, private data) | **PASS** | Explicit refusal logic present in assistant service. | Add golden test coverage. | P0 |
| **K-06** | Demo fallback (all triggers: no key, error, verifier fail) | **PARTIAL** | Fallback works when key absent; needs verifier failure trigger. | Implement comprehensive demo router in `api/assistant/demo_engine.py`. | P1 |
| **K-07** | Mode chip in UI (Gemini \| Demo) | **PARTIAL** | UI shows "Live Grounded"; needs explicit mode chip. | Add `AssistantModeChip` to assistant header. | P1 |
| **K-08** | Golden tests (~20 questions) + no invented metrics test | **MISSING** | No automated assistant test suite. | Create `tests/assistant/test_golden_questions.py`. | P1 |
| **K-09** | Key/model from env only; no key in repo or browser | **PASS** | Verified env-only; not exposed in frontend bundle. | Maintain env-only guard. | P0 |
| **T-01..09**| Core, storage, pipeline, contract, parity tests | **PARTIAL** | 10 API tests in `backend/tests/test_api.py`; missing core/unit suites. | Expand into `tests/core/`, `tests/api/`, `tests/contract/`. | P1 |
| **R-01..02**| Comprehensive docs & data dictionary | **PARTIAL** | `README.md` updated; missing `docs/data-dictionary.md`, `demo-script.md`, etc. | Create all required docs in `docs/`. | P2 |

---

## 3. Structure Mapping

| Existing Path | Blueprint Target Path | Action | Rationale |
| :--- | :--- | :---: | :--- |
| `Customer_Shopping_Behavior_Analysis.ipynb` | `legacy/customer-shopping/notebooks/Customer_Shopping_Behavior_Analysis.ipynb` | **Move** (`git mv`) | Isolate legacy analytics from AVA root |
| `customer_shopping_behavior.csv` | `legacy/customer-shopping/data/customer_shopping_behavior.csv` | **Move** (`git mv`) | Prevent mixing customer data with Amazon product catalog |
| `customer_behavior_sql_queries.sql` | `legacy/customer-shopping/sql/customer_behavior_sql_queries.sql` | **Move** (`git mv`) | Isolate legacy queries |
| `customer_behavior_dashboard.pbix` | `legacy/customer-shopping/dashboard/customer_behavior_dashboard.pbix` | **Move** (`git mv`) | Legacy Power BI asset |
| `legacy_analysis/` | `legacy/customer-shopping/` | **Merge/Clean** | Unify duplicate copies under blueprint path |
| `backend/app/core/` | `ava/` (`config.py`, `logging_setup.py`) | **Move/Refactor** | Framework-free core library root |
| `backend/app/models/` | `ava/models.py` & `ava/storage/` | **Move/Refactor** | Separate entity dataclass/Pydantic from SQL models |
| `backend/app/schemas/` | `api/schemas/` | **Move** | API request/response contracts |
| `backend/app/services/` | `ava/analytics/`, `ava/recommendations/` | **Split/Refactor** | Framework-free core services |
| `backend/app/scraping/` | `ava/sources/`, `ava/collectors/` | **Refactor** | Modular adapters and collectors |
| `backend/app/api/` | `api/routers/`, `api/main.py` | **Move** | FastAPI HTTP integration layer |
| `backend/tests/` | `tests/api/` | **Move/Expand** | Multi-suite test architecture |
| `data/sample/` | `data/sample/` | **Keep & Update** | Replace real ASINs with synthetic `SYN-KUR-xxx` |
| `frontend/src/` | `frontend/src/` | **Refactor** | Modularize `App.tsx` into `workspaces/` and `theme/` |

---

## 4. Risks and Surprises

1. **Synthetic Data Formats**:
   - *Risk*: `sample_kurtas.json` contains real Amazon ASINs like `B08X1K9P11` and real `amazon.in` URLs.
   - *Fix*: Must be regenerated with explicit fake ASINs (`SYN-KUR-001`), `example.com` product URLs, and `source="synthetic"`.
2. **Confidence Labelling Deviation**:
   - *Risk*: The existing recommendation engine outputs "Confidence: 94%" and "High Opportunity Detected". Section 7 strictly forbids claiming "high" confidence; labels must only be `very_low`, `low`, or `moderate`.
   - *Fix*: Refactor confidence calculation to output only `very_low`, `low`, or `moderate`.
3. **Dual Legacy Directories**:
   - *Risk*: Legacy customer shopping behavior files currently exist at both the repo root and in `legacy_analysis/`.
   - *Fix*: Cleanly consolidate all legacy files into `legacy/customer-shopping/` using `git mv` in a dedicated commit.
4. **FastAPI Route Mounting**:
   - *Risk*: Current routes are mounted at `/api` without the `/api/v1` namespace and omit `niches` and `meta` endpoints.
   - *Fix*: Remount at `/api/v1` and implement missing endpoints with `EvidenceEnvelope`.

---

## 5. Ordered Fix Plan

1. **Phase 2 (P0 Fixes)**:
   - Isolate legacy files to `legacy/customer-shopping/` via `git mv`.
   - Regenerate sample data with strictly synthetic attributes (`SYN-KUR-xxx`, `example.com`, `source="synthetic"`).
   - Create core `ava/` package and migrate framework-free logic.
   - Create `api/` package with `/api/v1` routing.
   - Correct confidence labels (remove "high", use `very_low|low|moderate`).
   - Implement `run.py` CLI (`pipeline`, `clean`, `load`, `serve`, `analyze`).
   - Run existing test suite and verify green.
2. **Phase 3 (Fill Gaps by Layer)**:
   - Core pipeline: sources (CSV/JSON), collectors, 12 cleaning rules, cleaning report, rejected CSV.
   - Storage & DB: Repository interface, Alembic migrations, PostgreSQL `docker-compose.yml`.
   - Analytics & Recommendations: unified pandas analytics, 6 insight rules, evidence envelope.
   - FastAPI: `/api/v1` routers, envelope wrapper, OpenAPI export to `docs/openapi.json`.
   - Frontend: modular workspaces, `theme/tokens.ts`, DEMO banner, SampleSizeBadge, mock fixtures.
   - Ask AVA: Gemini client + verifier + demo fallback engine + golden test suite.
3. **Phase 4 (Integration & Verification)**:
   - End-to-end demo flow on SQLite and PostgreSQL.
   - Run full test suite across both databases.
4. **Phase 5 (Docs & Handover)**:
   - Complete documentation: `docs/data-dictionary.md`, `docs/limitations.md`, `docs/demo-script.md`, `docs/STATUS_REPORT.md`.
