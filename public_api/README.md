# MOMENTUMBOT_AI public status API

The files under `public_api/` are **a separate, read-only informational service**.
This service intentionally does not import or expose the private trading backend,
the database, paper ledger, personal accounts, credentials, or trading endpoints.

## Local verification

```sh
python -m pip install -r public_api/requirements.txt pytest httpx
pytest -q public_api/tests
uvicorn public_api.app:app --host 127.0.0.1 --port 8001
```

Local endpoints:
- `GET http://127.0.0.1:8001/healthz` — public process health only
- `GET http://127.0.0.1:8001/api/public/status` — public project status

**The health check is not evidence that the trading engine is healthy.**

## HTTPS deployment

A dedicated container Dockerfile is at the GitHub repository root. It copies
**only** the public service code, and its command listens on the host-supplied
`PORT`. Connect a hosting account, create a new web service from this GitHub
repository, use the Dockerfile, and set its healthcheck path to `/healthz`.
Enable the host's public HTTPS domain. The website will remain disconnected
until the actual verified HTTPS origin is added to `api-config.json`.

The sole allowed browser origin defaults to
`https://magobajoseph170-cpu.github.io`. If explicitly configuring
`MOMENTUMBOT_PUBLIC_CORS_ORIGINS`, provide comma-separated **exact HTTPS
origins without paths**, not wildcards. Allowed cross-origin methods are GET
only; browser credentials are not shared.

Do **not** supply the private database URL, JWT secret, paper ledger,
exchange keys, Telegram credentials, or production trading routers.
Do not expose the existing private `backend.main:app` service.

## Frontend status integration

The frontend reads `api-config.json` at its own GitHub Pages origin.
`api_base_url: null` means the service is **not configured**.
Once the hosted API is live, put **only** its HTTPS origin in this file
(no paths, credentials, query strings, or secrets).
The website fetches only `/api/public/status` and displays an explicit
informational status. No trading interface is enabled.

## Required production verification

1. Host reports the container running; `GET /healthz` responds over HTTPS.
2. `GET /api/public/status` returns `trading_enabled: false`.
3. CORS returns the exact GitHub Pages origin for allowed GET requests but
   does not authorize foreign origins or write requests.
4. `/users/login`, `/paper-trading/kill-switch`, `/trade-execution`,
   `/docs`, and `/openapi.json` are unavailable.
5. Browser loads project status and does not display **connected** if
   the API cannot be reached.

**Security boundary:** CORS is a browser restriction, not authorization.
The private trading backend requires a separate route-by-route authorization
and operational security review before any remote exposure.
