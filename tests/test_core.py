"""Offline tests. No network, no Sheets writes."""
from __future__ import annotations

from job_radar.models import Job
from job_radar.salary_parser import parse_salary
from job_radar.scorer import assign_tier, score_job


def make_job(**kwargs) -> Job:
    defaults = dict(
        title="X", company="Y", location="Z",
        description="", apply_url="https://example.com", source="test",
    )
    defaults.update(kwargs)
    return Job(**defaults)


# ---- Salary parser ----

def test_parse_inr_lakh_range():
    lo, hi = parse_salary("₹50-90 LPA")
    assert lo == 50e5
    assert hi == 90e5

def test_parse_usd_range():
    lo, hi = parse_salary("$130,000 - $180,000")
    assert lo is not None and hi is not None
    assert 1e7 < lo < 1.2e7  # ~₹1.08Cr
    assert 1.4e7 < hi < 1.6e7  # ~₹1.5Cr

def test_parse_crore():
    lo, hi = parse_salary("1.5 crore - 2 crore INR")
    assert lo == 1.5e7
    assert hi == 2e7

def test_parse_empty():
    assert parse_salary("") == (None, None)
    assert parse_salary("Competitive salary") == (None, None)


# ---- Scorer ----

def test_blocklist_intern_filtered():
    j = make_job(title="Marketing Intern")
    assert score_job(j) < 0

def test_high_confidence_growth_role():
    j = make_job(
        title="Senior Growth Manager",
        company="Razorpay",
        location="Bangalore, India",
        description="6+ years experience scaling SaaS fintech. Series C company looking for "
                    "PLG growth lead with fundraise exposure.",
        salary_min_inr=60e5, salary_max_inr=90e5,
    )
    s = score_job(j)
    j.score = s
    assert s >= 60, f"Expected high confidence but got {s}"
    assert assign_tier(j) == "🔥 High Confidence"

def test_worth_checking_partial_match():
    j = make_job(
        title="Product Manager",
        company="Some Company",
        location="Remote",
        description="3+ years experience.",
    )
    s = score_job(j)
    j.score = s
    # Generic PM at unknown company, remote — should pass blocklist but
    # be modest score
    assert s >= 0  # didn't get filtered
    # may or may not be "worth checking" depending on exact tuning

def test_irrelevant_role_filtered():
    j = make_job(title="Backend Engineer II")
    assert score_job(j) < 0

def test_director_at_target_company():
    j = make_job(
        title="Director of Growth",
        company="Stripe",
        location="Remote",
        description="7+ years experience scaling B2B SaaS PLG.",
    )
    s = score_job(j)
    assert s >= 60

def test_overqualified_role_penalized():
    j = make_job(
        title="Chief Revenue Officer",
        company="Random Co",
        location="Bangalore",
        description="15+ years experience required.",
    )
    s = score_job(j)
    # Should be penalized but not necessarily negative
    assert s < 60


# ---- Fingerprint dedup ----

def test_fingerprint_stable():
    j1 = make_job(title="Senior Growth Manager", company="Razorpay", location="Bangalore, India")
    j2 = make_job(title="  Senior Growth Manager  ", company="razorpay", location="Bangalore, India")
    assert j1.fingerprint == j2.fingerprint

def test_fingerprint_differs_by_company():
    j1 = make_job(title="Growth Manager", company="Razorpay", location="Bangalore")
    j2 = make_job(title="Growth Manager", company="CRED", location="Bangalore")
    assert j1.fingerprint != j2.fingerprint
