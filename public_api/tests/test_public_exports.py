"""Fail-closed, public-only approval checks for the curated export channel.

The public repository does not fetch or inspect private SharePoint storage.
Any change to the approved public release needs a reviewed change to this
allowlist and its associated editorial policy.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ROOT / "public_exports"

APPROVED_SUMMARY = {
    "schema_version": 1,
    "project": "MOMENTUMBOT_AI",
    "visibility": "public",
    "status": "under-development",
    "public_trading_enabled": False,
    "homepage_url": "https://magobajoseph170-cpu.github.io/MOMENTUMBOT_AI/",
    "summary": (
        "MOMENTUMBOT_AI is a research and development project exploring "
        "market intelligence, adaptive strategy learning, decision support, "
        "and risk-aware system design. This website is informational only "
        "and does not offer a public trading service."
    ),
    "reviewed_on": "2026-10-30",
}


def test_only_approved_export_file_can_be_published():
    assert EXPORTS.is_dir()
    files = sorted(p.relative_to(EXPORTS).as_posix() for p in EXPORTS.rglob("*") if p.is_file())
    assert files == ["project-summary.json"], "Unapproved file added to public_exports"
    assert not any(p.is_symlink() for p in EXPORTS.rglob("*"))


def test_public_summary_fields_and_values_are_explicitly_approved():
    file = EXPORTS / "project-summary.json"
    assert file.stat().st_size < 1024
    data = json.loads(file.read_text(encoding="utf-8"))
    assert data == APPROVED_SUMMARY, "Changed export content requires editorial/security approval"
    assert data["public_trading_enabled"] is False
