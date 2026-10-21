import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests


SECURITY_HEADERS = {
    "content-security-policy": {
        "severity": "Medium",
        "description": "Helps reduce risks from injected content such as XSS.",
        "recommendation": "Define a Content-Security-Policy appropriate for the application.",
    },
    "strict-transport-security": {
        "severity": "Medium",
        "description": "Tells browsers to use HTTPS for future connections.",
        "recommendation": "Configure HSTS on HTTPS sites after checking deployment requirements.",
    },
    "x-content-type-options": {
        "severity": "Low",
        "description": "Helps prevent MIME-type sniffing.",
        "recommendation": "Set X-Content-Type-Options: nosniff.",
    },
    "x-frame-options": {
        "severity": "Low",
        "description": "Provides protection against some clickjacking scenarios.",
        "recommendation": "Set X-Frame-Options: DENY or SAMEORIGIN, or use CSP frame-ancestors.",
    },
    "referrer-policy": {
        "severity": "Low",
        "description": "Controls how much referrer information browsers send.",
        "recommendation": "Set an appropriate Referrer-Policy, such as strict-origin-when-cross-origin.",
    },
}


def validate_url(url):
    """Accept only HTTP and HTTPS URLs with a hostname."""
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.hostname:
        raise ValueError("Enter a complete URL beginning with http:// or https://")

    if parsed.username or parsed.password:
        raise ValueError("Do not include usernames or passwords in the URL.")

    return url


def add_finding(findings, category, severity, status, details, recommendation=""):
    findings.append({
        "category": category,
        "severity": severity,
        "status": status,
        "details": details,
        "recommendation": recommendation,
    })


def get_set_cookie_headers(response):
    """Retrieve individual Set-Cookie headers when supported."""
    raw_headers = getattr(response.raw, "headers", None)

    if raw_headers and hasattr(raw_headers, "getlist"):
        return raw_headers.getlist("Set-Cookie")

    value = response.headers.get("Set-Cookie")
    return [value] if value else []


