import json
from unittest.mock import MagicMock, mock_open, patch

import pytest

from src.agent.tools.research import (
    search_compliance_kb,
    search_crm,
    search_historical_sows,
    search_opportunities,
    search_product_kb,
)


@pytest.fixture
def mock_crm_data():
    return {
        "clients": [
            {
                "id": "CLIENT-001",
                "name": "Acme Financial Services",
                "industry": "Banking",
                "size": "Enterprise",
                "compliance_tier": "HIGH",
            }
        ]
    }


@pytest.fixture
def mock_opportunities_data():
    return {
        "opportunities": [
            {"client_id": "CLIENT-001", "opportunity_name": "New Deal", "amount": 100000}
        ]
    }


@pytest.fixture
def mock_compliance_data():
    return {
        "sla_requirements_by_tier": {"HIGH": {"uptime": "99.99%"}},
        "mandatory_clauses": [{"name": "Data Privacy", "required_for": ["HIGH", "ALL"]}],
        "prohibited_terms": ["guarantee"],
    }


def test_search_crm_found(mock_crm_data):
    with (
        patch("builtins.open", mock_open(read_data=json.dumps(mock_crm_data))),
        patch("pathlib.Path.exists", return_value=True),
    ):

        result = search_crm.invoke("Acme")
        assert result["id"] == "CLIENT-001"
        assert result["name"] == "Acme Financial Services"


def test_search_crm_not_found(mock_crm_data):
    with (
        patch("builtins.open", mock_open(read_data=json.dumps(mock_crm_data))),
        patch("pathlib.Path.exists", return_value=True),
    ):

        result = search_crm.invoke("NonExistent")
        assert "error" in result


def test_search_opportunities_found(mock_opportunities_data):
    with (
        patch("builtins.open", mock_open(read_data=json.dumps(mock_opportunities_data))),
        patch("pathlib.Path.exists", return_value=True),
    ):

        result = search_opportunities.invoke("CLIENT-001")
        assert len(result) == 1
        assert result[0]["opportunity_name"] == "New Deal"


def test_search_historical_sows():
    mock_retriever_instance = MagicMock()
    mock_retriever_instance.search.return_value = [
        {
            "content": "Past SOW content",
            "metadata": {"file_name": "sow1.md", "client_id": "C1", "product": "P1"},
            "score": 0.9,
        }
    ]

    with patch("src.agent.tools.research.DocumentRetriever", return_value=mock_retriever_instance):
        result = search_historical_sows.invoke({"query": "payment", "client_id": "C1"})

        assert len(result) == 1
        assert result[0]["content"] == "Past SOW content"
        mock_retriever_instance.search.assert_called_once()
        assert mock_retriever_instance.search.call_args[1]["filters"]["client_id"] == "C1"


def test_search_product_kb_mock_file():
    # Test the "deterministic mock data" path
    mock_products = {
        "products": [
            {
                "name": "Test Product",
                "aliases": [],
                "category": "Test",
                "pricing_model": "Fixed",
                "description": "Desc",
                "features": [],
                "technical_requirements": [],
            }
        ]
    }

    with (
        patch("builtins.open", mock_open(read_data=json.dumps(mock_products))),
        patch("pathlib.Path.exists", return_value=True),
    ):

        result = search_product_kb.invoke("Test Product")
        assert result["name"] == "Test Product"
        assert result["source"] == "Internal Product Catalog (Demo)"


def test_search_product_kb_rag_fallback():
    # Test fallback to RAG when mock file doesn't exist or product not found in it
    mock_retriever_instance = MagicMock()
    mock_retriever_instance.search.return_value = [
        {
            "content": "Product info from RAG",
            "metadata": {"file_name": "prod.md"},
        }
    ]

    # Mock Path.exists to return False for the json file, forcing RAG
    with (
        patch("pathlib.Path.exists", return_value=False),
        patch("src.agent.tools.research.DocumentRetriever", return_value=mock_retriever_instance),
    ):

        result = search_product_kb.invoke("RAG Product")
        assert result["product"] == "RAG Product"
        assert "Product info from RAG" in result["content"]


def test_search_compliance_kb(mock_compliance_data):
    with (
        patch("builtins.open", mock_open(read_data=json.dumps(mock_compliance_data))),
        patch("pathlib.Path.exists", return_value=True),
    ):

        result = search_compliance_kb.invoke({"client_tier": "HIGH"})
        assert result["sla_requirements"] == {"uptime": "99.99%"}
        assert len(result["mandatory_clauses"]) == 1
        assert result["mandatory_clauses"][0]["name"] == "Data Privacy"
