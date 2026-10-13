"""Compliance and source adapter tests (Checklist C-01 to C-08, D-01, D-02)."""
import os
import pytest
from ava.exceptions import (
    ComplianceViolation,
    DomainBlockedError,
    SourceUnavailable,
)
from ava.http_client import CompliantHttpClient
from ava.sources.csv_source import CSVSource
from ava.sources.json_source import JSONSource
from ava.sources.creators_api_source import CreatorsApiSource


def test_blocked_domains_compliance():
    # C-05: Amazon domains strictly blocked from scraping
    client = CompliantHttpClient()
    with pytest.raises(DomainBlockedError) as exc:
        client.get("https://www.amazon.in/dp/B08N5WRWNW")
    assert "blocked" in str(exc.value).lower()
    assert "Prohibited marketplace domain" in str(exc.value)

    with pytest.raises(DomainBlockedError):
        client.get("https://m.media-amazon.com/images/I/71xyz.jpg")


def test_creators_api_missing_credentials():
    # C-06: Missing credentials raises clear SourceUnavailable error, suggests CSV/JSON
    original_key = os.environ.pop("AMAZON_CREATORS_API_KEY", None)
    try:
        source = CreatorsApiSource()
        with pytest.raises(SourceUnavailable) as exc:
            source.fetch()
        assert "Amazon Creators API credentials not configured" in str(exc.value)
        assert "CSV or JSON" in str(exc.value)
    finally:
        if original_key:
            os.environ["AMAZON_CREATORS_API_KEY"] = original_key


def test_csv_source_bom_ragged_blanks(tmp_path):
    # D-01: CSV source with BOM, ragged rows, blank lines
    csv_file = tmp_path / "test_bom.csv"
    content = (
        "\ufeffASIN,Product Name,Price,Brand\n"  # BOM header
        "\n"                                     # blank line
        "SYN-001,Kurta A,₹799,BrandA\n"
        "SYN-002,Kurta B,₹899\n"                 # ragged row (too short)
        "\n"
        "SYN-003,Kurta C,₹999,BrandC,ExtraCol\n" # ragged row (too long)
    )
    csv_file.write_text(content, encoding="utf-8")

    source = CSVSource(str(csv_file))
    records = source.fetch()

    assert len(records) == 3
    assert records[0]["ASIN"] == "SYN-001"
    assert records[0]["Brand"] == "BrandA"
    assert records[1]["ASIN"] == "SYN-002"
    assert records[1]["Brand"] == ""  # padded


def test_json_source_formats(tmp_path):
    # D-02: JSON array, JSON Lines, wrapped envelope

    # 1. Standard Array
    f1 = tmp_path / "array.json"
    f1.write_text('[{"asin": "A1", "name": "Item 1"}]', encoding="utf-8")
    assert len(JSONSource(str(f1)).fetch()) == 1

    # 2. Wrapped Object
    f2 = tmp_path / "wrapped.json"
    f2.write_text('{"items": [{"asin": "W1"}, {"asin": "W2"}]}', encoding="utf-8")
    assert len(JSONSource(str(f2)).fetch()) == 2

    # 3. JSON Lines
    f3 = tmp_path / "lines.jsonl"
    f3.write_text('{"asin": "L1"}\n\n{"asin": "L2"}\n', encoding="utf-8")
    assert len(JSONSource(str(f3)).fetch()) == 2
