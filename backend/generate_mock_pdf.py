"""
Generate a realistic mock RBI circular PDF for demo purposes.
Run this script once to create the sample circular.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
import os

def generate_mock_circular():
    output_path = os.path.join(os.path.dirname(__file__), "samples", "mock_rbi_circular.pdf")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm,
        leftMargin=2*cm,
        rightMargin=2*cm
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CircularTitle',
        parent=styles['Heading1'],
        fontSize=14,
        alignment=TA_CENTER,
        spaceAfter=6,
        textColor=HexColor('#1a1a2e')
    )

    header_style = ParagraphStyle(
        'CircularHeader',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=4,
        textColor=HexColor('#333333')
    )

    section_style = ParagraphStyle(
        'SectionHead',
        parent=styles['Heading2'],
        fontSize=12,
        spaceBefore=16,
        spaceAfter=8,
        textColor=HexColor('#1a1a2e')
    )

    body_style = ParagraphStyle(
        'CircularBody',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=8,
        leading=14
    )

    ref_style = ParagraphStyle(
        'RefStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=HexColor('#666666'),
        spaceAfter=4
    )

    elements = []

    # Header
    elements.append(Paragraph("भारतीय रिज़र्व बैंक", header_style))
    elements.append(Paragraph("RESERVE BANK OF INDIA", title_style))
    elements.append(Paragraph("Department of Information Technology", header_style))
    elements.append(Paragraph("Central Office, Mumbai - 400001", header_style))
    elements.append(Spacer(1, 8))
    elements.append(HRFlowable(width="100%", thickness=2, color=HexColor('#1a1a2e')))
    elements.append(Spacer(1, 12))

    # Circular reference
    elements.append(Paragraph("RBI/2026-27/42", ref_style))
    elements.append(Paragraph("DIT.CO.CSEC/2026-27/1042", ref_style))
    elements.append(Paragraph("June 1, 2026", ref_style))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(
        "The Chairman / Managing Director / Chief Executive Officer<br/>"
        "All Scheduled Commercial Banks<br/>"
        "All Payment System Operators",
        body_style
    ))
    elements.append(Spacer(1, 8))

    elements.append(Paragraph(
        "<b>Re: Master Directions on Cyber Security, IT Governance, and Operational "
        "Resilience Framework for Regulated Entities — Revised Guidelines 2026</b>",
        ParagraphStyle('Subject', parent=body_style, fontSize=11, alignment=TA_CENTER, spaceBefore=8, spaceAfter=12)
    ))

    elements.append(Paragraph(
        "Dear Sir / Madam,",
        body_style
    ))

    elements.append(Paragraph(
        "In view of the evolving cyber threat landscape and the increasing digitization of banking "
        "services, the Reserve Bank of India has reviewed the existing framework for cyber security "
        "and IT governance. Based on feedback from regulated entities, international best practices, "
        "and recommendations of the Standing Committee on Cyber Security, the following revised "
        "guidelines are hereby issued for compliance by all scheduled commercial banks and payment "
        "system operators.",
        body_style
    ))

    # Section 1
    elements.append(Paragraph("1. Vulnerability Assessment and Penetration Testing (VAPT)", section_style))
    elements.append(Paragraph(
        "All scheduled commercial banks shall conduct Vulnerability Assessment and Penetration "
        "Testing (VAPT) of their core banking systems, internet banking platforms, and mobile "
        "banking applications at least once every six months. The VAPT shall be conducted by "
        "CERT-In empanelled auditors. Reports must be submitted to the Chief Information Security "
        "Officer (CISO) within 15 days of completion. Any critical vulnerabilities identified must "
        "be remediated within 30 days of discovery.",
        body_style
    ))

    # Section 2
    elements.append(Paragraph("2. Enhanced Customer Due Diligence (CDD)", section_style))
    elements.append(Paragraph(
        "Banks shall implement enhanced due diligence procedures for accounts classified as "
        "high-risk under the risk-based approach. This includes: (a) periodic review of KYC "
        "documents every 6 months instead of annually; (b) transaction monitoring with automated "
        "alerts for unusual patterns; (c) mandatory senior management sign-off for accounts "
        "exceeding ₹50 lakhs in aggregate quarterly transactions; and (d) enhanced screening "
        "against updated sanctions lists and PEP databases on a real-time basis.",
        body_style
    ))

    # Section 3
    elements.append(Paragraph("3. Cyber Incident Reporting Framework", section_style))
    elements.append(Paragraph(
        "All regulated entities must report cyber security incidents to RBI's Cyber Security "
        "Incident Reporting (CSIR) portal within 6 hours of detection. A detailed incident "
        "report including root cause analysis, impact assessment, and remediation steps must be "
        "submitted within 72 hours. Banks must maintain a dedicated Cyber Security Operations "
        "Centre (CSOC) operational 24x7 with at least Level 2 SOC analyst coverage. Quarterly "
        "drill exercises simulating cyber attack scenarios are mandatory.",
        body_style
    ))

    # Section 4
    elements.append(Paragraph("4. Operational Risk Capital Adequacy — Revised Approach", section_style))
    elements.append(Paragraph(
        "Banks shall recalculate operational risk capital requirements using the revised "
        "standardized approach effective from the reporting quarter ending September 2026. "
        "The Basic Indicator Approach (BIA) multiplier has been revised from 15% to 18% of "
        "gross income averaged over the previous three years. All internal models used for "
        "operational risk assessment must be re-validated by an independent validation unit "
        "and approved by the Risk Management Committee of the Board before implementation.",
        body_style
    ))

    # Section 5
    elements.append(Paragraph("5. Data Localization and Cross-Border Data Transfer", section_style))
    elements.append(Paragraph(
        "All payment system data including full end-to-end transaction details, customer "
        "information, and payment credentials shall be stored exclusively in systems and data "
        "centers located within India. Banks currently storing any payment-related data in "
        "overseas facilities shall complete migration to domestic data centers within 6 months "
        "from the date of this circular. A compliance certificate signed by the CISO must be "
        "filed with the Department of Payment and Settlement Systems on a quarterly basis.",
        body_style
    ))

    # Section 6
    elements.append(Paragraph("6. Branch Audit Trail Digitization", section_style))
    elements.append(Paragraph(
        "All bank branches shall maintain digital audit trails for: (a) cash transactions "
        "exceeding ₹10 lakhs; (b) foreign exchange transactions irrespective of value; "
        "(c) demand draft issuances above ₹5 lakhs; and (d) any transaction flagged by the "
        "automated monitoring system. The digital records must be tamper-proof, time-stamped "
        "with NTP-synchronized clocks, and retained for a minimum period of 10 years. "
        "Integration with the central audit management system is mandatory within 150 days.",
        body_style
    ))

    # Compliance timeline
    elements.append(Spacer(1, 12))
    elements.append(Paragraph("Compliance Timeline", section_style))

    timeline_data = [
        ['Section', 'Requirement', 'Deadline'],
        ['1. VAPT', 'First assessment under new frequency', '90 days'],
        ['2. Enhanced CDD', 'Process deployment', '60 days'],
        ['3. Cyber Reporting', 'CSOC operationalization', '45 days'],
        ['4. Risk Capital', 'Recalculation submission', '120 days'],
        ['5. Data Localization', 'Complete data migration', '180 days'],
        ['6. Audit Digitization', 'System integration', '150 days'],
    ]

    table = Table(timeline_data, colWidths=[2.5*cm, 8*cm, 3*cm])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 0.5, HexColor('#cccccc')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#f8f8f8'), HexColor('#ffffff')]),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elements.append(table)

    # Footer
    elements.append(Spacer(1, 24))
    elements.append(Paragraph(
        "This circular is effective immediately. Non-compliance will be viewed seriously "
        "and may attract supervisory action under the provisions of the Banking Regulation Act, 1949.",
        body_style
    ))
    elements.append(Spacer(1, 16))
    elements.append(Paragraph("Yours faithfully,", body_style))
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("<b>(Rajesh Kumar Sharma)</b>", body_style))
    elements.append(Paragraph("Chief General Manager", ref_style))
    elements.append(Paragraph("Department of Information Technology", ref_style))

    doc.build(elements)
    print(f"[OK] Mock RBI circular generated: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_mock_circular()
