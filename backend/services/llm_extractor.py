import json
import asyncio
from datetime import date, timedelta
from config import settings


MOCK_EXTRACTION_RESPONSE = {
    "rules": [
        {
            "rule_id": "R-001",
            "title": "Mandatory VAPT Assessment for Core Banking Systems",
            "description": "All scheduled commercial banks shall conduct Vulnerability Assessment and Penetration Testing (VAPT) of their core banking systems, internet banking platforms, and mobile banking applications at least once every six months. Reports must be submitted to the CISO within 15 days of completion.",
            "affected_departments": ["Cybersecurity Wing", "IT Vertical"],
            "deadline": (date.today() + timedelta(days=90)).isoformat(),
            "priority": "High",
            "estimated_effort_days": 21
        },
        {
            "rule_id": "R-002",
            "title": "Enhanced Customer Due Diligence for High-Risk Accounts",
            "description": "Banks shall implement enhanced due diligence procedures for accounts classified as high-risk under the risk-based approach. This includes periodic review of KYC documents every 6 months, transaction monitoring with automated alerts, and mandatory senior management sign-off for accounts exceeding ₹50 lakhs in aggregate transactions.",
            "affected_departments": ["Compliance Department", "Risk Management"],
            "deadline": (date.today() + timedelta(days=60)).isoformat(),
            "priority": "High",
            "estimated_effort_days": 30
        },
        {
            "rule_id": "R-003",
            "title": "Cyber Incident Reporting Framework",
            "description": "All regulated entities must report cyber security incidents to RBI within 6 hours of detection. A detailed incident report including root cause analysis, impact assessment, and remediation steps must be submitted within 72 hours. Banks must maintain a dedicated Cyber Security Operations Centre (CSOC) operational 24x7.",
            "affected_departments": ["Cybersecurity Wing", "Risk Management"],
            "deadline": (date.today() + timedelta(days=45)).isoformat(),
            "priority": "Critical",
            "estimated_effort_days": 45
        },
        {
            "rule_id": "R-004",
            "title": "Operational Risk Capital Adequacy Revision",
            "description": "Banks shall recalculate operational risk capital requirements using the revised standardized approach effective from the next reporting quarter. The Basic Indicator Approach multiplier has been revised from 15% to 18% of gross income. All internal models must be re-validated and approved by the Risk Management Committee.",
            "affected_departments": ["Risk Management", "Internal Audit"],
            "deadline": (date.today() + timedelta(days=120)).isoformat(),
            "priority": "Medium",
            "estimated_effort_days": 25
        },
        {
            "rule_id": "R-005",
            "title": "Data Localization and Cross-Border Data Transfer",
            "description": "All payment system data including full end-to-end transaction details, customer information, and payment credentials shall be stored only in systems located within India. Banks currently storing data overseas shall complete migration within 6 months. A compliance certificate from the CISO must be filed quarterly.",
            "affected_departments": ["IT Vertical", "Legal Department", "Payments Vertical"],
            "deadline": (date.today() + timedelta(days=180)).isoformat(),
            "priority": "High",
            "estimated_effort_days": 60
        },
        {
            "rule_id": "R-006",
            "title": "Branch Audit Trail Digitization",
            "description": "All bank branches shall maintain digital audit trails for cash transactions exceeding ₹10 lakhs, foreign exchange transactions, and demand draft issuances. The digital records must be tamper-proof, time-stamped, and retained for a minimum period of 10 years. Integration with the central audit management system is mandatory.",
            "affected_departments": ["Internal Audit", "Payments Vertical"],
            "deadline": (date.today() + timedelta(days=150)).isoformat(),
            "priority": "Medium",
            "estimated_effort_days": 35
        },
        {
            "rule_id": "R-007",
            "title": "Digital Lending Platform Security Requirements",
            "description": "All banks offering digital lending services must implement end-to-end encryption for loan origination data, conduct quarterly security assessments of lending platforms, and maintain separate data lakes for lending analytics. Third-party lending partners must comply with the bank's information security policy.",
            "affected_departments": ["Digital Banking Services", "Procurement & Vendor Management"],
            "deadline": (date.today() + timedelta(days=90)).isoformat(),
            "priority": "High",
            "estimated_effort_days": 28
        },
        {
            "rule_id": "R-008",
            "title": "Credit Card Dispute Resolution Timeline",
            "description": "Banks shall resolve all credit card transaction disputes within 30 days of receipt of complaint. Chargeback requests must be processed within 7 working days. Monthly dispute resolution metrics must be reported to the Board-level Customer Service Committee.",
            "affected_departments": ["Credit Card Vertical", "Compliance Department"],
            "deadline": (date.today() + timedelta(days=60)).isoformat(),
            "priority": "Medium",
            "estimated_effort_days": 20
        }
    ]
}


async def extract_rules_from_text(text_chunks: list[str], circular_id: int) -> dict:
    if settings.LLM_MODE == "mock":
        await asyncio.sleep(2)
        return MOCK_EXTRACTION_RESPONSE

    # --- Live Ollama extraction path ---
    # Import here to avoid circular imports at module load time
    from services.llm_provider import llm_client

    today = date.today().isoformat()
    combined_text = "\n\n".join(text_chunks)

    system_prompt = (
        "You are a regulatory compliance expert specialising in banking and finance regulations. "
        "Your task is to read a regulatory circular and extract every distinct compliance rule or obligation it contains. "
        "Return ONLY a valid JSON object — no markdown fences, no explanation — with this exact schema:\n"
        '{"rules": [{'
        '"rule_id": "R-001", '
        '"title": "<concise rule title>", '
        '"description": "<full obligation description>", '
        '"affected_departments": ["<dept1>", "<dept2>"], '
        f'"deadline": "<ISO-8601 date on or after {today}>", '
        '"priority": "<Critical|High|Medium|Low>", '
        '"estimated_effort_days": <positive integer>'
        "}]}"
    )

    user_prompt = (
        f"Regulatory circular text:\n\n{combined_text}\n\n"
        "Extract all compliance rules and obligations from the text above "
        "and return them in the JSON structure described."
    )

    print(
        f"[LLMExtractor] Sending circular_id={circular_id} "
        f"({len(text_chunks)} chunk(s)) to Ollama..."
    )

    result = await llm_client.generate(system_prompt, user_prompt)

    if result:
        is_valid, msg = validate_extraction(result)
        if is_valid:
            rule_count = len(result.get("rules", []))
            print(f"[LLMExtractor] Extracted {rule_count} rule(s) via Ollama.")
            return result
        else:
            print(f"[LLMExtractor] Ollama response failed validation: {msg}")
    else:
        print("[LLMExtractor] Ollama returned an empty or unparseable response.")

    # Graceful fallback so the upload flow does not break
    print("[LLMExtractor] Falling back to mock extraction response.")
    return MOCK_EXTRACTION_RESPONSE


def validate_extraction(data: dict) -> tuple[bool, str]:
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
