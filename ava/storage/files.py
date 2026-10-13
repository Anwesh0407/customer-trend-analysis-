"""Loader to read cleaned files from disk into the database."""
from __future__ import annotations

import csv
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional
import uuid

from ava.models import Product, Review
from ava.storage.base import Repository

logger = logging.getLogger("ava.storage.files")


def load_cleaned_data_to_db(
    repo: Repository,
    cleaned_dir: str = "data/cleaned",
) -> Dict[str, Any]:
    """Loads products_clean and reviews_clean into the repository and verifies against cleaning_report.json."""
    c_path = Path(cleaned_dir)
    prod_csv = c_path / "products_clean.csv"
    prod_json = c_path / "products_clean.json"
    rev_csv = c_path / "reviews_clean.csv"
    report_file = c_path / "cleaning_report.json"

    if not prod_csv.exists() and not prod_json.exists():
        raise FileNotFoundError(f"No cleaned products file found in {cleaned_dir}")

    # 1. Read products
    products: List[Product] = []
    if prod_csv.exists():
        with open(prod_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # parse sizes
                raw_sizes = row.get("sizes", "")
                parsed_sizes = []
                if raw_sizes:
                    try:
                        parsed_sizes = json.loads(raw_sizes)
                    except Exception:
                        parsed_sizes = [s.strip() for s in raw_sizes.split(",") if s.strip()]

                def _parse_float(v: Any) -> Optional[float]:
                    if v is None or v == "":
                        return None
                    try:
                        return float(v)
                    except ValueError:
                        return None

                def _parse_int(v: Any) -> Optional[int]:
                    if v is None or v == "":
                        return None
                    try:
                        return int(float(v))
                    except ValueError:
                        return None

                def _parse_dt(v: Any) -> Optional[datetime]:
                    if not v:
                        return None
                    try:
                        return datetime.fromisoformat(v.replace("Z", "+00:00"))
                    except Exception:
                        return None

                p = Product(
                    asin=row["asin"],
                    product_name=row["product_name"],
                    category=row.get("category", "Women's Kurtas & Kurtis"),
                    brand=row.get("brand"),
                    price=_parse_float(row.get("price")),
                    mrp=_parse_float(row.get("mrp")),
                    discount_pct=_parse_float(row.get("discount_pct")),
                    rating=_parse_float(row.get("rating")),
                    review_count=_parse_int(row.get("review_count")),
                    colour=row.get("colour"),
                    material=row.get("material"),
                    pattern=row.get("pattern"),
                    sizes=parsed_sizes,
                    seller=row.get("seller"),
                    availability=row.get("availability", "in_stock"),
                    product_url=row.get("product_url"),
                    source=row.get("source", "file"),
                    collected_at=_parse_dt(row.get("collected_at")),
                )
                products.append(p)
    elif prod_json.exists():
        with open(prod_json, "r", encoding="utf-8") as f:
            data = json.load(f)
            for row in data:
                products.append(Product(**row))

    # 2. Read reviews
    reviews: List[Review] = []
    if rev_csv.exists():
        with open(rev_csv, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                def _parse_dt(v: Any) -> Optional[datetime]:
                    if not v:
                        return None
                    try:
                        return datetime.fromisoformat(v.replace("Z", "+00:00"))
                    except Exception:
                        return None

                dt_rev = _parse_dt(row.get("review_date")) or row.get("review_date") or None
                dt_col = _parse_dt(row.get("collected_at")) or row.get("collected_at") or datetime.now(timezone.utc).isoformat()

                reviews.append(
                    Review(
                        review_id=row["review_id"],
                        product_id=row["product_id"],
                        rating=int(row["rating"]),
                        review_title=row.get("review_title"),
                        review_text=row.get("review_text"),
                        review_date=dt_rev,
                        source=row.get("source", "file"),
                        collected_at=dt_col,
                    )
                )

    # 3. Save to repository
    prods_saved = repo.save_products(products)
    revs_saved = repo.save_reviews(reviews)

    # 4. Read report and verify
    report_data = {}
    verified = False
    expected_rows_out = None
    if report_file.exists():
        with open(report_file, "r", encoding="utf-8") as f:
            report_data = json.load(f)
            expected_rows_out = report_data.get("rows_out")
            if expected_rows_out is not None:
                verified = (len(products) == expected_rows_out)

    data_mode = "demo"
    if any("synthetic" in p.source.lower() or "demo" in p.source.lower() or "sample" in p.source.lower() for p in products):
        data_mode = "demo"
    else:
        data_mode = "real"

    run_record = {
        "id": f"run_{uuid.uuid4().hex[:8]}",
        "source": "cleaned_files",
        "file": str(prod_csv if prod_csv.exists() else prod_json),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "completed_at": datetime.now(timezone.utc).isoformat(),
        "rows_in": len(products),
        "rows_out": prods_saved,
        "rows_rejected": 0,
        "status": "completed",
        "data_mode": data_mode,
        "details": {
            "products_count": len(products),
            "reviews_count": len(reviews),
            "verified_against_report": verified,
            "expected_rows_out": expected_rows_out,
        },
    }
    repo.save_ingest_run(run_record)

    logger.info(
        "Loaded %d products and %d reviews to database. Report match: %s",
        len(products),
        len(reviews),
        verified,
    )

    return {
        "products_loaded": len(products),
        "products_saved": prods_saved,
        "reviews_loaded": len(reviews),
        "reviews_saved": revs_saved,
        "verified_against_report": verified,
        "expected_rows_out": expected_rows_out,
        "data_mode": data_mode,
    }
