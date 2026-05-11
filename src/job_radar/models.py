"""Common Job model used across all sources."""
from __future__ import annotations

import hashlib
import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Job(BaseModel):
    """Normalized job posting from any source."""

    title: str
    company: str
    location: str
    description: str = ""
    apply_url: str
    posted_at: Optional[datetime] = None
    salary_text: str = ""           # raw salary string from posting
    salary_min_inr: Optional[float] = None  # parsed minimum INR per year
    salary_max_inr: Optional[float] = None  # parsed max INR per year
    source: str                     # e.g., "adzuna", "greenhouse:stripe"
    raw_id: str = ""                # source's own ID
    score: int = 0
    tier: str = ""                  # "🔥 High", "🟡 Worth Checking", or filtered

    @property
    def fingerprint(self) -> str:
        """Stable hash for dedup across runs and sources."""
        norm_title = re.sub(r"\s+", " ", self.title.lower().strip())
        norm_company = re.sub(r"\s+", " ", self.company.lower().strip())
        norm_loc = re.sub(r"\s+", " ", self.location.lower().strip()[:30])
        key = f"{norm_company}|{norm_title}|{norm_loc}"
        return hashlib.sha256(key.encode()).hexdigest()[:16]
