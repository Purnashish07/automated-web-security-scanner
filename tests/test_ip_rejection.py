"""Tests for SSRF / private-IP rejection."""

import socket

import pytest

from app import validate_public_target


def _make_mock(ip):
    """Return a mock getaddrinfo that always resolves to the given IP."""
    def mock_getaddrinfo(host, port, **kwargs):
        return [(socket.AF_INET, socket.SOCK_STREAM, 6, "", (ip, port))]
    return mock_getaddrinfo


@pytest.mark.parametrize("ip", [
    "127.0.0.1",       # loopback
    "10.0.0.1",        # private class A
    "192.168.1.1",     # private class C
    "169.254.0.1",     # link-local
    "::1",             # IPv6 loopback
])
def test_private_ip_rejected(ip, monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", _make_mock(ip))
    with pytest.raises(ValueError, match="publicly routable"):
        validate_public_target("http://example.com")
