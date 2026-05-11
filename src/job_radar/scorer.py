"""Rule-based profile fit scorer. No AI cost. Tunable via profile_config."""
from __future__ import annotations

from .models import Job
from .profile_config import (
    JD_BONUS_KEYWORDS,
    LOCATIONS_PREFERRED,
    PROFILE_LEVEL_TARGETS,
    TARGET_COMPANIES_HOT,
    TIER1_KEYWORDS,
    TIER2_KEYWORDS,
    TITLE_BLOCKLIST,
    TITLE_BONUS_KEYWORDS,
)


def _contains_any(text: str, keywords: list[str]) -> int:
    """Return count of keywords present in lowercased text."""
    if not text:
        return 0
    t = text.lower()
    return sum(1 for k in keywords if k.lower() in t)


def score_job(job: Job) -> int:
    """
    Returns an integer score. >60 = high confidence, 30-60 = worth checking.
    Negative score = filtered out before reaching the sheet.
    """
    title = (job.title or "").lower()
    desc = (job.description or "").lower()
    company = (job.company or "").lower()
    location = (job.location or "").lower()

    # ---- Hard filters first ----
    for bad in TITLE_BLOCKLIST:
        if bad in title:
            return -100

    # ---- Function fit ----
    tier1_hits = _contains_any(title, TIER1_KEYWORDS)
    tier2_hits = _contains_any(title, TIER2_KEYWORDS)
    if tier1_hits == 0 and tier2_hits == 0:
        # Sometimes the function is only in description; check JD too
        tier1_hits_jd = _contains_any(desc, TIER1_KEYWORDS)
        if tier1_hits_jd == 0:
            return -50  # not your function
        # JD-only match = lower confidence
        function_score = 5
    else:
        function_score = tier1_hits * 15 + tier2_hits * 10

    # ---- Seniority ----
    seniority_score = 0
    if any(lvl in title for lvl in PROFILE_LEVEL_TARGETS):
        seniority_score = 20
    elif "manager" in title and "associate" not in title:
        seniority_score = 8  # plain "Manager" — could be junior or senior

    # Penalty for over-senior roles (you have 7 YoE)
    over_senior_signals = ["svp", "chief executive", "ceo,", " cto", " cfo",
                          "chief revenue officer", "chief product officer"]
    if any(s in title for s in over_senior_signals):
        seniority_score -= 30

    # ---- Title bonus ----
    title_bonus = _contains_any(title, TITLE_BONUS_KEYWORDS) * 3

    # ---- Location ----
    loc_score = 10 if any(l in location for l in LOCATIONS_PREFERRED) else -10
    if "remote" in location or "anywhere" in location:
        loc_score += 5

    # ---- Company prestige ----
    company_score = 0
    for hot in TARGET_COMPANIES_HOT:
        if hot in company:
            company_score = 20
            break

    # ---- JD signals ----
    jd_score = min(_contains_any(desc, JD_BONUS_KEYWORDS) * 2, 15)

    # YoE matching from description
    yoe_score = 0
    if any(p in desc for p in ["6+ year", "7+ year", "5+ year", "6-10 year",
                                "7-10 year", "5-8 year", "6 to 10 year"]):
        yoe_score = 10
    if any(p in desc for p in ["12+ year", "15+ year", "10-15 year", "10+ year"]):
        yoe_score -= 5  # marginally over your YoE

    # ---- Salary ----
    salary_score = 0
    if job.salary_max_inr and job.salary_max_inr >= 50e5:
        salary_score = 30
    elif job.salary_max_inr and job.salary_max_inr >= 35e5:
        salary_score = 10
    elif job.salary_min_inr and job.salary_min_inr < 25e5:
        salary_score = -20  # explicitly too low

    total = (function_score + seniority_score + title_bonus +
             loc_score + company_score + jd_score + yoe_score + salary_score)
    return total


def assign_tier(job: Job) -> str:
    s = job.score
    if s >= 60:
        return "🔥 High Confidence"
    elif s >= 30:
        return "🟡 Worth Checking"
    else:
        return ""  # filtered out
