"""User profile + scoring keywords. Edit this file to tune the radar."""
from __future__ import annotations

# Profile (Paras Bhaisora)
PROFILE_NAME = "Paras Bhaisora"
PROFILE_YOE = 7
PROFILE_LEVEL_TARGETS = [
    "senior", "sr.", "sr ", "lead", "principal", "staff",
    "director", "head of", "vp ", "vice president",
    "chief of staff", "cos ", "manager iii", "manager 3",
]

# Negative title signals — drop any role whose title contains these
TITLE_BLOCKLIST = [
    "intern", "internship", "fresher", "trainee", "graduate",
    "junior", "jr.", "jr ", "associate ", "entry level", "entry-level",
    "engineer i ", "engineer 1", "engineer ii ", "engineer 2",
    "software developer", "qa engineer", "test engineer",
    "support engineer", "sales executive", "sdr ", "bdr ",
    "data entry", "operations executive", "customer support",
    "store manager", "retail", "telecaller", "field sales",
    "accountant", "hr executive", "delivery boy", "rider",
]

# Tier-1 function keywords (your main targets)
TIER1_KEYWORDS = [
    "growth", "strategy", "chief of staff", "business development",
    "partnerships", "investor", "operations strategy", "go to market",
    "go-to-market", "gtm",
]

# Tier-2 function keywords (PM and adjacent)
TIER2_KEYWORDS = [
    "product manager", "product management", "product lead",
    "product marketing", "product strategy", "ai product",
]

# Bonus signals in title
TITLE_BONUS_KEYWORDS = [
    "ai", "fintech", "saas", "b2b", "enterprise",
    "platform", "monetization", "revenue",
]

# Industry/JD bonus signals
JD_BONUS_KEYWORDS = [
    "saas", "fintech", "plg", "product-led", "series b", "series c", "series d",
    "scale-up", "0 to 1", "0-to-1", "fundraise", "fundraising",
    "founder", "ex-founder", "ex founder", "founding team",
    "ai agent", "llm", "generative ai", "growth marketing",
    "lifecycle", "performance marketing", "ltv", "cac",
    "experimentation", "a/b test", "ab testing",
]

# Locations (case-insensitive substring match)
LOCATIONS_PREFERRED = [
    # India
    "delhi", "new delhi", "ncr", "gurgaon", "gurugram", "noida",
    "bangalore", "bengaluru", "blr",
    "mumbai", "bombay", "pune",
    "hyderabad", "chennai", "kolkata",
    "india",
    # International OK
    "singapore", "sgp",
    "dubai", "uae", "abu dhabi",
    "london", "uk ", "united kingdom",
    "europe", "berlin", "amsterdam", "paris", "dublin",
    "sydney", "melbourne", "australia",
    "toronto", "canada",
    # Remote
    "remote",
]

# Locations to deprioritize (excluding US-on-site since no US visa)
LOCATIONS_NEGATIVE = [
    # We don't want US-onsite roles unless explicitly remote
]

# Target companies — bump score when these appear
TARGET_COMPANIES_HOT = {
    # Big Tech India
    "google", "alphabet", "meta", "facebook", "amazon", "aws",
    "microsoft", "apple", "netflix", "uber",
    # International fintech / SaaS
    "stripe", "plaid", "ramp", "brex", "mercury",
    "notion", "linear", "vercel", "figma", "canva",
    "atlassian", "asana", "miro", "rippling", "deel", "remote.com",
    "hubspot", "salesforce", "zoom", "shopify",
    # Indian unicorns / late-stage
    "razorpay", "cred", "phonepe", "zerodha", "groww", "meesho",
    "zepto", "postman", "freshworks", "zoho", "browserstack",
    "swiggy", "zomato", "ola", "paytm", "policybazaar",
    "upgrad", "byju", "unacademy", "physicswallah",
    "slice", "jupiter", "jar", "fi money", "navi",
    "khatabook", "okcredit", "vedantu", "leadsquared",
    # Top VCs
    "peak xv", "sequoia", "accel", "lightspeed", "elevation",
    "nexus venture", "blume", "matrix", "kalaari",
    "sequoia capital", "general catalyst", "tiger global", "softbank",
    # Conglomerate strategy
    "tata digital", "tata sons", "reliance", "jio", "bajaj",
    "mahindra", "adani", "aditya birla",
}

# Geo bucket map for sources that accept country codes
ADZUNA_COUNTRIES = ["in", "gb", "sg", "ae", "au"]  # India, UK, Singapore, UAE, Australia

# Greenhouse / Lever companies to poll directly (free, no scraping)
# Format: (display_name, slug_or_token, board_type)
DIRECT_BOARDS = [
    # Greenhouse
    ("Stripe", "stripe", "greenhouse"),
    ("Notion", "notion", "greenhouse"),
    ("Figma", "figma", "greenhouse"),
    ("Vercel", "vercel", "greenhouse"),
    ("Linear", "linear", "greenhouse"),
    ("Rippling", "rippling", "greenhouse"),
    ("Plaid", "plaid", "greenhouse"),
    ("Ramp", "ramp", "greenhouse"),
    ("Brex", "brex", "greenhouse"),
    ("Mercury", "mercury", "greenhouse"),
    ("Airbnb", "airbnb", "greenhouse"),
    ("Anthropic", "anthropic", "greenhouse"),
    ("OpenAI", "openai", "greenhouse"),
    ("Atlassian", "atlassian", "greenhouse"),
    ("Asana", "asana", "greenhouse"),
    ("Miro", "miro", "greenhouse"),
    ("Postman", "postman", "greenhouse"),
    ("Razorpay", "razorpay", "greenhouse"),
    ("BrowserStack", "browserstack", "greenhouse"),
    # Lever
    ("Deel", "deel", "lever"),
    ("Remote.com", "remotecom", "lever"),
    ("CRED", "cred", "lever"),
    ("Zepto", "zepto", "lever"),
    ("PhonePe", "phonepe", "lever"),
    ("Groww", "groww", "lever"),
    ("Meesho", "meesho", "lever"),
    ("Slice", "sliceit", "lever"),
    ("Freshworks", "freshworks", "lever"),
]
