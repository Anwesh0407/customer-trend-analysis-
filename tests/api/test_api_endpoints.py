"""FastAPI endpoint and evidence envelope integration tests (Checklist P-01 to P-06, T-06)."""
import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/api/v1/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] in ("ok", "degraded")
    assert "version" in data
    assert "database" in data


def test_meta_endpoint():
    res = client.get("/api/v1/meta")
    assert res.status_code == 200
    data = res.json()
    assert "total_products" in data
    assert "data_mode" in data
    assert "limitations" in data


def test_categories_endpoint():
    res = client.get("/api/v1/categories")
    assert res.status_code == 200
    cats = res.json()
    assert len(cats) >= 3
    # Check Kurtas & Kurtis is active
    kurtas = next((c for c in cats if "Kurtas" in c["name"]), None)
    assert kurtas is not None
    assert kurtas["is_active"] is True


def test_niches_crud_and_preview():
    # 1. Preview
    prev_res = client.post("/api/v1/niches/preview", json={
        "category": "Women's Kurtas & Kurtis",
        "filters": {"max_price": 1000.0}
    })
    assert prev_res.status_code == 200
    p_data = prev_res.json()
    assert "sample_size" in p_data
    assert "below_threshold" in p_data

    # 2. Create
    create_res = client.post("/api/v1/niches", json={
        "name": "API Test Niche",
        "category": "Women's Kurtas & Kurtis",
        "filters": {"max_price": 1200.0, "colours": ["Navy Blue"]}
    })
    assert create_res.status_code == 201
    created = create_res.json()
    niche_id = created["id"]
    assert created["name"] == "API Test Niche"

    # 3. Get by ID
    get_res = client.get(f"/api/v1/niches/{niche_id}")
    assert get_res.status_code == 200
    assert get_res.json()["id"] == niche_id

    # 4. Delete
    del_res = client.delete(f"/api/v1/niches/{niche_id}")
    assert del_res.status_code == 204


def test_products_list_and_envelope():
    # P-02: Every analytic/product response carries EvidenceEnvelope
    res = client.get("/api/v1/products?limit=10")
    assert res.status_code == 200
    body = res.json()
    assert "data" in body
    assert "meta" in body
    meta = body["meta"]
    assert "sample_size" in meta
    assert "data_mode" in meta
    assert "sources" in meta
    assert "limitations" in meta

    items = body["data"]["items"]
    assert len(items) <= 10
    if items:
        # Check all 18 fields present
        p0 = items[0]
        for field in ["asin", "product_name", "category", "brand", "price", "mrp", "discount_pct",
                      "rating", "review_count", "colour", "material", "pattern", "sizes", "seller",
                      "availability", "product_url", "source", "collected_at"]:
            assert field in p0, f"Field {field} missing in ProductResponse"


def test_product_detail_and_similar():
    # First get an ASIN
    list_res = client.get("/api/v1/products?limit=1")
    items = list_res.json()["data"]["items"]
    if not items:
        pytest.skip("No products loaded in database.")

    asin = items[0]["asin"]

    # 1. Detail
    det_res = client.get(f"/api/v1/products/{asin}")
    assert det_res.status_code == 200
    det_body = det_res.json()
    assert det_body["data"]["asin"] == asin
    assert "percentile_in_niche" in det_body["data"]
    assert "quality_flags" in det_body["data"]

    # 2. Similar
    sim_res = client.get(f"/api/v1/products/{asin}/similar?limit=3")
    assert sim_res.status_code == 200
    sim_body = sim_res.json()
    assert "similar_items" in sim_body["data"]


def test_analytics_summary_and_opportunities():
    # Summary
    sum_res = client.get("/api/v1/analytics/summary")
    assert sum_res.status_code == 200
    sum_body = sum_res.json()
    assert "price_metrics" in sum_body["data"]
    assert "price_bands" in sum_body["data"]
    assert "meta" in sum_body
    assert sum_body["meta"]["sample_size"] >= 0

    # Opportunities
    opp_res = client.get("/api/v1/analytics/opportunities")
    assert opp_res.status_code == 200
    opp_body = opp_res.json()
    assert "insights" in opp_body["data"]
    assert "insights_suppressed" in opp_body["data"]


def test_reviews_summary_and_list():
    # Summary
    res = client.get("/api/v1/reviews/summary")
    assert res.status_code == 200
    body = res.json()
    assert "total_reviews" in body["data"]
    assert "coverage_pct" in body["data"]
    assert body["data"]["sentiment_badge"] == "planned"

    # List
    list_res = client.get("/api/v1/reviews?limit=5")
    assert list_res.status_code == 200
    assert "items" in list_res.json()["data"]


def test_recommendations_endpoint():
    res = client.get("/api/v1/recommendations")
    assert res.status_code == 200
    body = res.json()
    assert "cards" in body["data"]
    assert "meta" in body


def test_assistant_status_and_ask():
    # 1. Status
    st_res = client.get("/api/v1/assistant/status")
    assert st_res.status_code == 200
    st_data = st_res.json()
    assert "mode" in st_data
    assert "sample_questions" in st_data

    # 2. Ask (in demo fallback)
    ask_res = client.post("/api/v1/assistant/ask", json={
        "question": "What is the median price for kurtas?"
    })
    assert ask_res.status_code == 200
    ask_data = ask_res.json()
    assert "answer" in ask_data
    assert "evidence" in ask_data
    assert len(ask_data["evidence"]) >= 1
    assert ask_data["mode"] in ("demo", "gemini")
