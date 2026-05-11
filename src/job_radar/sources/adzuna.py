"""Adzuna job board API. Free tier: 1k calls/month per app_id."""
from __future__ import annotations

import os
from datetime import datetime
from typing import Iterable

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..models import Job
from ..profile_config import ADZUNA_COUNTRIES
from ..salary_parser import parse_salary

ADZUNA_BASE = "https://api.adzuna.com/v1/api/jobs"

# Search queries — keep small to stay within free quota
ADZUNA_QUERIES = [
    "growth manager",
    "head of growth",
    "director growth",
    "chief of staff",
    "product manager senior",
    "strategy manager",
    "business development director",
]


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=10))
def _fetch_country(country: str, query: str, app_id: str, app_key: str) -> list[dict]:
    url = f"{ADZUNA_BASE}/{country}/search/1"
    params = {
        "app_id": app_id,
        "app_key": app_key,
        "what": query,
        "results_per_page": 50,
        "sort_by": "date",
        "max_days_old": 7,
    }
    with httpx.Client(timeout=30) as client:
        r = client.get(url, params=params)
        if r.status_code == 429:
            raise httpx.HTTPStatusError("Rate limited", request=r.request, response=r)
        r.raise_for_status()
        return r.json().get("results", [])


def fetch_adzuna_jobs() -> Iterable[Job]:
    app_id = os.getenv("ADZUNA_APP_ID", "").strip()
    app_key = os.getenv("ADZUNA_APP_KEY", "").strip()
    if not app_id or not app_key:
        return  # silently skip if not configured

    seen = set()
    for country in ADZUNA_COUNTRIES:
        for query in ADZUNA_QUERIES:
            try:
                raw_jobs = _fetch_country(country, query, app_id, app_key)
            except Exception as e:
                print(f"  [adzuna] {country}/{query} failed: {e}")
                continue

            for r in raw_jobs:
                jid = str(r.get("id", ""))
                if jid in seen:
                    continue
                seen.add(jid)

                salary_text = ""
                if r.get("salary_min") and r.get("salary_max"):
                    cur = r.get("salary_is_predicted") and "USD" or ""
                    salary_text = f"{r['salary_min']:.0f} - {r['salary_max']:.0f} {cur}"

                min_inr, max_inr = parse_salary(salary_text)
                # Adzuna's salary is in local currency
                if r.get("salary_min") and not min_inr:
                    # Direct numeric
                    from ..salary_parser import _to_inr
                    local_cur = {
                        "in": "INR", "gb": "GBP", "sg": "SGD",
                        "ae": "AED", "au": "USD"  # AU returns AUD ~= USD/0.65
                    }.get(country, "USD")
                    min_inr = _to_inr(float(r["salary_min"]), local_cur)
                    max_inr = _to_inr(float(r.get("salary_max", r["salary_min"])), local_cur)

                posted_at = None
                if r.get("created"):
                    try:
                        posted_at = datetime.fromisoformat(
                            r["created"].replace("Z", "+00:00")
                        )
                    except (ValueError, TypeError):
                        pass

                yield Job(
                    title=r.get("title", "").strip(),
                    company=r.get("company", {}).get("display_name", "").strip(),
                    location=r.get("location", {}).get("display_name", "").strip(),
                    description=r.get("description", "")[:2000],
                    apply_url=r.get("redirect_url", ""),
                    posted_at=posted_at,
                    salary_text=salary_text,
                    salary_min_inr=min_inr,
                    salary_max_inr=max_inr,
                    source=f"adzuna:{country}",
                    raw_id=jid,
                )
