# keyword_filter.py

# 1. Conversational / flow continuity (always allowed)
SMALL_TALK = [
    "hi", "hello", "hey", "thanks", "thank you", "ok", "okay",
    "yes", "no", "hmm", "please", "help", "tell me", "explain",
    "more", "continue", "towards", "about this", "what about"
]

# 2. Core cattle keywords (explicit)
CATTLE_KEYWORDS = [
    "cow", "cows", "cattle", "buffalo", "buffaloes",
    "livestock", "dairy", "herd",

    # health
    "health", "disease", "ill", "sick", "fever", "mastitis",
    "lameness", "parasite", "infection", "vaccination",

    # nutrition
    "feed", "fodder", "nutrition", "diet", "silage", "hay",
    "water", "mineral", "protein", "energy",

    # milk
    "milk", "yield", "production", "udder", "milking",

    # reproduction / breeding
    "reproduction", "breeding", "estrus", "heat",
    "calving", "pregnant", "pregnancy", "fertility",
    "insemination", "ai", "semen", "bull",

    # housing & environment
    "shed", "housing", "ventilation", "bedding",
    "environment", "climate", "temperature",
    "heat stress", "humidity",

    # management
    "management", "farm", "records", "comfort"
]

# 3. Implicit cattle intent combinations
IMPLICIT_INTENT_PAIRS = [
    ("milk", "environment"),
    ("milk", "climate"),
    ("milk", "housing"),
    ("milk", "temperature"),
    ("milk", "heat"),
    ("milk", "ventilation"),
    ("milk", "humidity"),
    ("production", "environment"),
]

def is_cattle_related(query: str) -> bool:
    q = query.lower().strip()

    # allow short conversational continuity
    if len(q.split()) <= 3 and any(x in q for x in SMALL_TALK):
        return True

    # allow explicit cattle domain
    if any(k in q for k in CATTLE_KEYWORDS):
        return True

    # allow implicit cattle intent
    for a, b in IMPLICIT_INTENT_PAIRS:
        if a in q and b in q:
            return True

    return False
