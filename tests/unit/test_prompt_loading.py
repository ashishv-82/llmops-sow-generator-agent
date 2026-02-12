from unittest.mock import mock_open, patch

import pytest

from src.agent.prompts import get_system_prompt, load_prompt


def test_load_prompt_success():
    mock_yaml = """
    name: test
    description: test prompt
    system_prompt: You are a test bot.
    """

    with (
        patch("builtins.open", mock_open(read_data=mock_yaml)),
        patch("pathlib.Path.exists", return_value=True),
    ):

        result = load_prompt("test")
        assert result["name"] == "test"
        assert result["system_prompt"] == "You are a test bot."


def test_load_prompt_not_found():
    with patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(FileNotFoundError):
            load_prompt("non_existent")


def test_get_system_prompt():
    mock_yaml = """
    system_prompt: System prompt content.
    """

    with (
        patch("builtins.open", mock_open(read_data=mock_yaml)),
        patch("pathlib.Path.exists", return_value=True),
    ):

        result = get_system_prompt("test")
        assert result == "System prompt content."
