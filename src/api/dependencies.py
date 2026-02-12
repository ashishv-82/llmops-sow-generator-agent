"""
Dependency injection for API endpoints.

Provides singleton instances of agent and other shared resources.
"""

from functools import lru_cache

from src.agent.core import SOWAgent, get_agent


@lru_cache
def get_sow_agent() -> SOWAgent:
    """
    Get singleton instance of SOW agent.

    Returns:
        SOWAgent instance
    """
    return get_agent()
