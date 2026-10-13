"""Core parsing tests (Checklist D-06, D-07, D-08, D-09, D-10)."""
import pytest
from ava.processing.parsing import (
    parse_inr_price,
    parse_rating,
    parse_review_count,
    normalize_sizes,
    normalize_availability,
)
from ava.processing.validation import (
    reconcile_price_and_mrp,
    compute_discount,
    validate_and_extract_asin,
    validate_product_name,
)


def test_inr_price_parsing():
    # Rupee signs, commas, decimals, suffixes
    p, note = parse_inr_price("₹1,299.00")
    assert p == 1299.0 and note is None

    p, note = parse_inr_price("Rs. 849/-")
    assert p == 849.0 and note is None

    p, note = parse_inr_price("INR 15,000")  # Indian grouping within cap
    assert p == 15000.0 and note is None

    p, note = parse_inr_price("INR 1,50,000")  # Exceeds 50k cap
    assert p is None and note == "price_exceeds_cap"

    p, note = parse_inr_price("500")
    assert p == 500.0

    # Invalid: range, zero, negative, extreme values
    p, note = parse_inr_price("500 - 800")
    assert p is None and note == "price_range_rejected"

    p, note = parse_inr_price("-150")
    assert p is None and note == "negative_price_rejected"

    p, note = parse_inr_price("0")
    assert p is None and note == "zero_price_rejected"

    p, note = parse_inr_price("₹999,999.00")
    assert p is None and note == "price_exceeds_cap"

    p, note = parse_inr_price(None)
    assert p is None and note is None


def test_rating_parsing():
    r, note = parse_rating("4.3 out of 5 stars")
    assert r == 4.3 and note is None

    r, note = parse_rating("4.5")
    assert r == 4.5 and note is None

    r, note = parse_rating("0")  # 0 means unrated -> None
    assert r is None and note == "unrated_zero_rating"

    r, note = parse_rating("5.8")  # outside 1-5 -> None
    assert r is None and note == "rating_outside_range"


def test_review_count_parsing():
    c, note = parse_review_count("1,234")
    assert c == 1234

    c, note = parse_review_count("1.2K")
    assert c == 1200

    c, note = parse_review_count("2 ratings")
    assert c == 2

    c, note = parse_review_count("0")
    assert c == 0

    c, note = parse_review_count("N/A")
    assert c is None


def test_size_normalization():
    # Canonical ordering: XS, S, M, L, XL, XXL, 3XL, 4XL, 5XL, 6XL, Free Size
    sizes = normalize_sizes("XXL, S, M, Free Size, 3XL, XS, L")
    assert sizes == ["XS", "S", "M", "L", "XXL", "3XL", "Free Size"]


def test_availability_normalization():
    assert normalize_availability("In stock") == "in_stock"
    assert normalize_availability("Only 2 left in stock") == "limited"
    assert normalize_availability("Currently unavailable") == "out_of_stock"
    assert normalize_availability("discontinued") == "out_of_stock"
    assert normalize_availability("random text") == "unknown"


def test_mrp_less_than_price():
    # Rule 7: If MRP < price -> MRP nulled and flagged
    price, mrp, note = reconcile_price_and_mrp(899.0, 599.0)
    assert price == 899.0
    assert mrp is None
    assert "mrp_less_than_price" in note


def test_discount_computation():
    # Rule 8: Discount computed from price and MRP
    # Price 799, MRP 1599 -> (1599 - 799) / 1599 = 50.03% -> 50%
    disc, note = compute_discount(799.0, 1599.0, source_discount="40%")
    assert disc == 50
    assert "discount_mismatch" in note
