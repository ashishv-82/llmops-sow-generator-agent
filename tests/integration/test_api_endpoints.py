from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.api.dependencies import get_sow_agent
from src.api.main import app

# Create a module-level mock agent that all tests share
_mock_agent = MagicMock()


def _override_get_sow_agent():
    """Return mock agent instead of real one (avoids AWS calls)."""
    return _mock_agent


# Override FastAPI dependency before creating TestClient
app.dependency_overrides[get_sow_agent] = _override_get_sow_agent
client = TestClient(app)


def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_sow_endpoint():
    _mock_agent.run.return_value = "# Generated SOW\n\nContent..."

    payload = {"client_id": "CLIENT-001", "product": "Product X", "requirements": "Standard terms"}

    response = client.post("/api/v1/sow/create", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["sow_text"] == "# Generated SOW\n\nContent..."

    # Verify agent was called with constructed prompt
    _mock_agent.run.assert_called_once()
    prompt = _mock_agent.run.call_args[0][0]
    assert "CLIENT-001" in prompt
    assert "Product X" in prompt

    # Reset for other tests
    _mock_agent.run.reset_mock()


@patch("src.agent.tools.research.search_crm.func")
def test_research_client_endpoint(mock_search):
    mock_search.return_value = {"name": "Test Client", "industry": "Tech"}

    payload = {"client_name": "Test Client"}
    response = client.post("/api/v1/research/client", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["client_data"]["name"] == "Test Client"


@patch("src.agent.tools.research.search_product_kb.func")
def test_research_product_endpoint(mock_search):
    mock_search.return_value = {
        "product": "Prod Y",
        "content": "Info",
        "name": "Prod Y",
        "features": ["Feature 1"],
    }

    payload = {"product_name": "Prod Y"}
    response = client.post("/api/v1/research/product", json=payload)

    assert response.status_code == 200
    data = response.json()
    # ProductResearchResponse uses product_info, features, and requirements keys
    assert data["product_info"]["name"] == "Prod Y"
    assert "features" in data
