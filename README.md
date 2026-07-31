# API Security Posture Assessment Through Automated Header Analysis

A comprehensive API security assessment tool that automates the detection of security misconfigurations through HTTP header analysis. Built with Python and Flask, this tool evaluates critical security headers, generates security scores, and provides Explainable AI (XAI) insights for actionable remediation recommendations.

---

##  Features

✅ HTTPS Enforcement Verification - Checks if the API enforces secure HTTPS connections

✅ Security Header Analysis - Evaluates 5 critical HTTP security headers:
   - X-Frame-Options
   - Content-Security-Policy (CSP)
   - Strict-Transport-Security (HSTS)
   - X-Content-Type-Options
   - Referrer-Policy

✅ Security Score Calculation - Generates a score out of 100 based on header compliance

✅ Risk Classification - Classifies risk as HIGH, MEDIUM, or LOW

✅ Explainable AI Insights - Provides plain-language explanations of findings

✅ Priority-Based Recommendations - Actionable remediation steps with priority levels

✅ Interactive Dashboard - Visual analytics with charts and indicators

✅ PDF Report Generation - Professional compliance-ready audit reports

---

##  Tech Stack

Backend: Python , Flask
Frontend: HTML, CSS
PDF Generation: ReportLab
HTTP Client: Requests
URL Validation: Validators
Development: VS Code

---

##  Project Structure

API_Security_Posture_Assessment/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Web interface
├── static/
│   └── style.css         # CSS styling
├── requirements.txt      # Dependencies
└── README.md             # Project documentation

---

##  Installation

Prerequisites:
- Python 3.8 or higher
- pip (Python package installer)

Step 1: Clone the Repository

git clone https://github.com/your-username/api-security-posture-assessment.git
cd api-security-posture-assessment

Step 2: Create Virtual Environment

Windows:
python -m venv venv
venv\Scripts\activate

Linux/Mac:
python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies

pip install -r requirements.txt

Step 4: Run the Application

python app.py

Step 5: Open Browser
Navigate to: http://127.0.0.1:5000/

---

##  Requirements

Flask==2.3.3
requests==2.31.0
validators==0.22.0
reportlab==4.0.4

---

##  Usage Guide

1. Enter API URL
Enter the API endpoint you want to assess (e.g., https://api.github.com)

2. Run Scan
Click the "Run Scan" button to start the security assessment

3. View Results
The dashboard displays:
- Security Score (0-100)
- Risk Level (HIGH/MEDIUM/LOW)
- Header Coverage Status
- Explainable AI Insights
- Priority Recommendations

4. Download Report
Click "Download Complete Security Report" to get a professional PDF document

---

##  How It Works

Security Score Calculation:

Component          Points    Condition
Base Score         20        Always applied
HTTPS              +20       If enabled
X-Frame-Options    +12       If present
Content-Security-Policy +12  If present
Strict-Transport-Security +12 If present
X-Content-Type-Options +12   If present
Referrer-Policy    +12       If present
Maximum            100       All controls enabled

Risk Classification:

Score Range    Risk Level    Action Required
90-100         LOW           Minor adjustments needed
70-89          MEDIUM        Moderate hardening required
0-69           HIGH          Immediate remediation required

---

##  Security Headers Analyzed

Header                    Purpose                          Risk if Missing
X-Frame-Options           Prevents Clickjacking attacks    UI redress attacks
Content-Security-Policy   Prevents XSS and data injection  Cross-Site Scripting (XSS)
Strict-Transport-Security Forces HTTPS connections          SSL stripping attacks
X-Content-Type-Options    Prevents MIME sniffing           Content-type attacks
Referrer-Policy           Controls referrer information    Information leakage

---

##  Sample PDF Report Sections

1. Cover Page - Title, logo, scan date
2. Executive Summary - Score, risk level, key findings
3. Security Headers Analysis - Detailed header status
4. OWASP Mapping - Compliance with API8:2023
5. Explainable AI Insights - Plain-language explanations
6. Security Recommendations - Priority-based action plan
7. Improvement Analysis - Current vs. potential score
8. Final Verdict - Clear recommendation

---

##  OWASP Compliance

Security Check              OWASP Category    Severity
HTTPS Enabled               API8:2023         CRITICAL
X-Frame-Options             API8:2023         MEDIUM
Content-Security-Policy     API8:2023         HIGH
Strict-Transport-Security   API8:2023         HIGH
X-Content-Type-Options      API8:2023         MEDIUM
Referrer-Policy             API8:2023         MEDIUM

---

##  Example API Endpoints to Test

GitHub API: https://api.github.com
Example API: https://api.example.com
JSONPlaceholder: https://jsonplaceholder.typicode.com

---

##  Limitations

- Focuses only on HTTP security headers and HTTPS
- Does not detect SQL Injection, XSS payloads
- No support for authenticated endpoints
- Single URL scanning (not multi-API)
- Basic PDF reports (no custom templates)
- No CI/CD integration

---

##  Future Enhancements

Vulnerabilities: Add SQL Injection, XSS, CSRF detection
Authentication: OAuth 2.0, JWT, API key testing
AI: Machine learning for anomaly detection
Monitoring: Scheduled scans, real-time alerts
Integration: CI/CD, Slack, SIEM integration
Reporting: Custom templates, trend analysis
Multi-API: Simultaneous scanning, portfolio view

---

##  Sample Explainable AI Output

INFO:  Initiating security scan for https://api.example.com
INFO:  Endpoint responded in 731.44 ms

OK:    HTTPS: Encrypted transport verified
WARN:  X-Frame-Options: Missing — Clickjacking risk
WARN:  Content-Security-Policy: Absent — XSS risk elevated
OK:    HSTS: Enforced — browsers will always use HTTPS
WARN:  X-Content-Type-Options: Missing — MIME sniffing risk
WARN:  Referrer-Policy: Absent — information leakage

INFO:  Header compliance: 1/5 recommended headers configured
RESULT: Final score: 52/100 — Risk classification: HIGH

---

##  Contributors

Sarmitha G - Developer
Bsc computer science with cyber security 
PSGR krishnammal college for womens.

---

## 📄 License

MIT License

Copyright (c) 2026 Sarmitha G

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## References

OWASP API Security Top 10: https://owasp.org/www-project-api-security/
Mozilla Developer Network - Security Headers: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers
Flask Documentation: https://flask.palletsprojects.com/
ReportLab Documentation: https://www.reportlab.com/

---

## Quick Links

Project Repository: https://github.com/your-username/api-security-posture-assessment
OWASP API Top 10: https://owasp.org/www-project-api-security/
Security Headers: https://securityheaders.com/

---

Made with ❤️ for API Security

© 2026 API Security Posture Assessment Through Automated Header Analysis
