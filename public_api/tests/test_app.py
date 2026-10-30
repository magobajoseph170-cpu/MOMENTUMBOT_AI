"""Security regression tests for the isolated public status API."""
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from public_api.app import app, allowed_origins

SITE_ORIGIN = "https://magobajoseph170-cpu.github.io"


def test_health_only_reports_public_process():
    response = TestClient(app).get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "momentumbot-public-api"}
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"


def test_public_status_is_read_only_and_not_trading():
    client = TestClient(app)
    response = client.get("/api/public/status")
    assert response.status_code == 200
    body = response.json()
    assert body["project"] == "MOMENTUMBOT_AI"
    assert body["trading_enabled"] is False
    for path in ("/users", "/users/login", "/users/profile", "/paper-trading/status", "/paper-trading/kill-switch", "/trade-execution", "/docs", "/openapi.json", "/redoc"):
        assert client.get(path).status_code == 404
        assert client.post(path, json={}).status_code == 404
    assert client.post("/api/public/status", json={}).status_code == 405


def test_exact_cors_origin_and_preflight_restrictions():
    client = TestClient(app)
    ok = client.get("/api/public/status", headers={"Origin": SITE_ORIGIN})
    assert ok.headers["access-control-allow-origin"] == SITE_ORIGIN
    assert ok.headers.get("access-control-allow-credentials") is None
    bad = client.get("/api/public/status", headers={"Origin": "https://attacker.example"})
    assert "access-control-allow-origin" not in bad.headers
    preflight = client.options("/api/public/status", headers={
        "Origin": SITE_ORIGIN, "Access-Control-Request-Method": "POST"
    })
    assert preflight.status_code == 400
    bad_preflight = client.options("/api/public/status", headers={
        "Origin": "https://attacker.example", "Access-Control-Request-Method": "GET"
    })
    assert bad_preflight.status_code == 400


def test_config_fail_closed_for_wildcards_and_paths(monkeypatch):
    for value in ("*", "http://magobajoseph170-cpu.github.io",
                  "https://magobajoseph170-cpu.github.io/MOMENTUMBOT_AI",
                  "", "https://host.example,"):
        monkeypatch.setenv("MOMENTUMBOT_PUBLIC_CORS_ORIGINS", value)
        with pytest.raises(ValueError):
            allowed_origins()
    monkeypatch.setenv("MOMENTUMBOT_PUBLIC_CORS_ORIGINS", SITE_ORIGIN)
    assert allowed_origins() == [SITE_ORIGIN]
