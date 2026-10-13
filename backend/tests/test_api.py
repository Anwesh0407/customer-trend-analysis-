import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Amazon Vendor Assist" in data["app"]

def test_categories_endpoint():
    response = client.get("/api/categories")
    assert response.status_code == 200
    data = response.json()
    assert "categories" in data
    assert "regions" in data

def test_products_list():
    response = client.get("/api/products")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] > 0
    assert len(data["items"]) > 0
    first = data["items"][0]
    assert "asin" in first
    assert "price_inr" in first
    assert "badge" in first

def test_products_filtering():
    response = client.get("/api/products?min_price=800&max_price=1000&material=Cotton")
    assert response.status_code == 200
    data = response.json()
    for item in data["items"]:
        assert 800 <= item["price_inr"] <= 1000
        assert "cotton" in item["material"].lower()

def test_product_detail():
    list_resp = client.get("/api/products")
    first_asin = list_resp.json()["items"][0]["asin"]
    detail_resp = client.get(f"/api/products/{first_asin}")
    assert detail_resp.status_code == 200
    assert detail_resp.json()["asin"] == first_asin

def test_analytics_overview():
    response = client.get("/api/analytics/overview")
    assert response.status_code == 200
    data = response.json()
    assert data["total_products"] > 0
    assert data["median_price_inr"] > 0

def test_price_analytics():
    response = client.get("/api/analytics/prices")
    assert response.status_code == 200
    data = response.json()
    assert len(data["price_bands"]) > 0
    assert "sweet_spot" in data

def test_reviews_endpoint():
    response = client.get("/api/reviews")
    assert response.status_code == 200
    data = response.json()
    assert len(data["positive_drivers"]) > 0
    assert len(data["recurring_complaints"]) > 0

def test_recommendations_endpoint():
    response = client.get("/api/recommendations")
    assert response.status_code == 200
    data = response.json()
    assert data["total_recommendations"] > 0
    first = data["items"][0]
    assert "what_observed" in first
    assert "why_it_matters" in first
    assert "what_to_do" in first
    assert "limitations" in first

def test_assistant_chat():
    payload = {"message": "Which price range has the most opportunity?"}
    response = client.post("/api/assistant/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert len(data["reply"]) > 0
    assert len(data["grounded_evidence"]) > 0
