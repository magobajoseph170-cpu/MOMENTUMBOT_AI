# MOMENTUMBOT_AI — Public-only SharePoint-to-GitHub release workflow

**Direction:** Private SharePoint public-release staging → reviewed GitHub public export.

This is an **approval-gated, manual one-way synchronization process**, not an
unattended connection, repository mirror, or a GitHub Actions download from
SharePoint. The private original trading application remains separate.

## Approved source and destination

- Private staging: `Documents/ChatGPT/MOMENTUMBOT_AI/PUBLIC_RELEASE_CANDIDATES`
  in the owner's connected SharePoint/OneDrive.
- Public destination: `public_exports/project-summary.json` in this GitHub repo.
- Current allowed export: a non-sensitive, fixed informational project summary,
  with `public_trading_enabled: false`.
- This approved first export was authored afresh from already-public project
  information; **none** of the private SharePoint development files were copied.

## Publishing steps

1. Draft a candidate in the private staging area, without copying private
   source files, databases, credentials or the full blueprint.
2. Verify exact content and ensure it contains no secrets, user data, strategy
   algorithms, performance claims, trading signals, unpublished blueprints,
   file-sharing links or internal system paths.
3. Get explicit owner approval for the exact public candidate.
4. Change **only** `public_exports/project-summary.json`. Use a GitHub pull
   request for review and do not merge until its diff is approved. If the
   approved text itself changes, update the strict validator in the same
   reviewed PR; do not weaken the validator to silence a failure.
5. GitHub Actions runs `python -m pytest -q public_api/tests` on PRs and pushes,
   including the exact-file allowlist and approved-value checks at
   `public_api/tests/test_public_exports.py`.
6. Record the resulting commit and verify its public content. The website and
   public API do not read this file automatically; this is a documentation
   publication channel only.

## Never synchronize to this public repository

- `src/`, `backend/`, `venv/`, `data/`, source ZIPs or private backup files
- `momentumbot.db`, `paper.sqlite3`, account or trading ledgers
- Any `.env`, secret keys, access tokens, exchange credentials or connection strings
- `TRADING_BOT_BLUEPRINT.md` and strategy implementation details
- Unreviewed `README.md`, research notes or private folder references

## Operational limitations

The workflow does **not** authenticate GitHub Actions to OneDrive/SharePoint,
and there is **no scheduled synchronization**. CI validates what reaches the
repository, not the safety of arbitrary future content. Require human review
and, if available, protect `main` using GitHub repository rules / required
status checks. GitHub does not automatically stop direct pushes unless branch
protection is configured.

The isolated public status API retains `api-config.json` with
`api_base_url: null`. No private trading backend or database is connected.
