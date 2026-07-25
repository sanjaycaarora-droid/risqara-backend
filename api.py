"""
Risqara API — thin FastAPI wrapper around risqara_engine.

Keeps XAI_API_KEY and the SEC contact email server-side; the mobile app
only ever talks to this service over HTTPS, never to xAI/SEC directly.

Run locally:
    uvicorn api:app --reload --host 0.0.0.0 --port 8000
"""

from concurrent.futures import ThreadPoolExecutor
import asyncio
import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

import risqara_engine as engine

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Risqara API", version="1.0.0")

# This URL is now permanently public (no shared-secret gate like the old
# ngrok setup), so cap requests per IP to protect against a bot/scraper
# running up the xAI bill. In-memory, per-process — resets on redeploy,
# which is fine at this scale; move to a shared store (Redis) if this
# service ever runs more than one instance.
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Demo-scope CORS: the mobile app is untrusted-origin (Expo dev server /
# device), so allow all origins. Lock this down to the app's real origin(s)
# before shipping to production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_executor = ThreadPoolExecutor(max_workers=8)


class AnalyzeRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=100)


class BatchAnalyzeRequest(BaseModel):
    queries: list[str] = Field(..., min_length=1, max_length=10)


async def _run_analysis(query: str) -> dict:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(_executor, engine.run_analysis, query)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "grok_configured": bool(engine.XAI_API_KEY),
        "claude_cross_check_configured": bool(engine.ANTHROPIC_API_KEY),
    }


@app.post("/analyze")
@limiter.limit("20/hour")
async def analyze(request: Request, req: AnalyzeRequest):
    query = req.query.strip()
    if not query:
        raise HTTPException(400, "query must not be empty")
    return await _run_analysis(query)


@app.post("/analyze/batch")
@limiter.limit("5/hour")
async def analyze_batch(request: Request, req: BatchAnalyzeRequest):
    queries = [q.strip() for q in req.queries if q.strip()]
    if not queries:
        raise HTTPException(400, "queries must contain at least one non-empty target")

    results = await asyncio.gather(*(_run_analysis(q) for q in queries))
    return {"results": results}
