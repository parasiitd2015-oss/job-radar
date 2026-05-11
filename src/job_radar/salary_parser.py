"""Parse salary text into INR per year. Handles INR, USD, GBP, SGD, AED, ranges."""
from __future__ import annotations

import re
from typing import Optional

USD_INR = 83.5
GBP_INR = 105.0
SGD_INR = 62.0
AED_INR = 22.7
EUR_INR = 90.5

# Currency hints
CURRENCY_PATTERNS = {
    "INR": [r"₹", r"\bRs\.?\b", r"\bINR\b", r"\bLakhs?\b", r"\bLPA\b", r"\bCrores?\b", r"\bCr\b"],
    "USD": [r"\$", r"\bUSD\b", r"\bUS dollars?\b"],
    "GBP": [r"£", r"\bGBP\b", r"\bBritish pounds?\b"],
    "SGD": [r"\bSGD\b", r"S\$"],
    "AED": [r"\bAED\b", r"\bdirham"],
    "EUR": [r"€", r"\bEUR\b", r"\beuros?\b"],
}


def _detect_currency(text: str) -> str:
    for cur, patterns in CURRENCY_PATTERNS.items():
        for p in patterns:
            if re.search(p, text, flags=re.IGNORECASE):
                return cur
    return "UNKNOWN"


def _to_inr(amount: float, currency: str) -> float:
    return {
        "INR": amount,
        "USD": amount * USD_INR,
        "GBP": amount * GBP_INR,
        "SGD": amount * SGD_INR,
        "AED": amount * AED_INR,
        "EUR": amount * EUR_INR,
        "UNKNOWN": amount,  # assume INR if currency missing
    }.get(currency, amount)


def parse_salary(text: str) -> tuple[Optional[float], Optional[float]]:
    """
    Returns (min_inr_per_year, max_inr_per_year) or (None, None) if unparseable.
    Handles common patterns:
        - "₹50-90 LPA"
        - "$130,000 - $180,000"
        - "65L - 90L"
        - "1.5 crore - 2 crore"
        - "150K USD"
    """
    if not text:
        return None, None

    text = text.strip()
    currency = _detect_currency(text)

    # Pattern: "X - Y unit" or "X to Y unit"
    # Capture all numeric-like tokens
    nums = re.findall(r"(\d+(?:[\.,]\d+)*)", text)
    if not nums:
        return None, None

    # Normalize: strip commas, parse
    try:
        parsed = [float(n.replace(",", "")) for n in nums]
    except ValueError:
        return None, None

    if not parsed:
        return None, None

    # Determine multiplier from unit hints
    lower = text.lower()
    multiplier = 1.0
    if any(x in lower for x in ["crore", "cr ", "cr.", " cr"]):
        multiplier = 1e7
    elif any(x in lower for x in ["lakh", "lac", "lpa", "l ", "l."]):
        # "65 LPA" or "65L" → 65 lakh
        multiplier = 1e5
    elif "k" in lower and currency != "INR":
        # "$150K" → 150,000
        multiplier = 1e3
    elif currency in ("USD", "GBP", "SGD", "AED", "EUR") and max(parsed) < 1000:
        # Probably annual but tiny — likely a unit like "150" meaning 150K
        multiplier = 1e3

    # Filter out obviously non-salary numbers (years, dates, percentages)
    plausible = []
    for n in parsed:
        scaled = n * multiplier
        scaled_inr = _to_inr(scaled, currency)
        # Plausible annual salary range: ₹3L to ₹10Cr
        if 3e5 <= scaled_inr <= 1e8:
            plausible.append(scaled_inr)

    if not plausible:
        return None, None
    if len(plausible) == 1:
        return plausible[0], plausible[0]
    return min(plausible), max(plausible)
