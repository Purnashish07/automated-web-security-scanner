# SecureScan — Automated Web Security Scanner

![SecureScan Project Banner](demo-video/SecureScan_Thumbnail.png)

A lightweight, production-ready Python web security configuration scanner built with **Flask**, **Requests**, **Tailwind CSS**, and **Vanilla JavaScript**.

[![Live Demo](https://img.shields.io/badge/Live_Demo-Vercel-00ffcc?style=for-the-badge&logo=vercel)]([[https://automated-web-security-scanner-abxd.vercel.app/](https://automated-web-security-scanner-v1ab.vercel.app/)](https://automated-web-security-scanner-v1ab.vercel.app/))
[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

---

## 🌐 Live Application

- **Live URL**: [https://automated-web-security-scanner-abxd.vercel.app/](https://automated-web-security-scanner-abxd.vercel.app/)
- **GitHub Repository**: [https://github.com/Purnashish07/automated-web-security-scanner](https://github.com/Purnashish07/automated-web-security-scanner)

---

## 🎥 Project Demonstration & Video Assets

A complete 1080p Full HD video presentation and AI-narrated walkthrough is included in the [`demo-video/`](demo-video/) directory:

- 🎬 **Video Walkthrough**: [`demo-video/SecureScan_Demo_1080p.mp4`](demo-video/SecureScan_Demo_1080p.mp4) (1080p Full HD, 3:21 duration, synchronized subtitles and ambient score)
- 🎙️ **AI Voiceover Audio**: [`demo-video/SecureScan_Voiceover.mp3`](demo-video/SecureScan_Voiceover.mp3) (Clear American male voiceover using `en-US-ChristopherNeural`)
- 📜 **Official Script**: [`demo-video/SecureScan_Demo_Script.txt`](demo-video/SecureScan_Demo_Script.txt) (Full timed narration script with visual cues)
- 🖼️ **Project Thumbnail**: [`demo-video/SecureScan_Thumbnail.png`](demo-video/SecureScan_Thumbnail.png) (High-resolution cybersecurity SaaS banner)

---

## 📌 Project Overview

**SecureScan** helps developers, security students, and system administrators audit critical website security configurations through an intuitive, dark-mode cybersecurity dashboard. It passively inspects HTTPS usage, common browser security headers, CORS response headers, and cookie protection attributes.

> **Ethical Note**: This project performs **passive configuration analysis** and does not conduct invasive penetration testing or exploit vulnerabilities. Always obtain explicit permission before scanning target websites.

---

## 🛡️ Key Features

- **HTTPS & SSL/TLS Verification**: Confirms encrypted transport protocols and tracks redirect chains.
- **Security Header Auditing**:
  - `Content-Security-Policy` (CSP) — Mitigates Cross-Site Scripting (XSS) and injection attacks.
  - `Strict-Transport-Security` (HSTS) — Enforces HTTPS connections and prevents downgrade attacks.
  - `X-Content-Type-Options` — Blocks MIME-type sniffing.
  - `X-Frame-Options` — Protects against clickjacking.
  - `Referrer-Policy` — Governs referrer metadata leakage.
- **Cookie Security Checks**: Inspects `Secure`, `HttpOnly`, and `SameSite` attributes across all `Set-Cookie` directives.
- **CORS Configuration Review**: Identifies overly permissive wildcard origins (`*`) paired with credentials.
- **SSRF Defense**: Built-in pre-flight DNS validation rejects loopback (`127.0.0.1`), private subnets (`10.0.0.0/8`, `192.168.0.0/16`), and link-local targets.
- **Rate Limiting**: In-memory token bucket protects the API against abusive traffic.
- **One-Click JSON Export**: Download standardized audit data ready for reporting and CI/CD pipelines.

---

## 🏗️ Technology Stack

- **Backend**: Python 3.12, Flask, Requests
- **Frontend**: HTML5, Tailwind CSS, Vanilla JavaScript
- **Testing**: Pytest, Requests-Mock
- **Deployment**: Vercel Serverless Functions
- **Multimedia Production**: FFmpeg, Pillow, Edge-TTS, Selenium

---

## 📂 Project Structure

```text
automated-web-security-scanner/
├── app.py                     # Flask application (Vercel entrypoint)
├── security_scanner.py        # Core scanning and validation engine
├── requirements.txt           # Production dependencies
├── dev-requirements.txt       # Testing dependencies (pytest, requests-mock)
├── vercel.json                # Vercel deployment configuration
├── .python-version            # Python version pin (3.12)
├── .gitignore
├── .vercelignore
├── README.md
├── assemble_video.py          # Video production pipeline script
├── capture_frames.py          # Automated UI screenshot capture tool
├── generate_voiceover.py      # AI voiceover generation script
├── demo-video/                # Video demonstration deliverables
│   ├── SecureScan_Demo_1080p.mp4
│   ├── SecureScan_Thumbnail.png
│   ├── SecureScan_Voiceover.mp3
│   └── SecureScan_Demo_Script.txt
├── templates/
│   └── index.html             # Dashboard UI (Tailwind CSS)
├── public/
│   └── static/
│       ├── style.css          # Theme overrides & severity badge styles
│       └── app.js             # Async client fetch, render, and export logic
└── tests/
    ├── conftest.py            # Pytest test client fixtures
    ├── test_validation.py     # URL validation unit tests
    ├── test_ip_rejection.py   # SSRF / private IP rejection tests
    └── test_api.py            # Flask REST API endpoint tests
```

---

## 🚀 Installation & Local Development

### 1. Clone the Repository
```bash
git clone https://github.com/Purnashish07/automated-web-security-scanner.git
cd automated-web-security-scanner
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt -r dev-requirements.txt
```

### 4. Run the Development Server
```bash
python app.py
```
Visit **`http://127.0.0.1:5000`** in your browser.

---

## 🧪 Running Automated Tests

Run the full pytest suite (17 comprehensive tests for validation, SSRF guards, rate limits, and scan mocks):

```bash
python -m pytest -v
```

---

## ☁️ Deploying to Vercel

```bash
# Install Vercel CLI (if not installed)
npm i -g vercel

# Deploy to production
vercel --prod
```

---

## 📊 Understanding Results

- **PASS**: The tested security indicator is properly configured.
- **WARNING**: A recommended security header or attribute is missing or misconfigured.
- **REVIEW**: Contextual check (e.g. CORS origin configuration) requiring manual confirmation.

---

## 👤 Author

**Purnashish Atroliya**  
*Madhav Institute of Technology and Science (MITS), Gwalior*  
*Developed for the IBM SkillsBuild Cyber Security BootCamp 2026*  
GitHub: [@Purnashish07](https://github.com/Purnashish07)
