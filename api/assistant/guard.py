"""Guardrails for Ask AVA: input validation, scope enforcement, and refusals."""
from __future__ import annotations

import re
from typing import Optional, Tuple

REFUSAL_SALES = (
    "AVA does not track private competitor sales counts, daily order volumes, or revenue numbers. "
    "Marketplace sales volumes are proprietary to Amazon and individual vendors. "
    "However, we can analyze cumulative customer review counts as an indicator of relative customer attention and listing maturity."
)

REFUSAL_PRIVATE_DATA = (
    "AVA strictly refuses access to private customer identities, email addresses, phone numbers, or personal accounts. "
    "In accordance with marketplace compliance and privacy policies, reviewer identities are never collected or stored. "
    "All review analytics are performed strictly on anonymized, public review text and star ratings."
)


def check_input_guards(question: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """Checks input question against scope and abuse guardrails.

    Returns:
        (is_allowed: bool, refusal_response: Optional[str], refusal_category: Optional[str])
    """
    clean_q = question.strip()
    if len(clean_q) < 2:
        return False, "Please enter a valid question with at least 2 characters.", "too_short"
    if len(clean_q) > 1000:
        return False, "Question exceeds the maximum length of 1000 characters. Please shorten your query.", "too_long"

    lower_q = clean_q.lower()

    # 1. Competitor sales / revenue / units sold refusal (Non-negotiable Rule 8)
    sales_patterns = [
        r'\bhow many (units|items|pieces|orders) (does|did|has|is) .+ (sell|sold)',
        r'\b(sales|unit sales|units sold|daily orders|monthly orders|order count)\b',
        r'\bcompetitor (revenue|turnover|profit|earnings|sales)\b',
        r'\bshow (me )?(competitor|brand) (revenue|turnover|sales count)\b',
        r'\bexact sales volume\b',
    ]
    for pat in sales_patterns:
        if re.search(pat, lower_q):
            return False, REFUSAL_SALES, "sales_refusal"

    # 2. Private customer data / PII refusal
    private_patterns = [
        r'\b(customer|buyer) (email|phone|contact|address|name|identity|pii|data)\b',
        r'\bgive (me )?(customer|buyer) emails\b',
        r'\bwho (bought|reviewed|purchased)\b',
        r'\buser identities\b',
        r'\blead generation\b',
    ]
    for pat in private_patterns:
        if re.search(pat, lower_q):
            return False, REFUSAL_PRIVATE_DATA, "privacy_refusal"

    return True, None, None
