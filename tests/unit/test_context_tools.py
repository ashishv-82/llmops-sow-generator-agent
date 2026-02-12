from src.agent.tools.context import assemble_client_brief, assemble_context


def test_assemble_context():
    crm_data = {"name": "Test Client"}
    product_info = {"name": "Test Product"}
    history = [{"id": "SOW1"}]
    compliance = {"tier": "HIGH"}
    opportunities = [{"id": "OPP1"}]

    result = assemble_context.invoke(
        {
            "crm_data": crm_data,
            "product_info": product_info,
            "history": history,
            "compliance": compliance,
            "opportunities": opportunities,
        }
    )

    assert result["client"] == crm_data
    assert result["product"] == product_info
    assert result["historical_sows"] == history
    assert result["compliance"] == compliance
    assert result["opportunities"] == opportunities


def test_assemble_client_brief():
    crm_data = {
        "name": "Test Client",
        "contacts": ["Alice"],
        "notes": "Good client",
        "compliance_tier": "HIGH",
    }
    opportunities = [{"status": "Won", "value": 100}, {"status": "Lost", "value": 50}]

    result = assemble_client_brief.invoke({"crm_data": crm_data, "opportunities": opportunities})

    assert result["client"] == crm_data
    assert result["summary_stats"]["total_opportunities"] == 2
    assert result["summary_stats"]["won_opportunities"] == 1
    assert result["summary_stats"]["total_contract_value"] == 100
