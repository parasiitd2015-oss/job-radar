"""Push deduped, scored jobs to a Google Sheet.

Auth via service account. The service account email must be granted Editor
access to the target sheet.
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

from .models import Job

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Sheet schema
HEADERS = [
    "Date Added", "Tier", "Score", "Title", "Company", "Location",
    "Salary (INR/yr)", "Source", "Posted", "Apply URL",
    "Description Preview", "Fingerprint",
]


def _get_credentials() -> Credentials:
    """Load service account creds from env (GOOGLE_SERVICE_ACCOUNT_JSON)
    or from a local file path (GOOGLE_SA_FILE)."""
    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if raw:
        info = json.loads(raw)
        return Credentials.from_service_account_info(info, scopes=SCOPES)
    path = os.getenv("GOOGLE_SA_FILE", "").strip()
    if path and Path(path).exists():
        return Credentials.from_service_account_file(path, scopes=SCOPES)
    raise RuntimeError(
        "No Google service account configured. Set GOOGLE_SERVICE_ACCOUNT_JSON "
        "(full JSON string) or GOOGLE_SA_FILE (path to key.json)."
    )


def _ensure_headers(ws) -> None:
    """If sheet is empty, write headers in row 1."""
    existing = ws.row_values(1) if ws.row_count > 0 else []
    if existing != HEADERS:
        ws.update("A1", [HEADERS])
        ws.format("A1:L1", {"textFormat": {"bold": True},
                            "backgroundColor": {"red": 0.12, "green": 0.22, "blue": 0.39},
                            "horizontalAlignment": "CENTER"})


def _existing_fingerprints(ws) -> set[str]:
    """Read column L (fingerprints) from row 2 onwards."""
    try:
        col = ws.col_values(12)  # column L
    except Exception:
        return set()
    return set(col[1:])  # skip header


def _format_salary(job: Job) -> str:
    if not job.salary_max_inr and not job.salary_min_inr:
        return ""

    def fmt(v: float) -> str:
        if v >= 1e7:
            return f"₹{v / 1e7:.2f} Cr"
        if v >= 1e5:
            return f"₹{v / 1e5:.1f} L"
        return f"₹{v:,.0f}"

    if job.salary_min_inr and job.salary_max_inr and job.salary_min_inr != job.salary_max_inr:
        return f"{fmt(job.salary_min_inr)} – {fmt(job.salary_max_inr)}"
    return fmt(job.salary_max_inr or job.salary_min_inr)


def push_to_sheet(jobs: list[Job], sheet_id: str, worksheet_name: str = "Jobs") -> int:
    """
    Append new jobs (by fingerprint) to the target Google Sheet.
    Returns the number of new rows appended.
    """
    creds = _get_credentials()
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(sheet_id)

    try:
        ws = sh.worksheet(worksheet_name)
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title=worksheet_name, rows=2000, cols=len(HEADERS))

    _ensure_headers(ws)
    seen_before = _existing_fingerprints(ws)

    # Filter to new jobs only
    new_jobs = [j for j in jobs if j.fingerprint not in seen_before]
    if not new_jobs:
        return 0

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    rows = []
    for j in new_jobs:
        posted = j.posted_at.strftime("%Y-%m-%d") if j.posted_at else ""
        desc_preview = (j.description or "")[:300].replace("\n", " ")
        rows.append([
            now,
            j.tier,
            j.score,
            j.title,
            j.company,
            j.location,
            _format_salary(j),
            j.source,
            posted,
            j.apply_url,
            desc_preview,
            j.fingerprint,
        ])

    ws.append_rows(rows, value_input_option="USER_ENTERED")
    return len(rows)
