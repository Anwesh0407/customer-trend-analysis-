"""
AVA Master Data Cleaning Pipeline
Executes the 12 non-negotiable cleaning rules.
Produces data/cleaned/ products, rejected records with reasons, and comprehensive cleaning_report.json.
"""

import json
import csv
import os
import hashlib
import re
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple, Optional, Set
from pydantic import ValidationError as PydanticValidationError

from ava.models import Product, Review, CleaningReport
from ava.processing.columns import normalize_columns
from ava.processing.parsing import (
    parse_inr_price,
    parse_rating,
    parse_review_count,
    normalize_sizes,
    normalize_availability
)
from ava.processing.validation import (
    validate_and_extract_asin,
    validate_product_name,
    reconcile_price_and_mrp,
    compute_discount
)
from ava.logging_setup import logger

class DataCleaner:
    def __init__(self, cleaned_dir: str = "data/cleaned"):
        self.cleaned_dir = cleaned_dir
        os.makedirs(self.cleaned_dir, exist_ok=True)

    def clean_products(
        self,
        raw_items: List[Dict[str, Any]],
        source_name: str = "unknown"
    ) -> Tuple[List[Product], List[Dict[str, Any]], CleaningReport]:
        rejected_rows: List[Dict[str, Any]] = []
        quality_notes: Dict[str, int] = {}
        missing_counts: Dict[str, int] = {}
        unrecognised_set = set()

        pre_dedup_valid: List[Product] = []

        for idx, raw in enumerate(raw_items):
            # Rule 1: Column normalization
            norm_row, unrecognised = normalize_columns(raw)
            for u in unrecognised:
                unrecognised_set.add(u)

            # Rule 3: ASIN & Name validation
            url = norm_row.get("product_url", "")
            asin, asin_err = validate_and_extract_asin(norm_row.get("asin"), url)
            if asin_err:
                rejected_rows.append({"raw_index": idx, "asin": norm_row.get("asin"), "reason": asin_err, "raw": raw})
                continue

            name, name_err = validate_product_name(norm_row.get("product_name"))
            if name_err:
                rejected_rows.append({"raw_index": idx, "asin": asin, "reason": name_err, "raw": raw})
                continue

            # Rule 4 & 7: Price & MRP parsing
            price, price_note = parse_inr_price(norm_row.get("price"))
            if price_note:
                quality_notes[price_note] = quality_notes.get(price_note, 0) + 1
            if price is None:
                rejected_rows.append({"raw_index": idx, "asin": asin, "reason": "invalid_or_missing_price", "raw": raw})
                continue

            mrp, mrp_note = parse_inr_price(norm_row.get("mrp"))
            if mrp_note:
                quality_notes[mrp_note] = quality_notes.get(mrp_note, 0) + 1

            price, mrp, reconcile_note = reconcile_price_and_mrp(price, mrp)
            if reconcile_note:
                quality_notes[reconcile_note] = quality_notes.get(reconcile_note, 0) + 1

            # Rule 8: Computed Discount
            source_disc = norm_row.get("discount_pct")
            discount, disc_note = compute_discount(price, mrp, source_disc)
            if disc_note:
                quality_notes[disc_note] = quality_notes.get(disc_note, 0) + 1

            # Rule 5 & 6: Rating & Review count
            rating, rating_note = parse_rating(norm_row.get("rating"))
            if rating_note:
                quality_notes[rating_note] = quality_notes.get(rating_note, 0) + 1

            review_cnt, rev_note = parse_review_count(norm_row.get("review_count"))
            if rev_note:
                quality_notes[rev_note] = quality_notes.get(rev_note, 0) + 1

            # Rule 9: Sizes, Availability, Category, Brand
            sizes = normalize_sizes(norm_row.get("sizes"))
            availability = normalize_availability(norm_row.get("availability"))
            category = str(norm_row.get("category") or "Women's Clothing").strip()
            brand = str(norm_row.get("brand") or "Generic").strip()
            colour = str(norm_row.get("colour") or "Unknown").strip()
            material = str(norm_row.get("material") or "Unknown").strip()
            pattern = str(norm_row.get("pattern") or "Unknown").strip()
            seller = str(norm_row.get("seller") or "Unknown").strip()
            source = str(norm_row.get("source") or source_name).strip()
            collected_at = str(norm_row.get("collected_at") or datetime.now(timezone.utc).isoformat()).strip()

            candidate_dict = {
                "asin": asin,
                "product_name": name,
                "category": category,
                "brand": brand,
                "price": price,
                "mrp": mrp,
                "discount_pct": discount,
                "rating": rating,
                "review_count": review_cnt,
                "colour": colour,
                "material": material,
                "pattern": pattern,
                "sizes": sizes,
                "seller": seller,
                "availability": availability,
                "product_url": url or f"https://example.com/products/{asin}",
                "source": source,
                "collected_at": collected_at
            }

            # Track missing fields
            for k, v in candidate_dict.items():
                if v in (None, "", [], "Unknown"):
                    missing_counts[k] = missing_counts.get(k, 0) + 1

            # Rule 11: Final Pydantic validation
            try:
                prod = Product(**candidate_dict)
                pre_dedup_valid.append(prod)
            except PydanticValidationError as e:
                rejected_rows.append({"raw_index": idx, "asin": asin, "reason": f"pydantic_error:{e}", "raw": raw})

        # Rule 10: Deduplication to one row per ASIN
        # Newest collected_at wins; ties broken by completeness (count of non-empty attributes)
        dedup_map: Dict[str, Product] = {}
        duplicates_removed = 0

        for p in pre_dedup_valid:
            if p.asin not in dedup_map:
                dedup_map[p.asin] = p
            else:
                duplicates_removed += 1
                existing = dedup_map[p.asin]
                # Compare collected_at
                if p.collected_at > existing.collected_at:
                    dedup_map[p.asin] = p
                elif p.collected_at == existing.collected_at:
                    # Tiebreak by completeness
                    p_comp = sum(1 for _, v in p.model_dump().items() if v not in (None, "", [], "Unknown"))
                    ex_comp = sum(1 for _, v in existing.model_dump().items() if v not in (None, "", [], "Unknown"))
                    if p_comp > ex_comp:
                        dedup_map[p.asin] = p

        clean_products = list(dedup_map.values())

        # Compile rejection counts by reason
        rejected_counts: Dict[str, int] = {}
        for r in rejected_rows:
            reason = r.get("reason", "unknown")
            rejected_counts[reason] = rejected_counts.get(reason, 0) + 1

        report = CleaningReport(
            timestamp=datetime.now(timezone.utc).isoformat(),
            source_file=source_name,
            rows_in=len(raw_items),
            rows_out=len(clean_products),
            duplicates_removed=duplicates_removed,
            rejected_counts=rejected_counts,
            data_quality_notes=quality_notes,
            missing_counts_per_field=missing_counts,
            unrecognised_columns=sorted(list(unrecognised_set))
        )

        # Output to files
        self._save_cleaned_products(clean_products, rejected_rows, report)
        return clean_products, rejected_rows, report

    def clean_reviews(
        self,
        raw_reviews: List[Dict[str, Any]],
        known_asins: List[str]
    ) -> Tuple[List[Review], int]:
        """
        Rule 12: Reviews cleaning.
        - rating must be integer 1-5
        - title or text required
        - date parsed
        - duplicates removed
        - orphan reviews counted
        - stable SHA-256 hash review_id
        """
        seen_hashes = set()
        clean_reviews: List[Review] = []
        orphan_count = 0

        for r in raw_reviews:
            pid = str(r.get("product_id") or r.get("asin") or "").strip().upper()
            if not pid:
                continue

            if known_asins and pid not in known_asins:
                orphan_count += 1

            title = str(r.get("review_title") or r.get("title") or "").strip()
            text = str(r.get("review_text") or r.get("text") or "").strip()
            if not title and not text:
                continue

            try:
                raw_rating = r.get("rating", 5)
                rating = int(round(float(raw_rating)))
                rating = max(1, min(5, rating))
            except ValueError:
                continue

            raw_date = str(r.get("review_date") or r.get("date") or "2026-01-01").strip()
            # Clean "Reviewed in India on ..." text
            date_clean = re.sub(r'Reviewed in [a-zA-Z\s]+ on\s*', '', raw_date, flags=re.IGNORECASE).strip()

            source = str(r.get("source") or "synthetic_review").strip()
            collected_at = str(r.get("collected_at") or datetime.now(timezone.utc).isoformat()).strip()

            # Stable SHA-256 hash ID
            hash_input = f"{pid}_{rating}_{title}_{text[:100]}_{date_clean}"
            review_id = hashlib.sha256(hash_input.encode("utf-8")).hexdigest()[:16]

            if review_id in seen_hashes:
                continue
            seen_hashes.add(review_id)

            clean_reviews.append(
                Review(
                    review_id=review_id,
                    product_id=pid,
                    rating=rating,
                    review_title=title,
                    review_text=text,
                    review_date=date_clean,
                    source=source,
                    collected_at=collected_at
                )
            )

        self._save_cleaned_reviews(clean_reviews)
        logger.info(f"Cleaned {len(clean_reviews)} reviews (orphans={orphan_count})")
        return clean_reviews, orphan_count

    def _save_cleaned_products(
        self,
        products: List[Product],
        rejected: List[Dict[str, Any]],
        report: CleaningReport
    ):
        # 1. products_clean.json
        clean_json_path = os.path.join(self.cleaned_dir, "products_clean.json")
        with open(clean_json_path, "w", encoding="utf-8") as f:
            json.dump([p.model_dump() for p in products], f, indent=2)

        # 2. products_clean.csv
        clean_csv_path = os.path.join(self.cleaned_dir, "products_clean.csv")
        if products:
            fields = list(Product.model_fields.keys())
            with open(clean_csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for p in products:
                    row = p.model_dump()
                    row["sizes"] = json.dumps(row["sizes"])
                    writer.writerow(row)

        # 3. products_rejected.csv
        rej_csv_path = os.path.join(self.cleaned_dir, "products_rejected.csv")
        with open(rej_csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["raw_index", "asin", "reason", "raw_data"])
            writer.writeheader()
            for r in rejected:
                writer.writerow({
                    "raw_index": r.get("raw_index"),
                    "asin": r.get("asin"),
                    "reason": r.get("reason"),
                    "raw_data": json.dumps(r.get("raw", {}))
                })

        # 4. cleaning_report.json
        report_path = os.path.join(self.cleaned_dir, "cleaning_report.json")
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report.model_dump(), f, indent=2)

    def _save_cleaned_reviews(self, reviews: List[Review]):
        # reviews_clean.csv
        csv_path = os.path.join(self.cleaned_dir, "reviews_clean.csv")
        if reviews:
            fields = list(Review.model_fields.keys())
            with open(csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for r in reviews:
                    writer.writerow(r.model_dump())


def _find_latest_file(directory: str, prefix: str) -> Optional[str]:
    p = os.path.join(directory)
    if not os.path.exists(p):
        return None
    matches = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if f.startswith(prefix) and (f.endswith(".json") or f.endswith(".csv"))
    ]
    if not matches:
        return None
    matches.sort(key=os.path.getmtime, reverse=True)
    return matches[0]


