"""
Research tools for the SOW Generator agent.

Provides tools to search CRM, opportunities, historical SOWs, product KB, and compliance rules.
"""

import json
from pathlib import Path
from typing import Annotated, Dict, List

from langchain_core.tools import tool

from src.rag.retriever import DocumentRetriever

# Data directory (project root / data)
DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


@tool
def search_crm(client_name: Annotated[str, "Name of the client to search for"]) -> Dict:
    """
    Search the CRM for client information.

    Returns client profile including contacts, industry, compliance tier, and notes.

    Args:
        client_name: Name of the client (partial match supported)

    Returns:
        Client profile dictionary or error message
    """
    crm_file = DATA_DIR / "mock_crm.json"

    if not crm_file.exists():
        return {"error": "CRM data file not found"}

    with open(crm_file, "r") as f:
        data = json.load(f)

    # Search for client (case-insensitive partial match on name or exact match on ID)
    client_name_lower = client_name.lower()
    for client in data.get("clients", []):
        if (client_name_lower in client["name"].lower()) or (client_name_lower == client["id"].lower()):
            return client

    return {"error": f"Client '{client_name}' not found in CRM"}


@tool
def search_opportunities(
    client_id: Annotated[str, "Client ID to search opportunities for"]
) -> List[Dict]:
    """
    Search for past opportunities and deals for a client.

    Returns list of opportunities including status, value, and products.

    Args:
        client_id: Client ID (e.g., CLIENT-001)

    Returns:
        List of opportunity dictionaries
    """
    opportunities_file = DATA_DIR / "mock_opportunities.json"

    if not opportunities_file.exists():
        return [{"error": "Opportunities data file not found"}]

    with open(opportunities_file, "r") as f:
        data = json.load(f)

    # Filter opportunities by client_id
    client_opps = [
        opp for opp in data.get("opportunities", []) if opp.get("client_id") == client_id
    ]

    if not client_opps:
        return [{"message": f"No opportunities found for client {client_id}"}]

    return client_opps


@tool
def search_historical_sows(
    query: Annotated[str, "Search query describing what to look for"],
    client_id: Annotated[str | None, "Optional client ID filter"] = None,
    product: Annotated[str | None, "Optional product name filter"] = None,
) -> List[Dict]:
    """
    Search historical SOW documents using semantic search.

    Returns relevant past SOWs that match the query and filters.

    Args:
        query: Natural language search query
        client_id: Optional client ID to filter results
        product: Optional product name to filter results

    Returns:
        List of relevant SOW excerpts with metadata
    """
    retriever = DocumentRetriever()

    # Build filters
    filters = {"doc_type": "historical_sow"}
    if client_id:
        filters["client_id"] = client_id
    if product:
        filters["product"] = product

    # Search
    results = retriever.search(query, n_results=5, filters=filters)

    # Format results
    formatted = []
    for result in results:
        formatted.append(
            {
                "content": result["content"],
                "source": result["metadata"].get("file_name", "unknown"),
                "client": result["metadata"].get("client_id", "unknown"),
                "product": result["metadata"].get("product", "unknown"),
                "relevance_score": result["score"],
            }
        )

    return formatted


@tool
def search_product_kb(product: Annotated[str, "Product name to search for"]) -> Dict:
    """
    Search the product knowledge base.

    Returns product information including features, pricing, and technical requirements.

    Args:
        product: Product name (e.g., "Real-Time Payments", "Fraud Detection")

    Returns:
        Product information dictionary
    """
    # FIRST: Check for deterministic mock data (for Demo)
    products_file = DATA_DIR / "mock_products.json"
    if products_file.exists():
        try:
            with open(products_file, "r") as f:
                product_data = json.load(f)
            
            for p in product_data.get("products", []):
                # Check for name or alias match
                if (product.lower() in p["name"].lower()) or \
                   (product.lower() in [a.lower() for a in p.get("aliases", [])]):
                    
                    return {
                        "name": p["name"],
                        "category": p["category"],
                        "pricing_model": p["pricing_model"],
                        "description": p["description"],
                        "features": p["features"],
                        "technical_requirements": p["technical_requirements"],
                        "sla_tier": p.get("sla_tier", "Standard"),
                        "source": "Internal Product Catalog (Demo)"
                    }
        except Exception as e:
            # Fallback to RAG if mock file read fails
            print(f"Error reading mock products: {e}")

    retriever = DocumentRetriever()

    # Search for product documents
    results = retriever.search(
        query=f"Product overview features pricing for {product}",
        n_results=3,
        filters={"doc_type": "product_kb"},
    )

    if not results:
        return {"error": f"No product information found for '{product}'"}

    # Combine results into a single response
    content = "\n\n".join([r["content"] for r in results])

    return {
        "product": product,
        "content": content,
        "sources": [r["metadata"].get("file_name", "unknown") for r in results],
    }


@tool
def search_compliance_kb(
    client_tier: Annotated[str, "Client compliance tier (HIGH, MEDIUM, LOW)"],
    product: Annotated[str | None, "Optional product name"] = None,
) -> Dict:
    """
    Search compliance requirements knowledge base.

    Returns mandatory clauses, prohibited terms, and SLA requirements.

    Args:
        client_tier: Compliance tier (HIGH, MEDIUM, LOW)
        product: Optional product name for product-specific requirements

    Returns:
        Compliance requirements dictionary
    """
    compliance_file = DATA_DIR / "compliance_rules" / "compliance_rules.json"

    if not compliance_file.exists():
        return {"error": "Compliance rules file not found"}

    with open(compliance_file, "r") as f:
        data = json.load(f)

    # Get requirements for tier
    tier_requirements = data.get("sla_requirements_by_tier", {}).get(client_tier, {})

    # Filter mandatory clauses for tier
    all_clauses = data.get("mandatory_clauses", [])
    relevant_clauses = []
    for c in all_clauses:
        req_for = c.get("required_for", [])
        if "ALL" in req_for or client_tier in req_for:
            relevant_clauses.append(c)

    response = {
        "client_tier": client_tier,
        "sla_requirements": tier_requirements,
        "mandatory_clauses": relevant_clauses,
        "prohibited_terms": data.get("prohibited_terms", []),
    }

    return response
