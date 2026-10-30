# MOMENTUMBOT_AI — Repository and document storage boundary

This public GitHub repository is the source of truth for the **public website**
and the deliberately isolated **read-only public status API**.

The original trading project, its development blueprint, local datasets, and
private backend files are maintained separately in the owner's **private
Microsoft OneDrive/SharePoint project folder**.

## Separation policy

- Public here: GitHub Pages homepage, SEO assets, favicon, social image,
  isolated informational API, its tests, and public project checkpoints.
- Private: trading-engine source, local database, strategy memory, private
  API routers, exchange credentials, account details, and the full trading
  blueprint.
- Do **not** publish or automatically mirror the private folder into this
  public repository.
- Do not publish private OneDrive folder URLs or access tokens.
- A future approved integration should sync a reviewed, explicitly allowlisted
  subset of **public documentation only**, without database or secrets.

## Public project checkpoint

The repository's `PUBLIC_SITE_CHECKPOINT.md` records the last public
website/API verification checkpoint. CI tests are located in
`.github/workflows/public-checks.yml`.

The informational API remains disconnected from GitHub Pages until a separate
HTTPS service is verified and the owner explicitly configures
`api-config.json`. No private trading endpoint should be exposed.

**Note:** This document describes the ownership boundary and cross-references
the two storage locations. It does not create automatic two-way synchronization.
