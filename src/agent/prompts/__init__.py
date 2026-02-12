"""Prompt loading utilities."""

from pathlib import Path
from typing import Any

import yaml

PROMPTS_DIR = Path(__file__).parent


def load_prompt(name: str) -> dict[str, Any]:
    """
    Load a prompt template from YAML file.

    Args:
        name: Name of the prompt (without .yaml extension)

    Returns:
        Dictionary with prompt data

    Raises:
        FileNotFoundError: If prompt file doesn't exist
    """
    prompt_file = PROMPTS_DIR / f"{name}.yaml"

    if not prompt_file.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_file}")

    from typing import cast
    with open(prompt_file) as f:
        data = yaml.safe_load(f)

    return cast(dict[str, Any], data) if isinstance(data, dict) else {}


def get_system_prompt(name: str) -> str:
    """
    Get the system prompt from a prompt template.

    Args:
        name: Name of the prompt

    Returns:
        System prompt string
    """
    data = load_prompt(name)
    return data.get("system_prompt", "")
