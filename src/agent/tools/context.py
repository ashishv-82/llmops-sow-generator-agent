"""
Context assembly tools for the SOW Generator agent.

Provides tools to assemble research data into structured context for generation.
"""

from typing import Annotated

from langchain_core.tools import tool
from pydantic import BaseModel


class ContextPackage(BaseModel):
    """Structured context package for SOW generation."""

    client: dict
    product: dict
    historical_sows: list[dict]
    compliance: dict
    opportunities: list[dict]


class ClientBrief(BaseModel):
    """Client research summary."""

    client: dict
    opportunities: list[dict]
    past_engagements: list[dict]


@tool
def assemble_context(
    crm_data: Annotated[dict, "Client data from CRM"],
    product_info: Annotated[dict, "Product information"],
    history: Annotated[list[dict], "Historical SOW data"],
    compliance: Annotated[dict, "Compliance requirements"],
    opportunities: Annotated[list[dict] | None, "Optional opportunities data"] = None,
) -> dict:
    """
    Assemble all research data into a structured context package for SOW generation.

    Combines client info, product details, historical context, and compliance requirements.

    Args:
        crm_data: Client profile from CRM
        product_info: Product information from knowledge base
        history: Relevant historical SOWs
        compliance: Compliance requirements
        opportunities: Optional list of past opportunities

    Returns:
        Structured context package
    """
    context = {
        "client": crm_data,
        "product": product_info,
        "historical_sows": history,
        "compliance": compliance,
        "opportunities": opportunities or [],
    }

    return context


@tool
def assemble_client_brief(
    crm_data: Annotated[dict, "Client data from CRM"],
    opportunities: Annotated[list[dict], "Opportunities data"],
) -> dict:
    """
    Create a client briefing document for sales/delivery teams.

    Summarizes client profile, contacts, past deals, and key notes.

    Args:
        crm_data: Client profile from CRM
        opportunities: List of opportunities for this client

    Returns:
        Client brief dictionary
    """
    # Calculate summary stats
    total_deals = len(opportunities)
    won_deals = [opp for opp in opportunities if opp.get("status") == "Won"]
    total_value = sum(opp.get("value", 0) for opp in won_deals)

    brief = {
        "client": crm_data,
        "opportunities": opportunities,
        "summary_stats": {
            "total_opportunities": total_deals,
            "won_opportunities": len(won_deals),
            "total_contract_value": total_value,
        },
        "key_contacts": crm_data.get("contacts", []),
        "relationship_notes": crm_data.get("notes", ""),
        "compliance_tier": crm_data.get("compliance_tier", "UNKNOWN"),
    }

    return brief
