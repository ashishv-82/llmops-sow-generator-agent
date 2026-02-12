import json
from unittest.mock import mock_open, patch

import pytest

from src.agent.tools.compliance import (
    check_mandatory_clauses_v2,
    check_prohibited_terms,
    check_sla_requirements,
)


@pytest.fixture
def mock_compliance_rules():
    return {
        "prohibited_terms": ["guarantee", "unlimited"],
        "sla_requirements_by_tier": {"HIGH": {"uptime": "99.9%", "max_response_time": "1 hour"}},
    }


def test_check_mandatory_clauses_pass():
    sow_text = "This agreement includes Data Privacy and Liability terms."
    requirements = ["Data Privacy", "Liability"]

    result = check_mandatory_clauses_v2.invoke({"sow_text": sow_text, "requirements": requirements})
    assert result["status"] == "PASS"
    assert len(result["missing_clauses"]) == 0


def test_check_mandatory_clauses_fail():
    sow_text = "This agreement includes Data Privacy terms."
    requirements = ["Data Privacy", "Liability"]

    result = check_mandatory_clauses_v2.invoke({"sow_text": sow_text, "requirements": requirements})
    assert result["status"] == "FAIL"
    assert "Liability" in result["missing_clauses"]


def test_check_prohibited_terms_pass(mock_compliance_rules):
    sow_text = "We promise reasonable efforts."

    with (
        patch("builtins.open", mock_open(read_data=json.dumps(mock_compliance_rules))),
        patch("pathlib.Path.exists", return_value=True),
    ):

        result = check_prohibited_terms.invoke(sow_text)
        assert result["status"] == "PASS"
        assert result["prohibited_terms_found"] == 0


def test_check_prohibited_terms_fail(mock_compliance_rules):
    sow_text = "We guarantee unlimited resources."

    with (
        patch("builtins.open", mock_open(read_data=json.dumps(mock_compliance_rules))),
        patch("pathlib.Path.exists", return_value=True),
    ):

        result = check_prohibited_terms.invoke(sow_text)
        assert result["status"] == "WARNING"
        assert result["prohibited_terms_found"] == 2


def test_check_sla_requirements_pass(mock_compliance_rules):
    sow_text = "Uptime will be 99.9% and response time is 1 hour."

    with (
        patch("builtins.open", mock_open(read_data=json.dumps(mock_compliance_rules))),
        patch("pathlib.Path.exists", return_value=True),
    ):

        result = check_sla_requirements.invoke(
            {"sow_text": sow_text, "product": "Test", "client_tier": "HIGH"}
        )
        assert result["status"] == "PASS"
        assert len(result["findings"]) == 0
