# Automated Web Security Scanner

A lightweight Python-based web security configuration scanner built with Flask, Requests, HTML, CSS, and JavaScript.

## Project Overview

Automated Web Security Scanner helps users review basic website security configurations through a local web dashboard. It checks HTTPS usage, common HTTP security headers, basic CORS response headers, and cookie security attributes.

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
- Flask backend with HTML, CSS, and JavaScript frontend

## Technology Stack

- Python 3
- Flask
- Requests
- HTML5
- CSS3
- JavaScript
- JSON

## Project Structure

```text
automated-web-security-scanner/
â”œâ”€â”€ app.py
â”œâ”€â”€ app_cli_backup.py
â”œâ”€â”€ security_scanner.py
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ README.md
â”œâ”€â”€ templates/
â”‚   â””â”€â”€ index.html
â””â”€â”€ static/
    â”œâ”€â”€ style.css
    â””â”€â”€ app.js
```

## Installation

1. Install Python 3.
2. Open PowerShell in the project directory.
3. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

4. Activate it:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Run the Application

Start the local Flask server:

```powershell
python app.py
```

Open this address in your browser:

http://127.0.0.1:5000

Enter a website URL you own or have explicit permission to test, then select Run Security Scan. Use Export JSON to save the results.

## Understanding Results

- PASS: The tested configuration indicator was observed.
- WARNING: A recommended security header or configuration indicator was missing or needs attention.
- REVIEW: The result needs contextual review and is not necessarily a vulnerability.

A scan checks only the indicators implemented in this project. It is not a complete penetration test or guarantee of security.

## Dataset

This project does not require a training dataset. It performs live HTTP configuration checks against a user-supplied, authorized target. For demonstration, use a website you own or a deliberately configured local test environment.

## Ethical Use and Limitations

- Scan only websites you own or have explicit permission to test.
- Run the application locally for educational demonstrations.
- Findings may depend on redirects, application behavior, and server configuration.
- A missing header does not by itself prove a vulnerability.
- Do not use this tool as a substitute for a professional security assessment.

## Future Improvements

- Add automated unit tests and controlled test fixtures.
- Improve redirect and DNS/IP validation safeguards.
- Add HTML or PDF report generation.
- Add scan history and severity-based summaries.

## Author

Purnashish Atroliya  
Madhav Institute of Technology and Science, Gwalior

## Project Purpose

Developed as an educational project for the IBM SkillsBuild Cyber Security BootCamp 2026.
