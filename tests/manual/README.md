# Manual Testing Scripts

This folder contains manual testing and verification scripts for Phase 2 components.

## Scripts

### `test_phase2.py`
Comprehensive component test that verifies:
- Module imports
- Configuration loading
- Tool registration (16 tools)
- AWS credentials
- ChromaDB vector store
- Agent initialization

**Usage:**
```bash
source .venv/bin/activate
python tests/manual/test_phase2.py
```

### `manual_agent_test.py`
Interactive script for manual agent testing with sample queries.

**Usage:**
```bash
source .venv/bin/activate
python tests/manual/manual_agent_test.py
```

### `verify_phase2.py`
Basic verification script to confirm all Phase 2 components can be imported.

**Usage:**
```bash
source .venv/bin/activate
python tests/manual/verify_phase2.py
```

## When to Use

These scripts are for:
- Manual verification during development
- Debugging configuration issues
- Testing after environment changes
- Demonstrating the agent to stakeholders

For automated testing, use:
- `tests/unit/` - Unit tests
- `tests/integration/` - Integration tests
- `tests/evals/` - LLM evaluation tests
