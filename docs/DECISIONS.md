# Architecture & Technical Decisions Log

| Decision ID | Date | Topic | Decision | Justification |
| :--- | :--- | :--- | :--- | :--- |
| DEC-001 | 2026-10-14 | Repository Structure | Migrate to target blueprint (`ava/`, `api/`, `legacy/customer-shopping/`, `run.py`) | Comply with Blueprint Rule 3 and Section 2 layout. |
| DEC-002 | 2026-10-14 | Data Contract Harmonization | Adopt exact 18 fields (`price`, `mrp`, `colour`, `sizes`) | Align with Section 3 data contract and Pydantic validation rules. |
| DEC-003 | 2026-10-14 | Synthetic Sample Data | Use `SYN-KUR-xxx`, `example.com` URLs, and `source="synthetic_curated"` | Enforce Rule 5: never fabricate real marketplace data or impersonate Amazon listings. |
| DEC-004 | 2026-10-14 | Dependency: Alembic | Add `alembic` to `backend/requirements.txt` (or root `requirements.txt`) | Required by Blueprint Section 6 for unified SQLite & PostgreSQL migrations. |
| DEC-005 | 2026-10-14 | Dependency: Docker Compose | Add `docker-compose.yml` for PostgreSQL service only | Required by Blueprint Section 6 (PostgreSQL on port 5432 for Stage 2 load/verification). |
| DEC-006 | 2026-10-14 | Single Analytics Implementation | Centralize all metric calculations in `ava/analytics/` using pandas | Enforce Section 1 & 7: identical medians across SQLite/PostgreSQL; zero metrics in UI. |
