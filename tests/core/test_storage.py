"""Storage and repository tests (Checklist B-01, B-02, B-04, B-05, T-04)."""
import pytest
from datetime import datetime, timezone
from ava.models import Product, Review, Niche
from ava.storage.sql_repository import SQLAlchemyRepository


def test_sqlite_repository_roundtrip(tmp_path):
    db_file = tmp_path / "test_ava.db"
    db_url = f"sqlite:///{db_file}"
    repo = SQLAlchemyRepository(database_url=db_url)
    repo.init_db()

    # 1. Categories seeded
    cats = repo.get_categories()
    assert len(cats) >= 3
    assert any(c["name"] == "Women's Kurtas & Kurtis" for c in cats)

    # 2. Products save and upsert
    p1 = Product(
        asin="SYN-TST-001",
        product_name="Test Kurta",
        category="Women's Kurtas & Kurtis",
        brand="AVA Brand",
        price=799.0,
        mrp=1499.0,
        discount_pct=47,
        rating=4.5,
        review_count=120,
        colour="Blue",
        material="Cotton",
        pattern="Solid",
        sizes=["S", "M", "L"],
        seller="AVA Direct",
        availability="in_stock",
        product_url="https://example.com/dp/SYN-TST-001",
        source="synthetic_test",
        collected_at=datetime.now(timezone.utc).isoformat(),
    )
    saved_cnt = repo.save_products([p1])
    assert saved_cnt == 1

    # Fetch product by ASIN
    fetched = repo.get_product_by_asin("SYN-TST-001")
    assert fetched is not None
    assert fetched["product_name"] == "Test Kurta"
    assert fetched["price"] == 799.0
    assert fetched["sizes"] == ["S", "M", "L"]

    # Upsert with newer date -> updates
    p1_updated = p1.model_copy(update={"product_name": "Test Kurta Updated", "price": 849.0})
    repo.save_products([p1_updated])
    fetched_updated = repo.get_product_by_asin("SYN-TST-001")
    assert fetched_updated["price"] == 849.0
    assert fetched_updated["product_name"] == "Test Kurta Updated"

    # 3. Niches CRUD
    niche = Niche(
        id="niche_cotton_under_1000",
        name="Cotton Under ₹1000",
        category="Women's Kurtas & Kurtis",
        filters={"max_price": 1000.0, "materials": ["Cotton"]},
        description="Daily wear budget cotton kurtas",
    )
    saved_niche = repo.save_niche(niche)
    assert saved_niche["id"] == "niche_cotton_under_1000"

    all_niches = repo.get_niches()
    assert len(all_niches) == 1
    assert all_niches[0]["name"] == "Cotton Under ₹1000"

    # Delete niche
    assert repo.delete_niche("niche_cotton_under_1000") is True
    assert repo.get_niche_by_id("niche_cotton_under_1000") is None


def test_postgresql_schema_compilation():
    """Verify all table DDL compiles cleanly for PostgreSQL dialect (B-02, B-03, T-06)."""
    from sqlalchemy.dialects import postgresql
    from sqlalchemy.schema import CreateTable
    from ava.storage.sql_repository import (
        CategoryModel,
        ProductModel,
        ReviewModel,
        NicheModel,
        IngestRunModel,
        ChatLogModel,
    )

    pg_dialect = postgresql.dialect()
    tables = [
        CategoryModel.__table__,
        ProductModel.__table__,
        ReviewModel.__table__,
        NicheModel.__table__,
        IngestRunModel.__table__,
        ChatLogModel.__table__,
    ]

    for table in tables:
        ddl = str(CreateTable(table).compile(dialect=pg_dialect))
        assert "CREATE TABLE" in ddl
        assert table.name in ddl

