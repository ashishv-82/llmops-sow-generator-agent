"""Tool module initialization - exports all tools."""

from src.agent.tools.compliance import (
    check_mandatory_clauses,
    check_prohibited_terms,
    check_sla_requirements,
    generate_compliance_report,
)
from src.agent.tools.content import (
    generate_section,
    generate_sow_draft,
    generate_sow_draft_with_reflection,
    generate_summary,
    revise_section,
)
from src.agent.tools.context import assemble_client_brief, assemble_context
from src.agent.tools.research import (
    search_compliance_kb,
    search_crm,
    search_historical_sows,
    search_opportunities,
    search_product_kb,
)

# All available tools for the agent
ALL_TOOLS = [
    # Research tools
    search_crm,
    search_opportunities,
    search_historical_sows,
    search_product_kb,
    search_compliance_kb,
    # Context tools
    assemble_context,
    assemble_client_brief,
    # Content tools
    generate_sow_draft,
    generate_sow_draft_with_reflection,
    generate_section,
    revise_section,
    generate_summary,
    # Compliance tools
    check_mandatory_clauses,
    check_prohibited_terms,
    check_sla_requirements,
    generate_compliance_report,
]

__all__ = ["ALL_TOOLS"]
