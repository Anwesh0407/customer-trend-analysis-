"""Core validation and cleaning tests (Checklist D-11, D-12, D-13, D-14, D-15, D-16)."""
import pytest
from ava.processing.validation import (
    validate_and_extract_asin,
    validate_product_name,
)
from ava.processing.cleaning import DataCleaner
from ava.models import Product, Review


def test_asin_validation_and_url_extraction():
    # Valid 10 char
    asin, err = validate_and_extract_asin("b09xyz1234", "")
    assert asin == "B09XYZ1234" and err is None

    # Synthetic format
    asin, err = validate_and_extract_asin("SYN-KUR-001", "")
    assert asin == "SYN-KUR-001" and err is None

    # Extract from /dp/ URL
    asin, err = validate_and_extract_asin("", "https://example.com/dp/B08N5WRWNW?ref=123")
    assert asin == "B08N5WRWNW" and err is None

    # Extract from /gp/product/ URL
    asin, err = validate_and_extract_asin("", "https://example.com/gp/product/B07XYZ9999")
    assert asin == "B07XYZ9999" and err is None

    # Invalid ASIN
    asin, err = validate_and_extract_asin("INVALID", "")
    assert asin is None and "invalid_asin" in err


def test_product_name_validation():
    name, err = validate_product_name("Women A-Line Kurta")
    assert name == "Women A-Line Kurta" and err is None

    name, err = validate_product_name("")
    assert name is None and "missing_product_name" in err


def test_cleaning_deduplication_and_report(tmp_path):
    cleaner = DataCleaner(cleaned_dir=str(tmp_path))

    raw_items = [
        # Older item
        {
            "asin": "B011111111",
            "product_name": "Older Kurta",
            "price": "₹799",
            "collected_at": "2026-01-01T10:00:00Z",
            "material": "Cotton",
        },
        # Newer item with same ASIN -> should win
        {
            "asin": "B011111111",
            "product_name": "Newer Kurta Updated",
            "price": "₹899",
            "collected_at": "2026-02-01T10:00:00Z",
            "material": "Pure Cotton",
        },
        # Tie in time, but higher completeness
        {
            "asin": "B022222222",
            "product_name": "Tied Kurta Sparsely Filled",
            "price": "₹699",
            "collected_at": "2026-02-01T10:00:00Z",
            "colour": None,
            "material": None,
        },
        {
            "asin": "B022222222",
            "product_name": "Tied Kurta Complete",
            "price": "₹699",
            "mrp": "₹1,299",
            "collected_at": "2026-02-01T10:00:00Z",
            "colour": "Navy Blue",
            "material": "Rayon",
            "pattern": "Solid",
        },
        # Invalid row without name
        {
            "asin": "B033333333",
            "product_name": "",
            "price": "₹500",
        },
    ]

    products, rejected, report = cleaner.clean_products(raw_items, source_name="test_raw")

    # Verify counts
    assert report.rows_in == 5
    assert report.rows_out == 2  # B011111111 and B022222222
    assert report.duplicates_removed == 2
    assert report.rows_rejected == 1  # missing name

    # Verify newer collected_at won
    p1 = next(p for p in products if p.asin == "B011111111")
    assert p1.product_name == "Newer Kurta Updated"
    assert p1.price == 899.0

    # Verify completeness tiebreaker won
    p2 = next(p for p in products if p.asin == "B022222222")
    assert p2.product_name == "Tied Kurta Complete"
    assert p2.colour == "Navy Blue"


def test_review_cleaning_rules(tmp_path):
    cleaner = DataCleaner(cleaned_dir=str(tmp_path))

    raw_reviews = [
        {
            "product_id": "SYN-KUR-001",
            "rating": "5.0",
            "title": "Loved it!",
            "text": "Very breathable fabric.",
            "date": "Reviewed in India on 12 January 2026",
        },
        # Duplicate review
        {
            "product_id": "SYN-KUR-001",
            "rating": "5.0",
            "title": "Loved it!",
            "text": "Very breathable fabric.",
            "date": "Reviewed in India on 12 January 2026",
        },
        # Orphan review (ASIN not in known_asins)
        {
            "product_id": "UNKNOWN_ASIN_999",
            "rating": "4",
            "title": "Decent",
            "text": "Good fit",
            "date": "2026-02-01",
        },
        # Invalid rating outside 1-5
        {
            "product_id": "SYN-KUR-001",
            "rating": "0",
            "title": "",
            "text": "",
        },
    ]

    known_asins = {"SYN-KUR-001"}
    reviews, orphan_count = cleaner.clean_reviews(raw_reviews, known_asins=known_asins)

    # Duplicates removed, invalid dropped, orphan counted
    assert len(reviews) == 2  # SYN-KUR-001 and UNKNOWN_ASIN_999
    assert orphan_count == 1
    assert reviews[0].review_id is not None
    assert len(reviews[0].review_id) == 16  # Stable sha256 prefix
    assert "Reviewed in India on" not in reviews[0].review_date
