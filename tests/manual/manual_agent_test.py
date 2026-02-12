#!/usr/bin/env python
"""
Manual test script for the SOW Generator Agent.
Tests end-to-end agent execution with sample queries.
"""

import sys
from pathlib import Path

# Add project root to path (2 levels up from tests/manual/)
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.agent.core import get_agent

print("=" * 60)
print("SOW Generator Agent - Manual Test")
print("=" * 60)
print()

# Initialize agent
print("Initializing agent...")
agent = get_agent()
print("✅ Agent initialized\n")

# Test queries
test_queries = [
    "Search for client information about Acme Financial Services",
    "What products do we offer?",
    "Find historical SOWs for Acme",
]

print("Select a test query:")
for i, query in enumerate(test_queries, 1):
    print(f"  {i}. {query}")
print(f"  {len(test_queries) + 1}. Custom query")
print()

try:
    choice = input("Enter choice (1-4): ").strip()

    if choice in ["1", "2", "3"]:
        query = test_queries[int(choice) - 1]
    elif choice == "4":
        query = input("Enter your query: ").strip()
    else:
        print("Invalid choice")
        sys.exit(1)

    print()
    print("=" * 60)
    print(f"Query: {query}")
    print("=" * 60)
    print()

    # Run agent
    print("Running agent...")
    print("-" * 60)
    response = agent.run(query)
    print()
    print("=" * 60)
    print("RESPONSE:")
    print("=" * 60)
    print(response)
    print()

except KeyboardInterrupt:
    print("\n\nTest cancelled by user.")
    sys.exit(0)
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback

    traceback.print_exc()
    sys.exit(1)
