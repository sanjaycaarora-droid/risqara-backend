"""
Reference map of non-US filing systems and local financial news sources —
roadmap item 1 (international coverage). This is a DATA/REFERENCE module
only; nothing here is wired into risqara_engine.py yet. Each market below
is either "ready to integrate" (has a real, accessible API) or explicitly
flagged as harder, so the next engineering step per market is honest about
its own difficulty rather than uniform.

Verified 2026-09-07 — API landscapes shift, so re-check before building
against any of these if this file is more than a few months old.
"""

# -----------------------------------------------------------------------
# Filing systems, by country. "api_status" is the single most important
# field here — it tells you whether the next step is "sign up and build"
# or "this needs a different approach entirely."
# -----------------------------------------------------------------------
FILING_SYSTEMS = {
    "US": {
        "exchanges": ["NYSE", "NASDAQ"],
        "system": "SEC EDGAR",
        "api_status": "integrated",
        "api_url": "https://www.sec.gov/edgar",
        "notes": "Already live in risqara_engine.py (fetch_sec_filings). Free, no key required.",
    },
    "CA": {
        "exchanges": ["TSX", "TSXV"],
        "system": "SEDAR+",
        "api_status": "hard — confirmed (2026-09-07) there is no official public API at all. "
                       "Anonymous public access is browser-search-only, capped at exporting 30 "
                       "documents at a time as CSV. Real options are browser-automation scraping "
                       "against the public UI (fragile, ToS risk) or a paid third-party vendor "
                       "(e.g. QuoteMedia). Reclassified from 'moderate' to the same tier as "
                       "Italy/India — no free API path exists, period.",
        "api_url": "https://www.sedarplus.ca",
        "notes": "Example: any TSX-listed company, e.g. Shopify, RBC.",
    },
    "GB": {
        "exchanges": ["LSE"],
        "system": "Companies House",
        "api_status": "ready — official, free, no per-call charges. Sign up at "
                       "developer.company-information.service.gov.uk for an API key.",
        "api_url": "https://developer.company-information.service.gov.uk/",
        "notes": (
            "Covers company filings/accounts, not the LSE's own Regulatory News Service (RNS) "
            "for market announcements — that's a separate, less openly-documented feed. Start "
            "with Companies House for filings; revisit RNS access separately if needed."
        ),
    },
    "JP": {
        "exchanges": ["TSE (Tokyo Stock Exchange)"],
        "system": "EDINET",
        "api_status": "ready — official free API (needs a free key from the FSA). A third-party "
                       "(edinetdb.com) also offers a free tier (100 req/day) if the official "
                       "one proves awkward to integrate directly.",
        "api_url": "https://disclosure2dl.edinet-fsa.go.jp/guide/static/disclosure/WZEK0110.html",
        "notes": "Example: Sony, Toyota. Official docs are Japanese-first; EDINET DB's docs are English.",
    },
    "KR": {
        "exchanges": ["KRX (KOSPI/KOSDAQ)"],
        "system": "DART / OpenDART",
        "api_status": "ready — official free Open API, JSON + XBRL. Korea has been expanding "
                       "an English-language disclosure layer through 2026, which should make "
                       "this one of the more approachable non-English-market integrations.",
        "api_url": "https://opendart.fss.or.kr/",
        "notes": "Example: Samsung, SK Hynix. englishdart.fss.or.kr is the English-facing portal.",
    },
    "DE": {
        "exchanges": ["Deutsche Börse (Frankfurt)"],
        "system": "Unternehmensregister / Bundesanzeiger",
        "api_status": "moderate — no single official free developer API, but the official portal "
                       "(unternehmensregister.de) is genuinely public, and several third-party "
                       "wrappers (OpenRegister, handelsregister.ai, a Bundesanzeiger API on "
                       "Parse.bot) offer structured access, some with free/low-cost tiers. "
                       "Realistic path is a paid or low-cost third-party wrapper, not a from-"
                       "scratch scraper.",
        "api_url": "https://www.unternehmensregister.de",
        "notes": "Example: SAP, Siemens. Full detailed documents (e.g. complete financials) sometimes cost ~€1 each even via official channels.",
    },
    "FR": {
        "exchanges": ["Euronext Paris"],
        "system": "AMF (BALO / regulated information)",
        "api_status": "moderate — filings are real and public (URD/annual reports in iXBRL under "
                       "EU ESEF, ad-hoc disclosures), but no confirmed official free API was found. "
                       "Third-party aggregators (e.g. FinancialFilings) offer near-real-time API/"
                       "webhook access commercially. Similar shape to Germany: accessible, not free-official.",
        "api_url": "https://www.amf-france.org",
        "notes": "Example: LVMH, TotalEnergies. Revisit once ESAP (below) is actually live.",
    },
    "IT": {
        "exchanges": ["Euronext Milan (Borsa Italiana)"],
        "system": "CONSOB (1Info)",
        "api_status": "hard — disclosures are filed through CONSOB's 1Info/Mercato Elettronico "
                       "system, but no public API access was found in research. Would need direct "
                       "inquiry with CONSOB or a commercial data vendor. Same tier as India for now.",
        "api_url": "https://www.consob.it/en/web/consob/home-page-en",
        "notes": "Example: Ferrari, Eni.",
    },
    "_EU_FUTURE": {
        "exchanges": ["all EU-regulated markets"],
        "system": "ESAP (European Single Access Point)",
        "api_status": "NOT YET USABLE — Phase 1 data collection just started July 2026 (national "
                       "authorities loading entity metadata into a central repository). Public "
                       "launch with a real API is scheduled for July 2027, with sustainability-"
                       "disclosure data following in a Phase 2 starting January 2028. Worth "
                       "revisiting this whole file once ESAP goes public — it could eventually "
                       "replace the FR/DE/IT entries above with one unified integration.",
        "api_url": "https://www.esma.europa.eu/esg-and-innovation/esap",
        "notes": "Not a country — a placeholder to remember why FR/DE/IT are handled separately for now.",
    },
    "IN": {
        "exchanges": ["BSE", "NSE"],
        "system": "BSE/NSE corporate announcements",
        "api_status": "hard — no official public API. Real options are unofficial scraping "
                       "libraries (fragile, carries ToS risk, breaks on site changes) or paid "
                       "commercial vendors (quoted around ₹3 lakh/year for official BSE data). "
                       "Not recommended as a first build target given the cost/fragility tradeoff.",
        "api_url": "https://www.nseindia.com/companies-listing/corporate-filings-announcements",
        "notes": (
            "Example: HDFC Bank. Until a real API path exists, this market is better served by "
            "the local news sources below plus Grok's live web search than by a formal filings feed."
        ),
    },
}

