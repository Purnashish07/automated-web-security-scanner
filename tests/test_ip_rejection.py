import pytest
import socket
from app import validate_public_target

def mock_getaddrinfo_private(host, port, type):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('10.0.0.1', port))]

def mock_getaddrinfo_local(host, port, type):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('127.0.0.1', port))]

def mock_getaddrinfo_linklocal(host, port, type):
    return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', ('169.254.0.1', port))]

@pytest.mark.parametrize("mock_func", [mock_getaddrinfo_private, mock_getaddrinfo_local, mock_getaddrinfo_linklocal])
def test_private_ip_rejection(mock_func, monkeypatch):
    monkeypatch.setattr(socket, "getaddrinfo", mock_func)
    with pytest.raises(ValueError):
        validate_public_target("http://example.com")
