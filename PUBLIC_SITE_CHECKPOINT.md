# MOMENTUMBOT_AI public website & status API checkpoint

**Checkpoint date:** 2026-10-30

**Scope:** Public website and isolated read-only informational API only. This
checkpoint does not advance or substitute for the original private trading
system's Phase 2 development blueprint.

## Verified locally

- Existing public API regression suite: **4 passed** with FastAPI 0.128.2,
  pytest 9.0.2, and httpx 0.28.1.
- API routes: `GET /healthz` and `GET /api/public/status` respond with 200;
  `POST /api/public/status` responds with 405; private login and API docs
  endpoints respond with 404.
- Against the GitHub `main` contents: **13 of 13 source/asset checks passed**,
  including page metadata, local navigation links, sitemap, icon files,
  manifesto scope, financial risk disclosure, and disconnected API configuration.
- New regression tests have been added at
  `public_api/tests/test_public_site.py`; GitHub Actions runs all tests using
  `.github/workflows/public-checks.yml` on pushes and pull requests.
- CI run success is **not yet independently confirmed**. Check the repository
  Actions tab for the `Public website and isolated API checks` workflow.

## Current safety boundary

- `api-config.json` is `{"api_base_url": null}`, leaving the public website
  disconnected from the API by default.
- The public API does not import private trading modules or database code.
- The public API response explicitly uses `trading_enabled: false`.
- Do not expose private trading routes, paper-trading balances, account data,
  exchange credentials, database URLs, or JWT secrets.
- No live public API deployment or cloud HTTPS endpoint is verified at this
  checkpoint.

## Recommended next checkpoint

1. Confirm the new GitHub Actions checks pass on `main`.
2. Confirm the live GitHub Pages website, social-preview image, and public
   page assets work in browser, separate from source-file inspection.
3. Review Docker build and runtime environment in a real container environment.
4. If a public status service is needed, deploy **only** the isolated public API,
   verify CORS, route exposure, and health checks externally, and then configure
   its HTTPS origin in `api-config.json`.
5. Keep the original private MOMENTUMBOT_AI Phase 2 blueprint independent and
   resume it only from its verified source checkpoint.
