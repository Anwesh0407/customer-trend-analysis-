"""
AVA Validation Rules
Rules 3, 7, 8, 10, 11: ASIN extraction & validation, MRP/Price reconciliation, computed discounts.
"""

import re
from typing import Optional, Tuple, Dict, Any

ASIN_REGEX = re.compile(r'^[A-Z0-9]{10}$')
SYNTHETIC_ASIN_REGEX = re.compile(r'^SYN-[A-Z0-9_\-]+$', re.IGNORECASE)
URL_DP_REGEX = re.compile(r'/(?:dp|gp/product)/([A-Z0-9]{10})', re.IGNORECASE)

def validate_and_extract_asin(raw_asin: Any, product_url: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """
    Validates ASIN. If invalid or missing, attempts extraction from URL.
    Returns (clean_asin, rejection_reason).
    """
    candidate = str(raw_asin).strip().upper() if raw_asin is not None else ""

    # Synthetic ASINs accepted for demo compliance
    if SYNTHETIC_ASIN_REGEX.match(candidate):
        return candidate, None

    # Standard 10-char alphanumeric ASIN
    if ASIN_REGEX.match(candidate):
        return candidate, None

    # Attempt extraction from URL if available
    if product_url:
        match = URL_DP_REGEX.search(product_url)
        if match:
            return match.group(1).upper(), None

    return None, "missing_or_invalid_asin"

def validate_product_name(name: Any) -> Tuple[Optional[str], Optional[str]]:
    if name is None or str(name).strip() == "":
        return None, "missing_product_name"
    return str(name).strip(), None

def reconcile_price_and_mrp(
    price: Optional[float],
    mrp: Optional[float]
) -> Tuple[Optional[float], Optional[float], Optional[str]]:
    """
    Rule 7: If MRP < price, MRP is nulled and a data-quality note is returned.
    """
    if price is None:
        return None, None, "missing_price"

    if mrp is not None and mrp < price:
        return price, None, "mrp_less_than_price_nulled"

    return price, mrp, None

def compute_discount(
    price: Optional[float],
    mrp: Optional[float],
    source_discount: Any = None,
) -> Tuple[Optional[int], Optional[str]]:
    """
    Rule 8: Discount is COMPUTED from price and MRP. Source value is only fallback.
    Mismatches greater than 2 percentage points are logged.
    """
    src_val = None
    if source_discount is not None and str(source_discount).strip():
        m = re.search(r'(\d+)', str(source_discount))
        if m:
            src_val = int(m.group(1))

    if price is not None and mrp is not None and mrp > price and mrp > 0:
        computed = int(round(((mrp - price) / mrp) * 100))
        computed = max(0, min(100, computed))

        note = None
        if src_val is not None:
            diff = abs(computed - src_val)
            if diff > 2:
                note = f"discount_mismatch_computed_{computed}_vs_source_{src_val}"

        return computed, note

    if src_val is not None:
        return max(0, min(100, src_val)), None

    return None, None
