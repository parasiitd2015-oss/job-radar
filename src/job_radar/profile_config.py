"""User profile + scoring keywords. Edit this file to tune the radar."""
from __future__ import annotations

# Profile (Paras Bhaisora)
PROFILE_NAME = "Paras Bhaisora"
PROFILE_YOE = 7
PROFILE_LEVEL_TARGETS = [

    # Existing
    "senior", "sr.", "sr ", "lead", "principal", "staff",
    "director", "head of", "vp ", "vice president",
    "chief of staff", "cos ", "manager iii", "manager 3", "cbo",

    # Founder / Office of CEO / Strategic Leadership
    "founder's office",
    "founders office",
    "office of the ceo",
    "office of ceo",
    "ceo office",
    "strategy and operations",
    "strategic initiatives",
    "business operations",
    "bizops",
    "business strategy",
    "corporate strategy",
    "growth strategy",
    "revenue strategy",
    "special projects",
    "executive office",
    "executive strategy",
    "chief executive office",
    "ceo strategist",
    "strategic partnerships",
    "partnerships lead",
    "strategic growth",

    # Entrepreneur / Venture / EIR
    "entrepreneur in residence",
    "eir",
    "venture builder",
    "venture lead",
    "new initiatives",
    "incubation lead",
    "startup program manager",
    "venture studio",
    "innovation lead",

    # Growth / GTM / Revenue
    "growth lead",
    "growth manager",
    "head of growth",
    "growth and strategy",
    "growth operations",
    "revenue operations",
    "revops",
    "go to market",
    "gtm lead",
    "market expansion",
    "category lead",
    "marketplace growth",
    "user acquisition lead",

    # Product + Business Hybrid
    "product strategy",
    "product operations",
    "business program manager",
    "program lead",
    "strategy manager",
    "operations manager",
    "commercial strategy",
    "monetization strategy",

    # Investor / VC / Startup Ecosystem
    "investment associate",
    "investment analyst",
    "venture capital",
    "portfolio operations",
    "platform lead",
    "startup partnerships",

    # Leadership / High Ownership
    "general manager",
    "gm ",
    "country manager",
    "business head",
    "p&l owner",
    "vertical lead",
    "expansion lead",
    "transformation office",

    # AI / Emerging Tech Strategic Roles
    "ai strategy",
    "ai operations",
    "chief ai officer",
    "genai strategy",
    "automation strategy",
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
# ============================================
# Tier-1 function keywords (highest priority)
# Founder-office / Strategy / GTM / Growth
# ============================================

TIER1_KEYWORDS = [

    # Strategy / Leadership
    "strategy",
    "business strategy",
    "corporate strategy",
    "growth strategy",
    "revenue strategy",
    "commercial strategy",
    "market strategy",
    "strategic initiatives",
    "strategic projects",
    "special projects",

    # Founder Office / CEO Office
    "chief of staff",
    "cos ",
    "founder's office",
    "founders office",
    "office of the ceo",
    "office of ceo",
    "ceo office",
    "executive office",

    # Growth / Revenue / GTM
    "growth",
    "growth lead",
    "head of growth",
    "growth operations",
    "growth manager",
    "revenue operations",
    "revops",
    "go to market",
    "go-to-market",
    "gtm",
    "gtm strategy",
    "market expansion",
    "marketplace growth",
    "user acquisition",

    # Business Ops / BizOps
    "business operations",
    "bizops",
    "operations strategy",
    "program management",
    "business program manager",
    "transformation office",

    # Partnerships / Expansion
    "business development",
    "strategic partnerships",
    "partnerships",
    "alliances",
    "ecosystem partnerships",
    "channel partnerships",

    # Founder / Venture / EIR
    "entrepreneur in residence",
    "eir",
    "venture builder",
    "venture lead",
    "new initiatives",
    "incubation",
    "innovation",

    # Investment / VC
    "investor",
    "investment associate",
    "investment analyst",
    "venture capital",
    "portfolio operations",

    # Leadership
    "general manager",
    "gm ",
    "business head",
    "category lead",
    "vertical lead",
    "country manager",
]

# ============================================
# Tier-2 function keywords
# Product / Monetization / AI / Ops Hybrid
# ============================================

TIER2_KEYWORDS = [

    # Product
    "product manager",
    "product management",
    "product lead",
    "group product manager",
    "senior product manager",
    "product owner",

    # Product Strategy
    "product strategy",
    "product operations",
    "product growth",
    "product analytics",
    "platform product",

    # Product Marketing
    "product marketing",
    "growth marketing",
    "performance marketing",
    "lifecycle marketing",

    # AI / Tech
    "ai product",
    "genai",
    "artificial intelligence",
    "machine learning",
    "automation",

    # Revenue / Monetization
    "monetization",
    "pricing strategy",
    "revenue growth",

    # Startup Ops
    "startup operations",
    "cross functional",
    "founding team",
    "operator",

    # Analytics
    "business analyst",
    "strategy analyst",
    "growth analyst",
]

# ============================================
# Bonus scoring keywords
# Adds extra score if found in title/company
# ============================================

TITLE_BONUS_KEYWORDS = [

    # AI
    "ai",
    "genai",
    "llm",
    "machine learning",
    "artificial intelligence",
    "automation",
    "agentic",

    # SaaS / B2B
    "saas",
    "b2b",
    "enterprise",
    "platform",
    "api",

    # Revenue / Business
    "monetization",
    "revenue",
    "growth",
    "commercial",

    # Fintech
    "fintech",
    "payments",
    "lending",
    "wealthtech",
    "insurtech",

    # Startup / Scale
    "0 to 1",
    "zero to one",
    "scale",
    "high growth",
    "hypergrowth",

    # Data / Infra
    "data",
    "analytics",
    "cloud",
    "infrastructure",

    # Consumer Internet
    "marketplace",
    "consumer",
    "creator economy",

    # Leadership Signals
    "founding",
    "strategy",
    "special projects",
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

    # =========================
    # GREENHOUSE
    # =========================

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
    ("Canva", "canva", "greenhouse"),
    ("Databricks", "databricks", "greenhouse"),
    ("Snowflake", "snowflake", "greenhouse"),
    ("HubSpot", "hubspot", "greenhouse"),
    ("Coinbase", "coinbase", "greenhouse"),
    ("Cloudflare", "cloudflare", "greenhouse"),
    ("Hashicorp", "hashicorp", "greenhouse"),
    ("Snyk", "snyk", "greenhouse"),
    ("Cockroach Labs", "cockroachlabs", "greenhouse"),
    ("Scale AI", "scaleai", "greenhouse"),
    ("Perplexity", "perplexity", "greenhouse"),
    ("Glean", "glean", "greenhouse"),
    ("Deel", "deel", "greenhouse"),
    ("Remote", "remote", "greenhouse"),
    ("Zapier", "zapier", "greenhouse"),
    ("Webflow", "webflow", "greenhouse"),
    ("Framer", "framer", "greenhouse"),
    ("Retool", "retool", "greenhouse"),
    ("Airtable", "airtable", "greenhouse"),
    ("ClickUp", "clickup", "greenhouse"),
    ("Amplitude", "amplitude", "greenhouse"),
    ("Mixpanel", "mixpanel", "greenhouse"),
    ("Datadog", "datadog", "greenhouse"),
    ("Elastic", "elastic", "greenhouse"),
    ("Confluent", "confluent", "greenhouse"),
    ("Redis", "redis", "greenhouse"),
    ("MongoDB", "mongodb", "greenhouse"),
    ("Mistral", "mistral", "greenhouse"),
    ("HuggingFace", "huggingface", "greenhouse"),
    ("Palantir", "palantir", "greenhouse"),
    ("Anduril", "anduril", "greenhouse"),
    ("Cohere", "cohere", "greenhouse"),

    # =========================
    # LEVER
    # =========================

    ("Deel", "deel", "lever"),
    ("Remote.com", "remotecom", "lever"),
    ("CRED", "cred", "lever"),
    ("Zepto", "zepto", "lever"),
    ("PhonePe", "phonepe", "lever"),
    ("Groww", "groww", "lever"),
    ("Meesho", "meesho", "lever"),
    ("Slice", "sliceit", "lever"),
    ("Freshworks", "freshworks", "lever"),
    ("CoinDCX", "coindcx", "lever"),
    ("CoinSwitch", "coinswitch", "lever"),
    ("Acko", "acko", "lever"),
    ("Navi", "navi", "lever"),
    ("Jupiter", "jupiter", "lever"),
    ("Fi Money", "epifi", "lever"),
    ("BharatPe", "bharatpe", "lever"),
    ("ShareChat", "sharechat", "lever"),
    ("MPL", "mplgaming", "lever"),
    ("Dream11", "dream11", "lever"),
    ("Urban Company", "urbancompany", "lever"),
    ("Lenskart", "lenskart", "lever"),
    ("Swiggy", "swiggy", "lever"),
    ("Zomato", "zomato", "lever"),
    ("PhysicsWallah", "physicswallah", "lever"),
    ("upGrad", "upgrad", "lever"),
    ("Apna", "apna", "lever"),
    ("Cars24", "cars24", "lever"),
    ("Spinny", "spinny", "lever"),
    ("Porter", "porter", "lever"),
    ("BlackBuck", "blackbuck", "lever"),
    ("Delhivery", "delhivery", "lever"),
    ("Shiprocket", "shiprocket", "lever"),
    ("Infra.Market", "inframarket", "lever"),
    ("Chargebee", "chargebee", "lever"),
    ("MoEngage", "moengage", "lever"),
    ("CleverTap", "clevertap", "lever"),
    ("Darwinbox", "darwinbox", "lever"),
    ("Whatfix", "whatfix", "lever"),
    ("Innovaccer", "innovaccer", "lever"),
    ("HighRadius", "highradius", "lever"),
    ("Yellow.ai", "yellowdotai", "lever"),
    ("Uniphore", "uniphore", "lever"),
    ("Gupshup", "gupshup", "lever"),
    ("DevRev", "devrev", "lever"),
    ("Rocketlane", "rocketlane", "lever"),
    ("Hasura", "hasura", "lever"),
    ("Observe.ai", "observeai", "lever"),

    # =========================
    # ASHBY
    # =========================

    ("Cursor", "cursor", "ashby"),
    ("Replit", "replit", "ashby"),
    ("Windsurf", "windsurf", "ashby"),
    ("Harvey", "harvey", "ashby"),
    ("Turing", "turing", "ashby"),
    ("Runway", "runway", "ashby"),
    ("ElevenLabs", "elevenlabs", "ashby"),
    ("Character AI", "characterai", "ashby"),
    ("Groq", "groq", "ashby"),
    ("Suno", "suno", "ashby"),

    # =========================
    # WELLFOUND / ANGELLIST
    # =========================

    ("AngelList", "angellist", "wellfound"),
    ("Wellfound", "wellfound", "wellfound"),

    # =========================
    # YC JOBS
    # =========================

    ("Y Combinator", "ycombinator", "yc"),

    # =========================
    # REMOTE-FIRST JOB BOARDS
    # =========================

    ("RemoteOK", "remoteok", "remoteok"),
    ("WeWorkRemotely", "weworkremotely", "remote"),
    ("Remotive", "remotive", "remote"),
    ("FlexJobs", "flexjobs", "remote"),

    # =========================
    # INDIA JOB PLATFORMS
    # =========================

    ("LinkedIn", "linkedin", "aggregator"),
    ("Naukri", "naukri", "aggregator"),
    ("Foundit", "foundit", "aggregator"),
    ("CutShort", "cutshort", "aggregator"),
    ("Instahyre", "instahyre", "aggregator"),
    ("Hirist", "hirist", "aggregator"),
    ("IIMJobs", "iimjobs", "aggregator"),
    ("Wellfound India", "wellfound-india", "aggregator"),
]
