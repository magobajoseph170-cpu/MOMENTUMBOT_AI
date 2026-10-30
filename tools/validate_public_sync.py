"""Fail-closed validation for hand-reviewed public documentation exports.

This is NOT a SharePoint crawler. Only specifically named, intentionally staged,
plain-text release documents may be copied to a public GitHub PR.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ALLOWED_NAMES = frozenset({"PROJECT_OVERVIEW.md", "PUBLIC_ROADMAP.md", "RELEASE_NOTES.md"})
MAX_BYTES = 64 * 1024
# Deliberately conservative: a false positive requires human review; false negatives
# remain possible, so review and repository branch protection are still necessary.
DENY_PATTERNS = (
    ("credential marker", re.compile(r"(?i)(?:github_pat_|gh[pousr]_|sk-[a-z0-9]{16,}|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")),
    ("secret assignment", re.compile(r"(?im)^\s*[\w.-]*(?:secret|password|passwd|api[_-]?key|access[_-]?token|refresh[_-]?token|private[_-]?key)[\w.-]*\s*[:=]\s*\S+")),
    ("connection string", re.compile(r"(?i)(?:postgres(?:ql)?(?:\+\w+)?|mysql|mongodb(?:\+srv)?|redis|sqlite)://\S+")),
    ("authorization header", re.compile(r"(?i)authorization\s*[:=]\s*(?:bearer|basic)\s+\S+")),
    ("private path", re.compile(r"(?i)(?:[a-z]:\\|/home/|/users/[^\s/]+/|\.env(?:\b|_)|(?:backend|src|data)/[a-z0-9_./-]+)")),
    ("personal email", re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b")),
)


def validate_directory(folder: Path) -> list[str]:
    errors: list[str] = []
    if folder.is_symlink() or not folder.is_dir():
        return ["public_exports must be a regular directory"]
    for path in folder.iterdir():
        if path.is_symlink() or not path.is_file():
            errors.append(f"{path.name}: nested folders, links, and non-files are forbidden")
            continue
        if path.name == ".gitkeep":
            if path.stat().st_size:
                errors.append(".gitkeep must be empty")
            continue
        if path.name not in ALLOWED_NAMES:
            errors.append(f"{path.name}: not on exact public filename allowlist")
            continue
        data = path.read_bytes()
        if len(data) > MAX_BYTES:
            errors.append(f"{path.name}: exceeds {MAX_BYTES} byte limit")
            continue
        if b"\x00" in data:
            errors.append(f"{path.name}: binary content forbidden")
            continue
        try:
            content = data.decode("utf-8")
        except UnicodeDecodeError:
            errors.append(f"{path.name}: not UTF-8")
            continue
        for reason, pattern in DENY_PATTERNS:
            if pattern.search(content):
                errors.append(f"{path.name}: possible {reason}; human review required")
    return errors


def main() -> int:
    base = Path(__file__).resolve().parents[1]
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else base / "public_exports"
    issues = validate_directory(folder)
    if issues:
        for issue in issues:
            print(f"BLOCKED: {issue}", file=sys.stderr)
        return 1
    print("Public export candidate validation passed. Human review still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
