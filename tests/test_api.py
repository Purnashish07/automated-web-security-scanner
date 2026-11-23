"""Tests for Flask API routes."""

import time
from unittest.mock import patch

import pytest


# ---------------------------------------------------------------------------
# /api/health
# ---------------------------------------------------------------------------
def test_health(client):
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# /api/scan – invalid / missing JSON
# ---------------------------------------------------------------------------
def test_scan_no_json(client):
    resp = client.post("/api/scan", data="not json", content_type="application/json")
    assert resp.status_code == 400
    assert "JSON" in resp.get_json()["error"]


def test_scan_missing_url(client):
    resp = client.post("/api/scan", json={})
    assert resp.status_code == 400


def test_scan_empty_url(client):
    resp = client.post("/api/scan", json={"url": "   "})
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# /api/scan – successful mocked scan
# ---------------------------------------------------------------------------
def test_scan_success(client):
    fake_report = {
        "target": "https://example.com",
        "scanned_at_utc": "2026-01-01T00:00:00+00:00",
        "status_code": 200,
        "final_url": "https://example.com",
        "https_used": True,
        "findings": [
            {
                "category": "HTTPS",
                "severity": "Info",
                "status": "PASS",
                "details": "The supplied URL uses HTTPS.",
                "recommendation": "",
            }
        ],
        "error": None,
        "redirect_chain": [],
    }
    with patch("app.validate_public_target"):
        with patch("app.scan_url", return_value=fake_report):
            resp = client.post("/api/scan", json={"url": "https://example.com"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status_code"] == 200
    assert len(data["findings"]) == 1


# ---------------------------------------------------------------------------
# Rate limiting → 429
# ---------------------------------------------------------------------------
def test_rate_limit(client):
    from app import rate_limit_data, RATE_LIMIT

    ip = "198.51.100.99"
    # Pre-fill the deque to simulate hitting the limit
    rate_limit_data[ip] = __import__("collections").deque(
        [time.time()] * RATE_LIMIT
    )
    resp = client.get("/api/health", headers={"X-Forwarded-For": ip})
    assert resp.status_code == 429
    assert "Rate limit" in resp.get_json()["error"]
    # clean up
    rate_limit_data.pop(ip, None)
