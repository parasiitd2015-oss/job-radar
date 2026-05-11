# job-radar

Daily job fetcher that pulls senior-level openings from public job APIs, scores them against your profile, and appends the matches to a Google Sheet. Runs daily on GitHub Actions for free.

**Built for:** Paras Bhaisora — IIT-D 2019, 7Y experience, targeting ₹50L+ Growth/Strategy/PM roles in India + remote international.

## What it does

1. **Pulls jobs** from 4 free sources daily:
   - **Adzuna API** (free tier: India + UK + Singapore + UAE + Australia)
   - **Greenhouse boards** (Stripe, Notion, Razorpay, Figma, Vercel, Linear, Postman, BrowserStack, ~20 companies)
   - **Lever boards** (CRED, Zepto, PhonePe, Groww, Meesho, Deel, Remote.com, ~10 companies)
   - **RemoteOK** (international remote)

2. **Scores each job** against your profile using a rule-based engine (no AI cost):
   - Function fit: Growth/Strategy/CoS/BD (+15 each), PM (+10 each), wrong function (filtered out)
   - Seniority: Senior/Lead/Director (+20), Junior/Intern (filtered out)
   - Location: India/Remote/SG/Dubai/UK/EU (+10), other (-10)
   - Company prestige: Big Tech + top unicorns (+20)
   - JD signals: SaaS, fintech, PLG, fundraise, 7+ YoE (+2-10 each)
   - Salary: ₹50L+ confirmed (+30)

3. **Deduplicates** by `(company, title, location)` fingerprint — no role appears twice across runs.

4. **Pushes new rows** to your Google Sheet, tagged with tier:
   - 🔥 **High Confidence** (score ≥ 60)
   - 🟡 **Worth Checking** (score 30-60)

5. **Runs daily at 8:30 AM IST** via GitHub Actions cron. Free forever within Actions' free tier.

## Setup (one-time, ~30 minutes)

### Step 1 — Create the Google Sheet

1. Go to https://sheets.google.com → New sheet → name it "Job Radar".
2. Copy the **Sheet ID** from the URL — it's the long string between `/d/` and `/edit`:
   ```
   https://docs.google.com/spreadsheets/d/1AbCdEfGhIjKlMnOpQrStUvWxYz/edit
                                          ↑↑↑ this is your SHEET_ID ↑↑↑
   ```

### Step 2 — Create a Google Service Account

1. Go to https://console.cloud.google.com → create new project (or reuse one). Name: "job-radar".
2. In the project: **APIs & Services → Enable APIs** → enable **Google Sheets API**.
3. **IAM & Admin → Service Accounts → Create Service Account**:
   - Name: `job-radar-bot`
   - Skip role assignment, click Done.
4. Click the created service account → **Keys → Add Key → Create new key → JSON**. Save the downloaded JSON.
5. Copy the service account's **email address** (looks like `job-radar-bot@your-project.iam.gserviceaccount.com`).
6. Open your Google Sheet → **Share** → paste the service account email → give **Editor** access. Uncheck "notify". Click Share.

### Step 3 — (Optional but recommended) Get Adzuna API keys

1. Go to https://developer.adzuna.com/
2. Sign up → create an app → copy `App ID` and `App Key`.
3. Free tier: 1,000 calls/month. We use ~35/day, so well within limit.

### Step 4 — Local testing

```bash
git clone <your-repo-url> job-radar
cd job-radar

python3 -m venv .venv && source .venv/bin/activate
pip install -e .

# Set up secrets
cp .env.example .env
nano .env   # paste your SHEET_ID, service account JSON, and Adzuna keys
```

Smoke test:

```bash
# 1. Check sources are reachable
job-radar test-sources

# 2. Dry run — fetches everything, prints top 20, does NOT write to sheet
job-radar run --sheet-id "$SHEET_ID" --dry-run

# 3. Real run — writes to your sheet
job-radar run --sheet-id "$SHEET_ID"
```

Open your sheet. You should see a "Jobs" tab populated with 50-200 matches.

### Step 5 — Deploy to GitHub Actions (free daily runs)

```bash
# Push to a new GitHub repo
git init && git add . && git commit -m "Initial job-radar setup"
git remote add origin https://github.com/yourusername/job-radar.git
git push -u origin main
```

