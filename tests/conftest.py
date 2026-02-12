import os
import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

from src.api.main import app
from src.agent.config import config


@pytest.fixture
def mock_aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"


@pytest.fixture
def mock_bedrock_client(mock_aws_credentials):
    """Mock boto3 bedrock-runtime client."""
    with patch("src.agent.config.Config.bedrock_runtime") as mock_bedrock:
        mock_client = MagicMock()
        mock_bedrock.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_chroma_client():
    """Mock chromadb client."""
    with patch("src.agent.config.Config.chroma_client") as mock_chroma:
        mock_client = MagicMock()
        mock_chroma.return_value = mock_client
        yield mock_client


@pytest.fixture
def api_client():
    """FastAPI TestClient."""
    return TestClient(app)


@pytest.fixture
def sample_crm_data():
    """Sample CRM data for testing."""
    return {
        "id": "CLIENT-TEST",
        "name": "Test Client",
        "industry": "Technology",
        "size": "Enterprise",
        "compliance_tier": "HIGH"
    }


@pytest.fixture
def sample_product_data():
    """Sample product data for testing."""
    return {
        "product": "Test Product",
        "content": "Test product description and features.",
        "sources": ["test_source.md"]
    }
