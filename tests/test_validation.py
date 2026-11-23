"""Tests for URL validation."""

import pytest

from security_scanner import validate_url


def test_valid_https():
    assert validate_url("https://example.com") == "https://example.com"


def test_valid_http():
    assert validate_url("http://example.com") == "http://example.com"


def test_invalid_scheme():
    with pytest.raises(ValueError):
        validate_url("ftp://example.com")


def test_missing_hostname():
    with pytest.raises(ValueError):
        validate_url("http://")


def test_username_in_url():
    with pytest.raises(ValueError):
        validate_url("http://user:pass@example.com")


def test_no_scheme():
    with pytest.raises(ValueError):
        validate_url("example.com")
