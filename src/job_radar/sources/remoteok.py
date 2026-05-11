"""RemoteOK — free, public JSON feed of remote jobs."""
from __future__ import annotations

from datetime import datetime
from typing import Iterable

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..models import Job
from ..salary_parser import parse_salary


@retry(stop=stop_after_attempt(2), wait=wait_exponential(min=1, max=5))
def _fetch() -> list[dict]:
    url = "https://remoteok.com/api"
    headers = {"User-Agent": "Mozilla/5.0 (job-radar/0.1)"}
    with httpx.Client(timeout=20, follow_redirects=True) as client:
        r = client.get(url, headers=headers)
        r.raise_for_status()
        data = r.json()
        # First item is metadata
        return [x for x in data if isinstance(x, dict) and x.get("id")]


def fetch_remoteok_jobs() -> Iterable[Job]:
    try:
        jobs = _fetch()
    except Exception as e:
        print(f"  [remoteok] failed: {e}")
        return

    for j in jobs:
        title = j.get("position", "") or j.get("title", "")
        company = j.get("company", "")
        if not title or not company:
            continue

        # RemoteOK lists tags — useful for filtering
        tags = j.get("tags", []) or []
        location = "Remote (" + ", ".join(tags[:3]) + ")" if tags else "Remote"

        description = j.get("description", "")[:2000]

        salary_min = j.get("salary_min")
        salary_max = j.get("salary_max")
        salary_text = ""
        min_inr = max_inr = None
        if salary_min and salary_max:
            # RemoteOK salaries are in USD
            salary_text = f"${salary_min:,} - ${salary_max:,} USD"
            from ..salary_parser import _to_inr
            min_inr = _to_inr(float(salary_min), "USD")
            max_inr = _to_inr(float(salary_max), "USD")

        posted_at = None
        if j.get("date"):
            try:
                posted_at = datetime.fromisoformat(j["date"].replace("Z", "+00:00"))
            except (ValueError, TypeError):
                pass

        yield Job(
            title=title,
            company=company,
            location=location,
            description=description,
            apply_url=j.get("url") or j.get("apply_url", ""),
            posted_at=posted_at,
            salary_text=salary_text,
            salary_min_inr=min_inr,
            salary_max_inr=max_inr,
            source="remoteok",
            raw_id=str(j.get("id", "")),
        )
