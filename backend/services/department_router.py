"""
Suraksha — Department Router Service
Routes extracted rules/tasks to the appropriate department using keyword matching.
"""

# Department keyword mappings
DEPARTMENT_KEYWORDS = {
    "IT Security": [
        "cybersecurity", "cyber security", "data protection", "encryption",
        "firewall", "vapt", "vulnerability", "penetration testing",
        "it audit", "information security", "csoc", "security operations",
        "data localization", "phishing", "malware", "intrusion",
        "access control", "authentication", "ciso", "network security",
        "ssl", "tls", "digital certificate", "cyber incident",
        "data breach", "security patch", "antivirus", "endpoint security"
    ],
    "Risk Management": [
        "risk assessment", "capital adequacy", "stress testing",
        "exposure limit", "credit risk", "market risk", "operational risk",
        "liquidity risk", "risk appetite", "risk framework",
        "risk management committee", "risk model", "risk capital",
        "risk-weighted", "provisioning", "npa", "non-performing",
        "basel", "crar", "risk mitigation", "counterparty risk",
        "concentration risk", "systemic risk"
    ],
    "Operations": [
        "kyc", "know your customer", "customer onboarding", "branch",
        "reporting", "audit trail", "transaction monitoring",
        "customer due diligence", "cdd", "aml", "anti-money laundering",
        "account opening", "remittance", "demand draft",
        "foreign exchange", "cash management", "cheque", "neft", "rtgs",
        "upi", "payment system", "settlement", "reconciliation",
        "customer grievance", "ombudsman"
    ]
}


def route_to_department(text: str) -> str:
    """
    Determine the most relevant department for a given rule/text.
    Uses keyword frequency matching.
    """
    text_lower = text.lower()
    scores = {}

    for dept, keywords in DEPARTMENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[dept] = score

    # Return department with highest score, default to Operations
    if max(scores.values()) == 0:
        return "Operations"

    return max(scores, key=scores.get)


def route_rule_to_departments(title: str, description: str) -> list[str]:
    """
    Route a rule to one or more departments based on title + description.
    Returns a list of affected departments.
    """
    combined_text = f"{title} {description}".lower()
    departments = []

    for dept, keywords in DEPARTMENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in combined_text)
        if score >= 1:
            departments.append(dept)

    # Default to Operations if no match
    if not departments:
        departments = ["Operations"]

    return departments


def get_department_color(department: str) -> str:
    """Get the display color for a department."""
    colors = {
        "IT Security": "#3b82f6",      # Blue
        "Risk Management": "#f59e0b",  # Amber
        "Operations": "#10b981",       # Emerald
    }
    return colors.get(department, "#6b7280")
