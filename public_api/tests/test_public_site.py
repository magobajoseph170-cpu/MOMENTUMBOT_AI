"""Regression checks for the public GitHub Pages site and separation boundary."""
import json
import re
import struct
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SITE = "https://magobajoseph170-cpu.github.io/MOMENTUMBOT_AI/"


def test_public_homepage_metadata_and_assets():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    assert len(re.findall(r"<title\\b", html, flags=re.I)) == 1
    assert len(re.findall(r'<meta name="description"', html)) == 1
    assert len(re.findall(r'property="og:title"', html)) == 1
    assert f'<link rel="canonical" href="{SITE}">' in html
    assert 'name="google-site-verification"' in html
    assert f'property="og:url" content="{SITE}"' in html
    assert f'property="og:image" content="{SITE}social-preview.png"' in html
    assert 'name="twitter:card" content="summary_large_image"' in html
    assert f'name="twitter:image" content="{SITE}social-preview.png"' in html
    assert 'href="/MOMENTUMBOT_AI/favicon.svg"' in html
    assert 'href="/MOMENTUMBOT_AI/apple-touch-icon.png"' in html
    assert 'href="/MOMENTUMBOT_AI/site.webmanifest"' in html
    assert (ROOT / "favicon.svg").is_file()
    assert (ROOT / "social-preview.png").is_file()
    assert (ROOT / "apple-touch-icon.png").is_file()


def test_navigation_risk_disclosure_and_disconnected_default():
    html = (ROOT / "index.html").read_text(encoding="utf-8")
    anchors = re.findall(r'href="#([^"]+)"', html)
    assert anchors
    for anchor in anchors:
        assert f'id="{anchor}"' in html
    assert 'id="risk"' in html
    assert "Nothing on this website is investment advice" in html
    assert "api-config.json" in html
    assert "trading_enabled!==false" in html
    assert "Not connected" in html
    config = json.loads((ROOT / "api-config.json").read_text(encoding="utf-8"))
    assert config == {"api_base_url": None}


def test_sitemap_and_manifest_scoped_to_public_site():
    root = ET.parse(ROOT / "sitemap.xml").getroot()
    namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    urls = [item.text for item in root.findall(f".//{namespace}loc")]
    assert urls == [SITE]
    manifest = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
    assert manifest["start_url"] == "/MOMENTUMBOT_AI/"
    assert manifest["scope"] == "/MOMENTUMBOT_AI/"


def test_touch_icon_is_png_with_expected_dimensions():
    raw = (ROOT / "apple-touch-icon.png").read_bytes()
    assert raw[:8] == b"\\x89PNG\\r\\n\\x1a\\n"
    width, height = struct.unpack(">II", raw[16:24])
    assert (width, height) == (180, 180)
