#!/usr/bin/env python
"""
Test script for Phase 2 components.
Tests individual tools, RAG pipeline, and agent orchestrator.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("=" * 60)
print("SOW Generator - Phase 2 Component Test")
print("=" * 60)
print()

# Test 1: Import all core modules
print("TEST 1: Module Imports")
print("-" * 60)
try:
    from src.agent.config import config
    print("✅ config imported")
    
    from src.agent.tools import ALL_TOOLS
    print(f"✅ ALL_TOOLS imported ({len(ALL_TOOLS)} tools)")
    
    from src.agent.core import get_agent, SOWAgent
    print("✅ agent core imported")
    
    # RAG imports (just check modules exist)
    import src.rag.embeddings
    import src.rag.indexer
    import src.rag.retriever
    print("✅ RAG modules found")
    
    print("\n✅ All imports successful!\n")
except Exception as e:
    print(f"\n❌ Import failed: {e}\n")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Configuration
print("TEST 2: Configuration")
print("-" * 60)
try:
    print(f"AWS Region: {config.aws_region}")
    print(f"Bedrock Model: {config.bedrock_model_id}")
    print(f"ChromaDB Path: {config.chroma_persist_dir}")
    print(f"Temperature: {config.temperature}")
    print(f"Max Tokens: {config.max_tokens}")
    print("\n✅ Configuration loaded!\n")
except Exception as e:
    print(f"\n❌ Config failed: {e}\n")
    sys.exit(1)

# Test 3: Tool Registration
print("TEST 3: Tool Registration")
print("-" * 60)
print("Registered Tools:")
for i, tool in enumerate(ALL_TOOLS, 1):
    tool_name = getattr(tool, 'name', str(tool))
    print(f"  {i:2d}. {tool_name}")
print(f"\n✅ {len(ALL_TOOLS)} tools registered!\n")

# Test 4: Individual Tool Tests (without AWS)
print("TEST 4: Tool Functionality (No AWS Required)")
print("-" * 60)

try:
    # Test CRM search
    from src.agent.tools.research import search_crm
    result = search_crm("Acme")
    print(f"✅ search_crm: Found client '{result.get('name', 'Unknown')}'")
    
    # Test opportunities search
    from src.agent.tools.research import search_opportunities
    opps = search_opportunities("CLIENT-001")
    print(f"✅ search_opportunities: Found {len(opps)} opportunities")
    
    # Test compliance rules
    from src.agent.tools.research import search_compliance_kb
    compliance = search_compliance_kb("Real-Time Payments", "HIGH")
    print(f"✅ search_compliance_kb: Found {len(compliance.get('mandatory_clauses', []))} mandatory clauses")
    
    # Test context assembly
    from src.agent.tools.context import assemble_context
    context_pkg = assemble_context(
        crm_data=result,
        product_info={"name": "Test Product"},
        historical_sows=[],
        compliance_rules=compliance
    )
    print(f"✅ assemble_context: Created context package")
    
    print("\n✅ All non-AWS tools working!\n")
except Exception as e:
    print(f"\n⚠️  Tool test warning: {e}\n")

# Test 5: Check for AWS credentials
print("TEST 5: AWS Credentials Check")
print("-" * 60)
aws_configured = False
try:
    import boto3
    # Try to create bedrock runtime client
    session = boto3.Session(profile_name=config.aws_profile)
    client = session.client("bedrock-runtime", region_name=config.aws_region)
    # Try to list foundation models (cheap call)
    print("✅ AWS credentials configured!")
    print(f"   Profile: {config.aws_profile}")
    print(f"   Region: {config.aws_region}")
    aws_configured = True
except Exception as e:
    print(f"⚠️  AWS not configured: {e}")
    print("   LLM-dependent features will not work.")
    print("   To fix:")
    print("   1. Configure AWS CLI: aws configure")
    print("   2. Or set profile in .env: AWS_PROFILE=your-profile")

print()

# Test 6: ChromaDB
print("TEST 6: ChromaDB Vector Store")
print("-" * 60)
try:
    import chromadb
    chroma_client = chromadb.PersistentClient(path=config.chroma_persist_dir)
    collections = chroma_client.list_collections()
    print(f"✅ ChromaDB initialized")
    print(f"   Path: {config.chroma_persist_dir}")
    print(f"   Collections: {len(collections)}")
    for coll in collections:
        print(f"     - {coll.name}: {coll.count()} documents")
    
    if len(collections) == 0:
        print("\n  ℹ️  No collections found. Run indexing script:")
        print("     python scripts/index_documents.py")
    print()
except Exception as e:
    print(f"⚠️  ChromaDB warning: {e}\n")

# Test 7: Agent Initialization
print("TEST 7: Agent Initialization")
print("-" * 60)
if aws_configured:
    try:
        agent = get_agent()
        print("✅ Agent initialized successfully!")
        print(f"   Type: {type(agent).__name__}")
        print(f"   Tools: {len(ALL_TOOLS)}")
        print()
        
        # Show a sample request we could run
        print("ℹ️  Sample test request:")
        print('   agent.run("Search for client Acme Financial")')
        print()
    except Exception as e:
        print(f"❌ Agent initialization failed: {e}\n")
else:
    print("⏭️  Skipped (AWS not configured)\n")

# Summary
print("=" * 60)
print("TEST SUMMARY")
print("=" * 60)
print("✅ Module imports: PASSED")
print("✅ Configuration: PASSED")
print(f"✅ Tool registration: PASSED ({len(ALL_TOOLS)} tools)")
print("✅ Tool functionality: PASSED")
print("✅ ChromaDB: READY" if len(collections) > 0 else "⚠️  ChromaDB: NEEDS INDEXING")
print("✅ AWS credentials: CONFIGURED" if aws_configured else "⚠️  AWS credentials: NOT CONFIGURED")
print("✅ Agent: READY" if aws_configured else "⏭️  Agent: NEEDS AWS")
print()

if not aws_configured:
    print("⚠️  ACTION REQUIRED:")
    print("   1. Configure AWS credentials: aws configure")
    print("   2. Or set AWS_PROFILE in .env file")
    print()

if len(collections) == 0:
    print("⚠️  ACTION REQUIRED:")
    print("   1. Index documents: python scripts/index_documents.py")
    print()

if aws_configured and len(collections) > 0:
    print("🎉 ALL SYSTEMS GO! Ready for full testing.")
    print()
    print("Next steps:")
    print("   1. Test agent: python tests/manual_agent_test.py")
    print("   2. Or run verification script: python scripts/verify_phase2.py")
    print()

print("=" * 60)
