import ipaddress
import socket
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from urllib.parse import urlparse

from flask import Flask, jsonify, render_template, request

from security_scanner import scan_url, validate_url

# ---------------------------------------------------------------------------
# Flask app – static assets live under public/static/ for Vercel compat.
# ---------------------------------------------------------------------------
app = Flask(__name__, static_folder="public/static", static_url_path="/static")
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


# ---------------------------------------------------------------------------
# SSRF guard: reject any hostname that resolves to a non-public IP.
# ---------------------------------------------------------------------------
def validate_public_target(url: str) -> str:
    """Validate URL format and ensure the hostname resolves to a public IP."""
    validate_url(url)
    parsed = urlparse(url)

    if parsed.port and not (1 <= parsed.port <= 65535):
        raise ValueError("Invalid port number.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("A hostname is required.")

    try:
        addresses = socket.getaddrinfo(
            hostname,
            parsed.port or (443 if parsed.scheme == "https" else 80),
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror:
        raise ValueError("The hostname could not be resolved.")

    if not addresses:
        raise ValueError("The hostname has no usable IP addresses.")

    for address in {item[4][0] for item in addresses}:
        ip = ipaddress.ip_address(address)
        if not ip.is_global:
            raise ValueError("Only publicly routable target addresses are allowed.")

    return url


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def index():
    return render_template("index.html")


# ---------------------------------------------------------------------------
# Simple in-memory rate limiting (5 req/min per client IP).
# Best-effort on serverless: each cold-start resets the counters.
# ---------------------------------------------------------------------------
rate_limit_data: dict[str, deque] = defaultdict(deque)
RATE_LIMIT = 5
RATE_WINDOW = 60  # seconds


def _get_client_ip() -> str:
    """Return the client IP from X-Forwarded-For (first value) or remote_addr."""
    xff = request.headers.get("X-Forwarded-For", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.remote_addr or "unknown"


def is_rate_limited(ip: str) -> bool:
    now = time.time()
    q = rate_limit_data[ip]
    # Discard timestamps outside the window
    while q and now - q[0] > RATE_WINDOW:
        q.popleft()
    # Clean up empty deques to prevent memory growth
    if not q:
        rate_limit_data.pop(ip, None)
    if len(q) >= RATE_LIMIT:
        return True
    q.append(now)
    return False


@app.before_request
def limit_requests():
    client_ip = _get_client_ip()
    if is_rate_limited(client_ip):
        return jsonify({"error": "Rate limit exceeded. Try again later."}), 429


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})


# ---------------------------------------------------------------------------
# Security headers (CSP whitelists Tailwind CDN + Google Fonts)
# ---------------------------------------------------------------------------
@app.after_request
def add_security_headers(response):
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; "
        "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "connect-src 'self'; "
        "frame-ancestors 'none';"
    )
    response.headers["Content-Security-Policy"] = csp
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = ""
    return response


# ---------------------------------------------------------------------------
# Scan endpoint
# ---------------------------------------------------------------------------
@app.post("/api/scan")
def api_scan():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({"error": "Send a JSON object containing a URL."}), 400

    url = payload.get("url")
    if not isinstance(url, str) or not url.strip():
        return jsonify({"error": "Please provide a website URL."}), 400

    url = url.strip()

    try:
        validate_public_target(url)
    except (ValueError, OSError) as exc:
        return jsonify({"error": str(exc)}), 400

    try:
        report = scan_url(url, timeout=10)
    except Exception as exc:
        return jsonify({"error": f"Scanner failed: {exc}"}), 502

    if report.get("error"):
        return jsonify({
            "error": report["error"],
            "target": report.get("target", url),
            "scanned_at_utc": report.get(
                "scanned_at_utc",
                datetime.now(timezone.utc).isoformat(),
            ),
        }), 502

    return jsonify(report)


# ---------------------------------------------------------------------------
# Local dev server
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
