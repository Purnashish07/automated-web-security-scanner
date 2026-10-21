
import ipaddress
import socket
from datetime import datetime, timezone
from urllib.parse import urlparse

from flask import Flask, jsonify, render_template, request

from app_cli_backup import scan_url, validate_url


app = Flask(__name__)

# Keep this development server local to your own computer.
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


def validate_public_target(url):
    """Validate the URL and reject hostnames resolving to non-public IPs."""
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


@app.get("/")
def index():
    return render_template("index.html")


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

    # The original scanner follows redirects automatically. Avoid using it
    # for untrusted public targets until redirects are revalidated per hop.
    # This endpoint is intended for authorized testing only.
    report = scan_url(url, timeout=10)

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


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
