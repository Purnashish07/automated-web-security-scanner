# Automated Web Security Scanner

A lightweight Python-based web security configuration scanner built with Flask, Requests, HTML, CSS, and JavaScript.

## Project Overview

Automated Web Security Scanner helps users review basic website security configurations through a web dashboard. It checks HTTPS usage, common HTTP security headers, basic CORS response headers, and cookie security attributes.

This project is intended for educational purposes and authorized security testing. Findings are configuration indicators, not confirmation of exploitable vulnerabilities.

## Features

- HTTPS usage check
- Security header checks:
  - Content-Security-Policy (CSP)
  - Strict-Transport-Security (HSTS)
  - X-Content-Type-Options
  - X-Frame-Options
  - Referrer-Policy
- Cookie attribute review: Secure, HttpOnly, and SameSite
- Basic CORS configuration review
- Dashboard showing PASS, WARNING, and REVIEW findings
- JSON report export
- SSRF protection (private IP rejection)
- In-memory rate limiting
- Flask backend with Tailwind CSS frontend

## Technology Stack

- Python 3.12
- Flask
- Requests
- HTML5 / Tailwind CSS
- JavaScript
- Vercel (deployment)

## Project Structure

```text
automated-web-security-scanner/
├── app.py                  # Flask application (Vercel entrypoint)
├── security_scanner.py     # Scanning engine
├── requirements.txt        # Production dependencies
├── dev-requirements.txt    # Test dependencies (pytest, requests-mock)
├── vercel.json             # Vercel deployment config
├── .python-version         # Python version pin (3.12)
├── .gitignore
├── .vercelignore
├── README.md
├── templates/
│   └── index.html          # Jinja2 template (Tailwind CSS)
├── public/
│   └── static/
│       ├── style.css       # Custom CSS overrides
│       └── app.js          # Frontend client script
└── tests/
    ├── conftest.py         # Shared test fixtures
    ├── test_validation.py  # URL validation tests
    ├── test_ip_rejection.py# SSRF / private-IP tests
    └── test_api.py         # Flask route tests
```

## Installation

1. Install Python 3.12+.
2. Open a terminal in the project directory.
3. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

4. Activate it:

   ```bash
   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1

   # macOS / Linux
   source .venv/bin/activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Run the Application

Start the local Flask server:

```bash
python app.py
```

Open <http://127.0.0.1:5000> in your browser.

Enter a website URL you own or have explicit permission to test, then click **Run scan**. Use **Export JSON** to save the results.

## Running Tests

```bash
pip install -r dev-requirements.txt
python -m pytest -v
```

## Deploy to Vercel

1. Install the [Vercel CLI](https://vercel.com/docs/cli):

   ```bash
   npm i -g vercel
   ```

2. Log in:

   ```bash
   vercel login
   ```

3. Deploy:

   ```bash
   vercel --prod
   ```

Vercel will auto-detect the Python/Flask build from `vercel.json`.

## Understanding Results

- **PASS**: The tested configuration indicator was observed.
- **WARNING**: A recommended security header or configuration indicator was missing or needs attention.
- **REVIEW**: The result needs contextual review and is not necessarily a vulnerability.

A scan checks only the indicators implemented in this project. It is not a complete penetration test or guarantee of security.

## Ethical Use and Limitations

- Scan only websites you own or have explicit permission to test.
- Findings may depend on redirects, application behavior, and server configuration.
- A missing header does not by itself prove a vulnerability.
- Do not use this tool as a substitute for a professional security assessment.

## Author

Purnashish Atroliya
Madhav Institute of Technology and Science, Gwalior

## Project Purpose

Developed as an educational project for the IBM SkillsBuild Cyber Security BootCamp 2026.
