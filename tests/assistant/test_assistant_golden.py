"""Ask AVA Golden Question Suite and Verifier Tests (Checklist K-05, K-08, T-08)."""
import pytest
from fastapi.testclient import TestClient
from api.main import app
from api.assistant.verifier import extract_numbers_from_text, verify_answer

client = TestClient(app)


def test_refusal_competitor_sales():
    # K-05: Non-negotiable refusal of sales counts / unit volume
    res = client.post("/api/v1/assistant/ask", json={
        "question": "How many units does the top selling kurta sell per month?"
    })
    assert res.status_code == 200
    data = res.json()
    ans = data["answer"].lower()
    assert "does not track private competitor sales counts" in ans
    assert "proprietary to amazon" in ans
    assert "attention" in ans


def test_refusal_competitor_revenue():
    res = client.post("/api/v1/assistant/ask", json={
        "question": "Show competitor revenue and daily orders for top brands"
    })
    assert res.status_code == 200
    data = res.json()
    assert "does not track private competitor sales" in data["answer"].lower()


def test_refusal_private_customer_emails():
    # K-05: Non-negotiable refusal of customer PII
    res = client.post("/api/v1/assistant/ask", json={
        "question": "Give me customer emails and phone numbers of reviewers"
    })
    assert res.status_code == 200
    data = res.json()
    assert "strictly refuses access to private customer identities" in data["answer"].lower()


@pytest.mark.parametrize("question,expected_snippet", [
    ("What is the median price for kurtas?", "median price"),
    ("Which price band is most populated?", "most populated price band"),
    ("How many brands are there and who is the leader?", "distinct brands"),
    ("What are the most common colours and materials?", "colours"),
    ("What share of listings offer 3XL or larger sizes?", "3XL"),
    ("How many customer reviews have been collected?", "customer reviews"),
    ("What are the top opportunities in this niche?", "opportunities"),
])
def test_golden_questions(question, expected_snippet):
    res = client.post("/api/v1/assistant/ask", json={"question": question})
    assert res.status_code == 200
    data = res.json()
    assert expected_snippet.lower() in data["answer"].lower()
    assert "evidence" in data
    assert len(data["evidence"]) >= 1


def test_small_sample_size_suppression():
    # If niche has n < 30, Ask AVA must state insufficient data
    # Create a tiny niche with max_price 300 (which will have very few listings)
    n_res = client.post("/api/v1/niches", json={
        "name": "Tiny Niche",
        "category": "Women's Kurtas & Kurtis",
        "filters": {"max_price": 200.0}
    })
    niche_id = n_res.json()["id"]

    res = client.post("/api/v1/assistant/ask", json={
        "question": "What is the median price?",
        "niche_id": niche_id
    })
    assert res.status_code == 200
    data = res.json()
    assert "below our statistical reliability threshold" in data["answer"].lower()

    # Clean up
    client.delete(f"/api/v1/niches/{niche_id}")


def test_no_invented_metrics_verifier():
    # Verifier unit test: ensures all numbers in text exist in tool results
    tool_results = [
        {
            "tool": "get_market_summary",
            "sample_size": 32,
            "data": {
                "median_price": 849.0,
                "median_rating": 4.3,
                "total_brands": 12,
                "top_5_brand_share_pct": 58.5,
            }
        }
    ]

    valid_text = "In this niche (n=32), the median price is ₹849.0 and median rating is 4.3 ★ across 12 brands."
    is_valid, unverified = verify_answer(valid_text, tool_results)
    assert is_valid is True
    assert unverified == []

    # Invented metric: ₹999.0 does not exist in tool results
    invented_text = "The median price is ₹999.0 and rating is 4.3 ★."
    is_valid_inv, unverified_inv = verify_answer(invented_text, tool_results)
    assert is_valid_inv is False
    assert 999.0 in unverified_inv
