from flask import Flask, render_template, request, send_file
import requests
import validators
import time
import io
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

app = Flask(__name__)
latest_scan = {}

REPORT_TITLE = "API SECURITY POSTURE ASSESSMENT THROUGH AUTOMATED HEADER ANALYSIS"
BRAND_SHORT  = "API SECURITY POSTURE"

def create_pdf_report():
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
        title=REPORT_TITLE
    )

    # ── Styles ──────────────────────────────────────────────────────────
    base = getSampleStyleSheet()
    S = lambda name, **kw: ParagraphStyle(name, parent=base['Normal'], **kw)

    cover_title = S('CoverTitle',
                    fontName='Helvetica-Bold', fontSize=18,
                    textColor=colors.HexColor('#FFFFFF'),
                    alignment=TA_CENTER, spaceAfter=8, leading=22)
    cover_sub = S('CoverSub',
                  fontName='Helvetica', fontSize=12,
                  textColor=colors.HexColor('#B0C4DE'),
                  alignment=TA_CENTER, spaceAfter=4)
    cover_meta = S('CoverMeta',
                   fontName='Helvetica', fontSize=10,
                   textColor=colors.HexColor('#8A9BC4'),
                   alignment=TA_CENTER)
    section_heading = S('SectionHeading',
                        fontName='Helvetica-Bold', fontSize=13,
                        textColor=colors.HexColor('#1A2D5A'),
                        spaceBefore=18, spaceAfter=6,
                        borderPadding=(0, 0, 4, 0))
    body = S('Body',
             fontName='Helvetica', fontSize=10,
             textColor=colors.HexColor('#2C3E50'),
             spaceAfter=5, leading=15)
    label_style = S('LabelStyle',
                    fontName='Helvetica-Bold', fontSize=9,
                    textColor=colors.HexColor('#556080'))
    mono = S('Mono',
             fontName='Courier', fontSize=10,
             textColor=colors.HexColor('#1A2D5A'))

    story = []

    DK_BLUE   = colors.HexColor('#0D1B3E')
    MID_BLUE  = colors.HexColor('#1A2D5A')
    ACCENT    = colors.HexColor('#22D3EE')
    OK        = colors.HexColor('#2DD4A7')
    WARN      = colors.HexColor('#F5A623')
    CRIT      = colors.HexColor('#F5455C')
    LIGHT_BG  = colors.HexColor('#F4F7FC')
    BORDER    = colors.HexColor('#D0D9EC')

    scan = latest_scan

    # ── Cover block ─────────────────────────────────────────────────────
    cover_data = [
        [Paragraph('🛡 API Security Console', cover_title)],
        [Paragraph(REPORT_TITLE, cover_sub)],
        [Paragraph('Security Assessment Report --- v1.0', cover_sub)],
        [Paragraph(f"Scan Date: {scan.get('Scan Time', 'N/A')}", cover_meta)],
    ]

    cover_table = Table(cover_data, colWidths=[17*cm])
    cover_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DK_BLUE),
        ('TOPPADDING', (0,0), (-1, 0), 28),
        ('BOTTOMPADDING',(0,-1),(-1,-1), 28),
        ('LEFTPADDING', (0,0), (-1,-1), 20),
        ('RIGHTPADDING',(0,0), (-1,-1), 20),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [DK_BLUE]),
    ]))
    story.append(cover_table)
    story.append(Spacer(1, 18))

    # ── Score summary row ───────────────────────────────────────────────
    score_val = scan.get('Security Score', 'N/A')
    risk_val  = scan.get('Risk Level', 'N/A')
    https_val = scan.get('HTTPS Enabled', 'N/A')
    rt_val    = scan.get('Response Time', 'N/A')
    target    = scan.get('API URL', 'N/A')
    code_val  = scan.get('Status Code', 'N/A')

    risk_color = {'HIGH': CRIT, 'MEDIUM': WARN, 'LOW': OK}.get(risk_val, MID_BLUE)

    summary_data = [
        [
            Paragraph('SECURITY SCORE', label_style),
            Paragraph('RISK LEVEL', label_style),
            Paragraph('HTTPS', label_style),
            Paragraph('RESPONSE TIME', label_style),
        ],
        [
            Paragraph(f'<font color="#1A2D5A"><b>{score_val}</b></font>',
                      S('sv', fontName='Helvetica-Bold', fontSize=18,
                        alignment=TA_CENTER, textColor=MID_BLUE)),
            Paragraph(f'<b>{risk_val}</b>',
                      S('rv', fontName='Helvetica-Bold', fontSize=14,
                        alignment=TA_CENTER, textColor=risk_color)),
            Paragraph(f'{https_val}',
                      S('hv', fontName='Helvetica', fontSize=11,
                        alignment=TA_CENTER, textColor=MID_BLUE)),
            Paragraph(f'{rt_val}',
                      S('tv', fontName='Courier', fontSize=11,
                        alignment=TA_CENTER, textColor=MID_BLUE)),
        ],
    ]

    summary_table = Table(summary_data, colWidths=[4.25*cm]*4)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG),
        ('BACKGROUND', (0,0), (-1,0), MID_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('ROUNDEDCORNERS', [4]),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph(
        f'<b>Target Endpoint:</b> <font name="Courier">{target}</font>',
        S('tgt', fontName='Helvetica', fontSize=10, textColor=MID_BLUE,
          backColor=LIGHT_BG, borderPadding=6, spaceAfter=12)))
    story.append(HRFlowable(width='100%', thickness=1, color=BORDER))
    story.append(Spacer(1, 8))

    # ── Security Headers Table ──────────────────────────────────────────
    story.append(Paragraph('1. Security Headers Analysis', section_heading))
    headers_raw = scan.get('Headers', {})
    hdr_data = [[
        Paragraph('HTTP Security Header', label_style),
        Paragraph('Status', label_style),
        Paragraph('OWASP Category', label_style),
    ]]
    for hdr, status in headers_raw.items():
        ok = str(status).startswith('Present')
        status_text = '✓ Present' if ok else '✗ Missing'
        status_color = OK if ok else CRIT
        hdr_data.append([
            Paragraph(hdr, mono),
            Paragraph(f'<b>{status_text}</b>',
                      S('ps', fontName='Helvetica-Bold', fontSize=10,
                        textColor=status_color, alignment=TA_CENTER)),
            Paragraph('API8:2023 Security Misconfiguration',
                      S('ow', fontName='Helvetica', fontSize=9,
                        textColor=colors.HexColor('#556080'))),
        ])

    hdr_table = Table(hdr_data, colWidths=[6.5*cm, 3.5*cm, 7*cm])
    hdr_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), MID_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(hdr_table)
    story.append(Spacer(1, 10))

    # ── Explainable AI ──────────────────────────────────────────────────
    story.append(Paragraph('2. Explainable AI --- Score Breakdown', section_heading))
    xai_text = scan.get('Explainable AI Text', '')
    for para in xai_text.split('\n\n'):
        para = para.strip()
        if para:
            story.append(Paragraph(para, body))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER))

    # ── AI Security Summary ─────────────────────────────────────────────
    story.append(Paragraph('3. AI Security Summary', section_heading))
    ai_text = scan.get('AI Security Summary Text', '')
    for para in ai_text.split('\n\n'):
        para = para.strip()
        if para:
            story.append(Paragraph(para, body))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER))

    # ── Priority Recommendations ────────────────────────────────────────
    story.append(Paragraph('4. Security Recommendations by Priority', section_heading))
    priority_data = [[
        Paragraph('HIGH PRIORITY',   S('ph', fontName='Helvetica-Bold', fontSize=9, textColor=CRIT)),
        Paragraph('MEDIUM PRIORITY', S('pm', fontName='Helvetica-Bold', fontSize=9, textColor=WARN)),
        Paragraph('LOW PRIORITY',    S('pl', fontName='Helvetica-Bold', fontSize=9, textColor=OK)),
    ]]
    high_items = scan.get('Priority High', [])
    med_items  = scan.get('Priority Medium', [])
    low_items  = scan.get('Priority Low', [])
    max_rows   = max(len(high_items), len(med_items), len(low_items), 1)

    def item_para(lst, idx, col_color):
        if idx < len(lst):
            return Paragraph(f'⚠ {lst[idx]}',
                             S('pi', fontName='Helvetica', fontSize=10,
                               textColor=colors.HexColor('#2C3E50')))
        return Paragraph('✓ No issues',
                         S('pc', fontName='Helvetica', fontSize=10, textColor=OK))

    for i in range(max_rows):
        priority_data.append([
            item_para(high_items, i, CRIT),
            item_para(med_items,  i, WARN),
            item_para(low_items,  i, OK),
        ])

    pri_table = Table(priority_data, colWidths=[5.67*cm]*3)
    pri_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor('#FFF0F2')),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor('#FFF8EC')),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor('#F0FEFA')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(pri_table)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER))

    # ── Improvement Analysis ────────────────────────────────────────────
    story.append(Paragraph('5. Security Improvement Analysis', section_heading))
    score_num = int(score_val.split('/')[0]) if '/' in str(score_val) else 0
    gain = 100 - score_num
    imp_data = [
        [Paragraph('Metric', label_style), Paragraph('Value', label_style)],
        [Paragraph('Current Security Score', body),   Paragraph(f'{score_num}/100', mono)],
        [Paragraph('Potential Security Score', body), Paragraph('100/100', mono)],
        [Paragraph('Possible Score Gain', body),
         Paragraph(f'+{gain} points', S('gn', fontName='Courier', fontSize=10, textColor=OK))],
        [Paragraph('Improvement Percentage', body),
         Paragraph(f'{gain}%', S('ip', fontName='Courier', fontSize=10, textColor=ACCENT))],
        [Paragraph('Estimated Risk Reduction', body),
         Paragraph(f'{risk_val} → LOW', S('rr', fontName='Courier', fontSize=10, textColor=MID_BLUE))],
        [Paragraph('Security Maturity After Fixes', body),
         Paragraph('Fair → Excellent', S('sm', fontName='Courier', fontSize=10, textColor=OK))],
    ]
    imp_table = Table(imp_data, colWidths=[10*cm, 7*cm])
    imp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), MID_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(imp_table)
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width='100%', thickness=0.5, color=BORDER))

    # ── Final Recommendation ────────────────────────────────────────────
    story.append(Paragraph('6. Final Security Recommendation Report', section_heading))
    verdict = 'CLEARED' if risk_val == 'LOW' else 'REQUIRES REMEDIATION'
    verdict_color = OK if risk_val == 'LOW' else CRIT

    exec_data = [
        [Paragraph('EXECUTIVE SUMMARY', label_style), Paragraph('', body)],
        [Paragraph('Current Risk Level', body),
         Paragraph(risk_val, S('rl2', fontName='Helvetica-Bold', fontSize=10, textColor=risk_color))],
        [Paragraph('Current Security Score', body), Paragraph(f'{score_num}/100', mono)],
        [Paragraph('Security Maturity Level', body), Paragraph('FAIR', mono)],
        [Paragraph('Assessment Verdict', body),
         Paragraph(verdict, S('vd', fontName='Helvetica-Bold', fontSize=10, textColor=verdict_color))],
    ]
    exec_table = Table(exec_data, colWidths=[8*cm, 9*cm])
    exec_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), MID_BLUE),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('SPAN', (0,0), (1,0)),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT_BG]),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 10))

    story.append(Paragraph('Audit Conclusion',
                           S('ac_h', fontName='Helvetica-Bold', fontSize=11,
                             textColor=MID_BLUE, spaceBefore=8, spaceAfter=4)))
    story.append(Paragraph(
        f'The scanned API is accessible and supports HTTPS encrypted communication. '
        f'However, {5 - int(scan.get("Present Header Count", 0))} critical HTTP security headers are absent, '
        f'leaving the API exposed to browser-side attacks including Clickjacking, Cross-Site Scripting (XSS), '
        f'SSL stripping, MIME-type sniffing, and referrer information leakage. '
        f'Security hardening is strongly recommended before deployment into any production environment.',
        body))

    story.append(Paragraph('Recommended Action Plan',
                           S('rap_h', fontName='Helvetica-Bold', fontSize=11,
                             textColor=MID_BLUE, spaceBefore=8, spaceAfter=4)))
    actions = [
        '1. Configure all missing HTTP security response headers on the target API server.',
        '2. Enable HSTS to enforce encrypted transport and prevent SSL-stripping attacks.',
        '3. Define a strict Content-Security-Policy to mitigate XSS injection vectors.',
        '4. Re-run this assessment after remediation to confirm score improvements.',
        '5. Validate all changes through a follow-up third-party security audit.',
    ]
    for action in actions:
        story.append(Paragraph(action, body))

    story.append(Spacer(1, 18))

    # ── Footer strip ────────────────────────────────────────────────────
    footer_data = [[
        Paragraph(BRAND_SHORT,
                  S('ft', fontName='Helvetica-Bold', fontSize=9,
                    textColor=colors.white, alignment=TA_CENTER)),
        Paragraph(f'Generated: {scan.get("Scan Time", "N/A")}',
                  S('fd', fontName='Helvetica', fontSize=9,
                    textColor=colors.HexColor('#B0C4DE'), alignment=TA_CENTER)),
        Paragraph('© 2026 API Security Posture Assessment',
                  S('fc', fontName='Helvetica', fontSize=9,
                    textColor=colors.HexColor('#8A9BC4'), alignment=TA_CENTER)),
    ]]
    footer_table = Table(footer_data, colWidths=[5.67*cm]*3)
    footer_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), DK_BLUE),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(footer_table)

    doc.build(story)
    buffer.seek(0)
    return buffer

