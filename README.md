# API Security Posture Assessment Through Automated Header Analysis

## Overview
API Security Posture Assessment Through Automated Header Analysis is a lightweight web-based application developed using Python and Flask. The system automatically evaluates the security posture of publicly accessible APIs by validating API URLs, verifying HTTPS implementation, analyzing essential HTTP security headers, calculating a security score, classifying risk levels, and generating security recommendations with a downloadable PDF report.

## Features
- API URL Validation
- HTTPS Verification
- HTTP Status Code and Response Time Analysis
- Automated HTTP Security Header Analysis
- Security Score Calculation
- Risk Level Classification
- OWASP API8:2023 Security Misconfiguration Mapping
- Explainable AI (XAI) Summary
- Security Recommendations
- Security Improvement Analysis
- PDF Report Generation

## Technologies Used
- Python
- Flask
- HTML
- CSS
- Requests
- Validators
- ReportLab

## Project Structure
```
API_Security_Posture_Assessment/
│── static/
│── templates/
│── app.py
│── requirements.txt
│── README.md
└── .gitignore
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
```

2. Navigate to the project directory:
```bash
cd API_Security_Posture_Assessment
```

3. Install the required dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and visit:
```
http://127.0.0.1:5000
```

## Workflow
1. Enter API URL
2. Validate URL
3. Process API Request
4. Verify HTTPS
5. Analyze HTTP Security Headers
6. Calculate Security Score
7. Classify Risk Level
8. Map Findings to OWASP API8:2023
9. Generate Explainable AI (XAI) Summary
10. Generate Security Recommendations
11. Generate PDF Report

## Output
The application provides:
- HTTPS Status
- HTTP Status Code
- Response Time
- HTTP Security Header Analysis
- Security Score
- Risk Classification
- OWASP API Mapping
- Explainable AI (XAI) Summary
- Security Recommendations
- Downloadable PDF Security Report

## Author
Sarmitha G  
B.Sc. Computer Science with Cyber Security  
PSGR Krishnammal College for Women
