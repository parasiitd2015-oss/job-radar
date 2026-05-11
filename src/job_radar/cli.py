"""Main orchestrator + CLI entrypoint."""
from __future__ import annotations

import os
import sys

import click
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table

from .models import Job
from .profile_config import DIRECT_BOARDS
from .scorer import assign_tier, score_job
from .sheet_writer import push_to_sheet
from .sources.adzuna import fetch_adzuna_jobs
from .sources.greenhouse import fetch_greenhouse_company
from .sources.lever import fetch_lever_company
from .sources.remoteok import fetch_remoteok_jobs

load_dotenv()
console = Console()


def collect_all_jobs() -> list[Job]:
    """Pull from every configured source. Resilient to single-source failures."""
    all_jobs: list[Job] = []

    # 1. Adzuna (if configured)
    console.print("[bold cyan]Fetching Adzuna…[/bold cyan]")
    count_before = len(all_jobs)
    all_jobs.extend(fetch_adzuna_jobs())
    console.print(f"  [dim]+{len(all_jobs) - count_before} jobs[/dim]")

    # 2. Greenhouse boards
    console.print("[bold cyan]Fetching Greenhouse boards…[/bold cyan]")
    for display, slug, board_type in DIRECT_BOARDS:
        if board_type != "greenhouse":
            continue
        before = len(all_jobs)
        all_jobs.extend(fetch_greenhouse_company(display, slug))
        added = len(all_jobs) - before
        if added > 0:
            console.print(f"  [dim]{display}: +{added}[/dim]")

    # 3. Lever boards
    console.print("[bold cyan]Fetching Lever boards…[/bold cyan]")
    for display, slug, board_type in DIRECT_BOARDS:
        if board_type != "lever":
            continue
        before = len(all_jobs)
        all_jobs.extend(fetch_lever_company(display, slug))
        added = len(all_jobs) - before
        if added > 0:
            console.print(f"  [dim]{display}: +{added}[/dim]")

    # 4. RemoteOK
    console.print("[bold cyan]Fetching RemoteOK…[/bold cyan]")
    count_before = len(all_jobs)
    all_jobs.extend(fetch_remoteok_jobs())
    console.print(f"  [dim]+{len(all_jobs) - count_before} jobs[/dim]")

    return all_jobs


def score_and_filter(jobs: list[Job]) -> list[Job]:
    """Score every job, assign tier, drop filtered-out (score < 30)."""
    kept: list[Job] = []
    for j in jobs:
        j.score = score_job(j)
        j.tier = assign_tier(j)
        if j.tier:  # non-empty tier = passed the filter
            kept.append(j)
    # Sort by score descending
    kept.sort(key=lambda x: x.score, reverse=True)
    return kept


def dedupe(jobs: list[Job]) -> list[Job]:
    """Remove duplicates within a single run by fingerprint (cross-source dedup)."""
    seen = set()
    out = []
    for j in jobs:
        if j.fingerprint in seen:
            continue
        seen.add(j.fingerprint)
        out.append(j)
    return out


@click.group()
def cli() -> None:
    """job-radar: daily job fetcher → Google Sheet."""


@cli.command()
@click.option("--sheet-id", envvar="SHEET_ID", required=True,
              help="Google Sheet ID (from the URL).")
@click.option("--worksheet", default="Jobs", help="Worksheet tab name.")
@click.option("--dry-run", is_flag=True, help="Print top 20, don't write to sheet.")
@click.option("--limit", type=int, default=200, help="Max rows to push per run.")
def run(sheet_id: str, worksheet: str, dry_run: bool, limit: int) -> None:
    """Fetch → score → push to sheet."""
    console.rule("[bold]job-radar daily run[/bold]")

    raw = collect_all_jobs()
    console.print(f"\n[bold]Raw jobs collected:[/bold] {len(raw)}")

    deduped = dedupe(raw)
    console.print(f"[bold]After dedup:[/bold] {len(deduped)}")

    matched = score_and_filter(deduped)
    matched = matched[:limit]
    console.print(f"[bold]Matched (score ≥ 30):[/bold] {len(matched)}")

    high = sum(1 for j in matched if j.tier == "🔥 High Confidence")
    worth = sum(1 for j in matched if j.tier == "🟡 Worth Checking")
    console.print(f"  🔥 High confidence: {high}")
    console.print(f"  🟡 Worth checking: {worth}")

    # Show top 20 in console
    if matched:
        t = Table(title="Top matches preview", show_lines=False)
        t.add_column("Tier", width=8)
        t.add_column("Sc", justify="right", width=4)
        t.add_column("Title", width=40)
        t.add_column("Company", width=18)
        t.add_column("Loc", width=16)
        t.add_column("Salary", width=18)
        for j in matched[:20]:
            from .sheet_writer import _format_salary
            t.add_row(
                j.tier.split()[0],
                str(j.score),
                j.title[:40],
                j.company[:18],
                j.location[:16],
                _format_salary(j) or "—",
            )
        console.print(t)

    if dry_run:
        console.print("\n[yellow]Dry run — not writing to sheet.[/yellow]")
        return

    if not matched:
        console.print("[yellow]Nothing to push.[/yellow]")
        return

    console.print(f"\n[bold cyan]Pushing to Google Sheet {sheet_id}/{worksheet}…[/bold cyan]")
    try:
        added = push_to_sheet(matched, sheet_id, worksheet)
        console.print(f"[bold green]✓ Added {added} new rows[/bold green]")
    except Exception as e:
        console.print(f"[bold red]✗ Sheet write failed: {e}[/bold red]")
        sys.exit(1)


@cli.command()
def test_sources() -> None:
    """Quick smoke test of each source — does NOT write to sheet."""
    console.rule("Source connectivity test")

    # Greenhouse: try Stripe (definitely exists)
    from .sources.greenhouse import _fetch_board
    try:
        n = len(_fetch_board("stripe"))
        console.print(f"[green]✓[/green] Greenhouse (stripe): {n} jobs")
    except Exception as e:
        console.print(f"[red]✗[/red] Greenhouse (stripe): {e}")

    # Lever: try Deel
    from .sources.lever import _fetch_board as lever_fetch
    try:
        n = len(lever_fetch("deel"))
        console.print(f"[green]✓[/green] Lever (deel): {n} jobs")
    except Exception as e:
        console.print(f"[red]✗[/red] Lever (deel): {e}")

    # RemoteOK
    from .sources.remoteok import _fetch as ro_fetch
    try:
        n = len(ro_fetch())
        console.print(f"[green]✓[/green] RemoteOK: {n} jobs")
    except Exception as e:
        console.print(f"[red]✗[/red] RemoteOK: {e}")

    # Adzuna (only if env vars set)
    if os.getenv("ADZUNA_APP_ID") and os.getenv("ADZUNA_APP_KEY"):
        try:
            count = sum(1 for _ in fetch_adzuna_jobs())
            console.print(f"[green]✓[/green] Adzuna: {count} jobs")
        except Exception as e:
            console.print(f"[red]✗[/red] Adzuna: {e}")
    else:
        console.print("[yellow]–[/yellow] Adzuna: not configured (set ADZUNA_APP_ID + ADZUNA_APP_KEY)")


if __name__ == "__main__":
    cli()
