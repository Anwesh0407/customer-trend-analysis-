"""Contract tests verifying OpenAPI specification and mock fixtures (Checklist P-07, T-07, F-05)."""
import json
import os
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.schemas import (
    CategoryResponse,
    HealthResponse,
    MetaResponse,
    NicheResponse,
    ProductListResponse,
    ProductResponse,
    MarketSummaryData,
    OpportunitiesData,
    ReviewSummaryData,
    ReviewListResponse,
    RecommendationListData,
    AssistantStatusResponse,
)

client = TestClient(app)

REQUIRED_V1_ENDPOINTS = [
    "/api/v1/health",
    "/api/v1/meta",
    "/api/v1/categories",
    "/api/v1/niches",
    "/api/v1/niches/preview",
    "/api/v1/niches/{niche_id}",
    "/api/v1/products",
    "/api/v1/products/{asin}",
    "/api/v1/products/{asin}/similar",
    "/api/v1/analytics/summary",
    "/api/v1/analytics/opportunities",
    "/api/v1/reviews/summary",
    "/api/v1/reviews",
    "/api/v1/recommendations",
    "/api/v1/assistant/ask",
    "/api/v1/assistant/status",
]


def test_openapi_schema_completeness():
    schema_path = Path("docs/openapi.json")
    assert schema_path.exists(), "docs/openapi.json does not exist. Run export on startup."

    with open(schema_path, "r", encoding="utf-8") as f:
        spec = json.load(f)

    assert "paths" in spec
    paths = spec["paths"]
    for ep in REQUIRED_V1_ENDPOINTS:
        assert ep in paths, f"Missing required endpoint '{ep}' in OpenAPI contract."


def test_generate_and_validate_frontend_fixtures():
    fixtures_dir = Path("frontend/fixtures")
    fixtures_dir.mkdir(parents=True, exist_ok=True)

    # 1. Categories fixture
    res_cat = client.get("/api/v1/categories")
    assert res_cat.status_code == 200
    cat_data = res_cat.json()
    with open(fixtures_dir / "categories.json", "w", encoding="utf-8") as f:
        json.dump(cat_data, f, indent=2)
    for c in cat_data:
        CategoryResponse(**c)

    # 2. Niches fixture
    res_niche = client.get("/api/v1/niches")
    assert res_niche.status_code == 200
    niche_data = res_niche.json()
    with open(fixtures_dir / "niches.json", "w", encoding="utf-8") as f:
        json.dump(niche_data, f, indent=2)

    # 3. Products fixture
    res_prod = client.get("/api/v1/products?limit=20")
    assert res_prod.status_code == 200
    prod_env = res_prod.json()
    with open(fixtures_dir / "products.json", "w", encoding="utf-8") as f:
        json.dump(prod_env, f, indent=2)
    ProductListResponse(**prod_env["data"])

    # 4. Analytics Summary fixture
    res_sum = client.get("/api/v1/analytics/summary")
    assert res_sum.status_code == 200
    sum_env = res_sum.json()
    with open(fixtures_dir / "analytics_summary.json", "w", encoding="utf-8") as f:
        json.dump(sum_env, f, indent=2)
    MarketSummaryData(**sum_env["data"])

    # 5. Opportunities fixture
    res_opp = client.get("/api/v1/analytics/opportunities")
    assert res_opp.status_code == 200
    opp_env = res_opp.json()
    with open(fixtures_dir / "opportunities.json", "w", encoding="utf-8") as f:
        json.dump(opp_env, f, indent=2)
    OpportunitiesData(**opp_env["data"])

    # 6. Reviews Summary fixture
    res_rev_sum = client.get("/api/v1/reviews/summary")
    assert res_rev_sum.status_code == 200
    rev_sum_env = res_rev_sum.json()
    with open(fixtures_dir / "reviews_summary.json", "w", encoding="utf-8") as f:
        json.dump(rev_sum_env, f, indent=2)
    ReviewSummaryData(**rev_sum_env["data"])

    # 7. Reviews List fixture
    res_revs = client.get("/api/v1/reviews?limit=10")
    assert res_revs.status_code == 200
    revs_env = res_revs.json()
    with open(fixtures_dir / "reviews.json", "w", encoding="utf-8") as f:
        json.dump(revs_env, f, indent=2)
    ReviewListResponse(**revs_env["data"])

    # 8. Recommendations fixture
    res_recs = client.get("/api/v1/recommendations")
    assert res_recs.status_code == 200
    recs_env = res_recs.json()
    with open(fixtures_dir / "recommendations.json", "w", encoding="utf-8") as f:
        json.dump(recs_env, f, indent=2)
    RecommendationListData(**recs_env["data"])
