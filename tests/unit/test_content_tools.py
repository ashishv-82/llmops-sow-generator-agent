import json
from unittest.mock import MagicMock, patch

import pytest

from src.agent.tools.content import (
    generate_section,
    generate_sow_draft,
    generate_summary,
    revise_section,
)


@pytest.fixture
def mock_context():
    return {
        "client": {"name": "Test Client"},
        "product": {"name": "Test Product"},
        "compliance": {"tier": "HIGH"},
        "historical_sows": [],
    }


def test_generate_sow_draft(mock_context):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Generated SOW Content"

    with (
        patch("src.agent.tools.content._get_llm", return_value=mock_llm),
        patch("pathlib.Path.exists", return_value=True),
        patch("pathlib.Path.read_text", return_value="# SOW Template"),
    ):

        result = generate_sow_draft.invoke({"context": mock_context, "template_name": "standard"})
        assert result == "Generated SOW Content"
        mock_llm.invoke.assert_called_once()


def test_generate_section(mock_context):
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Generated Section Content"

    with patch("src.agent.tools.content._get_llm", return_value=mock_llm):
        result = generate_section.invoke({"section_name": "Scope", "context": mock_context})
        assert result == "Generated Section Content"
        mock_llm.invoke.assert_called_once()


def test_revise_section():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Revised Content"

    with patch("src.agent.tools.content._get_llm", return_value=mock_llm):
        result = revise_section.invoke({"section": "Old Content", "feedback": "Make it better"})
        assert result == "Revised Content"


def test_generate_summary():
    mock_llm = MagicMock()
    mock_llm.invoke.return_value.content = "Summary Content"

    with patch("src.agent.tools.content._get_llm", return_value=mock_llm):
        result = generate_summary.invoke({"documents": ["Doc 1", "Doc 2"]})
        assert result == "Summary Content"