# -----------------------------------------------------------------------
# Local financial news/data sources worth folding into the news-fetch step
# per region — lower effort than filing-system integration, and covers the
# gap for markets (like India) where formal filings access is hard.
# Add each as an RSS/API source in risqara_engine.py's news fetcher once
# a feed URL or API is confirmed for it.
# -----------------------------------------------------------------------
LOCAL_NEWS_SOURCES = {
    "CA": ["The Globe and Mail (Report on Business)", "Financial Post"],
    "GB": ["Financial Times", "This Is Money", "London Stock Exchange RNS feed"],
    "JP": ["Nikkei Asia", "Japan Times (business)"],
    "KR": ["Korea Herald (business)", "Yonhap Infomax"],
    "DE": ["Handelsblatt", "Manager Magazin"],
    "FR": ["Les Echos", "La Tribune"],
    "IT": ["Il Sole 24 Ore", "MF Milano Finanza"],
    "IN": ["Economic Times", "Moneycontrol", "Business Standard"],
}

# -----------------------------------------------------------------------
# Next steps, in the order they should actually happen. This is G7 + Korea
# (Japan is in both groups — G7 membership doesn't duplicate the work).
# Not all eight markets are the same amount of effort, so don't batch them
# as one task — three are genuinely ready, three are commercial/uncertain,
# two are hard-skip-for-now.
# -----------------------------------------------------------------------
# TIER 1 — ready now, official free APIs. GB and KR are DONE (see
# fetch_uk_filings/fetch_kr_filings below); JP still needs exploration
# since its official API is date-indexed, not company-search-shaped:
# 1. GB (Companies House) — DONE, tested against a real key, working.
# 2. JP (EDINET) — register a free key, but expect to design around the
#    date-indexed shape rather than mirror fetch_sec_filings() directly.
# 3. KR (OpenDART) — DONE, tested against a real key, working.
#
# TIER 2 — accessible, but only via paid/third-party services or an
# unconfirmed official path. Worth a deliberate call before building,
# since "integrate" here likely means "pay for a data vendor," not
# "sign up for a free key":
# 4. DE (Bundesanzeiger/Unternehmensregister) — a third-party wrapper
#    (OpenRegister, handelsregister.ai) is the realistic path.
# 5. FR (AMF) — similar shape to Germany, commercial aggregators only.
#
# TIER 3 — hard, skip formal filings integration for now. Add the local
# news sources above to the news fetcher instead, and lean on Grok's live
# web/X search (already enabled) to cover the gap:
# 6. CA (SEDAR+) — confirmed no public API exists at all (2026-09-07).
# 7. IT (CONSOB/1Info) — no public API found.
# 8. IN (BSE/NSE) — no official public API found.
#
# Revisit DE/FR/IT as a group once ESAP goes public (July 2027) — it may
# replace all three national integrations with one EU-wide one.
