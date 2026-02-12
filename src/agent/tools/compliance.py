"""
Compliance validation tools for the SOW Generator agent.

Validates SOWs against mandatory clauses, prohibited terms, and SLA requirements.
"""

import json
import re
from pathlib import Path
from typing import Annotated, Any

from langchain_core.tools import tool

# Data directory
DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


@tool
def check_mandatory_clauses_v2(
    sow_text: Annotated[str, "SOW text to check"],
    requirements: Annotated[list[Any], "List of mandatory clauses (strings or dicts)"],
) -> dict:
    """
    Check if all mandatory clauses are present in the SOW.

    Args:
        sow_text: Full SOW text
        requirements: List of required clause keywords/phrases

    Returns:
        Validation results with missing clauses
    """
    missing_clauses = []
    found_clauses = []

    for item in requirements:
        # Handle dict inputs (graceful degradation)
        if isinstance(item, dict):
            clause = item.get("name") or item.get("text") or str(item)
        else:
            clause = str(item)

        # Case-insensitive search
        if re.search(re.escape(clause), sow_text, re.IGNORECASE):
            found_clauses.append(clause)
        else:
            missing_clauses.append(clause)

    status = "PASS" if not missing_clauses else "FAIL"

    return {
        "status": status,
        "found_clauses": found_clauses,
        "missing_clauses": missing_clauses,
        "total_required": len(requirements),
        "total_found": len(found_clauses),
    }


@tool
def check_prohibited_terms(sow_text: Annotated[str, "SOW text to check"]) -> dict:
    """
    Check for prohibited terms or risky language in the SOW.

    Scans for terms that should not appear in SOWs (e.g., "guarantee", "unlimited").

    Args:
        sow_text: Full SOW text

    Returns:
        Validation results with any prohibited terms found
    """
    # Load prohibited terms from compliance rules
    compliance_file = DATA_DIR / "compliance_rules" / "compliance_rules.json"

    if not compliance_file.exists():
        return {"error": "Compliance rules file not found"}

    with open(compliance_file) as f:
        data = json.load(f)

    prohibited_terms = data.get("prohibited_terms", [])
    findings = []

    for term in prohibited_terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        matches = pattern.finditer(sow_text)

        for match in matches:
            # Find line number
            line_num = sow_text[: match.start()].count("\n") + 1

            findings.append(
                {
                    "term": term,
                    "location": f"Line {line_num}",
                    "context": _get_context(sow_text, match.start(), match.end()),
                }
            )

    status = "PASS" if not findings else "WARNING"

    return {
        "status": status,
        "prohibited_terms_found": len(findings),
        "findings": findings,
    }


@tool
def check_sla_requirements(
    sow_text: Annotated[str, "SOW text to check"],
    product: Annotated[str, "Product name"],
    client_tier: Annotated[str, "Client compliance tier (HIGH, MEDIUM, LOW)"],
) -> dict:
    """
    Validate SLA requirements based on product and client tier.

    Checks for required uptime, response time, and support level commitments.

    Args:
        sow_text: Full SOW text
        product: Product name
        client_tier: Client compliance tier

    Returns:
        Validation results for SLA requirements
    """
    # Load compliance requirements
    compliance_file = DATA_DIR / "compliance_rules" / "compliance_rules.json"

    if not compliance_file.exists():
        return {"error": "Compliance rules file not found"}

    with open(compliance_file) as f:
        data = json.load(f)

    tier_requirements = data.get("sla_requirements_by_tier", {}).get(client_tier, {})

    if not tier_requirements:
        return {"error": f"No SLA requirements found for tier '{client_tier}'"}

    findings = []

    # Check uptime
    uptime = tier_requirements.get("uptime", "")
    if uptime and uptime not in sow_text:
        findings.append(
            {
                "severity": "HIGH",
                "issue": f"Missing uptime SLA: '{uptime}'",
                "location": "SLA Section",
                "suggestion": f"Add uptime commitment: '{uptime}'",
            }
        )

    # Check max response time
    response_time = tier_requirements.get("max_response_time", "")
    if response_time:
        # Look for any response time mention
        if not re.search(r"response.{0,20}time", sow_text, re.IGNORECASE):
            findings.append(
                {
                    "severity": "MEDIUM",
                    "issue": "Missing response time SLA",
                    "location": "SLA Section",
                    "suggestion": f"Add response time commitment: '{response_time}'",
                }
            )

    status = "PASS" if not findings else "WARNING"

    return {
        "status": status,
        "client_tier": client_tier,
        "required_slas": tier_requirements,
        "findings": findings,
    }


@tool
def generate_compliance_report(findings: Annotated[list[dict], "List of findings"]) -> str:
    """
    Generate a formatted compliance report from findings.

    Args:
        findings: List of finding dictionaries from compliance checks

    Returns:
        Formatted compliance report in markdown
    """
    report = "# SOW Compliance Report\n\n"

    if not findings:
        report += "✅ **Status: PASS**\n\nNo compliance issues found.\n"
        return report

    # Group by severity
    high = [f for f in findings if f.get("severity") == "HIGH"]
    medium = [f for f in findings if f.get("severity") == "MEDIUM"]
    low = [f for f in findings if f.get("severity") == "LOW"]

    total = len(findings)
    report += f"⚠️  **Status: ISSUES FOUND ({total} total)**\n\n"

    if high:
        report += f"## 🔴 High Severity ({len(high)})\n\n"
        for f in high:
            report += f"- **Issue**: {f.get('issue')}\n"
            report += f"  - **Location**: {f.get('location')}\n"
            report += f"  - **Suggestion**: {f.get('suggestion')}\n\n"

    if medium:
        report += f"## 🟡 Medium Severity ({len(medium)})\n\n"
        for f in medium:
            report += f"- **Issue**: {f.get('issue')}\n"
            report += f"  - **Location**: {f.get('location')}\n"
            report += f"  - **Suggestion**: {f.get('suggestion')}\n\n"

    if low:
        report += f"## 🟢 Low Severity ({len(low)})\n\n"
        for f in low:
            report += f"- **Issue**: {f.get('issue')}\n"
            report += f"  - **Location**: {f.get('location')}\n"
            report += f"  - **Suggestion**: {f.get('suggestion')}\n\n"

    return report


def _get_context(text: str, start: int, end: int, context_chars: int = 50) -> str:
    """Get surrounding context for a match."""
    context_start = max(0, start - context_chars)
    context_end = min(len(text), end + context_chars)
    return "..." + text[context_start:context_end] + "..."
