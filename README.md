# API Security Posture Assessment Through Automated Header Analysis

A Python- and Flask-based web application that assesses the security
posture of publicly accessible APIs through HTTPS verification and HTTP
response-header analysis. It calculates a security score, classifies
risk, and presents Explainable AI (XAI) insights with priority-based
recommendations.

------------------------------------------------------------------------

## Table of Contents

-   [Overview](#overview)
-   [Features](#features)
-   [Technology Stack](#technology-stack)
-   [Project Structure](#project-structure)
-   [Installation](#installation)
-   [Usage](#usage)
-   [How It Works](#how-it-works)
-   [Security Headers Analyzed](#security-headers-analyzed)
-   [Security Score and Risk
    Classification](#security-score-and-risk-classification)
-   [OWASP Mapping](#owasp-mapping)
-   [PDF Report Contents](#pdf-report-contents)
-   [Example API Endpoints](#example-api-endpoints)
-   [Limitations](#limitations)
-   [Future Enhancements](#future-enhancements)
-   [Sample Explainable AI Output](#sample-explainable-ai-output)
-   [Contributors](#contributors)
-   [License](#license)
-   [References](#references)

------------------------------------------------------------------------

## Overview

The **API Security Posture Assessment Through Automated Header
Analysis** project provides an automated way to review selected API
security configurations.

The application accepts an API endpoint, checks whether HTTPS is
enabled, and analyzes five recommended HTTP security headers in the
response. Based on these checks, it calculates a security score, assigns
a risk level, and displays findings through an interactive dashboard.

It also provides plain-language XAI insights and priority-based
remediation recommendations. Users can generate a PDF report containing
the assessment results.

## Features

-   **HTTPS Enforcement Verification** --- Checks whether the API
    endpoint uses HTTPS.
-   **HTTP Security Header Analysis** --- Evaluates five important
    response headers.
-   **Security Score Calculation** --- Produces a score from 0 to 100
    based on the configured checks.
-   **Risk Classification** --- Categorizes the result as **HIGH**,
    **MEDIUM**, or **LOW**.
-   **Explainable AI (XAI) Insights** --- Presents plain-language
    explanations of assessment findings.
-   **Priority-Based Recommendations** --- Provides remediation
    suggestions with priority levels.
-   **Interactive Dashboard** --- Displays assessment results using
    visual indicators and charts.
-   **PDF Report Generation** --- Creates a downloadable report
    containing the assessment details.

## Technology Stack

  Component                 Technology
  ------------------------- --------------------
  Programming language      Python
  Backend framework         Flask
  Frontend                  HTML, CSS
  HTTP client               Requests
  URL validation            Validators
  PDF generation            ReportLab
  Development environment   Visual Studio Code

## Project Structure

``` text
API_Security_Posture_Assessment/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html         # Web interface
├── static/
│   └── style.css          # CSS styling
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Installation

### Prerequisites

-   Python 3.8 or higher
-   pip (Python package installer)
-   Git

### 1. Clone the repository

Replace `<your-username>` with your GitHub username.

``` bash
git clone https://github.com/<your-username>/api-security-posture-assessment.git
cd api-security-posture-assessment
```

### 2. Create a virtual environment

**Windows**

``` bash
python -m venv venv
venv\Scripts\activate
```

**Linux / macOS**

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Start the application

``` bash
python app.py
```

### 5. Open the application

Open the following address in your browser:

``` text
http://127.0.0.1:5000/
```

> **Note:** These instructions assume the repository contains the
> project structure and files listed above. Confirm that the filenames
> and commands match your project before publishing.

## Usage

1.  **Enter an API URL**\
    Provide the API endpoint you want to assess. For example:
    `https://api.github.com`.

2.  **Run the scan**\
    Select **Run Scan** to begin the security assessment.

3.  **Review the results**\
    The dashboard displays:

    -   Security score (0--100)
    -   Risk level (HIGH / MEDIUM / LOW)
    -   Security-header status
    -   Explainable AI insights
    -   Priority-based recommendations

4.  **Download the report**\
    Select **Download Complete Security Report** to generate the PDF
    assessment report.

## How It Works

The application follows this assessment process:

1.  Accepts an API endpoint from the user.
2.  Validates the submitted URL.
3.  Sends an HTTP GET request to the endpoint.
4.  Retrieves the response information, including the status code,
    response time, and HTTP headers.
5.  Checks HTTPS usage and the five selected security headers.
6.  Calculates the security score and assigns a risk classification.
7.  Displays findings, explanations, and recommendations on the
    dashboard.
8.  Generates a downloadable PDF report.

## Security Headers Analyzed

  -----------------------------------------------------------------------------
  HTTP Header                   Purpose                 Potential Risk if
                                                        Missing
  ----------------------------- ----------------------- -----------------------
  `X-Frame-Options`             Helps protect against   UI redress attacks
                                clickjacking            

  `Content-Security-Policy`     Helps restrict          Increased exposure to
                                permitted content       cross-site scripting
                                sources                 (XSS) and content
                                                        injection

  `Strict-Transport-Security`   Tells browsers to use   SSL-stripping and
                                HTTPS for future        downgrade risks
                                connections             

  `X-Content-Type-Options`      Helps prevent MIME-type MIME-sniffing-related
                                sniffing                content risks

  `Referrer-Policy`             Controls referrer       Unintended information
                                information shared with disclosure
                                other destinations      
  -----------------------------------------------------------------------------

## Security Score and Risk Classification

### Score calculation

The README's documented scoring model assigns points as follows:

  Assessment component             Points Condition
  ----------------------------- --------- --------------------------
  Base score                           20 Always applied
  HTTPS                               +20 If enabled
  `X-Frame-Options`                   +12 If present
  `Content-Security-Policy`           +12 If present
  `Strict-Transport-Security`         +12 If present
  `X-Content-Type-Options`            +12 If present
  `Referrer-Policy`                   +12 If present
  **Maximum score**               **100** **All checks satisfied**

### Risk classification

  Score range   Risk level   Indicated action
  ------------- ------------ -------------------------------------------
  90--100       **LOW**      Minor adjustments may be needed
  70--89        **MEDIUM**   Further security hardening is recommended
  0--69         **HIGH**     Prioritized remediation is recommended

## OWASP Mapping

The project maps the assessed configuration checks to **OWASP API
Security Top 10 -- API8:2023 (Security Misconfiguration)**.

  Security check                OWASP category   Severity stated in the project
  ----------------------------- ---------------- --------------------------------
  HTTPS enabled                 API8:2023        CRITICAL
  `X-Frame-Options`             API8:2023        MEDIUM
  `Content-Security-Policy`     API8:2023        HIGH
  `Strict-Transport-Security`   API8:2023        HIGH
  `X-Content-Type-Options`      API8:2023        MEDIUM
  `Referrer-Policy`             API8:2023        MEDIUM

This mapping is used to contextualize the configuration findings; it
should not be interpreted as a complete OWASP API Security Top 10
assessment.

## PDF Report Contents

The generated PDF report is documented as containing:

1.  **Cover page** --- Report title, logo, and scan date.
2.  **Executive summary** --- Security score, risk level, and key
    findings.
3.  **Security header analysis** --- Detailed status of the analyzed
    headers.
4.  **OWASP mapping** --- Mapping to API8:2023.
5.  **Explainable AI insights** --- Plain-language explanations of
    findings.
6.  **Security recommendations** --- Priority-based remediation actions.
7.  **Improvement analysis** --- Current score compared with a potential
    score.
8.  **Final verdict** --- Summary recommendation.

## Example API Endpoints

The following public endpoints are listed as examples to assess:

-   GitHub API: `https://api.github.com`
-   Example API: `https://api.example.com`
-   JSONPlaceholder: `https://jsonplaceholder.typicode.com`

Only scan endpoints you own or are authorized to assess. The application
is intended for publicly accessible endpoints and the checks described
in this README.

## Limitations

The current project scope has the following limitations:

-   Focuses on HTTPS and HTTP security-header configuration.
-   Does not detect SQL injection or test XSS payloads.
-   Does not support authenticated endpoints.
-   Supports scanning one URL at a time.
-   Uses the PDF report format currently implemented in the project.
-   Does not include CI/CD integration.

The assessment is a configuration review and should not be treated as a
replacement for penetration testing or a comprehensive API security
audit.

## Future Enhancements

Potential future improvements identified for the project include:

-   **Additional vulnerability checks** --- Extend assessment coverage
    to other API security risks.
-   **Authentication support** --- Add testing for OAuth 2.0, JWT, and
    API keys.
-   **AI enhancements** --- Explore machine-learning-based anomaly
    detection.
-   **Monitoring** --- Add scheduled scans and real-time alerts.
-   **Integrations** --- Support CI/CD, Slack, and SIEM integrations.
-   **Reporting** --- Add customizable report templates and trend
    analysis.
-   **Multi-API scanning** --- Support simultaneous scans and
    portfolio-level views.

## Sample Explainable AI Output

The following is an example output documented for the project:

``` text
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
```

## Contributors

**Sarmitha G** --- Developer\
B.Sc. Computer Science with Cyber Security\
PSGR Krishnammal College for Women

## License

This project is distributed under the MIT License. See the `LICENSE`
file for the full license text.

> If you intend to publish the project under the MIT License, include a
> `LICENSE` file in the repository and confirm that the license is
> appropriate for your project.

## References

-   [OWASP API Security Top
    10](https://owasp.org/www-project-api-security/)
-   [MDN Web Docs --- HTTP
    Headers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers)
-   [Flask Documentation](https://flask.palletsprojects.com/)
-   [ReportLab Documentation](https://www.reportlab.com/)

------------------------------------------------------------------------

**API Security Posture Assessment Through Automated Header Analysis**\
*Automated API configuration assessment using Python and Flask.*
