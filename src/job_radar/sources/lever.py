"""Lever public job board JSON. Free, no auth.

Many growth-stage Indian unicorns (CRED, Zepto, PhonePe, Groww) use Lever.
Endpoint: https://api.lever.co/v0/postings/{slug}?mode=json
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Iterable

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from ..models import Job
from ..salary_parser import parse_salary


@retry(stop=stop_after_attempt(2), wait=wait_exponential(min=1, max=5))
def _fetch_board(slug: str) -> list[dict]:
    url = f"https://api.lever.co/v0/postings/{slug}?mode=json"
    with httpx.Client(timeout=20) as client:
        r = client.get(url)
        if r.status_code == 404:
            return []
        r.raise_for_status()
        return r.json()


def fetch_lever_company(display_name: str, slug: str) -> Iterable[Job]:
    try:
        jobs = _fetch_board(slug)
    except Exception as e:
        print(f"  [lever:{slug}] failed: {e}")
        return

    for j in jobs:
        title = j.get("text", "").strip()
        categories = j.get("categories", {}) or {}
        location = categories.get("location", "") or ""
        # commitment = full-time / contract; team = Engineering / etc.
        team = categories.get("team", "")

        description = (j.get("descriptionPlain") or
                       re.sub(r"<[^>]+>", " ", j.get("description", "") or ""))
        description = re.sub(r"\s+", " ", description).strip()

        # Lever sometimes includes salary in description or list
        min_inr, max_inr = parse_salary(description[:1500])

        posted_at = None
        if j.get("createdAt"):
            try:
                posted_at = datetime.fromtimestamp(
                    j["createdAt"] / 1000, tz=timezone.utc
                )
            except (ValueError, TypeError, OSError):
                pass

        yield Job(
            title=title,
            company=display_name,
            location=f"{location} ({team})" if team else location,
            description=description[:2000],
            apply_url=j.get("hostedUrl", ""),
            posted_at=posted_at,
            salary_text="",
            salary_min_inr=min_inr,
            salary_max_inr=max_inr,
            source=f"lever:{slug}",
            raw_id=j.get("id", ""),
        )
