import pytest
import socket
from urllib.parse import urlparse
from app import app
from security_scanner import validate_url

# ---------- validation unit tests ----------

def test_valid_url():
    assert validate_url("https://example.com") == "https://example.com"

def test_invalid_scheme():
    with pytest.raises(ValueError):
        validate_url("ftp://example.com")

def test_missing_hostname():
    with pytest.raises(ValueError):
        validate_url("http://")

def test_username_in_url():
    with pytest.raises(ValueError):
        validate_url("http://user:pass@example.com")