def scan_url(url, timeout=10):
    validate_url(url)

    findings = []
    result = {
        "target": url,
        "scanned_at_utc": datetime.now(timezone.utc).isoformat(),
        "status_code": None,
        "final_url": None,
        "https_used": urlparse(url).scheme == "https",
        "findings": findings,
        "error": None,
    }

    try:
        response = requests.get(
            url,
            timeout=timeout,
            allow_redirects=True,
            headers={"User-Agent": "BeginnerWebSecurityScanner/1.0"},
        )
    except requests.RequestException as exc:
        result["error"] = f"Request failed: {exc}"
        return result

    result["status_code"] = response.status_code
    result["final_url"] = response.url
    result["https_used"] = urlparse(response.url).scheme == "https"

    # HTTPS and redirect checks
    if urlparse(url).scheme == "https":
        add_finding(
            findings, "HTTPS", "Info", "PASS",
            "The supplied URL uses HTTPS."
        )
    elif result["https_used"]:
        add_finding(
            findings, "HTTPS", "Info", "PASS",
            "The HTTP URL redirected to HTTPS."
        )
    else:
        add_finding(
            findings, "HTTPS", "High", "WARNING",
            "The final URL does not use HTTPS.",
            "Configure HTTPS and redirect HTTP traffic to HTTPS."
        )

    # Common security headers
    headers_lower = {key.lower(): value for key, value in response.headers.items()}

    for header, info in SECURITY_HEADERS.items():
        if header in headers_lower:
            add_finding(
                findings, header, "Info", "PASS",
                f"Header is present: {headers_lower[header]}"
            )
        else:
            severity = info["severity"]

            # HSTS is relevant when the final connection uses HTTPS.
            if header == "strict-transport-security" and not result["https_used"]:
                add_finding(
                    findings, header, "Info", "REVIEW",
                    "HSTS was not evaluated because the final URL is not HTTPS.",
                    "Enable HTTPS first, then review HSTS configuration."
                )
            else:
                add_finding(
                    findings, header, severity, "WARNING",
                    info["description"], info["recommendation"]
                )

    # Basic CORS response-header review
    allow_origin = headers_lower.get("access-control-allow-origin")
    allow_credentials = headers_lower.get("access-control-allow-credentials", "")
    allow_credentials = allow_credentials.strip().lower()

    if not allow_origin:
        add_finding(
            findings, "CORS", "Info", "REVIEW",
            "No Access-Control-Allow-Origin header was observed.",
            "Confirm whether cross-origin access is required for this application."
        )
    elif allow_origin.strip() == "*" and allow_credentials == "true":
        add_finding(
            findings, "CORS", "High", "WARNING",
            "Wildcard origin and credentials=true were both observed.",
            "Review the CORS policy. Browsers reject this combination for credentialed CORS, but it may indicate a configuration error."
        )
    elif allow_origin.strip() == "*":
        add_finding(
            findings, "CORS", "Low", "REVIEW",
            "Wildcard origin is configured.",
            "Use an explicit origin allowlist if cross-origin access should be restricted."
        )
    else:
        add_finding(
            findings, "CORS", "Info", "REVIEW",
            f"Access-Control-Allow-Origin is set to: {allow_origin}",
            "Verify that the allowed origin is intentional. This basic check does not validate the full CORS policy."
        )

    # Cookie attribute checks
    cookies = get_set_cookie_headers(response)

    if not cookies:
        add_finding(
            findings, "Cookies", "Info", "REVIEW",
            "No Set-Cookie header was observed in this response."
        )
    else:
        for index, cookie in enumerate(cookies, start=1):
            parts = [part.strip() for part in cookie.split(";")]
            attributes = {
                part.split("=", 1)[0].strip().lower()
                for part in parts[1:]
                if part
            }
            cookie_name = parts[0].split("=", 1)[0] if parts else f"Cookie {index}"

            for attribute, recommendation in [
                ("secure", "Set Secure on cookies that should only travel over HTTPS."),
                ("httponly", "Set HttpOnly on cookies that do not need JavaScript access."),
                ("samesite", "Set an appropriate SameSite attribute based on application needs."),
            ]:
                if attribute in attributes:
                    add_finding(
                        findings, f"Cookie: {cookie_name}", "Info", "PASS",
                        f"{attribute} attribute is present."
                    )
                else:
                    add_finding(
                        findings, f"Cookie: {cookie_name}", "Low", "WARNING",
                        f"{attribute} attribute was not observed.",
                        recommendation
                    )

    response.close()
    return result


def print_report(report):
    print("\n" + "=" * 64)
    print("       AUTOMATED WEB SECURITY SCANNER")
    print("=" * 64)
    print(f"Target:      {report['target']}")
    print(f"Final URL:   {report.get('final_url') or 'Not available'}")
    print(f"HTTP Status: {report.get('status_code') or 'Not available'}")
    print(f"Scanned UTC: {report['scanned_at_utc']}")

    if report["error"]:
        print(f"\nERROR: {report['error']}")
        return

    print("\nFINDINGS")
    print("-" * 64)

    for item in report["findings"]:
        print(f"[{item['status']}] {item['category']} | {item['severity']}")
        print(f"  Details: {item['details']}")
        if item["recommendation"]:
            print(f"  Advice:  {item['recommendation']}")

    counts = {}
    for item in report["findings"]:
        counts[item["status"]] = counts.get(item["status"], 0) + 1

    print("\nSUMMARY")
    for status, count in sorted(counts.items()):
        print(f"{status}: {count}")

    print("\nNote: Findings are configuration indicators, not proof of exploitability.")


def main():
    parser = argparse.ArgumentParser(
        description="Check basic HTTP security configuration on an authorized target."
    )
    parser.add_argument(
        "url",
        help="Authorized URL, e.g. https://example.com"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="Request timeout in seconds (default: 10)"
    )
    parser.add_argument(
        "--output",
        default="reports/scan_report.json",
        help="Path for the JSON report"
    )
    args = parser.parse_args()

    if args.timeout < 1 or args.timeout > 60:
        parser.error("--timeout must be between 1 and 60 seconds")

    try:
        validate_url(args.url)
        report = scan_url(args.url, timeout=args.timeout)
    except ValueError as exc:
        parser.error(str(exc))

    print_report(report)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"\nJSON report saved to: {output_path}")

    if report["error"]:
        sys.exit(1)


if __name__ == "__main__":
    main()