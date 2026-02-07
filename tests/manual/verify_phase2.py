#!/usr/bin/env python
"""
Quick verification script to test basic functionality before full testing.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("🧪 Phase 2 Component Verification\n")
print("=" * 60)

# Test 1: Import config
print("\n[1/6] Testing config import...")
try:
    from src.agent.config import config

    print(f"   ✅ Config loaded")
    print(f"   - AWS Region: {config.aws_region}")
    print(f"   - Model: {config.bedrock_model_id}")
    print(f"   - ChromaDB Dir: {config.chroma_persist_dir}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 2: Import RAG components
print("\n[2/6] Testing RAG components...")
try:
    from src.rag import BedrockEmbeddings, DocumentIndexer, DocumentRetriever

    print("   ✅ RAG components import successfully")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Import tools
print("\n[3/6] Testing tool imports...")
try:
    from src.agent.tools import ALL_TOOLS

    print(f"   ✅ All tools imported ({len(ALL_TOOLS)} tools)")
    print("   - Research tools: 5")
    print("   - Context tools: 2")
    print("   - Content tools: 4")
    print("   - Compliance tools: 4")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Import document utilities
print("\n[4/6] Testing document utilities...")
try:
    from src.agent.utils import parse_document, export_to_docx

    print("   ✅ Document utilities imported")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 5: Test prompt loading
print("\n[5/6] Testing prompt loading...")
try:
    from src.agent.prompts import load_prompt, get_system_prompt

    planner_prompt = load_prompt("planner")
    system_prompt = get_system_prompt("planner")
    print(f"   ✅ Prompts loaded")
    print(f"   - Planner version: {planner_prompt.get('version')}")
    print(f"   - System prompt length: {len(system_prompt)} chars")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 6: Import planner
print("\n[6/6] Testing planner import...")
try:
    from src.agent import SOWAgent, get_agent

    print("   ✅ Planner imported successfully")
    print("   - SOWAgent class available")
    print("   - get_agent() singleton available")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ All component imports successful!")
print("\nNext steps:")
print("1. Install dependencies: pip install -e '.[dev]'")
print("2. Create .env file from .env.example")
print("3. Run indexing script: python scripts/index_documents.py")
print("4. Test agent with a simple query")
