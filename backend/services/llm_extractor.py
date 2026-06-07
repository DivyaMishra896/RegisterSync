"""
Suraksha — LLM Extractor Service
Uses Claude API (or mock) to extract structured rules from regulatory text.
Supports both live API calls and hardcoded mock responses for demo.
"""

import json
import asyncio
from datetime import date, timedelta
from config import settings

# Mock response for demo mode — realistic RBI circular extraction
MOCK_EXTRACTION_RESPONSE = {
    "rules": [
        {
            "rule_id": "R-001",
            "title": "Mandatory VAPT Assessment for Core Banking Systems",
            "description": "All scheduled commercial banks shall conduct Vulnerability Assessment and Penetration Testing (VAPT) of their core banking systems, internet banking platforms, and mobile banking applications at least once every six months. Reports must be submitted to the CISO within 15 days of completion.",
            "affected_departments": ["IT Security"],
            "deadline": (date.today() + timedelta(days=90)).isoformat(),
            "priority": "High",
            "estimated_effort_days": 21
        },
        {
            "rule_id": "R-002",
            "title": "Enhanced Customer Due Diligence for High-Risk Accounts",
            "description": "Banks shall implement enhanced due diligence procedures for accounts classified as high-risk under the risk-based approach. This includes periodic review of KYC documents every 6 months, transaction monitoring with automated alerts, and mandatory senior management sign-off for accounts exceeding ₹50 lakhs in aggregate transactions.",
            "affected_departments": ["Operations", "Risk Management"],
            "deadline": (date.today() + timedelta(days=60)).isoformat(),
            "priority": "High",
            "estimated_effort_days": 30
        },
        {
            "rule_id": "R-003",
            "title": "Cyber Incident Reporting Framework",
            "description": "All regulated entities must report cyber security incidents to RBI within 6 hours of detection. A detailed incident report including root cause analysis, impact assessment, and remediation steps must be submitted within 72 hours. Banks must maintain a dedicated Cyber Security Operations Centre (CSOC) operational 24x7.",
            "affected_departments": ["IT Security", "Risk Management"],
            "deadline": (date.today() + timedelta(days=45)).isoformat(),
            "priority": "Critical",
            "estimated_effort_days": 45
        },
        {
            "rule_id": "R-004",
            "title": "Operational Risk Capital Adequacy Revision",
            "description": "Banks shall recalculate operational risk capital requirements using the revised standardized approach effective from the next reporting quarter. The Basic Indicator Approach multiplier has been revised from 15% to 18% of gross income. All internal models must be re-validated and approved by the Risk Management Committee.",
            "affected_departments": ["Risk Management"],
            "deadline": (date.today() + timedelta(days=120)).isoformat(),
            "priority": "Medium",
            "estimated_effort_days": 25
        },
        {
            "rule_id": "R-005",
            "title": "Data Localization and Cross-Border Data Transfer",
            "description": "All payment system data including full end-to-end transaction details, customer information, and payment credentials shall be stored only in systems located within India. Banks currently storing data overseas shall complete migration within 6 months. A compliance certificate from the CISO must be filed quarterly.",
            "affected_departments": ["IT Security", "Operations"],
            "deadline": (date.today() + timedelta(days=180)).isoformat(),
            "priority": "High",
            "estimated_effort_days": 60
        },
        {
            "rule_id": "R-006",
            "title": "Branch Audit Trail Digitization",
            "description": "All bank branches shall maintain digital audit trails for cash transactions exceeding ₹10 lakhs, foreign exchange transactions, and demand draft issuances. The digital records must be tamper-proof, time-stamped, and retained for a minimum period of 10 years. Integration with the central audit management system is mandatory.",
            "affected_departments": ["Operations"],
            "deadline": (date.today() + timedelta(days=150)).isoformat(),
            "priority": "Medium",
            "estimated_effort_days": 35
        }
    ]
}


async def extract_rules_from_text(text_chunks: list[str], circular_id: int) -> dict:
    """
    Extract structured rules from regulatory text using Claude API or mock.

    Args:
        text_chunks: List of text chunks from the PDF
        circular_id: ID of the circular being processed

    Returns:
        Dictionary with extracted rules
    """
    if settings.LLM_MODE == "mock":
        # Simulate processing delay for realistic demo
        await asyncio.sleep(2)
        return MOCK_EXTRACTION_RESPONSE

    # Live Gemini API call
    try:
        from google import genai

        client = genai.Client(api_key=settings.GEMINI_API_KEY)

        combined_text = "\n\n---\n\n".join(text_chunks)

        prompt = f"""You are a regulatory compliance expert. Analyze the following RBI/SEBI circular text and extract all regulatory rules/requirements.

For each rule, provide:
- rule_id: Sequential ID (R-001, R-002, etc.)
- title: Short descriptive title
- description: Full rule description with key details
- affected_departments: Array of affected departments from: ["IT Security", "Risk Management", "Operations"]
- deadline: Estimated compliance deadline (ISO date format)
- priority: "Critical", "High", "Medium", or "Low"
- estimated_effort_days: Estimated implementation effort in days

CIRCULAR TEXT:
{combined_text}

Respond with valid JSON only:
{{"rules": [...]}}"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        response_text = response.text

        # Parse JSON from response
        # Handle potential markdown code blocks in response
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        return json.loads(response_text.strip())

    except Exception as e:
        print(f"Gemini API error: {e}")
        # Fallback to mock on API failure
        return MOCK_EXTRACTION_RESPONSE


def validate_extraction(data: dict) -> tuple[bool, str]:
    """Validate the structure of extracted rules."""
    if "rules" not in data:
        return False, "Missing 'rules' key"

    for i, rule in enumerate(data["rules"]):
        required_fields = ["rule_id", "title", "description", "affected_departments", "priority"]
        for field in required_fields:
            if field not in rule:
                return False, f"Rule {i}: missing '{field}'"

        if not isinstance(rule.get("affected_departments", []), list):
            return False, f"Rule {i}: 'affected_departments' must be a list"

        valid_priorities = ["Critical", "High", "Medium", "Low"]
        if rule.get("priority") not in valid_priorities:
            return False, f"Rule {i}: invalid priority '{rule.get('priority')}'"

    return True, "Valid"
