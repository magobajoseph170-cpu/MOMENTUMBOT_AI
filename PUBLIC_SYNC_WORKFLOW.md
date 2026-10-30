# SharePoint → GitHub public-only promotion workflow

**Mode:** Manual, approval-gated, no automatic SharePoint mirroring.

## Source and destination

- **Private source:** The owner's OneDrive / SharePoint project folder under
  `Documents/ChatGPT/MOMENTUMBOT_AI`. Its `PUBLIC_SYNC_STAGING` subfolder is
  the *only* source from which future public exports may be reviewed.
- **Public destination:** This repository, `public_exports/`, using a GitHub
  pull request. The public GitHub repository is **not** a backup of the private
  trading project.
- **Eligible names (exact case):** `PROJECT_OVERVIEW.md`,
  `PUBLIC_ROADMAP.md`, `RELEASE_NOTES.md`. These are *document templates
  for future deliberate releases*, not permissions to publish existing private
  documents merely because they are renamed.
- **Never eligible:** `TRADING_BOT_BLUEPRINT.md`, `src/`, `backend/`, `data/`,
  `momentumbot.db`, `.env*`, database dumps, keys, trade logs, customer data,
  project archives, credentials, local paths, and raw research/source notes.

## Review and promotion procedure

1. Author an **original, redacted, publication-ready** document in
   `PUBLIC_SYNC_STAGING` with one of the three approved names.
2. Review it sentence-by-sentence. Omit private strategy internals, account
   numbers, identifiers, links into private OneDrive storage, live trading
   instructions, internal architecture details, and any secret or personal data.
   Do not publish the private project README, blueprint, or source files.
3. Copy **only the reviewed document** into the public repo's
   `public_exports/` folder **on a new review branch**, not `main`.
4. Run `python tools/validate_public_sync.py` and
   `python -m pytest -q tests/test_public_sync_validator.py`. GitHub Actions
   repeats these checks for pull requests. The gate rejects unexpected paths,
   nested folders and symlinks, binary files, oversized documents, and common
   secret/path patterns; it cannot prove a document is safe.
5. Examine the complete GitHub diff and open a pull request for **manual
   owner approval**. Do not merge or publish before that review. Configure
   branch protection / a ruleset for `main` to require pull requests, approval
   and the `validate-public-export` check if the repository plan supports it.
6. After approval, merge. The named Markdown documents become public. Check
   GitHub's visible content and remove any inappropriate material immediately,
   remembering that Git history and caches can retain past disclosures.

## Security properties and limitations

- No SharePoint access token, PAT, secret, or private file is stored in GitHub.
- No GitHub Action polls, reads, or has credentials for SharePoint.
- There is **no automatic upload or background synchronization** and no
  two-way mirroring. A user must deliberately start each reviewed promotion.
- A passing CI scan is a *screening aid*, not an authorization to disclose.
- The existing `api-config.json` remains disconnected from the private
  trading backend. Nothing here exposes live trading, paper ledger or login.
- The private trading blueprint and development checkpoint are independent of
  the website and publication workflow.
