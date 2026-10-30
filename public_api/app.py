"""Public, read-only MOMENTUMBOT_AI status API.

Deliberately isolated from the private trading backend: do not import its
routers, database models, ledgers, or credentials into this module.
"""
import os
from urllib.parse import urlsplit
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

DEFAULT_SITE_ORIGIN = "https://magobajoseph170-cpu.github.io"

def allowed_origins() -> list[str]:
    """An exact list of HTTPS origins, never a wildcard or a URL path."""
    value = os.getenv("MOMENTUMBOT_PUBLIC_CORS_ORIGINS", DEFAULT_SITE_ORIGIN)
    origins = [part.strip() for part in value.split(",")]
    if not origins or not all(origins):
        raise ValueError("Public CORS origins must not be empty")
    for origin in origins:
        parsed = urlsplit(origin)
        if (parsed.scheme != "https" or not parsed.hostname
                or parsed.username or parsed.password or parsed.path not in ("",)
                or parsed.query or parsed.fragment or origin != f"https://{parsed.netloc}"):
            raise ValueError("Public CORS origins must be exact HTTPS origins")
    return list(dict.fromkeys(origins))

app = FastAPI(
    title="MOMENTUMBOT_AI Public Status API",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    debug=False,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["Accept"],
    max_age=600,
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Cache-Control"] = "no-store"
    # HTTPS is terminated by the hosting provider's reverse proxy.
    if request.url.scheme == "https" or request.headers.get("x-forwarded-proto", "").lower() == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response

@app.get("/healthz", include_in_schema=False)
def healthz():
    """Process health only; does not imply trading-engine readiness."""
    return {"status": "ok", "service": "momentumbot-public-api"}

@app.get("/api/public/status", include_in_schema=False)
def public_status():
    """Safe for any visitor: no balances, keys, trading signals or user data."""
    return {
        "project": "MOMENTUMBOT_AI",
        "service": "momentumbot-public-api",
        "status": "online",
        "mode": "public-information-only",
        "trading_enabled": False,
        "message": "Public information service; private paper trading is not exposed.",
    }
