"""
AVA Data Parsers
Rules 4, 5, 6, 8, 9: Price/INR parsing, ratings, review counts, canonical sizes, availability.
"""

import re
from typing import Optional, List, Tuple, Any
from ava.config import settings

CANONICAL_SIZES_ORDER = ["XS", "S", "M", "L", "XL", "XXL", "3XL", "4XL", "5XL", "6XL", "Free Size"]

def parse_inr_price(val: Any) -> Tuple[Optional[float], Optional[str]]:
    """
    Parses string or numeric price to float INR.
    Returns (price, quality_note).
    """
    if val is None or val == "" or str(val).strip().lower() in ("none", "nan", "null", "n/a"):
        return None, None

    s = str(val).strip()

    # Strip traditional Indian rupee suffix "/-" before range check
    s = re.sub(r'/-\s*$', '', s).strip()

    # Detect price ranges e.g. "500 - 800" or "500 to 800"
    if re.search(r'\d+\s*(?:-|to)\s*\d+', s, re.IGNORECASE):
        return None, "price_range_rejected"

    # Detect non-INR currencies
    if any(c in s for c in ["$", "€", "£", "USD", "EUR", "GBP"]):
        return None, "non_inr_currency"

    # Strip currency words and symbols, keeping digits and decimal period
    cleaned = re.sub(r'(?i)\b(rs|inr)\.?|[₹/–]', '', s).strip()
    cleaned = cleaned.replace(",", "")

    try:
        num = float(cleaned)
    except ValueError:
        return None, "unparseable_price"

    if num < 0.0:
        return None, "negative_price_rejected"

    if num == 0.0:
        return None, "zero_price_rejected"

    if num > settings.MAX_PRICE_CAP_INR:
        return None, "price_exceeds_cap"

    return round(num, 2), None

def parse_rating(val: Any) -> Tuple[Optional[float], Optional[str]]:
    """
    Parses rating to float between 1.0 and 5.0.
    Handles '4.3 out of 5 stars', '4.3/5', etc. 0 means unrated.
    """
    if val is None or val == "" or str(val).strip().lower() in ("none", "nan", "null", "n/a"):
        return None, None

    s = str(val).strip()
    match = re.search(r'([0-9]+(?:\.[0-9]+)?)', s)
    if not match:
        return None, "unparseable_rating"

    try:
        r = float(match.group(1))
    except ValueError:
        return None, "unparseable_rating"

    if r == 0.0:
        return None, "unrated_zero_rating"

    if r < 1.0 or r > 5.0:
        return None, "rating_outside_range"

    return round(r, 2), None

def parse_review_count(val: Any) -> Tuple[Optional[int], Optional[str]]:
    """
    Parses review count handling numbers with commas, K, M, and words.
    e.g. '1,234', '1.2K', '2 ratings' -> int.
    """
    if val is None or val == "" or str(val).strip().lower() in ("none", "nan", "null", "n/a"):
        return None, None

    s = str(val).strip().replace(",", "")
    match = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*([kKmM])?', s)
    if not match:
        return None, "unparseable_review_count"

    num_part = float(match.group(1))
    multiplier = match.group(2)

    if multiplier and multiplier.lower() == "k":
        count = int(num_part * 1000)
    elif multiplier and multiplier.lower() == "m":
        count = int(num_part * 1000000)
    else:
        count = int(num_part)

    if count < 0:
        return None, "negative_review_count"

    return count, None

def normalize_sizes(val: Any) -> List[str]:
    """
    Splits string/list into distinct sizes and sorts them in canonical order:
    XS, S, M, L, XL, XXL, 3XL ... 6XL, Free Size.
    """
    if not val:
        return []

    raw_list: List[str] = []
    if isinstance(val, list):
        raw_list = [str(x) for x in val]
    elif isinstance(val, str):
        raw_list = re.split(r'[,/|]+', val)

    mapped: List[str] = []
    for s in raw_list:
        clean = s.strip()
        if not clean:
            continue
        clean_upper = clean.upper()
        if clean_upper in ("EXTRA SMALL", "X-SMALL"):
            mapped.append("XS")
        elif clean_upper in ("SMALL",):
            mapped.append("S")
        elif clean_upper in ("MEDIUM", "MED"):
            mapped.append("M")
        elif clean_upper in ("LARGE",):
            mapped.append("L")
        elif clean_upper in ("EXTRA LARGE", "X-LARGE"):
            mapped.append("XL")
        elif clean_upper in ("DOUBLE EXTRA LARGE", "XX-LARGE", "2XL"):
            mapped.append("XXL")
        elif clean_upper in ("TRIPLE EXTRA LARGE", "3X-LARGE"):
            mapped.append("3XL")
        elif clean_upper in ("FREE", "FREESIZE", "FREE SIZE", "ONE SIZE", "ONESIZE"):
            mapped.append("Free Size")
        else:
            mapped.append(clean)

    # Sort according to canonical list
    ordered: List[str] = []
    for canon in CANONICAL_SIZES_ORDER:
        if canon in mapped:
            ordered.append(canon)

    # Add any non-standard remaining sizes
    for item in mapped:
        if item not in CANONICAL_SIZES_ORDER and item not in ordered:
            ordered.append(item)

    return ordered

def normalize_availability(val: Any) -> str:
    """Normalizes availability to in_stock | limited | out_of_stock | unknown."""
    if not val:
        return "unknown"
    s = str(val).strip().lower()
    if "discontinued" in s or "out of stock" in s or "unavailable" in s:
        return "out_of_stock"
    if "limited" in s or "only" in s or "left in stock" in s or "few left" in s:
        return "limited"
    if "in stock" in s or "available" in s or "instock" in s:
        return "in_stock"
    return "unknown"
