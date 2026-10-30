"""Regression tests for the fail-closed public promotion gate."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from validate_public_sync import validate_directory


def test_empty_staging_is_safe(tmp_path):
    (tmp_path / ".gitkeep").touch()
    assert validate_directory(tmp_path) == []


def test_only_exact_allowlisted_document_names(tmp_path):
    (tmp_path / "PROJECT_OVERVIEW.md").write_text("# Public research overview\n", encoding="utf-8")
    assert validate_directory(tmp_path) == []
    (tmp_path / "TRADING_BOT_BLUEPRINT.md").write_text("private", encoding="utf-8")
    assert any("allowlist" in issue for issue in validate_directory(tmp_path))


def test_block_secret_assignment_and_private_paths(tmp_path):
    candidate = tmp_path / "RELEASE_NOTES.md"
    candidate.write_text("API_KEY=real-value\n", encoding="utf-8")
    assert any("secret assignment" in issue for issue in validate_directory(tmp_path))
    candidate.write_text("Internal route: backend/main.py", encoding="utf-8")
    assert any("private path" in issue for issue in validate_directory(tmp_path))


def test_block_nested_content_and_symlinks(tmp_path):
    (tmp_path / "subdirectory").mkdir()
    assert any("nested folders" in issue for issue in validate_directory(tmp_path))
    (tmp_path / "subdirectory").rmdir()
    (tmp_path / "PUBLIC_ROADMAP.md").symlink_to(tmp_path / "nonexistent")
    assert any("nested folders" in issue for issue in validate_directory(tmp_path))


def test_block_email_and_binary_payload(tmp_path):
    candidate = tmp_path / "PUBLIC_ROADMAP.md"
    candidate.write_text("Contact: someone@example.com", encoding="utf-8")
    assert any("personal email" in issue for issue in validate_directory(tmp_path))
    candidate.write_bytes(b"\x00\x01")
    assert any("binary" in issue for issue in validate_directory(tmp_path))