In your GitHub repo:

1. **Settings → Secrets and variables → Actions → New repository secret**. Add these four:
   - `SHEET_ID` — your sheet ID
   - `GOOGLE_SERVICE_ACCOUNT_JSON` — paste the entire contents of the JSON key file
   - `ADZUNA_APP_ID`
   - `ADZUNA_APP_KEY`

2. **Actions tab → Daily Job Radar → "Run workflow"** to test it manually first.

3. Done. From tomorrow it runs at 8:30 AM IST every day automatically.

## Tuning the radar

The brain lives in `src/job_radar/profile_config.py`. Edit and commit:

| File / Setting | Purpose |
|---|---|
| `TIER1_KEYWORDS` | Functions you most want (Growth, Strategy, etc.) |
| `TIER2_KEYWORDS` | Secondary functions (PM) |
| `TITLE_BLOCKLIST` | Phrases that auto-filter (intern, junior, telecaller, etc.) |
| `LOCATIONS_PREFERRED` | Cities/countries to favor |
| `TARGET_COMPANIES_HOT` | Companies that get +20 score boost |
| `DIRECT_BOARDS` | Greenhouse/Lever slugs to poll daily |

The scoring weights are in `src/job_radar/scorer.py`. All numeric, easy to adjust.

## How to add a new company

Most modern startups use Greenhouse or Lever. To find a company's slug:

- **Greenhouse:** check `boards.greenhouse.io/{company}` — if it loads, the slug is `{company}`.
- **Lever:** check `jobs.lever.co/{company}` — same logic.

Add a line to `DIRECT_BOARDS` in `profile_config.py`:

```python
("Acme Corp", "acmecorp", "greenhouse"),
```

Commit, push. Next daily run picks it up.

## Output schema (Google Sheet columns)

| Column | Description |
|---|---|
| Date Added | When this run discovered the role |
| Tier | 🔥 High Confidence / 🟡 Worth Checking |
| Score | Numeric fit score |
| Title | Job title |
| Company | Company name |
| Location | City/country/remote |
| Salary (INR/yr) | Parsed and converted; blank if not in posting |
| Source | Where it came from |
| Posted | Original post date |
| Apply URL | Direct application link |
| Description Preview | First 300 chars |
| Fingerprint | Used for dedup; ignore |

## Daily workflow for you

1. **Morning:** open the sheet. Filter Column B = `🔥 High Confidence`.
2. **Sort by Score desc.** Top 5-10 are usually worth a deep look.
3. **Apply same day** to anything 70+ — recruiters batch-screen Monday-Wednesday.
4. **Use the outreach templates** in your other Excel (BigTech_India_Career_Targets.xlsx) to follow up after applying.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `No Google service account configured` | Check `.env` has either `GOOGLE_SERVICE_ACCOUNT_JSON` or `GOOGLE_SA_FILE` set |
| Sheet writes return 403 | You forgot to share the sheet with the service account email |
| `Adzuna: not configured` | Optional — works without Adzuna, just less coverage |
| Greenhouse/Lever returns empty for a company | Their slug might have changed. Visit `boards.greenhouse.io/{slug}` in browser. |
| GitHub Action fails on first run | Click into the failed run → expand "Run job-radar" → read the error |
| Too many irrelevant jobs | Tighten `TITLE_BLOCKLIST` and re-run |
| Missing real opportunities | Add more company slugs to `DIRECT_BOARDS`, or relax `LOCATIONS_PREFERRED` |

## Cost summary

| Item | Cost |
|---|---|
| Adzuna API (free tier) | ₹0 |
| Greenhouse/Lever/RemoteOK | ₹0 (public APIs) |
| GitHub Actions (free tier: 2000 min/month, run uses ~5 min) | ₹0 |
| Google Sheets | ₹0 |
| **Total** | **₹0/month forever** |

## What this does NOT do (by design)

- **No LinkedIn scraping** — against ToS, legally risky.
- **No auto-apply** — recruiters detect mass applications and blacklist. Manual + thoughtful wins.
- **No AI scoring** — rule-based is 90% as accurate at 0% the cost. You can always layer GPT/Claude later.
- **No salary scraping from Glassdoor** — they ban scrapers aggressively. Parse from JD only.

## License

Personal use. No license needed for now.