# ────────────────────────────────────────────────────────────────────────────
# Routes
# ────────────────────────────────────────────────────────────────────────────

@app.route("/download_report")
def download_report():
    if not latest_scan:
        return "No scan data available. Please run a scan first.", 400
    pdf_buffer = create_pdf_report()
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="api_security_posture_report.pdf",
        mimetype="application/pdf"
    )

@app.route("/", methods=["GET", "POST"])
def home():
    score = None
    risk = None
    response_time = None
    https_status = None
    status_code = None
    x_frame = None
    csp = None
    hsts = None
    x_content = None
    referrer = None
    xai_text = ""
    priority_board = {"high": [], "medium": [], "low": []}
    improvement = {}
    final_report = {}
    xai_lines = []
    ai_summary = {}
    result = ""
    api_url = ""
    present_headers = 0

    if request.method == "POST":
        api_url = request.form.get("api_url", "").strip()
        if not validators.url(api_url):
            result = "Invalid API URL. Please enter a valid URL including https://"
            return render_template("index.html", result=result, api_url=api_url)

        try:
            start = time.time()
            response = requests.get(api_url, timeout=10)
            end = time.time()
            response_time = round((end - start) * 1000, 2)
            status_code = response.status_code

            # ── Normalised status values (plain "Present"/"Missing") ───
            # The template compares to 'Present' exactly — so we must
            # return a clean string, not 'Present ✅'.
            https_status = "Present" if api_url.startswith("https://") else "Missing"
            x_frame      = "Present" if "X-Frame-Options" in response.headers else "Missing"
            csp          = "Present" if "Content-Security-Policy" in response.headers else "Missing"
            hsts         = "Present" if "Strict-Transport-Security" in response.headers else "Missing"
            x_content    = "Present" if "X-Content-Type-Options" in response.headers else "Missing"
            referrer     = "Present" if "Referrer-Policy" in response.headers else "Missing"

            score = 20
            if https_status == "Present": score += 20
            if x_frame      == "Present": score += 12
            if csp          == "Present": score += 12
            if hsts         == "Present": score += 12
            if x_content    == "Present": score += 12
            if referrer     == "Present": score += 12

            if score >= 90:   risk = "LOW"
            elif score >= 70: risk = "MEDIUM"
            else:             risk = "HIGH"

            for item in [x_frame, csp, hsts, x_content, referrer]:
                if item == "Present":
                    present_headers += 1

            # ── Structured XAI lines for terminal display ───────────────
            xai_lines = []
            xai_lines.append({"level": "info", "text": f"Initiating security scan for {api_url}"})
            xai_lines.append({"level": "info", "text": f"Endpoint responded in {response_time} ms with status {status_code}"})
            xai_lines.append({"level": "ok" if https_status == "Present" else "crit",
                              "text": f"HTTPS: {'Encrypted transport verified' if https_status == 'Present' else 'Unencrypted HTTP detected --- data in transit is exposed'}"})
            xai_lines.append({"level": "ok" if x_frame == "Present" else "warn",
                              "text": f"X-Frame-Options: {'Header present --- Clickjacking mitigated' if x_frame == 'Present' else 'Missing --- page may be embedded in malicious iframes (Clickjacking risk)'}"})
            xai_lines.append({"level": "ok" if csp == "Present" else "warn",
                              "text": f"Content-Security-Policy: {'Header present --- XSS injection surface restricted' if csp == 'Present' else 'Absent --- no script execution restrictions, XSS risk elevated'}"})
            xai_lines.append({"level": "ok" if hsts == "Present" else "crit",
                              "text": f"HSTS: {'Enforced --- browsers will always use HTTPS' if hsts == 'Present' else 'Not enforced --- SSL stripping attacks possible on first connection'}"})
            xai_lines.append({"level": "ok" if x_content == "Present" else "warn",
                              "text": f"X-Content-Type-Options: {'Present --- MIME sniffing disabled' if x_content == 'Present' else 'Missing --- browser may misinterpret content types (MIME sniffing risk)'}"})
            xai_lines.append({"level": "ok" if referrer == "Present" else "warn",
                              "text": f"Referrer-Policy: {'Present --- referrer information controlled' if referrer == 'Present' else 'Absent --- sensitive URL fragments may leak via Referer header'}"})
            xai_lines.append({"level": "info", "text": f"Header compliance: {present_headers}/5 recommended headers configured"})
            xai_lines.append({"level": "result", "text": f"Final score: {score}/100 --- Risk classification: {risk}"})

            # ── Plain-text XAI paragraph for PDF ───────────────────────
            xai_text = (
                f"The security assessment for {api_url} completed in {response_time} ms. "
                f"The endpoint returned HTTP status {status_code} and "
                f"{'uses HTTPS for encrypted transport' if https_status == 'Present' else 'is served over plain HTTP, which exposes all traffic in transit'}. "
                f"Of the five recommended HTTP security headers, only {present_headers} were detected in the response. "
                f"{'HSTS is missing, which allows SSL stripping on first contact. ' if hsts == 'Missing' else ''}"
                f"{'Content-Security-Policy is absent, increasing the XSS attack surface. ' if csp == 'Missing' else ''}"
                f"{'X-Frame-Options is not set, leaving the interface vulnerable to Clickjacking. ' if x_frame == 'Missing' else ''}"
                f"{'X-Content-Type-Options is missing, enabling potential MIME sniffing. ' if x_content == 'Missing' else ''}"
                f"{'Referrer-Policy is absent, which may expose URL parameters through the Referer header. ' if referrer == 'Missing' else ''}"
                f"Each missing header reduces the overall score. The composite score of {score}/100 places this API in the {risk} risk band."
            )

            # ── AI Summary structured for template ─────────────────────
            missing_count = 5 - present_headers
            exposure_list = []
            if x_frame == "Missing":   exposure_list.append("Clickjacking")
            if csp == "Missing":       exposure_list.append("Cross-Site Scripting (XSS)")
            if hsts == "Missing":      exposure_list.append("SSL Stripping")
            if x_content == "Missing": exposure_list.append("MIME-Type Sniffing")
            if referrer == "Missing":  exposure_list.append("Information Leakage")

            ai_summary = {
                "intro": (
                    f"The target API is reachable and responds within acceptable latency limits. "
                    f"HTTPS is {'enabled, providing basic transport-layer encryption' if https_status == 'Present' else 'not enabled, which means all traffic --- including any credentials or sensitive data --- is transmitted in plaintext'}. "
                    f"{missing_count} out of 5 recommended browser security controls are absent from the API response headers."
                ),
                "exposure": (
                    f"The missing headers expose users to {', '.join(exposure_list) if exposure_list else 'no additional risks'}. "
                    f"These are well-understood attack vectors catalogued under OWASP API8:2023 Security Misconfiguration."
                ) if exposure_list else None,
                "verdict": (
                    f"With a score of {score}/100 and a {risk} risk classification, this API requires "
                    f"{'immediate remediation before any production deployment' if risk == 'HIGH' else 'moderate hardening before it meets production security standards' if risk == 'MEDIUM' else 'only minor adjustments to achieve full compliance'}."
                ),
                "exposures": exposure_list,
            }

            # ── Priority board ──────────────────────────────────────────
            if hsts == "Missing":
                priority_board["high"].append("Enable Strict-Transport-Security (HSTS) to enforce encrypted connections")
            if csp == "Missing":
                priority_board["medium"].append("Configure Content-Security-Policy to restrict script execution")
            if x_frame == "Missing":
                priority_board["medium"].append("Set X-Frame-Options to prevent Clickjacking attacks")
            if x_content == "Missing":
                priority_board["low"].append("Enable X-Content-Type-Options to disable MIME sniffing")
            if referrer == "Missing":
                priority_board["low"].append("Configure Referrer-Policy to control referrer information leakage")

            # ── Improvement analysis ────────────────────────────────────
            improvement = {
                "current": score,
                "potential": 100,
                "gain": 100 - score,
                "headers_present": present_headers,
                "risk_from": risk,
                "risk_to": "LOW",
                "maturity_from": "Fair",
                "maturity_to": "Excellent",
            }

            # ── Final report ────────────────────────────────────────────
            final_report = {
                "status": risk,
                "score": score,
                "maturity": "FAIR",
                "potential": 100,
                "verdict": "CLEARED" if risk == "LOW" else "REMEDIATION REQUIRED",
                "conclusion": [
                    f"The API endpoint is functional and accessible over the public internet. "
                    f"{'HTTPS is properly configured, ensuring basic transport security.' if https_status == 'Present' else 'The absence of HTTPS is a critical finding that must be addressed immediately.'} "
                    f"However, {missing_count} browser-level security control{'s are' if missing_count != 1 else ' is'} not present in the response headers.",
                    f"These missing controls directly increase exposure to Clickjacking, XSS injection, and other browser-side attack vectors. "
                    f"Security hardening is recommended before this API is considered production-ready."
                ],
                "action_plan": [
                    "Configure all missing HTTP security response headers on the server.",
                    "Re-run this security assessment after applying the recommended changes.",
                    "Validate improvements through a structured follow-up security scan.",
                    "Consider implementing a Web Application Firewall (WAF) for additional protection.",
                ],
                "reassessment": f"Recommended re-assessment date: within 30 days of remediation.",
            }

            # ── Store for PDF ───────────────────────────────────────────
            latest_scan.clear()
            latest_scan.update({
                "API URL": api_url,
                "Security Score": f"{score}/100",
                "Risk Level": risk,
                "HTTPS Enabled": https_status,
                "Response Time": f"{response_time} ms",
                "Status Code": status_code,
                "Present Header Count": present_headers,
                "Explainable AI Text": xai_text,
                "AI Security Summary Text": (
                    ai_summary["intro"] + "\n\n" +
                    (ai_summary["exposure"] or "") + "\n\n" +
                    ai_summary["verdict"]
                ),
                "Priority High": priority_board["high"],
                "Priority Medium": priority_board["medium"],
                "Priority Low": priority_board["low"],
                "Headers": {
                    "X-Frame-Options": x_frame,
                    "Content-Security-Policy": csp,
                    "Strict-Transport-Security": hsts,
                    "X-Content-Type-Options": x_content,
                    "Referrer-Policy": referrer,
                },
                "Scan Time": time.strftime("%d-%m-%Y %H:%M:%S"),
            })

            result = "Scan completed successfully."

        except Exception as e:
            result = f"Error: {str(e)}"

    return render_template(
        "index.html",
        result=result,
        api_url=api_url,
        score=score,
        risk=risk,
        response_time=response_time,
        https_status=https_status,
        status_code=status_code,
        x_frame=x_frame,
        csp=csp,
        hsts=hsts,
        x_content=x_content,
        referrer=referrer,
        present_headers=present_headers,
        xai_lines=xai_lines,
        ai_summary=ai_summary,
        priority_board=priority_board,
        improvement=improvement,
        final_report=final_report,
    )

if __name__ == "__main__":
    app.run(debug=True)