def run_cleaning_pipeline(
    raw_product_path: Optional[str] = None,
    raw_review_path: Optional[str] = None,
    output_dir: str = "data/cleaned",
    limit: Optional[int] = None,
) -> Dict[str, Any]:
    """Top-level pipeline coordinator executing product and review cleaning."""
    from ava.sources.csv_source import CSVSource
    from ava.sources.json_source import JSONSource

    # 1. Resolve raw paths
    prod_path = raw_product_path or _find_latest_file("data/raw", "products_")
    if not prod_path:
        # Fall back to sample
        for fallback in ["data/sample/sample_products.csv", "data/sample/sample_products.json"]:
            if os.path.exists(fallback):
                prod_path = fallback
                break

    rev_path = raw_review_path or _find_latest_file("data/raw", "reviews_")
    if not rev_path:
        for fallback in ["data/sample/sample_reviews.csv", "data/sample/sample_reviews.json"]:
            if os.path.exists(fallback):
                rev_path = fallback
                break

    # 2. Fetch raw items
    raw_products: List[Dict[str, Any]] = []
    prod_source_name = "unknown"
    if prod_path:
        if prod_path.endswith(".json") or prod_path.endswith(".jsonl"):
            s = JSONSource(prod_path)
        else:
            s = CSVSource(prod_path)
        raw_products = s.fetch(limit=limit)
        prod_source_name = s.source_name

    raw_reviews: List[Dict[str, Any]] = []
    rev_source_name = "unknown"
    if rev_path:
        if rev_path.endswith(".json") or rev_path.endswith(".jsonl"):
            s = JSONSource(rev_path)
        else:
            s = CSVSource(rev_path)
        raw_reviews = s.fetch(limit=limit)
        rev_source_name = s.source_name

    # 3. Clean products and reviews
    cleaner = DataCleaner(cleaned_dir=output_dir)
    clean_products, rejected, report = cleaner.clean_products(raw_products, source_name=prod_source_name)

    known_asins = {p.asin for p in clean_products}
    clean_reviews, orphan_count = cleaner.clean_reviews(raw_reviews, known_asins=known_asins)

    return {
        "products_in": report.rows_in,
        "products_out": report.rows_out,
        "products_rejected": report.rows_rejected,
        "duplicates_removed": report.duplicates_removed,
        "reviews_in": len(raw_reviews),
        "reviews_out": len(clean_reviews),
        "orphan_reviews": orphan_count,
        "cleaning_report": report.model_dump(),
    }
