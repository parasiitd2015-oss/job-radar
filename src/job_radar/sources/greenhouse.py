"""Greenhouse public job board JSON. Free, no auth.

Stripe, Notion, Figma, Vercel, Linear, Razorpay, etc. all use Greenhouse.
Endpoint: https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true
"""
from __future__ import annotations

from datetime import datetime
from typing import Iterable

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..models import Job
from ..salary_parser import parse_salary


@retry(stop=stop_after_attempt(2), wait=wait_exponential(min=1, max=5))
def _fetch_board(slug: str) -> list[dict]:
    url = f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true"
    with httpx.Client(timeout=20) as client:
        r = client.get(url)
        if r.status_code == 404:
            return []
        r.raise_for_status()
        return r.json().get("jobs", [])


def fetch_greenhouse_company(display_name: str, slug: str) -> Iterable[Job]:
    try:
        jobs = _fetch_board(slug)
    except Exception as e:
        print(f"  [greenhouse:{slug}] failed: {e}")
        return

    for j in jobs:
        title = j.get("title", "").strip()
        location = (j.get("location") or {}).get("name", "").strip()
        url = j.get("absolute_url", "")
        content = j.get("content", "") or ""
        # Greenhouse content is HTML-encoded — strip basic tags
        import re
        text = re.sub(r"<[^>]+>", " ", content)
        text = re.sub(r"&nbsp;", " ", text)
        text = re.sub(r"&amp;", "&", text)
        text = re.sub(r"\s+", " ", text).strip()

        # Try to parse salary from content
        min_inr, max_inr = parse_salary(text[:1500])

        posted_at = None
        if j.get("updated_at"):
            try:
                posted_at = datetime.fromisoformat(
                    j["updated_at"].replace("Z", "+00:00")
                )
            except (ValueError, TypeError):
                pass

        yield Job(
            title=title,
            company=display_name,
            location=location,
            description=text[:2000],
            apply_url=url,
            posted_at=posted_at,
            salary_text="",
            salary_min_inr=min_inr,
            salary_max_inr=max_inr,
            source=f"greenhouse:{slug}",
            raw_id=str(j.get("id", "")),
        )
