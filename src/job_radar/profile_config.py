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
# Extended TARGET_COMPANIES_HOT Universe (1000+ Directional Company Expansion)

TARGET_COMPANIES_HOT = {
    # Big Tech
    "google", "alphabet", "meta", "facebook", "instagram", "whatsapp",
    "amazon", "aws", "microsoft", "apple", "netflix", "uber",
    "tesla", "spacex", "nvidia", "openai", "anthropic", "xai",
    "oracle", "sap", "adobe", "intel", "amd", "cisco",
    "ibm", "palantir", "airbnb", "dropbox", "slack", "discord",
    "spotify", "linkedin", "snap", "pinterest", "reddit",
    "cloudflare", "databricks", "snowflake", "mongodb", "confluent",
    "servicenow", "workday", "twilio", "okta", "datadog",
    "new relic", "hashicorp", "docker", "gitlab", "github",
    "digitalocean", "akamai", "fastly", "elastic", "redis",
    "huggingface", "perplexity", "mistral", "stability ai",

    # Global SaaS / Product / AI
    "notion", "linear", "vercel", "figma", "canva",
    "atlassian", "asana", "miro", "rippling", "deel", "remote.com",
    "hubspot", "salesforce", "zoom", "shopify", "webflow",
    "framer", "loom", "clickup", "monday.com", "airtable",
    "zapier", "intercom", "segment", "mixpanel", "amplitude",
    "gainsight", "gong", "outreach", "apollo", "braze",
    "klaviyo", "mailchimp", "convertkit", "drift", "typeform",
    "survey monkey", "qualtrics", "freshdesk", "freshchat",
    "freshservice", "zendesk", "smartsheet", "notable",

    # Fintech Global
    "stripe", "plaid", "ramp", "brex", "mercury",
    "wise", "revolut", "nubank", "sofi", "robinhood",
    "affirm", "klarna", "checkout.com", "marqeta", "block",
    "square", "cash app", "wise", "wise payments",
    "coinbase", "kraken", "binance", "ripple", "circle",
    "chime", "current", "varo", "betterment", "wealthfront",
    "payoneer", "adyen", "visa", "mastercard", "american express",
    "jpmorgan", "goldman sachs", "morgan stanley", "blackrock",
    "blackstone", "bridgewater", "citadel", "jane street",

    # Indian Unicorns / Late Stage
    "razorpay", "cred", "phonepe", "zerodha", "groww", "meesho",
    "zepto", "postman", "freshworks", "zoho", "browserstack",
    "swiggy", "zomato", "ola", "paytm", "policybazaar",
    "upgrad", "byju", "unacademy", "physicswallah",
    "slice", "jupiter", "jar", "fi money", "navi",
    "khatabook", "okcredit", "vedantu", "leadsquared",
    "urban company", "boAt", "lenskart", "mamaearth", "nykaa",
    "dream11", "mpl", "gameskraft", "sharechat", "moj",
    "dailyhunt", "inmobi", "glance", "curefit", "cult.fit",
    "no broker", "acko", "digit insurance", "coin dcx",
    "coin switch", "bharatpe", "mobikwik", "cashfree", "pine labs",
    "open financial", "smallcase", "neo", "indmoney", "ditto",
    "apna", "naukri", "foundit", "cars24", "spinny",
    "porter", "blackbuck", "delhivery", "elasticrun", "shadowfax",
    "elastic run", "uadaan", "udaan", "infra.market",
    "bizongo", "shiprocket", "captain fresh", "globalbees",
    "firstcry", "purplle", "dealshare", "magicpin", "payu",
    "simpl", "kissht", "zestmoney", "freo", "winkl",

    # India SaaS Ecosystem
    "chargebee", "wingify", "whatfix", "moengage", "webengage",
    "clevertap", "capillary", "darwinbox", "facilio", "yellow.ai",
    "observe.ai", "highradius", "innovaccer", "mindtickle",
    "gupshup", "postman", "survey sparrow", "kissflow",
    "perfios", "perfios software", "easyrewardz", "tally",
    "rezo.ai", "ai palette", "rocketlane", "devrev",
    "exotel", "amagi", "sprinklr", "people strong",
    "uniphore", "hasura", "edgeverve", "agnikul", "skyroot",

    # Consulting / Strategy
    "mckinsey", "bain", "bcg", "kearney", "oliver wyman",
    "lek consulting", "strategy&", "monitor deloitte",
    "accenture strategy", "ey parthenon", "kpmg", "pwc",
    "deloitte", "grant thornton", "alvarez marsal",

    # Top VC / PE / Investment
    "peak xv", "sequoia", "accel", "lightspeed", "elevation",
    "nexus venture", "blume", "matrix", "kalaari",
    "sequoia capital", "general catalyst", "tiger global", "softbank",
    "a16z", "andreessen horowitz", "benchmark", "greylock",
    "founders fund", "insight partners", "battery ventures",
    "bessemer", "y combinator", "yc", "catalyst", "warburg pincus",
    "advent international", "temasek", "prosus", "naspers",
    "westbridge", "chiratae", "beenext", "venture highway",

    # Conglomerates / Corporate Strategy
    "tata digital", "tata sons", "reliance", "jio", "bajaj",
    "mahindra", "adani", "aditya birla", "itc", "hul",
    "hindustan unilever", "nestle", "marico", "godrej",
    "dabur", "britannia", "asian paints", "pidilite",
    "ultratech", "vedanta", "jsw", "l&t", "ltimindtree",
    "infosys", "tcs", "wipro", "tech mahindra", "hcl",
    "persistent", "mphasis", "coforge", "zensar", "oracle financial",

    # Semiconductor / Deep Tech
    "arm", "qualcomm", "broadcom", "micron", "marvell",
    "texas instruments", "synopsys", "cadence", "applied materials",
    "lam research", "asml", "tsi", "globalfoundries",

    # Cybersecurity
    "crowdstrike", "sentinelone", "wiz", "zscaler", "palo alto networks",
    "fortinet", "checkpoint", "cyberark", "netskope", "snyk",

    # Consumer Internet
    "booking.com", "expedia", "tripadvisor", "agoda", "makemytrip",
    "oyo", "airasia", "ixigo", "cleartrip", "easemytrip",

    # Gaming
    "epic games", "riot games", "unity", "roblox", "activision",
    "electronic arts", "supercell", "niantic", "dream sports",

    # Healthtech
    "practo", "pharmeasy", "1mg", "apollo health", "mfine",
    "curebay", "medibuddy", "healthifyme", "sarvam ai",

    # Logistics / Mobility
    "uber", "lyft", "rapido", "porter", "blusmart",
    "rivigo", "mahindra logistics", "ecom express",

    # Edtech
    "coursera", "udemy", "simplilearn", "scaler", "newton school",
    "masai school", "great learning", "upgrad", "emeritus",

    # AI Native / Agentic
    "langchain", "pinecone", "weaviate", "twelve labs",
    "runway", "midjourney", "elevenlabs", "harvey ai",
    "glean", "adept", "replit", "windsurf", "cursor",

    # High-growth Startups
    "perplexity ai", "anduril", "scale ai", "helion", "cognition",
    "suno", "heygen", "character ai", "groq", "turing",
    "deel", "remote", "multiplier", "safetywing",

    # Additions for breadth
    "flipkart", "amazon india", "jiocinema", "hotstar",
    "netmeds", "bookmyshow", "snapdeal", "pepperfry",
    "wakefit", "bewakoof", "bombay shaving company",
    "the whole truth", "blue tokai", "chaayos", "wow momo",
    "rebel foods", "eatclub", "country delight", "ninjacart",
    "dehaat", "waycool", "gramophone", "agrostar",

    # Enterprise Infra
    "vmware", "nutanix", "cloudera", "redhat", "suse",
    "canonical", "grafana labs", "supabase", "planetscale",

    # Media / Creator Economy
    "substack", "patreon", "beehiiv", "kajabi", "gumroad",
    "youtube", "twitch", "spotify studios", "anchor",

    # Telecom / Infra
    "airtel", "vodafone idea", "bsnl", "ericsson", "nokia",

    # Energy / EV
    "aether", "ather", "ola electric", "tata motors", "hero electric",
    "exicom", "sun mobility", "battery smart",

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
